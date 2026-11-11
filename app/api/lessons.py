from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.models.user import User
from app.schemas.lesson import LessonCreate, LessonResponse
from app.security.rbac import require_role
from app.services.lesson_service import (
    create_new_lesson,
    get_lesson,
    list_lessons,
)


router = APIRouter(
    prefix="/modules",
    tags=["Lessons"],
)


@router.post(
    "/{module_id}/lessons",
    response_model=LessonResponse,
    status_code=201,
)
def create_lesson_endpoint(
    module_id: int,
    payload: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return create_new_lesson(
        db=db,
        module_id=module_id,
        title=payload.title,
        content=payload.content,
        order_index=payload.order_index,
        duration_minutes=payload.duration_minutes,
    )


@router.get(
    "/{module_id}/lessons",
    response_model=list[LessonResponse],
)
def get_lessons_endpoint(
    module_id: int,
    db: Session = Depends(get_db),
):
    return list_lessons(
        db=db,
        module_id=module_id,
    )


@router.get(
    "/lessons/{lesson_id}",
    response_model=LessonResponse,
)
def get_lesson_endpoint(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    return get_lesson(
        db=db,
        lesson_id=lesson_id,
    )