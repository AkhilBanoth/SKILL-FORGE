
def calculate_readiness(
    required_skills,
    user_skills,
    completed_projects=0,
    completed_assessments=0,
):
    """
    Calculate a career-readiness score.

    Skills contribute 70%.
    Projects contribute 20%.
    Assessments contribute 10%.
    """

    if completed_projects < 0 or completed_assessments < 0:
        raise ValueError(
            "Completed projects and assessments cannot be negative."
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

    if required:
        skill_score = (
            len(required.intersection(possessed))
            / len(required)
            * 100
        )
    else:
        skill_score = 100.0

    project_score = min(completed_projects / 3, 1) * 100
    assessment_score = min(completed_assessments / 5, 1) * 100

    readiness_score = (
        skill_score * 0.70
        + project_score * 0.20
        + assessment_score * 0.10
    )

    return {
        "readiness_score": round(readiness_score, 2),
        "skill_score": round(skill_score, 2),
        "project_score": round(project_score, 2),
        "assessment_score": round(assessment_score, 2),
        "missing_skills": sorted(required - possessed),
        "completed_projects": completed_projects,
        "completed_assessments": completed_assessments,
    }
