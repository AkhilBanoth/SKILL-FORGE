from sqlalchemy.orm import Session

from app.models.assessment_question import AssessmentQuestion


def get_question_by_id(
    db: Session,
    question_id: int,
) -> AssessmentQuestion | None:
    return (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.id == question_id)
        .first()
    )


def get_questions_by_assessment(
    db: Session,
    assessment_id: int,
) -> list[AssessmentQuestion]:
    return (
        db.query(AssessmentQuestion)
        .filter(
            AssessmentQuestion.assessment_id == assessment_id,
            AssessmentQuestion.is_active == True,
        )
        .order_by(AssessmentQuestion.id.asc())
        .all()
    )


def create_question(
    db: Session,
    assessment_id: int,
    question_text: str,
    question_type: str,
    option_a: str | None,
    option_b: str | None,
    option_c: str | None,
    option_d: str | None,
    correct_answer: str,
    marks: float,
) -> AssessmentQuestion:
    question = AssessmentQuestion(
        assessment_id=assessment_id,
        question_text=question_text.strip(),
        question_type=question_type.strip(),
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct_answer.strip(),
        marks=marks,
        is_active=True,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question