from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.models.user import User
from app.schemas.resource import ResourceCreate, ResourceResponse
from app.security.rbac import require_role
from app.services.resource_service import (
    create_new_resource,
    get_resource,
    list_resources,
)

router = APIRouter(
    prefix="/lessons",
    tags=["Resources"],
)


@router.post(
    "/{lesson_id}/resources",
    response_model=ResourceResponse,
    status_code=201,
)
def create_resource_endpoint(
    lesson_id: int,
    payload: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return create_new_resource(
        db=db,
        lesson_id=lesson_id,
        title=payload.title,
        resource_type=payload.resource_type,
        url=payload.url,
    )


@router.get(
    "/{lesson_id}/resources",
    response_model=list[ResourceResponse],
)
def get_resources_endpoint(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    return list_resources(
        db=db,
        lesson_id=lesson_id,
    )


@router.get(
    "/resources/{resource_id}",
    response_model=ResourceResponse,
)
def get_resource_endpoint(
    resource_id: int,
    db: Session = Depends(get_db),
):
    return get_resource(
        db=db,
        resource_id=resource_id,
    )