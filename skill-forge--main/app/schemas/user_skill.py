from pydantic import BaseModel, Field


class UserSkillCreate(BaseModel):
    skill_id: int = Field(
        gt=0
    )

    level: float = Field(
        ge=0,
        le=100,
    )


class UserSkillResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    level: float