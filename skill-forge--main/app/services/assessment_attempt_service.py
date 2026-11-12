from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.assessment_attempt_repository import (
    create_attempt,
    get_active_attempt,
    get_attempt_by_id,
    get_attempts_by_user,
)
from app.repositories.assessment_repository import get_assessment_by_id


def create_new_attempt(
    db: Session,
    user_id: int,
    assessment_id: int,
):
    assessment = get_assessment_by_id(
        db,
        assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    if assessment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to attempt this assessment",
        )

    existing_attempt = get_active_attempt(
        db,
        user_id,
        assessment_id,
    )

    if existing_attempt is not None:
        return existing_attempt

    return create_attempt(
        db=db,
        assessment_id=assessment_id,
        user_id=user_id,
        max_score=assessment.max_score,
    )


def get_attempt(
    db: Session,
    attempt_id: int,
    user_id: int,
):
    attempt = get_attempt_by_id(
        db,
        attempt_id,
    )

    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment attempt not found",
        )

    if attempt.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this attempt",
        )

    return attempt


def list_user_attempts(
    db: Session,
    user_id: int,
):
    return get_attempts_by_user(
        db,
        user_id,
    )