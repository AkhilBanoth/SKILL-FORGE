from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CertificationCreate(BaseModel):
    user_id: int = Field(gt=0)
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    expires_at: datetime | None = None


class CertificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    certificate_code: str
    issued_at: datetime
    expires_at: datetime | None
    is_revoked: bool

    model_config = ConfigDict(from_attributes=True)