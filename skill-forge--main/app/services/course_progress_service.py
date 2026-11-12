from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.course_module_repository import get_course_modules
from app.repositories.course_repository import get_course_by_id
from app.repositories.course_progress_repository import (
    create_course_progress,
    get_course_progress,
    get_user_course_progress,
    update_course_progress,
)
from app.repositories.lesson_repository import get_lessons_by_module


def calculate_course_progress(
    db: Session,
    user_id: int,
    course_id: int,
):
    course = get_course_by_id(db, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    modules = get_course_modules(db, course_id)

    total_lessons = 0

    for module in modules:
        lessons = get_lessons_by_module(db, module.id)
        total_lessons += len(lessons)

    progress = get_course_progress(
        db,
        user_id,
        course_id,
    )

    completed_lessons = progress.completed_lessons if progress else 0

    if total_lessons == 0:
        progress_percentage = 0.0
    else:
        progress_percentage = (
            completed_lessons / total_lessons
        ) * 100

    progress_percentage = min(
        progress_percentage,
        100.0,
    )

    is_completed = (
        total_lessons > 0
        and completed_lessons >= total_lessons
    )

    if progress is None:
        return create_course_progress(
            db=db,
            user_id=user_id,
            course_id=course_id,
            progress_percentage=progress_percentage,
            completed_lessons=completed_lessons,
            total_lessons=total_lessons,
            is_completed=is_completed,
        )

    return update_course_progress(
        db=db,
        progress=progress,
        progress_percentage=progress_percentage,
        completed_lessons=completed_lessons,
        total_lessons=total_lessons,
        is_completed=is_completed,
    )


def update_completed_lessons(
    db: Session,
    user_id: int,
    course_id: int,
    completed_lessons: int,
):
    course = get_course_by_id(db, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    modules = get_course_modules(db, course_id)

    total_lessons = 0

    for module in modules:
        lessons = get_lessons_by_module(db, module.id)
        total_lessons += len(lessons)

    if completed_lessons > total_lessons:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Completed lessons cannot exceed total lessons",
        )

    progress_percentage = (
        0.0
        if total_lessons == 0
        else (completed_lessons / total_lessons) * 100
    )

    is_completed = (
        total_lessons > 0
        and completed_lessons >= total_lessons
    )

    progress = get_course_progress(
        db,
        user_id,
        course_id,
    )

    if progress is None:
        return create_course_progress(
            db=db,
            user_id=user_id,
            course_id=course_id,
            progress_percentage=progress_percentage,
            completed_lessons=completed_lessons,
            total_lessons=total_lessons,
            is_completed=is_completed,
        )

    return update_course_progress(
        db=db,
        progress=progress,
        progress_percentage=progress_percentage,
        completed_lessons=completed_lessons,
        total_lessons=total_lessons,
        is_completed=is_completed,
    )


def list_user_course_progress(
    db: Session,
    user_id: int,
):
    return get_user_course_progress(
        db,
        user_id,
    )