from datetime import datetime

from pydantic import BaseModel, Field


class AssessmentAnswerCreate(BaseModel):
    question_id: int = Field(gt=0)
    selected_answer: str = Field(min_length=1, max_length=500)


class AssessmentAnswerResponse(BaseModel):
    id: int
    attempt_id: int
    question_id: int
    selected_answer: str
    is_correct: bool | None
    marks_awarded: float = Field(ge=0)
    answered_at: datetime