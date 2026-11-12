
import json

from app.ai.gemini_service import generate_response


def analyze_skill_gaps(
    current_skills: list[str],
    required_skills: list[str],
    target_career: str,
) -> dict:
    """Analyze skill gaps and generate an improvement plan using Gemini."""

    current_set = {skill.strip().casefold() for skill in current_skills}
    required_set = {skill.strip().casefold() for skill in required_skills}

    matched_skills = [
        skill for skill in required_skills
        if skill.strip().casefold() in current_set
    ]
    missing_skills = [
        skill for skill in required_skills
        if skill.strip().casefold() not in current_set
    ]

    coverage = (
        round(len(matched_skills) / len(required_skills) * 100, 2)
        if required_skills
        else 100.0
    )

    prompt = f"""
You are the SkillForge career skill-gap analyst.

Target career: {target_career}
Learner's current skills: {json.dumps(current_skills, ensure_ascii=False)}
Required career skills: {json.dumps(required_skills, ensure_ascii=False)}
Matched skills: {json.dumps(matched_skills, ensure_ascii=False)}
Missing skills: {json.dumps(missing_skills, ensure_ascii=False)}
Skill coverage: {coverage}%

Return ONLY a valid JSON object, without Markdown code fences, containing:
- "summary": a short explanation of the learner's readiness
- "improvement_plan": a list of practical steps to develop missing skills

Rules:
- Base the plan on the supplied skill data.
- Prioritize important missing skills.
- Do not invent skills, qualifications, or experience.
- If no skills are missing, recommend ways to strengthen existing skills.
"""

    response_text = generate_response(prompt).strip()

    if response_text.startswith("```"):
        lines = response_text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        response_text = "\n".join(lines).strip()

    try:
        ai_result = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid JSON for skill-gap analysis."
        ) from exc

    if not isinstance(ai_result, dict):
        raise ValueError("Gemini must return a JSON object.")

    if not isinstance(ai_result.get("summary"), str):
        raise ValueError("Gemini response must contain a summary string.")

    if not isinstance(ai_result.get("improvement_plan"), list):
        raise ValueError("Gemini response must contain an improvement_plan list.")

    # Keep these calculations deterministic; do not trust AI-generated scores.
    return {
        "target_career": target_career,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "coverage": coverage,
        "summary": ai_result["summary"],
        "improvement_plan": ai_result["improvement_plan"],
    }
