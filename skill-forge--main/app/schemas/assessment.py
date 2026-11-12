from datetime import datetime

from pydantic import BaseModel, Field


class AssessmentCreate(BaseModel):
    career_id: int | None = Field(default=None, gt=0)
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    max_score: float = Field(gt=0)


class AssessmentResponse(BaseModel):
    id: int
    user_id: int
    career_id: int | None
    title: str
    description: str | None
    score: float
    max_score: float
    status: str
    created_at: datetime