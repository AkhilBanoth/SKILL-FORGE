
from typing import Iterable


def match_careers(
    user_skills: Iterable[str],
    careers: Iterable[dict],
) -> list[dict]:
    """
    Rank careers according to how closely their required
    skills match the user's existing skills.

    Each career should contain:
        - id (optional)
        - title
        - required_skills (list of strings)
    """
    normalized_user_skills = {
        skill.strip().casefold()
        for skill in user_skills
        if isinstance(skill, str) and skill.strip()
    }

    results = []

    for career in careers:
        if not isinstance(career, dict):
            continue

        title = career.get("title", "Untitled Career")
        required_skills = career.get("required_skills", [])

        if not isinstance(required_skills, (list, tuple, set)):
            required_skills = []

        normalized_required = {
            skill.strip().casefold()
            for skill in required_skills
            if isinstance(skill, str) and skill.strip()
        }

        matched = sorted(
            normalized_required & normalized_user_skills
        )
        missing = sorted(
            normalized_required - normalized_user_skills
        )

        total = len(normalized_required)

        score = (
            round(len(matched) / total * 100, 2)
            if total
            else 0.0
        )

        results.append(
            {
                "career_id": career.get("id"),
                "career_title": title,
                "match_percentage": score,
                "matched_skills": matched,
                "missing_skills": missing,
                "required_skills_count": total,
            }
        )

    results.sort(
        key=lambda item: item["match_percentage"],
        reverse=True,
    )

    return results