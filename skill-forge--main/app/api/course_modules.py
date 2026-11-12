from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.models.user import User
from app.schemas.course_module import (
    CourseModuleCreate,
    CourseModuleResponse,
)
from app.security.rbac import require_role
from app.services.course_module_service import (
    create_new_course_module,
    get_course_module,
    list_course_modules,
)


router = APIRouter(
    prefix="/courses",
    tags=["Course Modules"],
)


@router.post(
    "/{course_id}/modules",
    response_model=CourseModuleResponse,
    status_code=201,
)
def create_module(
    course_id: int,
    payload: CourseModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return create_new_course_module(
        db=db,
        course_id=course_id,
        title=payload.title,
        description=payload.description,
        order_index=payload.order_index,
    )


@router.get(
    "/{course_id}/modules",
    response_model=list[CourseModuleResponse],
)
def get_modules(
    course_id: int,
    db: Session = Depends(get_db),
):
    return list_course_modules(
        db=db,
        course_id=course_id,
    )


@router.get(
    "/modules/{module_id}",
    response_model=CourseModuleResponse,
)
def get_module(
    module_id: int,
    db: Session = Depends(get_db),
):
    return get_course_module(
        db=db,
        module_id=module_id,
    )