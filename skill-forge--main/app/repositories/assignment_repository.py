from sqlalchemy.orm import Session

from app.models.assignment import Assignment


def get_assignments_by_lesson(
    db: Session,
    lesson_id: int,
) -> list[Assignment]:
    return (
        db.query(Assignment)
        .filter(Assignment.lesson_id == lesson_id)
        .order_by(Assignment.id.asc())
        .all()
    )


def get_assignment_by_id(
    db: Session,
    assignment_id: int,
) -> Assignment | None:
    return (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id)
        .first()
    )


def create_assignment(
    db: Session,
    lesson_id: int,
    title: str,
    description: str | None,
    max_score: float,
) -> Assignment:
    assignment = Assignment(
        lesson_id=lesson_id,
        title=title.strip(),
        description=description,
        max_score=max_score,
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment