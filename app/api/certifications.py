from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.certification import CertificationCreate, CertificationResponse
from app.security.rbac import require_role
from app.services.certification_service import (
    issue_certification,
    list_user_certifications,
    list_all_certifications,
    get_certification,
    verify_certification,
    revoke_user_certification,
)

router = APIRouter(prefix="/certifications", tags=["Certifications"])


@router.post("/", response_model=CertificationResponse, status_code=status.HTTP_201_CREATED)
def create_certificate(
    certification_data: CertificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):

    try:
        return issue_certification(db, certification_data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/my", response_model=list[CertificationResponse])
def get_my_certifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_certifications(db, current_user.id)


@router.get("/verify/{certificate_code}", response_model=CertificationResponse)
def verify_certificate(
    certificate_code: str,
    db: Session = Depends(get_db),
):
    try:
        return verify_certification(db, certificate_code)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/", response_model=list[CertificationResponse])
def get_certifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    return list_all_certifications(db)


@router.get("/{certification_id}", response_model=CertificationResponse)
def get_certificate(
    certification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    certification = get_certification(db, certification_id)

    if (current_user.role or "").strip().lower() != "admin" and certification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return certification


@router.patch("/{certification_id}/revoke", response_model=CertificationResponse)
def revoke_certificate(
    certification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    try:
        return revoke_user_certification(db, certification_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
