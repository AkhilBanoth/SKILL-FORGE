from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: Literal["admin", "learner"] | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
