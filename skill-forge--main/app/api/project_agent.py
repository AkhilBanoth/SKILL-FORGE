from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agents.project_agent import ask_project_agent
from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.ai_learning_recommendation_service import (
    generate_learning_recommendations,
)


router = APIRouter(
    prefix="/project-agent",
    tags=["SkillForge AI Agent"],
)


class ProjectAgentRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000,
        description="Ask SkillForge a project, technical, or career question.",
    )


class ProjectAgentResponse(BaseModel):
    question: str
    answer: str


LEARNING_KEYWORDS = (
    "my skill",
    "my skills",
    "my progress",
    "my course",
    "my assessment",
    "my learning",
    "my recommendation",
    "my recommendations",
    "skill gap",
    "skill gaps",
    "learning plan",
    "learning progress",
    "improve first",
)


@router.post("/ask", response_model=ProjectAgentResponse)
def ask_skillforge_project(
    request: ProjectAgentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectAgentResponse:
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    try:
        learner_context = None

        if any(
            keyword in question.casefold()
            for keyword in LEARNING_KEYWORDS
        ):
            learner_context = generate_learning_recommendations(
                db=db,
                user_id=current_user.id,
            )

        answer = ask_project_agent(
            question,
            learner_context=learner_context,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail="The SkillForge AI agent is temporarily unavailable.",
        ) from exc
   
    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc


    return ProjectAgentResponse(
        question=question,
        answer=answer,
    )
