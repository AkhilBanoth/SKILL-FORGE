from datetime import datetime

from pydantic import BaseModel, Field


class LessonCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    content: str | None = None

    order_index: int = Field(
        ge=1,
    )

    duration_minutes: int = Field(
        gt=0,
    )


class LessonResponse(BaseModel):
    id: int
    module_id: int
    title: str
    content: str | None
    order_index: int
    duration_minutes: int
    created_at: datetime