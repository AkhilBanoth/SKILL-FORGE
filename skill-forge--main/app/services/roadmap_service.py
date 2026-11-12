
from sqlalchemy.orm import Session

from app.business.roadmap_engine import generate_learning_roadmap
from app.repositories.career_repository import get_career_by_id
from app.repositories.career_skill_repository import get_career_skills
from app.repositories.skill_repository import get_skill_by_id
from app.repositories.user_skill_repository import get_user_skills


def create_career_learning_roadmap(
    db: Session,
    user_id: int,
    career_id: int,
):
    career = get_career_by_id(db, career_id)

    if career is None:
        return None

    career_skills = get_career_skills(db, career_id)
    user_skills = get_user_skills(db, user_id)

    required_skill_names = []
    for career_skill in career_skills:
        skill = get_skill_by_id(db, career_skill.skill_id)
        if skill is not None:
            required_skill_names.append(skill.name)

    user_skill_names = []
    for user_skill in user_skills:
        skill = get_skill_by_id(db, user_skill.skill_id)
        if skill is not None and user_skill.level > 0:
            user_skill_names.append(skill.name)

    result = generate_learning_roadmap(
        required_skills=required_skill_names,
        user_skills=user_skill_names,
    )

    return {
        "career_id": career.id,
        "career_title": career.title,
        **result,
    }
