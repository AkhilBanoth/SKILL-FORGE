from sqlalchemy import Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres import Base


class CareerSkill(Base):
    __tablename__ = "career_skills"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    career_id: Mapped[int] = mapped_column(
        ForeignKey("careers.id"),
        nullable=False,
        index=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        nullable=False,
        index=True,
    )

    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "career_id",
            "skill_id",
            name="uq_career_skill",
        ),
    )