from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.course_module_repository import (
    get_course_module_by_id,
)
from app.repositories.lesson_repository import (
    create_lesson,
    get_lesson_by_id,
    get_lessons_by_module,
)


def create_new_lesson(
    db: Session,
    module_id: int,
    title: str,
    content: str | None,
    order_index: int,
    duration_minutes: int,
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

    return create_lesson(
        db=db,
        module_id=module_id,
        title=title,
        content=content,
        order_index=order_index,
        duration_minutes=duration_minutes,
    )


def list_lessons(
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

    return get_lessons_by_module(
        db,
        module_id,
    )


def get_lesson(
    db: Session,
    lesson_id: int,
):
    lesson = get_lesson_by_id(
        db,
        lesson_id,
    )

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return lesson