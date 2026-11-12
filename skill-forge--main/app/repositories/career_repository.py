
from sqlalchemy.orm import Session

from app.models.career import Career


def get_all_careers(
    db: Session,
) -> list[Career]:
    return (
        db.query(Career)
        .order_by(Career.title.asc())
        .all()
    )


def get_career_by_id(
    db: Session,
    career_id: int,
) -> Career | None:
    return (
        db.query(Career)
        .filter(Career.id == career_id)
        .first()
    )


def get_career_by_title(
    db: Session,
    title: str,
) -> Career | None:
    return (
        db.query(Career)
        .filter(Career.title.ilike(title))
        .first()
    )


def create_career(
    db: Session,
    title: str,
    description: str | None = None,
) -> Career:

    career = Career(
        title=title.strip(),
        description=description,
    )

    db.add(career)
    db.commit()
    db.refresh(career)

    return career