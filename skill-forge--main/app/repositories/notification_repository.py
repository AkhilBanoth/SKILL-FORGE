from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate


def create_notification(db: Session, notification_data: NotificationCreate):
    notification = Notification(**notification_data.model_dump())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_notification_by_id(db: Session, notification_id: int):
    return db.query(Notification).filter(
        Notification.id == notification_id
    ).first()


def get_user_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(Notification.created_at.desc()).all()


def mark_notification_as_read(db: Session, notification: Notification):
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


def delete_notification(db: Session, notification: Notification):
    db.delete(notification)
    db.commit()