from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.models.user import User
from app.schemas.quiz import QuizCreate, QuizResponse
from app.security.rbac import require_role
from app.services.quiz_service import (
    create_new_quiz,
    get_quiz,
    list_quizzes,
)

router = APIRouter(
    prefix="/lessons",
    tags=["Quizzes"],
)


@router.post(
    "/{lesson_id}/quizzes",
    response_model=QuizResponse,
    status_code=201,
)
def create_quiz_endpoint(
    lesson_id: int,
    payload: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return create_new_quiz(
        db=db,
        lesson_id=lesson_id,
        title=payload.title,
        description=payload.description,
        passing_score=payload.passing_score,
    )


@router.get(
    "/{lesson_id}/quizzes",
    response_model=list[QuizResponse],
)
def get_quizzes_endpoint(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    return list_quizzes(
        db=db,
        lesson_id=lesson_id,
    )


@router.get(
    "/quizzes/{quiz_id}",
    response_model=QuizResponse,
)
def get_quiz_endpoint(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    return get_quiz(
        db=db,
        quiz_id=quiz_id,
    )