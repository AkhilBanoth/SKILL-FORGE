from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres import Base


class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("assessment_attempts.id"),
        nullable=False,
        index=True,
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("assessment_questions.id"),
        nullable=False,
        index=True,
    )

    selected_answer: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    is_correct: Mapped[bool | None] = mapped_column(
        nullable=True,
    )

    marks_awarded: Mapped[float] = mapped_column(
        nullable=False,
        default=0.0,
    )

    answered_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "attempt_id",
            "question_id",
            name="uq_attempt_question_answer",
        ),
    )