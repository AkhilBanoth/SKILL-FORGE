from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.readiness import ReadinessResponse
from app.services.readiness_service import calculate_readiness


router = APIRouter(
    prefix="/readiness",
    tags=["Readiness"],
)


@router.get(
    "/{career_id}",
    response_model=ReadinessResponse,
)
def get_readiness(
    career_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = calculate_readiness(
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