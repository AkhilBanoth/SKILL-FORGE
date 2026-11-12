
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.mongodb import check_mongodb, close_mongodb
from app.database.postgres import Base, engine

# Import models so SQLAlchemy can register the database tables.
from app.models import project
from app.models import user
from app.models.course_module import CourseModule
from app.models.lesson import Lesson
from app.models.course_progress import CourseProgress
from app.models import project_submission
from app.models import certification
from app.models import notification

# Import API routers.
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.skills import router as skills_router
from app.api.careers import router as careers_router
from app.api.skill_gap import router as skill_gap_router
from app.api.recommendations import router as recommendations_router
from app.api.readiness import router as readiness_router
from app.api.courses import router as courses_router
from app.api.course_modules import router as course_modules_router
from app.api.lessons import router as lessons_router
from app.api.resources import router as resources_router
from app.api.quizzes import router as quizzes_router
from app.api.assignments import router as assignments_router
from app.api.course_progress import router as course_progress_router
from app.api.assessments import router as assessments_router
from app.api.assessment_skills import router as assessment_skills_router
from app.api.projects import router as projects_router
from app.api.project_submissions import router as project_submissions_router
from app.api.certifications import router as certifications_router
from app.api.notifications import router as notifications_router
from app.api.analytics import router as analytics_router
from app.api.ai_learning_recommendations import (
    router as ai_learning_recommendations_router,
)
from app.api.ai_mentor import router as ai_mentor_router
from app.api.admin import router as admin_router
from app.api.ai import router as ai_router
from app.api import project_agent
from app.api.roadmap import router as roadmap_router
from app.api.resume import router as resume_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating PostgreSQL tables...")
    Base.metadata.create_all(bind=engine)

    print("Checking MongoDB connection...")
    app.state.mongodb_connected = check_mongodb()
    print(f"MongoDB connected: {app.state.mongodb_connected}")

    print("SkillForge application started.")

    yield

    close_mongodb()
    print("MongoDB connection closed.")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI Learning, Certification & Career Readiness Platform",
    lifespan=lifespan,
)

# CORS configuration: Allow React frontend to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all existing API routers.
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(skills_router)
app.include_router(careers_router)
app.include_router(skill_gap_router)
app.include_router(recommendations_router)
app.include_router(readiness_router)
app.include_router(course_progress_router)
app.include_router(courses_router)
app.include_router(course_modules_router)
app.include_router(lessons_router)
app.include_router(resources_router)
app.include_router(quizzes_router)
app.include_router(assignments_router)
app.include_router(assessments_router)
app.include_router(assessment_skills_router)
app.include_router(projects_router)
app.include_router(project_submissions_router)
app.include_router(certifications_router)
app.include_router(notifications_router)
app.include_router(analytics_router)
app.include_router(ai_learning_recommendations_router)
app.include_router(ai_mentor_router)
app.include_router(admin_router)
app.include_router(ai_router)
app.include_router(project_agent.router)
app.include_router(roadmap_router)
app.include_router(resume_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to SkillForge",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "mongodb_connected": getattr(
            app.state,
            "mongodb_connected",
            False,
        ),
    }
