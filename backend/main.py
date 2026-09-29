"""PrepPilot practice-exam API.

Typical client flow
-------------------
1. POST /users                  Identify (or create) the person taking the quiz.
2. GET  /exams                  Show available certifications (e.g. AWS SAA).
3. GET  /exams/{id}/topics      Show focus areas under that exam (Storage, Networking).
4. POST /sessions               Start a sitting: pick N random bank questions for that topic.
5. GET  /sessions/{id}          Render the quiz. Answer keys are hidden here.
6. POST /sessions/{id}/answers  Save (or change) the choice for one question.
7. POST /sessions/{id}/complete Lock the sitting and compute the score.
8. GET  /sessions/{id}/review   Show right/wrong, the correct choices, and explanations.

Why two response shapes exist
-----------------------------
While a session is in progress we never return `is_correct` or stored explanations.
That is what `session_to_public` / SessionOut is for. After complete, `session_to_review`
is allowed to reveal the answer key.

Database objects used here
--------------------------
- User: identified by email only (no passwords yet).
- Exam / Topic: the catalog the user browses.
- Question / QuestionChoice: the question bank. Each choice has `is_correct`.
- PracticeSession: one sitting (one user + one exam + one topic).
- PracticeSessionQuestion: the ordered list of questions chosen for that sitting.
- QuestionAttempt: the user's selected choice for a question in that sitting.
"""

from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from database import SessionLocal
from models import (
    Exam,
    PracticeSession,
    PracticeSessionQuestion,
    Question,
    QuestionAttempt,
    QuestionChoice,
    Topic,
    User,
)
from schemas import (
    AnswerCreate,
    AnswerOut,
    ChoicePublic,
    ChoiceReview,
    ExamOut,
    QuestionPublic,
    QuestionReview,
    SessionCreate,
    SessionOut,
    SessionReview,
    TopicOut,
    UserCreate,
    UserOut,
)

app = FastAPI()

# Stored on practice_sessions.status. Completing a session is what unlocks /review.
SESSION_IN_PROGRESS = "in_progress"
SESSION_COMPLETED = "completed"


def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


def now_utc():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_session_or_404(session_id: int, db: Session) -> PracticeSession:
    """Load one practice sitting and everything the API needs to render it.

    `selectinload` runs extra SELECTs for:
      practice_session_questions  ->  questions  ->  question_choices

    We do that up front so `session_to_public` / `session_to_review` can walk
    those relationships without triggering a query per question (N+1).

    404 if the id does not exist. Callers still have to check `status` themselves
    (e.g. review is only allowed after complete).
    """
    session = (
        db.query(PracticeSession)
        .options(
            selectinload(PracticeSession.session_questions)
            .selectinload(PracticeSessionQuestion.question)
            .selectinload(Question.choices)
        )
        .filter(PracticeSession.id == session_id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


def session_to_public(session: PracticeSession) -> SessionOut:
    """Build the mid-exam payload: questions and choice text only.

    Intentionally omitted so a client cannot cheat from the JSON:
    - QuestionChoice.is_correct
    - Question.explanation
    - QuestionChoice.explanation

    `position` comes from practice_session_questions, not from the bank, so the
    quiz order stays the one we assigned when the sitting was created.
    """
    questions = []
    for item in session.session_questions:
        question = item.question
        questions.append(
            QuestionPublic(
                id=question.id,
                position=item.position,
                question_text=question.question_text,
                difficulty=question.difficulty,
                choices=[
                    ChoicePublic(id=choice.id, choice_text=choice.choice_text)
                    for choice in question.choices
                ],
            )
        )
    return SessionOut(
        id=session.id,
        user_id=session.user_id,
        exam_id=session.exam_id,
        topic_id=session.topic_id,
        status=session.status,
        started_at=session.started_at,
        completed_at=session.completed_at,
        question_count=session.question_count,
        correct_count=session.correct_count,
        questions=questions,
    )


def session_to_review(session: PracticeSession, db: Session) -> SessionReview:
    """Build the post-exam payload: keys, explanations, and what the user picked.

    Attempts live in `question_attempts`, not on the question row. We load every
    attempt for this sitting and index them by question_id so each review item
    can attach:
    - selected_choice_id / is_correct if they answered
    - None / None if they completed without answering that question

    Choice-level `is_correct` is included here so the UI can highlight the
    right option even when the user picked a wrong one.
    """
    attempts = (
        db.query(QuestionAttempt)
        .filter(QuestionAttempt.session_id == session.id)
        .all()
    )
    attempts_by_question = {attempt.question_id: attempt for attempt in attempts}

    questions = []
    for item in session.session_questions:
        question = item.question
        attempt = attempts_by_question.get(question.id)
        questions.append(
            QuestionReview(
                id=question.id,
                position=item.position,
                question_text=question.question_text,
                difficulty=question.difficulty,
                explanation=question.explanation,
                choices=[
                    ChoiceReview(
                        id=choice.id,
                        choice_text=choice.choice_text,
                        is_correct=choice.is_correct,
                        explanation=choice.explanation,
                    )
                    for choice in question.choices
                ],
                selected_choice_id=attempt.selected_choice_id if attempt else None,
                is_correct=attempt.is_correct if attempt else None,
            )
        )

    return SessionReview(
        id=session.id,
        user_id=session.user_id,
        exam_id=session.exam_id,
        topic_id=session.topic_id,
        status=session.status,
        started_at=session.started_at,
        completed_at=session.completed_at,
        question_count=session.question_count,
        correct_count=session.correct_count,
        questions=questions,
    )


@app.get("/")
def root():
    """Health check. Confirms the process is up; does not touch the database."""
    return {"message": "PrepPilot API is running"}


@app.post("/users", response_model=UserOut)
def get_or_create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Find an existing user by email, or insert one.

    This is a stand-in for real auth. The client sends `{ "email": "..." }` and
    we return the `users` row. Later routes take `user_id` from that response.

    Email is normalized (trim + lowercase) so "Alex@X.com" and "alex@x.com"
    resolve to the same person. The check is intentionally light; we only
    reject strings that cannot be an email at all.

    `db.refresh` reloads DB defaults (id, created_at) after INSERT so the
    response includes the new primary key.
    """
    email = payload.email.strip().lower()
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise HTTPException(status_code=422, detail="Invalid email")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        user = User(email=email, created_at=now_utc())
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@app.get("/exams", response_model=list[ExamOut])
def get_exams(db: Session = Depends(get_db)):
    """List every exam in the catalog.

    FastAPI serializes each SQLAlchemy Exam through ExamOut (id, name, provider,
    description, created_at). The UI uses this list so the user can pick a
    certification before picking a topic.
    """
    return db.query(Exam).all()


@app.get("/exams/{exam_id}/topics", response_model=list[TopicOut])
def get_exam_topics(exam_id: int, db: Session = Depends(get_db)):
    """List focus areas that belong to one exam.

    `{exam_id}` is taken from the URL. We 404 if that exam does not exist so
    an empty topic list is not confused with "exam 999 is real but has no topics."

    Topics are the categories a user practices (Storage, Networking, …).
    Starting a session requires a topic_id from this list.
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db.query(Topic).filter(Topic.exam_id == exam_id).all()


@app.post("/sessions", response_model=SessionOut)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    """Start a practice sitting for one user, exam, and topic.

    Body (SessionCreate):
      user_id, exam_id, topic_id, question_count (optional, default 10)

    Steps:
    1. Prove the user, exam, and topic exist. The topic must belong to that exam
       so you cannot start "AWS Storage" under a different certification.
    2. Draw up to `question_count` random questions from the bank for that
       exam + topic. `func.random()` is Postgres's RANDOM(). If the bank is
       thinner than requested, we use whatever exists instead of failing.
    3. 404 only when the topic has zero questions (e.g. Networking in the seed).
    4. Insert practice_sessions, then one practice_session_questions row per
       drawn question with a 1-based `position` (quiz order).

    `db.flush()` assigns session.id before we insert the join rows, without
    committing yet. One `commit()` writes the sitting and its question list
    together. Then we reload via get_session_or_404 so the response includes
    nested questions/choices (still without answer keys).
    """
    user = db.query(User).filter(User.id == payload.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    exam = db.query(Exam).filter(Exam.id == payload.exam_id).first()
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")

    topic = (
        db.query(Topic)
        .filter(Topic.id == payload.topic_id, Topic.exam_id == payload.exam_id)
        .first()
    )
    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found for this exam",
        )

    bank_questions = (
        db.query(Question)
        .filter(
            Question.exam_id == payload.exam_id,
            Question.topic_id == payload.topic_id,
        )
        .order_by(func.random())
        .limit(payload.question_count)
        .all()
    )
    if not bank_questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found for this topic",
        )

    session = PracticeSession(
        user_id=user.id,
        exam_id=exam.id,
        topic_id=topic.id,
        status=SESSION_IN_PROGRESS,
        started_at=now_utc(),
        # Persist how many we actually drew, not the requested count.
        question_count=len(bank_questions),
    )
    db.add(session)
    db.flush()

    for position, question in enumerate(bank_questions, start=1):
        db.add(
            PracticeSessionQuestion(
                session_id=session.id,
                question_id=question.id,
                position=position,
            )
        )

    db.commit()
    return session_to_public(get_session_or_404(session.id, db))


@app.get("/sessions/{session_id}", response_model=SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Resume or re-render a sitting.

    Same safe shape as POST /sessions: metadata + question/choice text.
    Works for both in_progress and completed sessions. Use /review after
    complete if the client needs the answer key.
    """
    return session_to_public(get_session_or_404(session_id, db))


@app.post("/sessions/{session_id}/answers", response_model=AnswerOut)
def submit_answer(
    session_id: int,
    payload: AnswerCreate,
    db: Session = Depends(get_db),
):
    """Record the user's choice for one question in this sitting.

    Body: `{ "question_id": 1, "choice_id": 3 }`

    Guards:
    - Session must exist and still be in_progress (completed sittings are locked).
    - question_id must be one of the questions we assigned to this session
      (you cannot answer a bank question that was not drawn).
    - choice_id must belong to that question (stops submitting S3's answer
      onto a different item).

    Scoring happens now, but it is not returned. We copy
    `QuestionChoice.is_correct` onto the attempt so /complete can COUNT(*)
    later without re-joining choices. The HTTP body only echoes the ids the
    client sent, so the UI cannot infer right/wrong until /review.

    Upsert: one attempt per (session, question). Changing an answer updates
    the same row instead of inserting a second attempt.
    """
    session = get_session_or_404(session_id, db)
    if session.status == SESSION_COMPLETED:
        raise HTTPException(status_code=400, detail="Session is already completed")

    session_question_ids = {item.question_id for item in session.session_questions}
    if payload.question_id not in session_question_ids:
        raise HTTPException(status_code=400, detail="Question is not in this session")

    choice = (
        db.query(QuestionChoice)
        .filter(
            QuestionChoice.id == payload.choice_id,
            QuestionChoice.question_id == payload.question_id,
        )
        .first()
    )
    if choice is None:
        raise HTTPException(
            status_code=400,
            detail="Choice does not belong to this question",
        )

    attempt = (
        db.query(QuestionAttempt)
        .filter(
            QuestionAttempt.session_id == session.id,
            QuestionAttempt.question_id == payload.question_id,
        )
        .first()
    )
    if attempt is None:
        attempt = QuestionAttempt(
            user_id=session.user_id,
            question_id=payload.question_id,
            selected_choice_id=choice.id,
            is_correct=choice.is_correct,
            attempted_at=now_utc(),
            session_id=session.id,
        )
        db.add(attempt)
    else:
        attempt.selected_choice_id = choice.id
        attempt.is_correct = choice.is_correct
        attempt.attempted_at = now_utc()

    db.commit()
    return AnswerOut(
        question_id=payload.question_id,
        selected_choice_id=choice.id,
    )


@app.post("/sessions/{session_id}/complete", response_model=SessionOut)
def complete_session(session_id: int, db: Session = Depends(get_db)):
    """Lock the sitting and store the score.

    Sets status=completed, completed_at, and correct_count = number of attempts
    in this session with is_correct = true. Unanswered questions simply do not
    appear in that count (they do not increment the score).

    Calling this again on an already-completed session is a no-op: we skip
    the write and still return the public session payload. After this, /answers
    is rejected and /review is allowed.

    The response is still SessionOut (no answer key). The client should follow
    up with GET /sessions/{id}/review to show results.
    """
    session = get_session_or_404(session_id, db)
    if session.status != SESSION_COMPLETED:
        session.status = SESSION_COMPLETED
        session.completed_at = now_utc()
        session.correct_count = (
            db.query(QuestionAttempt)
            .filter(
                QuestionAttempt.session_id == session.id,
                QuestionAttempt.is_correct.is_(True),
            )
            .count()
        )
        db.commit()
        # Reload so relationships/fields match what we just wrote.
        session = get_session_or_404(session_id, db)
    return session_to_public(session)


@app.get("/sessions/{session_id}/review", response_model=SessionReview)
def review_session(session_id: int, db: Session = Depends(get_db)):
    """Return the graded exam: what they picked vs what was correct.

    Only after /complete. That keeps /review from being a backdoor to the
    answer key while the user is still taking the quiz.

    Each question includes all choices with `is_correct`, any stored
    explanation, the selected_choice_id, and whether that pick was right.
    This is the payload a "review missed questions" screen should use.
    """
    session = get_session_or_404(session_id, db)
    if session.status != SESSION_COMPLETED:
        raise HTTPException(status_code=400, detail="Session is not completed")
    return session_to_review(session, db)
