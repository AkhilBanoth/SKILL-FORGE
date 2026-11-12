from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.lesson_repository import get_lesson_by_id
from app.repositories.quiz_repository import (
    create_quiz,
    get_quiz_by_id,
    get_quizzes_by_lesson,
)


def create_new_quiz(
    db: Session,
    lesson_id: int,
    title: str,
    description: str | None,
    passing_score: float,
):
    lesson = get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return create_quiz(
        db=db,
        lesson_id=lesson_id,
        title=title,
        description=description,
        passing_score=passing_score,
    )


def list_quizzes(
    db: Session,
    lesson_id: int,
):
    lesson = get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return get_quizzes_by_lesson(
        db,
        lesson_id,
    )


def get_quiz(
    db: Session,
    quiz_id: int,
):
    quiz = get_quiz_by_id(
        db,
        quiz_id,
    )

    if quiz is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    return quiz