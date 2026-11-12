from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.assessment import AssessmentCreate, AssessmentResponse
from app.schemas.assessment_question import (
    AssessmentQuestionCreate,
    AssessmentQuestionResponse,
)
from app.schemas.assessment_attempt import (
    AssessmentAttemptCreate,
    AssessmentAttemptResponse,
)
from app.schemas.assessment_answer import (
    AssessmentAnswerCreate,
    AssessmentAnswerResponse,
)
from app.services.assessment_service import (
    create_new_assessment,
    get_assessment,
    list_user_assessments,
)
from app.services.assessment_question_service import (
    create_new_question,
    get_assessment_question,
    list_assessment_questions,
)
from app.services.assessment_attempt_service import (
    create_new_attempt,
    get_attempt,
    list_user_attempts,
)
from app.services.assessment_answer_service import (
    submit_assessment_answer,
    list_attempt_answers,
)
from app.services.assessment_score_service import calculate_assessment_score

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.post("", response_model=AssessmentResponse, status_code=201)
def create_assessment_endpoint(
    payload: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_assessment(
        db=db,
        user_id=current_user.id,
        career_id=payload.career_id,
        title=payload.title,
        description=payload.description,
        max_score=payload.max_score,
    )


@router.get("", response_model=list[AssessmentResponse])
def get_assessments_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_assessments(db, current_user.id)


@router.post(
    "/{assessment_id}/questions",
    response_model=AssessmentQuestionResponse,
    status_code=201,
)
def create_assessment_question_endpoint(
    assessment_id: int,
    payload: AssessmentQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = get_assessment(db, assessment_id)

    if assessment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return create_new_question(
        db=db,
        assessment_id=assessment_id,
        question_text=payload.question_text,
        question_type=payload.question_type,
        option_a=payload.option_a,
        option_b=payload.option_b,
        option_c=payload.option_c,
        option_d=payload.option_d,
        correct_answer=payload.correct_answer,
        marks=payload.marks,
    )


@router.get(
    "/{assessment_id}/questions",
    response_model=list[AssessmentQuestionResponse],
)
def get_assessment_questions_endpoint(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = get_assessment(db, assessment_id)

    if assessment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return list_assessment_questions(db, assessment_id)


@router.get(
    "/questions/{question_id}",
    response_model=AssessmentQuestionResponse,
)
def get_assessment_question_endpoint(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question = get_assessment_question(db, question_id)
    assessment = get_assessment(db, question.assessment_id)

    if assessment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return question


@router.post(
    "/{assessment_id}/attempt",
    response_model=AssessmentAttemptResponse,
    status_code=201,
)
def create_assessment_attempt_endpoint(
    assessment_id: int,
    payload: AssessmentAttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.assessment_id != assessment_id:
        raise HTTPException(
            status_code=400,
            detail="Assessment ID does not match request path",
        )

    return create_new_attempt(
        db=db,
        user_id=current_user.id,
        assessment_id=assessment_id,
    )


@router.get(
    "/attempts",
    response_model=list[AssessmentAttemptResponse],
)
def get_my_attempts_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_attempts(db, current_user.id)


@router.get(
    "/attempts/{attempt_id}",
    response_model=AssessmentAttemptResponse,
)
def get_attempt_endpoint(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_attempt(db, attempt_id, current_user.id)


@router.post(
    "/attempts/{attempt_id}/answers",
    response_model=AssessmentAnswerResponse,
    status_code=201,
)
def submit_answer_endpoint(
    attempt_id: int,
    payload: AssessmentAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return submit_assessment_answer(
        db=db,
        attempt_id=attempt_id,
        user_id=current_user.id,
        question_id=payload.question_id,
        selected_answer=payload.selected_answer,
    )


@router.get(
    "/attempts/{attempt_id}/answers",
    response_model=list[AssessmentAnswerResponse],
)
def get_attempt_answers_endpoint(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_attempt_answers(
        db=db,
        attempt_id=attempt_id,
        user_id=current_user.id,
    )


@router.post(
    "/attempts/{attempt_id}/submit",
    response_model=AssessmentAttemptResponse,
)
def submit_assessment_endpoint(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return calculate_assessment_score(
        db=db,
        attempt_id=attempt_id,
        user_id=current_user.id,
    )


@router.get(
    "/attempts/{attempt_id}/result",
    response_model=AssessmentAttemptResponse,
)
def get_assessment_result_endpoint(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempt = get_attempt(
        db=db,
        attempt_id=attempt_id,
        user_id=current_user.id,
    )

    if attempt.status != "submitted":
        raise HTTPException(
            status_code=400,
            detail="Assessment has not been submitted yet",
        )

    return attempt


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment_endpoint(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = get_assessment(db, assessment_id)

    if assessment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return assessment