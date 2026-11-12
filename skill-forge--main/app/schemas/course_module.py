from pydantic import BaseModel, Field


class CourseModuleCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    order_index: int = Field(
        ge=1,
    )


class CourseModuleResponse(BaseModel):
    id: int
    course_id: int
    title: str
    description: str | None
    order_index: int