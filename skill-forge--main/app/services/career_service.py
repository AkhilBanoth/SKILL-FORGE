from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.career_repository import (
    create_career,
    get_all_careers,
    get_career_by_id,
    get_career_by_title,
)


def create_new_career(
    db: Session,
    title: str,
    description: str | None = None,
):
    existing_career = get_career_by_title(
        db,
        title.strip(),
    )

    if existing_career:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Career already exists",
        )

    return create_career(
        db=db,
        title=title,
        description=description,
    )


def list_careers(
    db: Session,
):
    return get_all_careers(db)


def get_career(
    db: Session,
    career_id: int,
):
    career = get_career_by_id(
        db,
        career_id,
    )

    if career is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career not found",
        )

    return career