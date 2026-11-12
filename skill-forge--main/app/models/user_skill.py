from sqlalchemy import Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres import Base


class UserSkill(Base):
    __tablename__ = "user_skills"

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

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        nullable=False,
        index=True,
    )

    level: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "skill_id",
            name="uq_user_skill",
        ),
    )