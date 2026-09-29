from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from database import Base


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    provider = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime)

    topics = relationship("Topic", back_populates="exam")
    questions = relationship("Question", back_populates="exam")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    exam = relationship("Exam", back_populates="topics")
    questions = relationship("Question", back_populates="topic")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    question_text = Column(Text, nullable=False)
    difficulty = Column(String(50))
    explanation = Column(Text)
    created_at = Column(DateTime)
    source_type = Column(String(50))
    source_name = Column(String(255))
    source_url = Column(Text)
    license = Column(String(255))

    exam = relationship("Exam", back_populates="questions")
    topic = relationship("Topic", back_populates="questions")
    choices = relationship("QuestionChoice", back_populates="question")


class QuestionChoice(Base):
    __tablename__ = "question_choices"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    choice_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    explanation = Column(Text)

    question = relationship("Question", back_populates="choices")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime)

    sessions = relationship("PracticeSession", back_populates="user")
    attempts = relationship("QuestionAttempt", back_populates="user")


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    status = Column(String(50), nullable=False, default="in_progress")
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    question_count = Column(Integer, nullable=False)
    correct_count = Column(Integer)

    user = relationship("User", back_populates="sessions")
    exam = relationship("Exam")
    topic = relationship("Topic")
    session_questions = relationship(
        "PracticeSessionQuestion",
        back_populates="session",
        order_by="PracticeSessionQuestion.position",
    )
    attempts = relationship("QuestionAttempt", back_populates="session")


class PracticeSessionQuestion(Base):
    __tablename__ = "practice_session_questions"
    __table_args__ = (
        UniqueConstraint("session_id", "question_id", name="uq_session_question"),
    )

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("practice_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    position = Column(Integer, nullable=False)

    session = relationship("PracticeSession", back_populates="session_questions")
    question = relationship("Question")


class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_choice_id = Column(Integer, ForeignKey("question_choices.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    attempted_at = Column(DateTime)
    session_id = Column(Integer, ForeignKey("practice_sessions.id"))

    user = relationship("User", back_populates="attempts")
    question = relationship("Question")
    selected_choice = relationship("QuestionChoice")
    session = relationship("PracticeSession", back_populates="attempts")
