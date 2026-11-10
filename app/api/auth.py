from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.user import UserResponse
from app.services.auth_service import login_user, register_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    return register_user(
        db=db,
        full_name=payload.full_name,
        email=str(payload.email),
        password=payload.password,
    )


@router.post(
    "/login",
    response_model=dict,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=str(payload.email),
        password=payload.password,
        role=payload.role,
    )


