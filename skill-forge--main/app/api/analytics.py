from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.analytics import LearningDashboardResponse
from app.services.analytics_service import get_learning_dashboard

router = APIRouter(
    prefix="/analytics",
    tags=["Learning Analytics"],
)


@router.get("/my-dashboard", response_model=LearningDashboardResponse)
def read_my_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_learning_dashboard(db, current_user.id)