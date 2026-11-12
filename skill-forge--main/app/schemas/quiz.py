from datetime import datetime

from pydantic import BaseModel, Field


class QuizCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    passing_score: float = Field(ge=0, le=100)


class QuizResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    description: str | None
    passing_score: float
    is_active: bool
    created_at: datetime