from pydantic import BaseModel, Field


class ReadinessResponse(BaseModel):
    career_id: int
    career_title: str
    readiness_score: float = Field(
        ge=0,
        le=100,
    )