from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.assessment_answer_repository import (
    create_answer,
    get_answer_by_question,
    get_answers_by_attempt,
)
from app.repositories.assessment_attempt_repository import get_attempt_by_id
from app.repositories.assessment_question_repository import get_question_by_id


def submit_assessment_answer(
    db: Session,
    attempt_id: int,
    user_id: int,
    question_id: int,
    selected_answer: str,
):
    attempt = get_attempt_by_id(db, attempt_id)

    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment attempt not found",
        )

    if attempt.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to answer this attempt",
        )

    if attempt.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This assessment attempt is no longer accepting answers",
        )

    question = get_question_by_id(db, question_id)

    if question is None or not question.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment question not found",
        )

    if question.assessment_id != attempt.assessment_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question does not belong to this assessment",
        )

    existing_answer = get_answer_by_question(
        db,
        attempt_id,
        question_id,
    )

    if existing_answer is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already answered this question",
        )

    return create_answer(
        db=db,
        attempt_id=attempt_id,
        question_id=question_id,
        selected_answer=selected_answer,
    )


def list_attempt_answers(
    db: Session,
    attempt_id: int,
    user_id: int,
):
    attempt = get_attempt_by_id(db, attempt_id)

    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment attempt not found",
        )

    if attempt.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access these answers",
        )

    return get_answers_by_attempt(db, attempt_id)