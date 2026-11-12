
from fastapi import APIRouter, Depends, Query

from app.ai.question_generator import generate_questions
from app.ai.skill_analysis import analyze_skill_gaps
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/ai",
    tags=["AI Features"],
)


@router.get("/generate-questions")
def create_ai_questions(
    topic: str = Query(..., min_length=1, max_length=200),
    difficulty: str = Query("medium", pattern="^(easy|medium|hard)$"),
    number_of_questions: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
):
    questions = generate_questions(
        topic=topic,
        difficulty=difficulty,
        number_of_questions=number_of_questions,
    )

    return {
        "user_id": current_user.id,
        "topic": topic,
        "difficulty": difficulty,
        "total_questions": len(questions),
        "questions": questions,
    }


@router.get("/analyze-skill-gaps")
def create_ai_skill_analysis(
    current_skills: list[str] = Query(...),
    required_skills: list[str] = Query(...),
    target_career: str = Query(..., min_length=1, max_length=150),
    current_user: User = Depends(get_current_user),
):
    analysis = analyze_skill_gaps(
        current_skills=current_skills,
        required_skills=required_skills,
        target_career=target_career,
    )

    return {
        "user_id": current_user.id,
        **analysis,
    }