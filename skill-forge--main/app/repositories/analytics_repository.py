from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.course_progress import CourseProgress
from app.models.assessment_attempt import AssessmentAttempt
from app.models.project_submission import ProjectSubmission


def get_course_analytics(db: Session, user_id: int) -> dict:
    records = (
        db.query(CourseProgress)
        .filter(CourseProgress.user_id == user_id)
        .all()
    )

    total_courses = len(records)
    completed_courses = sum(
        1 for record in records if record.is_completed
    )
    in_progress_courses = sum(
        1
        for record in records
        if not record.is_completed and record.progress_percentage > 0
    )

    average_progress = (
        sum(record.progress_percentage for record in records)
        / total_courses
        if total_courses > 0
        else 0.0
    )

    return {
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "in_progress_courses": in_progress_courses,
        "average_progress": round(average_progress, 2),
    }


def get_assessment_analytics(db: Session, user_id: int) -> dict:
    result = (
        db.query(
            func.count(AssessmentAttempt.id),
            func.avg(
                AssessmentAttempt.score
                * 100.0
                / func.nullif(AssessmentAttempt.max_score, 0)
            ),
        )
        .filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.status == "submitted",
        )
        .first()
    )

    return {
        "total_attempts": result[0] or 0,
        "average_score": round(float(result[1] or 0.0), 2),
    }


def get_project_analytics(db: Session, user_id: int) -> dict:
    total_submissions = (
        db.query(func.count(ProjectSubmission.id))
        .filter(ProjectSubmission.user_id == user_id)
        .scalar()
        or 0
    )

    reviewed_submissions = (
        db.query(func.count(ProjectSubmission.id))
        .filter(
            ProjectSubmission.user_id == user_id,
            ProjectSubmission.reviewed_at.isnot(None),
        )
        .scalar()
        or 0
    )

    return {
        "total_submissions": total_submissions,
        "reviewed_submissions": reviewed_submissions,
    }