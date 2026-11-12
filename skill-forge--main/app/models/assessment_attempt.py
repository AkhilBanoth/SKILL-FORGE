from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres import Base


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

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

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    score: Mapped[float] = mapped_column(
        nullable=False,
        default=0.0,
    )

    max_score: Mapped[float] = mapped_column(
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="in_progress",
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )