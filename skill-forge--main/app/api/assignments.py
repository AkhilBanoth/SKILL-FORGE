from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.models.user import User
from app.security.rbac import require_role
from app.schemas.assignment import AssignmentCreate, AssignmentResponse
from app.services.assignment_service import (
    create_new_assignment,
    get_assignment,
    list_assignments,
)

router = APIRouter(
    prefix="/lessons",
    tags=["Assignments"],
)


@router.post(
    "/{lesson_id}/assignments",
    response_model=AssignmentResponse,
    status_code=201,
)
def create_assignment_endpoint(
    lesson_id: int,
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return create_new_assignment(
        db=db,
        lesson_id=lesson_id,
        title=payload.title,
        description=payload.description,
        max_score=payload.max_score,
    )


@router.get(
    "/{lesson_id}/assignments",
    response_model=list[AssignmentResponse],
)
def get_assignments_endpoint(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    return list_assignments(
        db=db,
        lesson_id=lesson_id,
    )


@router.get(
    "/assignments/{assignment_id}",
    response_model=AssignmentResponse,
)
def get_assignment_endpoint(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    return get_assignment(
        db=db,
        assignment_id=assignment_id,
    )