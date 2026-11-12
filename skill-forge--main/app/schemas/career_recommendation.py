from pydantic import BaseModel


class CareerRecommendationItem(BaseModel):
    career_id: int
    career_title: str
    match_score: float


class CareerRecommendationResponse(BaseModel):
    user_id: int
    recommendations: list[CareerRecommendationItem]