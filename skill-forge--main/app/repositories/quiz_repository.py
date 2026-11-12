from sqlalchemy.orm import Session

from app.models.quiz import Quiz


def get_quizzes_by_lesson(
    db: Session,
    lesson_id: int,
) -> list[Quiz]:
    return (
        db.query(Quiz)
        .filter(
            Quiz.lesson_id == lesson_id,
            Quiz.is_active == True,
        )
        .order_by(Quiz.id.asc())
        .all()
    )


def get_quiz_by_id(
    db: Session,
    quiz_id: int,
) -> Quiz | None:
    return (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id)
        .first()
    )


def create_quiz(
    db: Session,
    lesson_id: int,
    title: str,
    description: str | None,
    passing_score: float,
) -> Quiz:
    quiz = Quiz(
        lesson_id=lesson_id,
        title=title.strip(),
        description=description,
        passing_score=passing_score,
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz