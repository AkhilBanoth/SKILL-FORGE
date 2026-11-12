from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.career_recommendation import (
    CareerRecommendationResponse,
)
from app.services.recommendation_service import (
    calculate_career_recommendations,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "/careers",
    response_model=CareerRecommendationResponse,
)
def get_career_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return calculate_career_recommendations(
        db=db,
        user_id=current_user.id,
    )