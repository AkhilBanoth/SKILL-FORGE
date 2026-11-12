from sqlalchemy.orm import Session

from app.models.course import Course


def get_all_courses(
    db: Session,
) -> list[Course]:
    return (
        db.query(Course)
        .filter(Course.is_active == True)
        .order_by(Course.title.asc())
        .all()
    )


def get_course_by_id(
    db: Session,
    course_id: int,
) -> Course | None:
    return (
        db.query(Course)
        .filter(Course.id == course_id)
        .first()
    )


def get_course_by_title(
    db: Session,
    title: str,
) -> Course | None:
    return (
        db.query(Course)
        .filter(Course.title.ilike(title))
        .first()
    )


def create_course(
    db: Session,
    title: str,
    description: str | None,
    skill_id: int | None,
    level: str,
    duration_hours: float,
) -> Course:
    course = Course(
        title=title.strip(),
        description=description,
        skill_id=skill_id,
        level=level.strip(),
        duration_hours=duration_hours,
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course