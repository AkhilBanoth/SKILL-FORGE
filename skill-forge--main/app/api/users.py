from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.user_skill import (
    UserSkillCreate,
    UserSkillResponse,
)
from app.services.user_skill_service import (
    add_skill_to_user,
    list_user_skills,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post(
    "/me/skills",
    response_model=UserSkillResponse,
    status_code=201,
)
def add_my_skill(
    payload: UserSkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return add_skill_to_user(
        db=db,
        user_id=current_user.id,
        skill_id=payload.skill_id,
        level=payload.level,
    )


@router.get(
    "/me/skills",
    response_model=list[UserSkillResponse],
)
def get_my_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_user_skills(
        db=db,
        user_id=current_user.id,
    )