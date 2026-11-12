from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    skill_id: int | None = Field(
        default=None,
        gt=0,
    )

    level: str = Field(
        min_length=2,
        max_length=50,
    )

    duration_hours: float = Field(
        gt=0,
    )


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str | None
    skill_id: int | None
    level: str
    duration_hours: float
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )