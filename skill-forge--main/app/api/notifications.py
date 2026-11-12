from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
)
from app.services.notification_service import (
    create_user_notification,
    list_user_notifications,
    mark_user_notification_as_read,
    delete_user_notification,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def require_admin(current_user: User):
    if (current_user.role or "").strip().lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification_endpoint(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    return create_user_notification(db, notification_data)


@router.get("/my", response_model=list[NotificationResponse])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_notifications(db, current_user.id)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read_endpoint(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return mark_user_notification_as_read(
            db, notification_id, current_user.id
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification_endpoint(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_user_notification(db, notification_id, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
