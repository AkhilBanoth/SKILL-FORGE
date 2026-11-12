
from typing import Iterable


def analyze_skill_gap(
    required_skills: Iterable[str],
    user_skills: Iterable[str],
) -> dict:
    """
    Compare a user's skills with the skills required
    for a target career.
    """
    required = {
        skill.strip().casefold()
        for skill in required_skills
        if skill and skill.strip()
    }

    possessed = {
        skill.strip().casefold()
        for skill in user_skills
        if skill and skill.strip()
    }

    matched = sorted(required & possessed)
    missing = sorted(required - possessed)
    extra = sorted(possessed - required)

    total_required = len(required)

    gap_percentage = (
        round(len(missing) / total_required * 100, 2)
        if total_required
        else 0.0
    )

    match_percentage = (
        round(len(matched) / total_required * 100, 2)
        if total_required
        else 100.0
    )

    return {
        "required_skills": sorted(required),
        "user_skills": sorted(possessed),
        "matched_skills": matched,
        "missing_skills": missing,
        "additional_skills": extra,
        "total_required_skills": total_required,
        "matched_count": len(matched),
        "missing_count": len(missing),
        "gap_percentage": gap_percentage,
        "match_percentage": match_percentage,
    }
