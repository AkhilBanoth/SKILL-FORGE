from sqlalchemy.orm import Session

from app.repositories.notification_repository import (
    create_notification,
    delete_notification,
    get_notification_by_id,
    get_user_notifications,
    mark_notification_as_read,
)
from app.schemas.notification import NotificationCreate


def create_user_notification(
    db: Session,
    notification_data: NotificationCreate,
):
    return create_notification(db, notification_data)


def list_user_notifications(db: Session, user_id: int):
    return get_user_notifications(db, user_id)


def get_notification(db: Session, notification_id: int):
    notification = get_notification_by_id(db, notification_id)

    if notification is None:
        raise ValueError("Notification not found")

    return notification


def mark_user_notification_as_read(
    db: Session,
    notification_id: int,
    user_id: int,
):
    notification = get_notification(db, notification_id)

    if notification.user_id != user_id:
        raise PermissionError("Access denied")

    return mark_notification_as_read(db, notification)


def delete_user_notification(
    db: Session,
    notification_id: int,
    user_id: int,
):
    notification = get_notification(db, notification_id)

    if notification.user_id != user_id:
        raise PermissionError("Access denied")

    delete_notification(db, notification)