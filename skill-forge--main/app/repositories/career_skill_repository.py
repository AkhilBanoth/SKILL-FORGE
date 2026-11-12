from sqlalchemy.orm import Session

from app.models.career_skill import CareerSkill


def get_career_skills(
    db: Session,
    career_id: int,
) -> list[CareerSkill]:
    return (
        db.query(CareerSkill)
        .filter(CareerSkill.career_id == career_id)
        .all()
    )


def get_career_skill(
    db: Session,
    career_id: int,
    skill_id: int,
) -> CareerSkill | None:
    return (
        db.query(CareerSkill)
        .filter(
            CareerSkill.career_id == career_id,
            CareerSkill.skill_id == skill_id,
        )
        .first()
    )


def create_career_skill(
    db: Session,
    career_id: int,
    skill_id: int,
    weight: float,
) -> CareerSkill:

    career_skill = CareerSkill(
        career_id=career_id,
        skill_id=skill_id,
        weight=weight,
    )

    db.add(career_skill)
    db.commit()
    db.refresh(career_skill)

    return career_skill