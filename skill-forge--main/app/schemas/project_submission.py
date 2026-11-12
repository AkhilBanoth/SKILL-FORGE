from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProjectSubmissionCreate(BaseModel):
    project_id: int = Field(..., gt=0)
    repository_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None
    description: str | None = None


class ProjectSubmissionReview(BaseModel):
    status: str = Field(..., pattern="^(approved|rejected|revision_required)$")
    score: int | None = Field(None, ge=0, le=100)
    feedback: str | None = None


class ProjectSubmissionResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    repository_url: str | None
    demo_url: str | None
    description: str | None
    status: str
    score: int | None
    feedback: str | None
    submitted_at: datetime
    reviewed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)