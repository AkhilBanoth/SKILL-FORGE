from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse
from app.security.rbac import require_role
from app.services.course_service import (
    create_new_course,
    get_course,
    list_courses,
)


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    "",
    response_model=CourseResponse,
    status_code=201,
)
def create_course_endpoint(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return create_new_course(
        db=db,
        title=payload.title,
        description=payload.description,
        skill_id=payload.skill_id,
        level=payload.level,
        duration_hours=payload.duration_hours,
    )


@router.get(
    "",
    response_model=list[CourseResponse],
)
def get_all_courses_endpoint(
    db: Session = Depends(get_db),
):
    return list_courses(db)


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def get_course_endpoint(
    course_id: int,
    db: Session = Depends(get_db),
):
    return get_course(
        db=db,
        course_id=course_id,
    )