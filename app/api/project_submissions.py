from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.project_submission import (
    ProjectSubmissionCreate,
    ProjectSubmissionResponse,
    ProjectSubmissionReview,
)
from app.security.rbac import require_role
from app.services.project_submission_service import (
    create_new_submission,
    get_my_submissions,
    get_submission_details,
    get_submissions_for_project,
    review_project_submission,
)

router = APIRouter(
    prefix="/project-submissions",
    tags=["Project Submissions"],
)


def is_admin_user(user: User) -> bool:
    return (getattr(user, "role", "") or "").strip().lower() in {"admin", "mentor"}


@router.post(
    "",
    response_model=ProjectSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_submission_endpoint(
    submission_data: ProjectSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_submission(
        db=db,
        submission_data=submission_data,
        user_id=current_user.id,
    )


@router.get("/my", response_model=list[ProjectSubmissionResponse])
def list_my_submissions_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_submissions(
        db=db,
        user_id=current_user.id,
    )


@router.get("/project/{project_id}", response_model=list[ProjectSubmissionResponse])
def list_project_submissions_endpoint(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_submissions_for_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
    )


@router.get("/{submission_id}", response_model=ProjectSubmissionResponse)
def get_submission_endpoint(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_submission_details(
        db=db,
        submission_id=submission_id,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
    )


@router.put("/{submission_id}/review", response_model=ProjectSubmissionResponse)
def review_submission_endpoint(
    submission_id: int,
    review_data: ProjectSubmissionReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "mentor")),
):
    return review_project_submission(
        db=db,
        submission_id=submission_id,
        review_data=review_data,
        is_admin=is_admin_user(current_user),
    )