from sqlalchemy.orm import Session

from app.repositories.career_repository import get_all_careers
from app.repositories.career_skill_repository import get_career_skills
from app.repositories.user_skill_repository import get_user_skill


def calculate_career_recommendations(
    db: Session,
    user_id: int,
):
    careers = get_all_careers(db)

    recommendations = []

    for career in careers:
        career_skills = get_career_skills(
            db,
            career.id,
        )

        if not career_skills:
            continue

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

        if total_required == 0:
            match_score = 0.0
        else:
            match_score = (
                total_achieved / total_required
            ) * 100

        recommendations.append(
            {
                "career_id": career.id,
                "career_title": career.title,
                "match_score": round(
                    match_score,
                    2,
                ),
            }
        )

    recommendations.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    return {
        "user_id": user_id,
        "recommendations": recommendations,
    }