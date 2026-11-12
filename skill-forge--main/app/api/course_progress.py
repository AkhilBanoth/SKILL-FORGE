
from typing import Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.course_progress import (
    CourseProgressCreate,
    CourseProgressResponse,
    CourseProgressUpdate,
)
from app.services.course_progress_service import (
    calculate_course_progress,
    list_user_course_progress,
    update_completed_lessons,
)

router = APIRouter(prefix="/courses", tags=["Course Progress"])


@router.get(
    "/progress",
    response_model=list[CourseProgressResponse],
)
def get_my_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_course_progress(
        db=db,
        user_id=current_user.id,
    )


@router.post(
    "/{course_id}/progress",
    response_model=CourseProgressResponse,
)
def calculate_progress(
    course_id: Annotated[int, Path(ge=1)],
    payload: CourseProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return calculate_course_progress(
        db=db,
        user_id=current_user.id,
        course_id=course_id,
    )


@router.put(
    "/{course_id}/progress",
    response_model=CourseProgressResponse,
)
def update_progress(
    course_id: Annotated[int, Path(ge=1)],
    payload: CourseProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_completed_lessons(
        db=db,
        user_id=current_user.id,
        course_id=course_id,
        completed_lessons=payload.completed_lessons,
    )
