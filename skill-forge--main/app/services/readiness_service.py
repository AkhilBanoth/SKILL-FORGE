from sqlalchemy.orm import Session

from app.repositories.career_repository import get_career_by_id
from app.repositories.career_skill_repository import get_career_skills
from app.repositories.user_skill_repository import get_user_skill


def calculate_readiness(
    db: Session,
    user_id: int,
    career_id: int,
):
    career = get_career_by_id(
        db,
        career_id,
    )

    if career is None:
        return None

    career_skills = get_career_skills(
        db,
        career_id,
    )

    if not career_skills:
        return {
            "career_id": career_id,
            "career_title": career.title,
            "readiness_score": 0.0,
        }

    total_required = 0.0
    total_achieved = 0.0

    for career_skill in career_skills:
        user_skill = get_user_skill(
            db,
            user_id,
            career_skill.skill_id,
        )

        required_level = career_skill.weight

        current_level = (
            user_skill.level
            if user_skill
            else 0.0
        )

        current_level = min(
            current_level,
            required_level,
        )

        total_required += required_level
        total_achieved += current_level

    readiness_score = (
        total_achieved / total_required
    ) * 100

    return {
        "career_id": career_id,
        "career_title": career.title,
        "readiness_score": round(
            readiness_score,
            2,
        ),
    }