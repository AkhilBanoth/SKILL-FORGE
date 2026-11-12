from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.assessment_skill_service import evaluate_assessment_skill

router = APIRouter(
    prefix="/assessment-skills",
    tags=["Assessment Skills"],
)


@router.get("/{attempt_id}/evaluate")
def evaluate_assessment_skill_endpoint(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return evaluate_assessment_skill(
        db=db,
        attempt_id=attempt_id,
        user_id=current_user.id,
    )