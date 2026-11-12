from sqlalchemy.orm import Session

from app.models.certification import Certification
from app.schemas.certification import CertificationCreate


def create_certification(db: Session, certification_data: CertificationCreate):
    certification = Certification(**certification_data.model_dump())
    db.add(certification)
    db.commit()
    db.refresh(certification)
    return certification


def get_certification_by_id(db: Session, certification_id: int):
    return db.query(Certification).filter(
        Certification.id == certification_id
    ).first()


def get_certification_by_code(db: Session, certificate_code: str):
    return db.query(Certification).filter(
        Certification.certificate_code == certificate_code
    ).first()


def get_user_certifications(db: Session, user_id: int):
    return db.query(Certification).filter(
        Certification.user_id == user_id
    ).order_by(Certification.issued_at.desc()).all()


def get_all_certifications(db: Session):
    return db.query(Certification).order_by(
        Certification.issued_at.desc()
    ).all()


def revoke_certification(db: Session, certification: Certification):
    certification.is_revoked = True
    db.commit()
    db.refresh(certification)
    return certification