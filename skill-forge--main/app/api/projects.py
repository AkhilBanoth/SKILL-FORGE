from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import (
    create_new_project,
    delete_existing_project,
    get_all_projects,
    get_project_details,
    get_projects_by_user,
    update_existing_project,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


def is_admin_user(user: User) -> bool:
    return getattr(user, "role", None) == "admin"


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_endpoint(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_project(
        db=db,
        project_data=project_data,
        user_id=current_user.id,
    )


@router.get("", response_model=list[ProjectResponse])
def list_projects_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_projects(db=db, skip=skip, limit=limit)


@router.get("/my", response_model=list[ProjectResponse])
def list_my_projects_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_projects_by_user(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_endpoint(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_project_details(db=db, project_id=project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project_endpoint(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_existing_project(
        db=db,
        project_id=project_id,
        project_data=project_data,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
    )


@router.delete("/{project_id}", response_model=ProjectResponse)
def delete_project_endpoint(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_existing_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
    )