from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_submission import ProjectSubmission
from app.repositories.project_submission_repository import (
    create_submission,
    get_project_submissions,
    get_submission_by_id,
    get_user_submissions,
    review_submission,
)
from app.schemas.project_submission import (
    ProjectSubmissionCreate,
    ProjectSubmissionReview,
)


def create_new_submission(
    db: Session,
    submission_data: ProjectSubmissionCreate,
    user_id: int,
):
    project = (
        db.query(Project)
        .filter(
            Project.id == submission_data.project_id,
            Project.is_active.is_(True),
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return create_submission(
        db=db,
        submission_data=submission_data,
        user_id=user_id,
    )


def get_submission_details(
    db: Session,
    submission_id: int,
    user_id: int,
    is_admin: bool = False,
):
    submission = get_submission_by_id(db, submission_id)

    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project submission not found",
        )

    if submission.user_id != user_id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this submission",
        )

    return submission


def get_my_submissions(db: Session, user_id: int):
    return get_user_submissions(db, user_id)


def get_submissions_for_project(
    db: Session,
    project_id: int,
    user_id: int,
    is_admin: bool = False,
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if project.user_id != user_id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view these submissions",
        )

    return get_project_submissions(db, project_id)


def review_project_submission(
    db: Session,
    submission_id: int,
    review_data: ProjectSubmissionReview,
    is_admin: bool,
):
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can review project submissions",
        )

    submission = get_submission_by_id(db, submission_id)

    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project submission not found",
        )

    return review_submission(
        db=db,
        submission=submission,
        review_data=review_data,
    )