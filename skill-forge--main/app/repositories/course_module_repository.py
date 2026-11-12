from sqlalchemy.orm import Session

from app.models.course_module import CourseModule


def get_course_modules(
    db: Session,
    course_id: int,
) -> list[CourseModule]:
    return (
        db.query(CourseModule)
        .filter(
            CourseModule.course_id == course_id
        )
        .order_by(
            CourseModule.order_index.asc()
        )
        .all()
    )


def get_course_module_by_id(
    db: Session,
    module_id: int,
) -> CourseModule | None:
    return (
        db.query(CourseModule)
        .filter(
            CourseModule.id == module_id
        )
        .first()
    )


def create_course_module(
    db: Session,
    course_id: int,
    title: str,
    description: str | None,
    order_index: int,
) -> CourseModule:
    module = CourseModule(
        course_id=course_id,
        title=title.strip(),
        description=description,
        order_index=order_index,
    )

    db.add(module)
    db.commit()
    db.refresh(module)

    return module