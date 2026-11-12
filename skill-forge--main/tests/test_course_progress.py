from datetime import datetime
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import course_progress as course_progress_api
from app.database.postgres import get_db
from app.dependencies import get_current_user


def create_test_client():
    app = FastAPI()
    app.include_router(course_progress_api.router)

    app.dependency_overrides[get_db] = lambda: object()
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=1)

    return TestClient(app)


def sample_progress():
    return {
        "id": 1,
        "user_id": 1,
        "course_id": 10,
        "progress_percentage": 50.0,
        "completed_lessons": 5,
        "total_lessons": 10,
        "is_completed": False,
        "updated_at": datetime(2026, 10, 10, 10, 0, 0),
    }


def test_get_my_progress(monkeypatch):
    monkeypatch.setattr(
        course_progress_api,
        "list_user_course_progress",
        lambda db, user_id: [sample_progress()],
    )

    client = create_test_client()
    response = client.get("/courses/progress")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == 1
    assert response.json()[0]["course_id"] == 10


def test_calculate_course_progress(monkeypatch):
    monkeypatch.setattr(
        course_progress_api,
        "calculate_course_progress",
        lambda db, user_id, course_id: {
            **sample_progress(),
            "course_id": course_id,
            "user_id": user_id,
        },
    )

    client = create_test_client()
    response = client.post(
        "/courses/10/progress",
        json={"course_id": 10},
    )

    assert response.status_code == 200
    assert response.json()["course_id"] == 10
    assert response.json()["progress_percentage"] == 50.0


def test_update_course_progress(monkeypatch):
    def mock_update(db, user_id, course_id, completed_lessons):
        return {
            **sample_progress(),
            "user_id": user_id,
            "course_id": course_id,
            "completed_lessons": completed_lessons,
            "progress_percentage": completed_lessons * 10.0,
        }

    monkeypatch.setattr(
        course_progress_api,
        "update_completed_lessons",
        mock_update,
    )

    client = create_test_client()
    response = client.put(
        "/courses/10/progress",
        json={"completed_lessons": 7},
    )

    assert response.status_code == 200
    assert response.json()["completed_lessons"] == 7
    assert response.json()["progress_percentage"] == 70.0


def test_calculate_progress_rejects_invalid_course_id():
    client = create_test_client()

    response = client.post(
        "/courses/0/progress",
        json={"course_id": 10},
    )

    assert response.status_code == 422


def test_update_progress_rejects_negative_completed_lessons():
    client = create_test_client()

    response = client.put(
        "/courses/10/progress",
        json={"completed_lessons": -1},
    )

    assert response.status_code == 422
