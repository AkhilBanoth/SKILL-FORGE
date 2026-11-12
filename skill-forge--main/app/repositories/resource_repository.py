from sqlalchemy.orm import Session

from app.models.resource import Resource


def get_resources_by_lesson(
    db: Session,
    lesson_id: int,
) -> list[Resource]:
    return (
        db.query(Resource)
        .filter(Resource.lesson_id == lesson_id)
        .order_by(Resource.id.asc())
        .all()
    )


def get_resource_by_id(
    db: Session,
    resource_id: int,
) -> Resource | None:
    return (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )


def create_resource(
    db: Session,
    lesson_id: int,
    title: str,
    resource_type: str,
    url: str,
) -> Resource:
    resource = Resource(
        lesson_id=lesson_id,
        title=title.strip(),
        resource_type=resource_type.strip(),
        url=url.strip(),
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource