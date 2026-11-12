from sqlalchemy.orm import Session

from app.models.user_skill import UserSkill


def get_user_skills(
    db: Session,
    user_id: int,
) -> list[UserSkill]:
    return (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user_id)
        .all()
    )


def get_user_skill(
    db: Session,
    user_id: int,
    skill_id: int,
) -> UserSkill | None:
    return (
        db.query(UserSkill)
        .filter(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill_id,
        )
        .first()
    )


def create_user_skill(
    db: Session,
    user_id: int,
    skill_id: int,
    level: float,
) -> UserSkill:

    user_skill = UserSkill(
        user_id=user_id,
        skill_id=skill_id,
        level=level,
    )

    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)

    return user_skill