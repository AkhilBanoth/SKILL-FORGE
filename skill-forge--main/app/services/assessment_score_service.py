from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.assessment_attempt_repository import (
    get_attempt_by_id,
    submit_attempt,
)
from app.repositories.assessment_answer_repository import (
    get_answers_by_attempt,
    update_answer_result,
)
from app.repositories.assessment_question_repository import get_question_by_id


def calculate_assessment_score(
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
            detail="You do not have permission to submit this attempt",
        )

    if attempt.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This assessment attempt has already been submitted",
        )

    answers = get_answers_by_attempt(db, attempt_id)

    if not answers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submit at least one answer before submitting the assessment",
        )

    total_score = 0.0

    for answer in answers:
        question = get_question_by_id(db, answer.question_id)

        if question is None or not question.is_active:
            continue

        is_correct = (
            answer.selected_answer.strip().casefold()
            == question.correct_answer.strip().casefold()
        )

        marks_awarded = question.marks if is_correct else 0.0

        update_answer_result(
            db=db,
            answer=answer,
            is_correct=is_correct,
            marks_awarded=marks_awarded,
        )

        total_score += marks_awarded

    total_score = min(total_score, attempt.max_score)

    return submit_attempt(
        db=db,
        attempt=attempt,
        score=total_score,
    )