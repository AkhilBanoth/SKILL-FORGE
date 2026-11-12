from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.assignment_repository import (
    create_assignment,
    get_assignment_by_id,
    get_assignments_by_lesson,
)
from app.repositories.lesson_repository import get_lesson_by_id


def create_new_assignment(
    db: Session,
    lesson_id: int,
    title: str,
    description: str | None,
    max_score: float,
):
    lesson = get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return create_assignment(
        db=db,
        lesson_id=lesson_id,
        title=title,
        description=description,
        max_score=max_score,
    )


def list_assignments(
    db: Session,
    lesson_id: int,
):
    lesson = get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return get_assignments_by_lesson(
        db,
        lesson_id,
    )


def get_assignment(
    db: Session,
    assignment_id: int,
):
    assignment = get_assignment_by_id(
        db,
        assignment_id,
    )

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )

    return assignment