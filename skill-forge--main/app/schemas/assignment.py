from datetime import datetime

from pydantic import BaseModel, Field


class AssignmentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    max_score: float = Field(gt=0)


class AssignmentResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    description: str | None
    max_score: float
    created_at: datetime