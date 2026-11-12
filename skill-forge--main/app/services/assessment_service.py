from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.assessment_repository import (
    create_assessment,
    get_assessment_by_id,
    get_assessments_by_user,
)
from app.repositories.career_repository import get_career_by_id


def create_new_assessment(
    db: Session,
    user_id: int,
    career_id: int | None,
    title: str,
    description: str | None,
    max_score: float,
):
    if career_id is not None:
        career = get_career_by_id(db, career_id)

        if career is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Career not found",
            )

    return create_assessment(
        db=db,
        user_id=user_id,
        career_id=career_id,
        title=title,
        description=description,
        max_score=max_score,
    )


def list_user_assessments(
    db: Session,
    user_id: int,
):
    return get_assessments_by_user(
        db,
        user_id,
    )


def get_assessment(
    db: Session,
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

    return assessment