
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.roadmap_service import create_career_learning_roadmap


router = APIRouter(
    prefix="/roadmap",
    tags=["Learning Roadmap"],
)


@router.get("/{career_id}")
def get_learning_roadmap(
    career_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = create_career_learning_roadmap(
        db=db,
        user_id=current_user.id,
        career_id=career_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Career not found",
        )

    return result
