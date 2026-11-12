from sqlalchemy.orm import Session

from app.models.skill import Skill


def get_all_skills(
    db: Session,
) -> list[Skill]:
    return (
        db.query(Skill)
        .order_by(Skill.name.asc())
        .all()
    )


def get_skill_by_id(
    db: Session,
    skill_id: int,
) -> Skill | None:
    return (
        db.query(Skill)
        .filter(Skill.id == skill_id)
        .first()
    )


def get_skill_by_name(
    db: Session,
    name: str,
) -> Skill | None:
    return (
        db.query(Skill)
        .filter(Skill.name.ilike(name))
        .first()
    )


def create_skill(
    db: Session,
    name: str,
    category: str,
    description: str | None = None,
) -> Skill:

    skill = Skill(
        name=name.strip(),
        category=category.strip(),
        description=description,
    )

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return skill