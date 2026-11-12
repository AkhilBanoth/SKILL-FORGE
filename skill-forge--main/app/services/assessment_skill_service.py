from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.assessment_attempt import AssessmentAttempt
from app.models.assessment import Assessment


def evaluate_assessment_skill(
    db: Session,
    attempt_id: int,
    user_id: int,
):
    attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.user_id == user_id,
        )
        .first()
    )

    if attempt is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment attempt not found",
        )

    if attempt.status != "submitted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submit the assessment before evaluating skills",
        )

    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == attempt.assessment_id)
        .first()
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    percentage = (
        attempt.score / attempt.max_score * 100
        if attempt.max_score > 0
        else 0
    )

    if percentage >= 80:
        skill_level = "Advanced"
    elif percentage >= 60:
        skill_level = "Intermediate"
    else:
        skill_level = "Beginner"

    return {
        "attempt_id": attempt.id,
        "assessment_id": assessment.id,
        "assessment_title": assessment.title,
        "score": attempt.score,
        "max_score": attempt.max_score,
        "percentage": round(percentage, 2),
        "skill_level": skill_level,
    }