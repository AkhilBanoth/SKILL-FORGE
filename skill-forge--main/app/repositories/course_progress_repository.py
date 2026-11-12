from sqlalchemy.orm import Session

from app.models.course_progress import CourseProgress


def get_course_progress(
    db: Session,
    user_id: int,
    course_id: int,
) -> CourseProgress | None:
    return (
        db.query(CourseProgress)
        .filter(
            CourseProgress.user_id == user_id,
            CourseProgress.course_id == course_id,
        )
        .first()
    )


def get_user_course_progress(
    db: Session,
    user_id: int,
) -> list[CourseProgress]:
    return (
        db.query(CourseProgress)
        .filter(CourseProgress.user_id == user_id)
        .order_by(CourseProgress.course_id.asc())
        .all()
    )


def create_course_progress(
    db: Session,
    user_id: int,
    course_id: int,
    progress_percentage: float,
    completed_lessons: int,
    total_lessons: int,
    is_completed: bool,
) -> CourseProgress:
    progress = CourseProgress(
        user_id=user_id,
        course_id=course_id,
        progress_percentage=progress_percentage,
        completed_lessons=completed_lessons,
        total_lessons=total_lessons,
        is_completed=is_completed,
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)

    return progress


def update_course_progress(
    db: Session,
    progress: CourseProgress,
    progress_percentage: float,
    completed_lessons: int,
    total_lessons: int,
    is_completed: bool,
) -> CourseProgress:
    progress.progress_percentage = progress_percentage
    progress.completed_lessons = completed_lessons
    progress.total_lessons = total_lessons
    progress.is_completed = is_completed

    db.commit()
    db.refresh(progress)

    return progress