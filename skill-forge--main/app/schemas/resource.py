from datetime import datetime

from pydantic import BaseModel, Field


class ResourceCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    resource_type: str = Field(min_length=2, max_length=50)
    url: str = Field(min_length=1, max_length=500)


class ResourceResponse(BaseModel):
    id: int
    lesson_id: int
    title: str
    resource_type: str
    url: str
    created_at: datetime