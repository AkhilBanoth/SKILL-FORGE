from sqlalchemy.orm import Session

from app.services.ai_learning_recommendation_service import (
    generate_learning_recommendations,
)
from app.ai.mentor import generate_learning_guidance


def generate_ai_learning_guidance(
    db: Session,
    user_id: int,
) -> dict:
    learning_data = generate_learning_recommendations(
        db=db,
        user_id=user_id,
    )

    guidance = generate_learning_guidance(learning_data)

    return {
        "user_id": user_id,
        "guidance": guidance,
        "recommendations": learning_data["recommendations"],
        "summary": learning_data["summary"],
    }