
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_admin_user
from app.models.user import User
from app.models.course import Course
from app.models.assessment import Assessment
from app.models.project import Project
from app.models.course_progress import CourseProgress
from app.models.project_submission import ProjectSubmission

router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"],
)


@router.get("/dashboard/stats")
def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    return {
        "total_users": db.query(User).count(),
        "active_users": db.query(User).filter(User.is_active.is_(True)).count(),
        "total_courses": db.query(Course).count(),
        "total_assessments": db.query(Assessment).count(),
        "total_projects": db.query(Project).count(),
    }


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    users = db.query(User).order_by(User.id).all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }
        for user in users
    ]


@router.get("/users/{user_id}")
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
    }


@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.id == admin.id and not is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own account",
        )

    user.is_active = is_active
    db.commit()
    db.refresh(user)

    return {
        "message": "User status updated successfully",
        "user_id": user.id,
        "is_active": user.is_active,
    }


@router.get("/learning-progress")
def get_platform_learning_progress(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    records = db.query(CourseProgress).all()
    total = len(records)

    return {
        "total_progress_records": total,
        "completed_courses": sum(
            1 for record in records if record.is_completed
        ),
        "in_progress_courses": sum(
            1 for record in records if not record.is_completed
        ),
        "average_progress_percentage": round(
            sum(record.progress_percentage for record in records) / total,
            2,
        ) if total else 0,
        "records": [
            {
                "user_id": record.user_id,
                "course_id": record.course_id,
                "progress_percentage": record.progress_percentage,
                "completed_lessons": record.completed_lessons,
                "total_lessons": record.total_lessons,
                "is_completed": record.is_completed,
                "updated_at": record.updated_at,
            }
            for record in records
        ],
    }


@router.get("/project-submissions")
def get_platform_project_submissions(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user),
):
    submissions = (
        db.query(ProjectSubmission)
        .order_by(ProjectSubmission.submitted_at.desc())
        .all()
    )

    return {
        "total_submissions": len(submissions),
        "pending_reviews": sum(
            1 for submission in submissions
            if submission.status.lower() in ("submitted", "pending")
        ),
        "submissions": [
            {
                "id": submission.id,
                "project_id": submission.project_id,
                "user_id": submission.user_id,
                "repository_url": submission.repository_url,
                "demo_url": submission.demo_url,
                "description": submission.description,
                "status": submission.status,
                "score": submission.score,
                "feedback": submission.feedback,
                "submitted_at": submission.submitted_at,
                "reviewed_at": submission.reviewed_at,
            }
            for submission in submissions
        ],
    }