from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=5)
    difficulty: str = "Beginner"
    required_skills: str | None = None
    instructions: str | None = None


class ProjectUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=150)
    description: str | None = Field(None, min_length=5)
    difficulty: str | None = None
    required_skills: str | None = None
    instructions: str | None = None
    is_active: bool | None = None


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    difficulty: str
    required_skills: str | None
    instructions: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)