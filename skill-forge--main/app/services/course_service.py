from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.course_repository import (
    create_course,
    get_all_courses,
    get_course_by_id,
    get_course_by_title,
)
from app.repositories.skill_repository import get_skill_by_id


def create_new_course(
    db: Session,
    title: str,
    description: str | None,
    skill_id: int | None,
    level: str,
    duration_hours: float,
):
    existing_course = get_course_by_title(
        db,
        title.strip(),
    )

    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course already exists",
        )

    if skill_id is not None:
        skill = get_skill_by_id(
            db,
            skill_id,
        )

        if skill is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found",
            )

    return create_course(
        db=db,
        title=title,
        description=description,
        skill_id=skill_id,
        level=level,
        duration_hours=duration_hours,
    )


def list_courses(
    db: Session,
):
    return get_all_courses(db)


def get_course(
    db: Session,
    course_id: int,
):
    course = get_course_by_id(
        db,
        course_id,
    )

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    return course