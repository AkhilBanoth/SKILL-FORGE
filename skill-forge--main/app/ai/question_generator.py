
import json

from app.ai.gemini_service import generate_response


def generate_questions(
    topic: str,
    difficulty: str = "medium",
    number_of_questions: int = 5,
) -> list[dict]:
    """Generate multiple-choice questions using Gemini."""

    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    if difficulty not in {"easy", "medium", "hard"}:
        raise ValueError("Difficulty must be easy, medium, or hard.")

    if not 1 <= number_of_questions <= 20:
        raise ValueError("Number of questions must be between 1 and 20.")

    prompt = f"""
You are an assessment question generator for SkillForge.

Generate exactly {number_of_questions} multiple-choice questions.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY a valid JSON array. Do not use Markdown code fences.

Each array item must contain:
- "question": a string
- "options": an object with keys "A", "B", "C", "D"
- "correct_answer": one of "A", "B", "C", "D"
- "explanation": a string

Requirements:
- Questions must be relevant to the specified topic.
- Match the requested difficulty.
- Provide exactly four options per question.
- Only one option must be correct.
- Make explanations clear and concise.
- Generate exactly {number_of_questions} questions.
"""

    last_error = None

    for attempt in range(2):
        try:
            response_text = generate_response(prompt).strip()

            # Handle responses wrapped in Markdown code fences.
            if response_text.startswith("```"):
                lines = response_text.splitlines()
                if lines and lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                response_text = "\n".join(lines).strip()

            questions = json.loads(response_text)

            if not isinstance(questions, list):
                raise ValueError("Gemini response must be a JSON array.")

            if len(questions) != number_of_questions:
                raise ValueError(
                    f"Expected {number_of_questions} questions, "
                    f"received {len(questions)}."
                )

            for question in questions:
                if not isinstance(question, dict):
                    raise ValueError("Each question must be a JSON object.")

                if not all(
                    key in question
                    for key in (
                        "question",
                        "options",
                        "correct_answer",
                        "explanation",
                    )
                ):
                    raise ValueError("A question is missing required fields.")

                options = question["options"]
                if not isinstance(options, dict) or set(options.keys()) != {
                    "A", "B", "C", "D"
                }:
                    raise ValueError(
                        "Each question must have options A, B, C, and D."
                    )

                if question["correct_answer"] not in {"A", "B", "C", "D"}:
                    raise ValueError("Invalid correct_answer value.")

            return questions

        except (json.JSONDecodeError, ValueError) as exc:
            last_error = exc
            if attempt == 0:
                prompt += """
IMPORTANT: Your previous response was invalid.
Return only a valid JSON array with the exact required structure.
"""
            else:
                raise ValueError(
                    f"Could not generate valid questions: {last_error}"
                ) from last_error

    raise ValueError(f"Could not generate questions: {last_error}")
