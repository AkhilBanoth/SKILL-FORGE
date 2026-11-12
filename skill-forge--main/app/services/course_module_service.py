from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.course_module_repository import (
    create_course_module,
    get_course_module_by_id,
    get_course_modules,
)
from app.repositories.course_repository import get_course_by_id


def create_new_course_module(
    db: Session,
    course_id: int,
    title: str,
    description: str | None,
    order_index: int,
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

    return create_course_module(
        db=db,
        course_id=course_id,
        title=title,
        description=description,
        order_index=order_index,
    )


def list_course_modules(
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

    return get_course_modules(
        db,
        course_id,
    )


def get_course_module(
    db: Session,
    module_id: int,
):
    module = get_course_module_by_id(
        db,
        module_id,
    )

    if module is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course module not found",
        )

    return module