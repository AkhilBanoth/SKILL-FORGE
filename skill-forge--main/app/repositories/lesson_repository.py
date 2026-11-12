from sqlalchemy.orm import Session

from app.models.lesson import Lesson


def get_lessons_by_module(
    db: Session,
    module_id: int,
) -> list[Lesson]:
    return (
        db.query(Lesson)
        .filter(
            Lesson.module_id == module_id
        )
        .order_by(
            Lesson.order_index.asc()
        )
        .all()
    )


def get_lesson_by_id(
    db: Session,
    lesson_id: int,
) -> Lesson | None:
    return (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id
        )
        .first()
    )


def create_lesson(
    db: Session,
    module_id: int,
    title: str,
    content: str | None,
    order_index: int,
    duration_minutes: int,
) -> Lesson:
    lesson = Lesson(
        module_id=module_id,
        title=title.strip(),
        content=content,
        order_index=order_index,
        duration_minutes=duration_minutes,
    )

    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    return lesson