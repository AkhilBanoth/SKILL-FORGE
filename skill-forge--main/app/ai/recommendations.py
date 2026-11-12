
import json

from app.ai.gemini_service import generate_response


def generate_learning_recommendations(
    skills: list[str],
    completed_courses: list[str] | None = None,
    target_career: str | None = None,
) -> list[dict]:
    """Generate personalized learning recommendations using Gemini."""

    completed_courses = completed_courses or []

    prompt = f"""
You are the AI learning recommendation assistant for SkillForge.

Learner's current skills:
{json.dumps(skills, ensure_ascii=False)}

Completed courses:
{json.dumps(completed_courses, ensure_ascii=False)}

Target career:
{target_career or "Not specified"}

Generate exactly 5 personalized learning recommendations.

Return ONLY a valid JSON array, without Markdown code fences.

Each recommendation must contain:
- "topic": string
- "reason": string
- "priority": one of "high", "medium", "low"
- "next_step": string

Rules:
- Base recommendations on the provided learner information.
- Prioritize important missing skills for the target career when known.
- Do not claim the learner completed courses or possesses skills unless provided.
- If information is limited, make reasonable suggestions and state uncertainty.
- Return exactly 5 recommendations.
"""

    response_text = generate_response(prompt).strip()

    # Remove Markdown code fences if Gemini includes them.
    if response_text.startswith("```"):
        lines = response_text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        response_text = "\n".join(lines).strip()

    try:
        recommendations = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid JSON for learning recommendations."
        ) from exc

    if not isinstance(recommendations, list) or len(recommendations) != 5:
        raise ValueError(
            "Gemini must return exactly 5 learning recommendations."
        )

    required_fields = {"topic", "reason", "priority", "next_step"}
    valid_priorities = {"high", "medium", "low"}

    for item in recommendations:
        if not isinstance(item, dict):
            raise ValueError("Each recommendation must be a JSON object.")

        if not required_fields.issubset(item.keys()):
            raise ValueError("A recommendation is missing required fields.")

        if item["priority"] not in valid_priorities:
            raise ValueError("Recommendation priority must be high, medium, or low.")

    return recommendations
