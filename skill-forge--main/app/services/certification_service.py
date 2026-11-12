from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.repositories.certification_repository import (
    create_certification,
    get_all_certifications,
    get_certification_by_code,
    get_certification_by_id,
    get_user_certifications,
    revoke_certification,
)
from app.schemas.certification import CertificationCreate


def issue_certification(
    db: Session,
    certification_data: CertificationCreate,
):
    if certification_data.expires_at is not None:
        expiry = certification_data.expires_at
        now = datetime.now(timezone.utc)

        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)

        if expiry <= now:
            raise ValueError("Expiry date must be in the future")

    return create_certification(db, certification_data)


def list_user_certifications(db: Session, user_id: int):
    return get_user_certifications(db, user_id)


def list_all_certifications(db: Session):
    return get_all_certifications(db)


def get_certification(db: Session, certification_id: int):
    certification = get_certification_by_id(db, certification_id)

    if certification is None:
        raise ValueError("Certification not found")

    return certification


def verify_certification(db: Session, certificate_code: str):
    certification = get_certification_by_code(db, certificate_code)

    if certification is None:
        raise ValueError("Certificate code is invalid")

    if certification.is_revoked:
        raise ValueError("This certificate has been revoked")

    if certification.expires_at is not None:
        expiry = certification.expires_at

        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)

        if expiry <= datetime.now(timezone.utc):
            raise ValueError("This certificate has expired")

    return certification


def revoke_user_certification(db: Session, certification_id: int):
    certification = get_certification(db, certification_id)

    if certification.is_revoked:
        raise ValueError("Certification is already revoked")

    return revoke_certification(db, certification)