from sqlalchemy.orm import Session

from app.models.assessment_answer import AssessmentAnswer


def get_answer_by_id(
    db: Session,
    answer_id: int,
) -> AssessmentAnswer | None:
    return (
        db.query(AssessmentAnswer)
        .filter(AssessmentAnswer.id == answer_id)
        .first()
    )


def get_answer_by_question(
    db: Session,
    attempt_id: int,
    question_id: int,
) -> AssessmentAnswer | None:
    return (
        db.query(AssessmentAnswer)
        .filter(
            AssessmentAnswer.attempt_id == attempt_id,
            AssessmentAnswer.question_id == question_id,
        )
        .first()
    )


def get_answers_by_attempt(
    db: Session,
    attempt_id: int,
) -> list[AssessmentAnswer]:
    return (
        db.query(AssessmentAnswer)
        .filter(AssessmentAnswer.attempt_id == attempt_id)
        .order_by(AssessmentAnswer.id.asc())
        .all()
    )


def create_answer(
    db: Session,
    attempt_id: int,
    question_id: int,
    selected_answer: str,
) -> AssessmentAnswer:
    answer = AssessmentAnswer(
        attempt_id=attempt_id,
        question_id=question_id,
        selected_answer=selected_answer.strip(),
        is_correct=None,
        marks_awarded=0.0,
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer


def update_answer_result(
    db: Session,
    answer: AssessmentAnswer,
    is_correct: bool,
    marks_awarded: float,
) -> AssessmentAnswer:
    answer.is_correct = is_correct
    answer.marks_awarded = marks_awarded

    db.commit()
    db.refresh(answer)

    return answer