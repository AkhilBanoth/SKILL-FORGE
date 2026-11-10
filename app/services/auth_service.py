from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)
from app.security.jwt import create_access_token
from app.security.password import (
    hash_password,
    verify_password,
)


def register_user(
    db: Session,
    full_name: str,
    email: str,
    password: str,
):
    normalized_email = email.lower().strip()

    existing_user = get_user_by_email(
        db,
        normalized_email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    password_hash = hash_password(password)

    return create_user(
        db=db,
        full_name=full_name,
        email=normalized_email,
        hashed_password=password_hash,
    )


def login_user(
    db: Session,
    email: str,
    password: str,
    role: str | None = None,
):
    normalized_email = email.lower().strip()

    user = get_user_by_email(
        db,
        normalized_email,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    actual_role = (user.role or "").strip().lower()

    if role is not None and actual_role != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account does not have the selected login role",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
