from pydantic import BaseModel, Field


class CourseAnalytics(BaseModel):
    total_courses: int = Field(ge=0)
    completed_courses: int = Field(ge=0)
    in_progress_courses: int = Field(ge=0)
    average_progress: float = Field(ge=0, le=100)


class AssessmentAnalytics(BaseModel):
    total_attempts: int = Field(ge=0)
    average_score: float = Field(ge=0, le=100)


class ProjectAnalytics(BaseModel):
    total_submissions: int = Field(ge=0)
    reviewed_submissions: int = Field(ge=0)


class LearningDashboardResponse(BaseModel):
    courses: CourseAnalytics
    assessments: AssessmentAnalytics
    projects: ProjectAnalytics