from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SkillCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    category: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = None


class SkillResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )