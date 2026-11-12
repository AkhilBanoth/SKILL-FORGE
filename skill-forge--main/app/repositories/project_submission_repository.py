from datetime import datetime

from sqlalchemy.orm import Session

from app.models.project_submission import ProjectSubmission
from app.schemas.project_submission import (
    ProjectSubmissionCreate,
    ProjectSubmissionReview,
)


def create_submission(
    db: Session,
    submission_data: ProjectSubmissionCreate,
    user_id: int,
):
    submission = ProjectSubmission(
        project_id=submission_data.project_id,
        user_id=user_id,
        repository_url=(
            str(submission_data.repository_url)
            if submission_data.repository_url
            else None
        ),
        demo_url=(
            str(submission_data.demo_url)
            if submission_data.demo_url
            else None
        ),
        description=submission_data.description,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission


def get_submission_by_id(db: Session, submission_id: int):
    return (
        db.query(ProjectSubmission)
        .filter(ProjectSubmission.id == submission_id)
        .first()
    )


def get_user_submissions(db: Session, user_id: int):
    return (
        db.query(ProjectSubmission)
        .filter(ProjectSubmission.user_id == user_id)
        .order_by(ProjectSubmission.submitted_at.desc())
        .all()
    )


def get_project_submissions(db: Session, project_id: int):
    return (
        db.query(ProjectSubmission)
        .filter(ProjectSubmission.project_id == project_id)
        .order_by(ProjectSubmission.submitted_at.desc())
        .all()
    )


def review_submission(
    db: Session,
    submission: ProjectSubmission,
    review_data: ProjectSubmissionReview,
):
    submission.status = review_data.status
    submission.score = review_data.score
    submission.feedback = review_data.feedback
    submission.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(submission)

    return submission