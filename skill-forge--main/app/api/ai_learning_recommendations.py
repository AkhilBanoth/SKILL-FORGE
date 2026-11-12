from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.ai_learning_recommendation_service import (
    generate_learning_recommendations,
)

router = APIRouter(
    prefix="/ai-learning-recommendations",
    tags=["AI Learning Recommendations"],
)


@router.get("/me")
def get_my_learning_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return generate_learning_recommendations(
        db=db,
        user_id=current_user.id,
    )