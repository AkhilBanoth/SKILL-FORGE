from app.dependencies import get_current_user
from app.models.user import User
from app.security.rbac import require_role

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.schemas.skill import SkillCreate, SkillResponse
from app.services.skill_service import (
    create_new_skill,
    get_skill,
    list_skills,
)


router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
)


@router.post(
    "",
    response_model=SkillResponse,
    status_code=201,
)
def create_skill_endpoint(
    payload: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return create_new_skill(
        db=db,
        name=payload.name,
        category=payload.category,
        description=payload.description,
    )

@router.get(
    "",
    response_model=list[SkillResponse],
)
def get_all_skills_endpoint(
    db: Session = Depends(get_db),
):
    return list_skills(db)


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
)
def get_skill_endpoint(
    skill_id: int,
    db: Session = Depends(get_db),
):
    return get_skill(
        db=db,
        skill_id=skill_id,
    )