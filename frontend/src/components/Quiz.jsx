import { useEffect, useState } from "react";
import {
  completeSession,
  createSession,
  getOrCreateUser,
  getSessionReview,
  submitAnswer,
} from "../api.js";
import Review from "./Review.jsx";

// Stand-in until a login screen exists. POST /users reuses this email.
const PRACTICE_EMAIL = "you@example.com";

/**
 * One practice sitting for the topic the user just clicked.
 *
 * Props
 * -----
 * exam    — selected exam from App (needs id).
 * topic   — selected topic from App (needs id and name).
 * onBack  — returns to TopicList by clearing selectedTopic.
 *
 * A choice click saves POST /sessions/{id}/answers and keeps that choice
 * in `answers` so Previous/Next still shows it. Finish locks the sitting
 * and swaps this screen for Review.
 */
export default function Quiz({ exam, topic, onBack }) {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [saving, setSaving] = useState(false);
  const [finishing, setFinishing] = useState(false);
  const [review, setReview] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    setSession(null);
    setQuestionIndex(0);
    setAnswers({});
    setReview(null);

    getOrCreateUser(PRACTICE_EMAIL)
      .then((user) =>
        createSession({
          userId: user.id,
          examId: exam.id,
          topicId: topic.id,
        }),
      )
      .then((data) => {
        if (!cancelled) {
          const questions = [...data.questions].sort(
            (a, b) => a.position - b.position,
          );
          setSession({ ...data, questions });
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [exam.id, topic.id]);

  const question = session?.questions[questionIndex];
  const pickedChoiceId = question ? answers[question.id] : null;

  async function choose(choiceId) {
    const previous = answers[question.id];
    setAnswers((current) => ({ ...current, [question.id]: choiceId }));
    setSaving(true);
    setError(null);
    try {
      await submitAnswer(session.id, question.id, choiceId);
    } catch (err) {
      setAnswers((current) => ({ ...current, [question.id]: previous }));
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function finish() {
    setFinishing(true);
    setError(null);
    try {
      await completeSession(session.id);
      setReview(await getSessionReview(session.id));
    } catch (err) {
      setError(err.message);
    } finally {
      setFinishing(false);
    }
  }

  if (review) {
    return <Review review={review} onBack={onBack} />;
  }

  return (
    <section>
      <button type="button" className="back-button" onClick={onBack}>
        All topics
      </button>
      <h2 className="section-title">{topic.name}</h2>
      <p className="section-copy">{exam.name}</p>

      {loading && <p className="status">Starting practice…</p>}
      {error && <p className="status error">{error}</p>}

      {question && (
        <article className="exam-card">
          <p className="provider">
            Question {questionIndex + 1} of {session.questions.length}
            {question.difficulty ? ` · ${question.difficulty}` : ""}
          </p>
          <h2>{question.question_text}</h2>
          <ul className="choice-list">
            {question.choices.map((choice) => (
              <li key={choice.id}>
                <button
                  type="button"
                  className={
                    pickedChoiceId === choice.id
                      ? "choice-button choice-button-picked"
                      : "choice-button"
                  }
                  disabled={saving || finishing}
                  onClick={() => choose(choice.id)}
                >
                  {choice.choice_text}
                </button>
              </li>
            ))}
          </ul>
          <div className="quiz-nav">
            <button
              type="button"
              className="back-button"
              disabled={questionIndex === 0}
              onClick={() => setQuestionIndex(questionIndex - 1)}
            >
              Previous
            </button>
            <button
              type="button"
              className="back-button"
              disabled={questionIndex === session.questions.length - 1}
              onClick={() => setQuestionIndex(questionIndex + 1)}
            >
              Next
            </button>
            {questionIndex === session.questions.length - 1 && (
              <button
                type="button"
                className="back-button"
                disabled={finishing || saving}
                onClick={finish}
              >
                {finishing ? "Finishing…" : "Finish"}
              </button>
            )}
          </div>
        </article>
      )}
    </section>
  );
}
