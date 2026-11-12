from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres import Base


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id"),
        nullable=False,
        index=True,
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    question_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="mcq",
    )

    option_a: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    option_b: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    option_c: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    option_d: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    correct_answer: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    marks: Mapped[float] = mapped_column(
        nullable=False,
        default=1.0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )