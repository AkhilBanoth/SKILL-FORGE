from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.lesson_repository import get_lesson_by_id
from app.repositories.resource_repository import (
    create_resource,
    get_resource_by_id,
    get_resources_by_lesson,
)


def create_new_resource(
    db: Session,
    lesson_id: int,
    title: str,
    resource_type: str,
    url: str,
):
    lesson = get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return create_resource(
        db=db,
        lesson_id=lesson_id,
        title=title,
        resource_type=resource_type,
        url=url,
    )


def list_resources(
    db: Session,
    lesson_id: int,
):
    lesson = get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return get_resources_by_lesson(
        db,
        lesson_id,
    )


def get_resource(
    db: Session,
    resource_id: int,
):
    resource = get_resource_by_id(
        db,
        resource_id,
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )

    return resource