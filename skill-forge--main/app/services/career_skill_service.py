from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.career_repository import get_career_by_id
from app.repositories.career_skill_repository import (
    create_career_skill,
    get_career_skill,
    get_career_skills,
)
from app.repositories.skill_repository import get_skill_by_id


def add_skill_to_career(
    db: Session,
    career_id: int,
    skill_id: int,
    weight: float,
):
    # Check career exists
    career = get_career_by_id(
        db,
        career_id,
    )

    if career is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career not found",
        )

    # Check skill exists
    skill = get_skill_by_id(
        db,
        skill_id,
    )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    # Check duplicate relationship
    existing = get_career_skill(
        db,
        career_id,
        skill_id,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Skill is already assigned to this career",
        )

    return create_career_skill(
        db=db,
        career_id=career_id,
        skill_id=skill_id,
        weight=weight,
    )


def list_career_skills(
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

    return get_career_skills(
        db,
        career_id,
    )