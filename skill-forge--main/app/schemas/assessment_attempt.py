from datetime import datetime

from pydantic import BaseModel, Field


class AssessmentAttemptCreate(BaseModel):
    assessment_id: int = Field(gt=0)


class AssessmentAttemptResponse(BaseModel):
    id: int
    assessment_id: int
    user_id: int
    score: float = Field(ge=0)
    max_score: float = Field(gt=0)
    status: str
    started_at: datetime
    submitted_at: datetime | None