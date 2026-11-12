from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(
    db: Session,
    project_data: ProjectCreate,
    user_id: int,
):
    project = Project(
        user_id=user_id,
        title=project_data.title,
        description=project_data.description,
        difficulty=project_data.difficulty,
        required_skills=project_data.required_skills,
        instructions=project_data.instructions,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_project_by_id(db: Session, project_id: int):
    return (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Project)
        .filter(Project.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_projects(db: Session, user_id: int):
    return (
        db.query(Project)
        .filter(Project.user_id == user_id)
        .order_by(Project.created_at.desc())
        .all()
    )


def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
):
    update_data = project_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


def delete_project(db: Session, project: Project):
    project.is_active = False

    db.commit()
    db.refresh(project)

    return project