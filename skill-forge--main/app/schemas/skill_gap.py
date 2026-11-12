from pydantic import BaseModel, Field


class SkillGapItem(BaseModel):
    skill_id: int
    required_weight: float
    current_level: float
    gap: float


class SkillGapResponse(BaseModel):
    career_id: int
    user_id: int
    skills: list[SkillGapItem]
    overall_gap: float = Field(
        ge=0,
        le=100,
    )