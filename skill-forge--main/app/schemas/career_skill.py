from pydantic import BaseModel, Field


class CareerSkillCreate(BaseModel):
    skill_id: int = Field(
        gt=0
    )

    weight: float = Field(
        gt=0,
        le=100,
    )


class CareerSkillResponse(BaseModel):
    id: int
    career_id: int
    skill_id: int
    weight: float