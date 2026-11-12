from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.ai_mentor_service import (
    generate_ai_learning_guidance,
)

router = APIRouter(
    prefix="/ai-mentor",
    tags=["AI Mentor"],
)


@router.get("/learning-guidance")
def get_learning_guidance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return generate_ai_learning_guidance(
        db=db,
        user_id=current_user.id,
    )