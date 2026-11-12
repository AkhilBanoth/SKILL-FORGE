
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.resume_service import (
    detect_resume_skills,
    extract_resume_text,
)
from app.services.recommendation_service import (
    calculate_career_recommendations,
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume_text = await extract_resume_text(file)

    detected_skills = detect_resume_skills(
        db=db,
        resume_text=resume_text,
    )

    career_recommendations = calculate_career_recommendations(
        db=db,
        user_id=current_user.id,
    )

    return {
        "message": "Resume analyzed successfully.",
        "filename": file.filename,
        "extracted_text_length": len(resume_text),
        "detected_skills": detected_skills,
        "detected_skill_count": len(detected_skills),
        "career_recommendations": career_recommendations[
            "recommendations"
        ],
    }
