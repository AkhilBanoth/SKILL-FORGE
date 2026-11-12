from sqlalchemy.orm import Session

from app.models.assessment import Assessment


def get_assessment_by_id(
    db: Session,
    assessment_id: int,
) -> Assessment | None:
    return (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )


def get_assessments_by_user(
    db: Session,
    user_id: int,
) -> list[Assessment]:
    return (
        db.query(Assessment)
        .filter(Assessment.user_id == user_id)
        .order_by(Assessment.id.desc())
        .all()
    )


def create_assessment(
    db: Session,
    user_id: int,
    career_id: int | None,
    title: str,
    description: str | None,
    max_score: float,
) -> Assessment:
    assessment = Assessment(
        user_id=user_id,
        career_id=career_id,
        title=title.strip(),
        description=description,
        score=0.0,
        max_score=max_score,
        status="pending",
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment