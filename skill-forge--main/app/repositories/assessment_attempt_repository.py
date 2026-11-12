from datetime import datetime

from sqlalchemy.orm import Session

from app.models.assessment_attempt import AssessmentAttempt


def get_attempt_by_id(
    db: Session,
    attempt_id: int,
) -> AssessmentAttempt | None:
    return (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.id == attempt_id)
        .first()
    )


def get_attempts_by_user(
    db: Session,
    user_id: int,
) -> list[AssessmentAttempt]:
    return (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.user_id == user_id)
        .order_by(AssessmentAttempt.id.desc())
        .all()
    )


def get_active_attempt(
    db: Session,
    user_id: int,
    assessment_id: int,
) -> AssessmentAttempt | None:
    return (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.assessment_id == assessment_id,
            AssessmentAttempt.status == "in_progress",
        )
        .first()
    )


def create_attempt(
    db: Session,
    assessment_id: int,
    user_id: int,
    max_score: float,
) -> AssessmentAttempt:
    attempt = AssessmentAttempt(
        assessment_id=assessment_id,
        user_id=user_id,
        score=0.0,
        max_score=max_score,
        status="in_progress",
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


def submit_attempt(
    db: Session,
    attempt: AssessmentAttempt,
    score: float,
) -> AssessmentAttempt:
    attempt.score = score
    attempt.status = "submitted"
    attempt.submitted_at = datetime.utcnow()

    db.commit()
    db.refresh(attempt)

    return attempt