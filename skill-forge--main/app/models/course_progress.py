from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres import Base


class CourseProgress(Base):
    __tablename__ = "course_progress"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False,
        index=True,
    )

    progress_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    completed_lessons: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    total_lessons: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "course_id",
            name="uq_user_course_progress",
        ),
    )