from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.assessment_question_repository import (
    create_question,
    get_question_by_id,
    get_questions_by_assessment,
)
from app.repositories.assessment_repository import get_assessment_by_id


def create_new_question(
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
):
    assessment = get_assessment_by_id(
        db,
        assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    return create_question(
        db=db,
        assessment_id=assessment_id,
        question_text=question_text,
        question_type=question_type,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct_answer,
        marks=marks,
    )


def list_assessment_questions(
    db: Session,
    assessment_id: int,
):
    assessment = get_assessment_by_id(
        db,
        assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    return get_questions_by_assessment(
        db,
        assessment_id,
    )


def get_assessment_question(
    db: Session,
    question_id: int,
):
    question = get_question_by_id(
        db,
        question_id,
    )

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment question not found",
        )

    return question