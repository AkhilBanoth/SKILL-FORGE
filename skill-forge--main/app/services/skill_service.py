from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.skill_repository import (
    create_skill,
    get_all_skills,
    get_skill_by_id,
    get_skill_by_name,
)


def create_new_skill(
    db: Session,
    name: str,
    category: str,
    description: str | None = None,
):
    existing_skill = get_skill_by_name(
        db,
        name.strip(),
    )

    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Skill already exists",
        )

    return create_skill(
        db=db,
        name=name,
        category=category,
        description=description,
    )


def list_skills(
    db: Session,
):
    return get_all_skills(db)


def get_skill(
    db: Session,
    skill_id: int,
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

    return skill