
def generate_learning_roadmap(
    required_skills,
    user_skills,
):
    """
    Generate a learning roadmap from missing career skills.

    Missing skills are placed in the order provided
    in required_skills.
    """

    possessed = {
        skill.strip().casefold()
        for skill in user_skills
        if isinstance(skill, str) and skill.strip()
    }

    roadmap = []
    step_number = 1

    for skill in required_skills:
        if not isinstance(skill, str) or not skill.strip():
            continue

        normalized_skill = skill.strip()

        if normalized_skill.casefold() in possessed:
            continue

        roadmap.append({
            "step": step_number,
            "skill": normalized_skill,
            "objective": (
                f"Learn the fundamentals of {normalized_skill} "
                "and practise with hands-on exercises."
            ),
            "recommended_activity": (
                f"Complete a beginner tutorial and build a small "
                f"project using {normalized_skill}."
            ),
            "status": "not_started",
        })

        step_number += 1

    return {
        "total_steps": len(roadmap),
        "roadmap": roadmap,
        "message": (
            "Learning roadmap generated successfully."
            if roadmap
            else "No skill gaps found. You already have all "
                 "the listed required skills."
        ),
    }
