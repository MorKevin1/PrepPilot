from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ExamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    provider: str | None = None
    description: str | None = None
    created_at: datetime | None = None


class TopicOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    exam_id: int
    name: str
    description: str | None = None


class UserCreate(BaseModel):
    email: str = Field(min_length=3, max_length=255)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    created_at: datetime | None = None


class SessionCreate(BaseModel):
    user_id: int
    exam_id: int
    topic_id: int
    question_count: int = Field(default=10, ge=1, le=100)


class ChoicePublic(BaseModel):
    id: int
    choice_text: str


class QuestionPublic(BaseModel):
    id: int
    position: int
    question_text: str
    difficulty: str | None = None
    choices: list[ChoicePublic]


class SessionOut(BaseModel):
    id: int
    user_id: int
    exam_id: int
    topic_id: int
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    question_count: int
    correct_count: int | None = None
    questions: list[QuestionPublic]


class AnswerCreate(BaseModel):
    question_id: int
    choice_id: int


class AnswerOut(BaseModel):
    question_id: int
    selected_choice_id: int


class ChoiceReview(BaseModel):
    id: int
    choice_text: str
    is_correct: bool
    explanation: str | None = None


class QuestionReview(BaseModel):
    id: int
    position: int
    question_text: str
    difficulty: str | None = None
    explanation: str | None = None
    choices: list[ChoiceReview]
    selected_choice_id: int | None = None
    is_correct: bool | None = None


class SessionReview(BaseModel):
    id: int
    user_id: int
    exam_id: int
    topic_id: int
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    question_count: int
    correct_count: int | None = None
    questions: list[QuestionReview]
