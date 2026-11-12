
from datetime import datetime
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import assignments as assignments_api
from app.database.postgres import get_db
from app.dependencies import get_current_user


def create_test_client(role="admin"):
    app = FastAPI()
    app.include_router(assignments_api.router)

    app.dependency_overrides[get_db] = lambda: None
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=1, role=role, is_active=True
    )

    return TestClient(app)


def sample_assignment(assignment_id=1, **overrides):
    assignment = {
        "id": assignment_id,
        "lesson_id": 1,
        "title": "Python Practice",
        "description": "Practice Python fundamentals",
        "max_score": 100.0,
        "created_at": datetime(2026, 1, 1),
    }

    assignment.update(overrides)
    return assignment


def test_create_assignment(monkeypatch):
    client = create_test_client()

    def fake_create_new_assignment(
        db, lesson_id, title, description, max_score
    ):
        return sample_assignment(
            lesson_id=lesson_id,
            title=title,
            description=description,
            max_score=max_score,
        )

    monkeypatch.setattr(
        assignments_api,
        "create_new_assignment",
        fake_create_new_assignment,
    )

    response = client.post(
        "/lessons/1/assignments",
        json={
            "title": "Python Practice",
            "description": "Practice Python fundamentals",
            "max_score": 100,
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["lesson_id"] == 1
    assert response.json()["title"] == "Python Practice"
    assert response.json()["max_score"] == 100.0


def test_list_assignments(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        assignments_api,
        "list_assignments",
        lambda db, lesson_id: [
            sample_assignment(lesson_id=lesson_id),
            sample_assignment(
                assignment_id=2,
                lesson_id=lesson_id,
                title="Loops Practice",
            ),
        ],
    )

    response = client.get("/lessons/1/assignments")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["lesson_id"] == 1
    assert response.json()[1]["title"] == "Loops Practice"


def test_get_assignment(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        assignments_api,
        "get_assignment",
        lambda db, assignment_id: sample_assignment(
            assignment_id=assignment_id
        ),
    )

    response = client.get("/lessons/assignments/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Python Practice"


def test_create_assignment_rejects_short_title():
    client = create_test_client()

    response = client.post(
        "/lessons/1/assignments",
        json={
            "title": "A",
            "description": "Practice Python fundamentals",
            "max_score": 100,
        },
    )

    assert response.status_code == 422


def test_create_assignment_rejects_invalid_max_score():
    client = create_test_client()

    response = client.post(
        "/lessons/1/assignments",
        json={
            "title": "Python Practice",
            "description": "Practice Python fundamentals",
            "max_score": 0,
        },
    )

    assert response.status_code == 422


def test_create_assignment_denied_for_learner():
    client = create_test_client(role="learner")

    response = client.post(
        "/lessons/1/assignments",
        json={
            "title": "Python Practice",
            "description": "Practice Python fundamentals",
            "max_score": 100,
        },
    )

    assert response.status_code == 403
