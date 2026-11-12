
def check_certification_eligibility(
    required_skills,
    user_skills,
    required_readiness_score=70,
    user_readiness_score=0,
    required_projects=0,
    completed_projects=0,
):
    """
    Check whether a user meets the configured certification
    eligibility requirements.

    These are configurable example rules. Adjust them to
    match the actual requirements of each certification.
    """

    if not 0 <= required_readiness_score <= 100:
        raise ValueError(
            "Required readiness score must be between 0 and 100."
        )

    if not 0 <= user_readiness_score <= 100:
        raise ValueError(
            "User readiness score must be between 0 and 100."
        )

    if required_projects < 0 or completed_projects < 0:
        raise ValueError(
            "Project counts cannot be negative."
        )

    required = {
        skill.strip().casefold()
        for skill in required_skills
        if isinstance(skill, str) and skill.strip()
    }

    possessed = {
        skill.strip().casefold()
        for skill in user_skills
        if isinstance(skill, str) and skill.strip()
    }

    missing_skills = sorted(required - possessed)

    readiness_met = (
        user_readiness_score >= required_readiness_score
    )

    projects_met = completed_projects >= required_projects

    eligible = (
        not missing_skills
        and readiness_met
        and projects_met
    )

    reasons = []

    if missing_skills:
        reasons.append("Required skills are missing.")

    if not readiness_met:
        reasons.append(
            "The required readiness score has not been reached."
        )

    if not projects_met:
        reasons.append(
            "The required number of projects has not been completed."
        )

    if eligible:
        reasons.append(
            "All configured certification requirements are met."
        )

    return {
        "eligible": eligible,
        "missing_skills": missing_skills,
        "readiness_score": user_readiness_score,
        "required_readiness_score": required_readiness_score,
        "completed_projects": completed_projects,
        "required_projects": required_projects,
        "reasons": reasons,
    }
