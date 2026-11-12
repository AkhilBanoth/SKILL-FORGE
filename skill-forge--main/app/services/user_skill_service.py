from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.skill_repository import get_skill_by_id
from app.repositories.user_skill_repository import (
    create_user_skill,
    get_user_skill,
    get_user_skills,
)


def add_skill_to_user(
    db: Session,
    user_id: int,
    skill_id: int,
    level: float,
):
    skill = get_skill_by_id(
        db,
        skill_id,
    )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    existing = get_user_skill(
        db,
        user_id,
        skill_id,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Skill is already added to this user",
        )

    return create_user_skill(
        db=db,
        user_id=user_id,
        skill_id=skill_id,
        level=level,
    )


def list_user_skills(
    db: Session,
    user_id: int,
):
    return get_user_skills(
        db,
        user_id,
    )