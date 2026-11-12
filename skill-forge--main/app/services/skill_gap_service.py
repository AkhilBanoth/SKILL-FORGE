from sqlalchemy.orm import Session

from app.repositories.career_repository import get_career_by_id
from app.repositories.career_skill_repository import get_career_skills
from app.repositories.user_skill_repository import get_user_skill


def calculate_skill_gap(
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

    results = []

    total_gap = 0.0

    for career_skill in career_skills:
        user_skill = get_user_skill(
            db,
            user_id,
            career_skill.skill_id,
        )

        current_level = (
            user_skill.level
            if user_skill
            else 0.0
        )

        required_level = career_skill.weight

        gap = max(
            required_level - current_level,
            0.0,
        )

        total_gap += gap

        results.append(
            {
                "skill_id": career_skill.skill_id,
                "required_weight": required_level,
                "current_level": current_level,
                "gap": gap,
            }
        )

    if career_skills:
        overall_gap = total_gap / len(career_skills)
    else:
        overall_gap = 0.0

    return {
        "career_id": career_id,
        "user_id": user_id,
        "skills": results,
        "overall_gap": overall_gap,
    }