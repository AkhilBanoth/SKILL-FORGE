from sqlalchemy.orm import Session

from app.repositories.analytics_repository import (
    get_assessment_analytics,
    get_course_analytics,
    get_project_analytics,
)


def get_learning_dashboard(db: Session, user_id: int) -> dict:
    return {
        "courses": get_course_analytics(db, user_id),
        "assessments": get_assessment_analytics(db, user_id),
        "projects": get_project_analytics(db, user_id),
    }