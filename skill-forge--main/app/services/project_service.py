from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.project_repository import (
    create_project,
    delete_project,
    get_project_by_id,
    get_projects,
    get_user_projects,
    update_project,
)
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_new_project(
    db: Session,
    project_data: ProjectCreate,
    user_id: int,
):
    return create_project(
        db=db,
        project_data=project_data,
        user_id=user_id,
    )


def get_project_details(db: Session, project_id: int):
    project = get_project_by_id(db, project_id)

    if project is None or not project.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


def get_all_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    return get_projects(db, skip=skip, limit=limit)


def get_projects_by_user(db: Session, user_id: int):
    return get_user_projects(db, user_id)


def update_existing_project(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate,
    user_id: int,
    is_admin: bool = False,
):
    project = get_project_details(db, project_id)

    if project.user_id != user_id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this project",
        )

    return update_project(
        db=db,
        project=project,
        project_data=project_data,
    )


def delete_existing_project(
    db: Session,
    project_id: int,
    user_id: int,
    is_admin: bool = False,
):
    project = get_project_details(db, project_id)

    if project.user_id != user_id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this project",
        )

    return delete_project(db=db, project=project)