
from datetime import datetime
from types import SimpleNamespace

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.api import courses as courses_api
from app.database.postgres import get_db
from app.dependencies import get_current_user


def create_test_client():
    app = FastAPI()
    app.include_router(courses_api.router)
    app.dependency_overrides[get_db] = lambda: None
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=1, role="admin", is_active=True
    )
    return TestClient(app)


def sample_course(course_id=1, **overrides):
    course = {
        "id": course_id,
        "title": "Python Fundamentals",
        "description": "Learn Python basics",
        "skill_id": None,
        "level": "Beginner",
        "duration_hours": 10.0,
        "is_active": True,
        "created_at": datetime(2026, 1, 1),
    }
    course.update(overrides)
    return course


def test_list_courses(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        courses_api,
        "list_courses",
        lambda db: [sample_course()],
    )

    response = client.get("/courses")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Python Fundamentals"


def test_get_course(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        courses_api,
        "get_course",
        lambda db, course_id: sample_course(course_id),
    )

    response = client.get("/courses/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["level"] == "Beginner"


def test_get_missing_course(monkeypatch):
    client = create_test_client()

    def fake_get_course(db, course_id):
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    monkeypatch.setattr(
        courses_api,
        "get_course",
        fake_get_course,
    )

    response = client.get("/courses/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"


def test_create_course(monkeypatch):
    client = create_test_client()

    def fake_create_course(
        db, title, description, skill_id, level, duration_hours
    ):
        return sample_course(
            course_id=2,
            title=title,
            description=description,
            skill_id=skill_id,
            level=level,
            duration_hours=duration_hours,
        )

    monkeypatch.setattr(
        courses_api,
        "create_new_course",
        fake_create_course,
    )

    response = client.post(
        "/courses",
        json={
            "title": "Java Fundamentals",
            "description": "Learn Java basics",
            "skill_id": None,
            "level": "Beginner",
            "duration_hours": 12,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Java Fundamentals"
    assert response.json()["duration_hours"] == 12.0


def test_create_course_rejects_invalid_duration():
    client = create_test_client()

    response = client.post(
        "/courses",
        json={
            "title": "Python Fundamentals",
            "description": "Learn Python basics",
            "skill_id": None,
            "level": "Beginner",
            "duration_hours": 0,
        },
    )

    assert response.status_code == 422


def test_create_course_denied_for_learner():
    app = FastAPI()
    app.include_router(courses_api.router)
    app.dependency_overrides[get_db] = lambda: None
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=1, role="learner", is_active=True
    )
    client = TestClient(app)

    response = client.post(
        "/courses",
        json={
            "title": "Python Fundamentals",
            "description": "Learn Python basics",
            "skill_id": None,
            "level": "Beginner",
            "duration_hours": 10,
        },
    )

    assert response.status_code == 403
