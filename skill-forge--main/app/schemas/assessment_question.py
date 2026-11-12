from datetime import datetime

from pydantic import BaseModel, Field


class AssessmentQuestionCreate(BaseModel):
    question_text: str = Field(min_length=2)
    question_type: str = Field(default="mcq", min_length=2, max_length=50)
    option_a: str | None = None
    option_b: str | None = None
    option_c: str | None = None
    option_d: str | None = None
    correct_answer: str = Field(min_length=1, max_length=10)
    marks: float = Field(gt=0)


class AssessmentQuestionResponse(BaseModel):
    id: int
    assessment_id: int
    question_text: str
    question_type: str
    option_a: str | None
    option_b: str | None
    option_c: str | None
    option_d: str | None
    correct_answer: str
    marks: float
    is_active: bool
    created_at: datetime