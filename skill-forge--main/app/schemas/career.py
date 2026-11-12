from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CareerCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=150,
    )

    description: str | None = None


class CareerResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )