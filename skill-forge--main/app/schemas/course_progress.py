from datetime import datetime

from pydantic import BaseModel, Field


class CourseProgressCreate(BaseModel):
    course_id: int = Field(gt=0)


class CourseProgressUpdate(BaseModel):
    completed_lessons: int = Field(ge=0)


class CourseProgressResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    progress_percentage: float = Field(ge=0, le=100)
    completed_lessons: int = Field(ge=0)
    total_lessons: int = Field(ge=0)
    is_completed: bool
    updated_at: datetime