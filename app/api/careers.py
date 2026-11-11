from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.models.user import User
from app.security.rbac import require_role
from app.schemas.career import CareerCreate, CareerResponse
from app.schemas.career_skill import (
    CareerSkillCreate,
    CareerSkillResponse,
)
from app.services.career_service import (
    create_new_career,
    get_career,
    list_careers,
)
from app.services.career_skill_service import (
    add_skill_to_career,
    list_career_skills,
)


router = APIRouter(
    prefix="/careers",
    tags=["Careers"],
)


@router.post(
    "",
    response_model=CareerResponse,
    status_code=201,
)
def create_career_endpoint(
    payload: CareerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return create_new_career(
        db=db,
        title=payload.title,
        description=payload.description,
    )


@router.get(
    "",
    response_model=list[CareerResponse],
)
def get_all_careers_endpoint(
    db: Session = Depends(get_db),
):
    return list_careers(db)


@router.get(
    "/{career_id}",
    response_model=CareerResponse,
)
def get_career_endpoint(
    career_id: int,
    db: Session = Depends(get_db),
):
    return get_career(
        db=db,
        career_id=career_id,
    )


@router.post(
    "/{career_id}/skills",
    response_model=CareerSkillResponse,
    status_code=201,
)
def add_skill_to_career_endpoint(
    career_id: int,
    payload: CareerSkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return add_skill_to_career(
        db=db,
        career_id=career_id,
        skill_id=payload.skill_id,
        weight=payload.weight,
    )


@router.get(
    "/{career_id}/skills",
    response_model=list[CareerSkillResponse],
)
def get_career_skills_endpoint(
    career_id: int,
    db: Session = Depends(get_db),
):
    return list_career_skills(
        db=db,
        career_id=career_id,
    )