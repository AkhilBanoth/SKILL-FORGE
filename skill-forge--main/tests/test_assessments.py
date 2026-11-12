
from datetime import datetime
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import assessments as assessments_api
from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User


def create_test_client():
    app = FastAPI()
    app.include_router(assessments_api.router)

    test_user = User(
        id=1,
        full_name="Test User",
        email="testuser@example.com",
        hashed_password="test-password",
        role="learner",
        is_active=True,
        created_at=datetime(2026, 1, 1),
    )

    app.dependency_overrides[get_current_user] = lambda: test_user
    app.dependency_overrides[get_db] = lambda: None

    return TestClient(app)


def sample_assessment(assessment_id=1, **overrides):
    assessment = {
        "id": assessment_id,
        "user_id": 1,
        "career_id": None,
        "title": "Python Assessment",
        "description": "Python fundamentals",
        "score": 0.0,
        "max_score": 100.0,
        "status": "pending",
        "created_at": datetime(2026, 1, 1),
    }

    assessment.update(overrides)
    return assessment


def test_create_assessment(monkeypatch):
    client = create_test_client()

    def fake_create_new_assessment(
        db, user_id, career_id, title, description, max_score
    ):
        return sample_assessment(
            assessment_id=1,
            user_id=user_id,
            career_id=career_id,
            title=title,
            description=description,
            max_score=max_score,
        )

    monkeypatch.setattr(
        assessments_api,
        "create_new_assessment",
        fake_create_new_assessment,
    )

    response = client.post(
        "/assessments",
        json={
            "title": "Python Assessment",
            "description": "Python fundamentals",
            "max_score": 100,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Python Assessment"
    assert response.json()["user_id"] == 1
    assert response.json()["max_score"] == 100.0


def test_list_assessments(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        assessments_api,
        "list_user_assessments",
        lambda db, user_id: [
            sample_assessment(user_id=user_id)
        ],
    )

    response = client.get("/assessments")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Python Assessment"


def test_get_assessment(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        assessments_api,
        "get_assessment",
        lambda db, assessment_id: SimpleNamespace(
            **sample_assessment(assessment_id)
        ),
    )

    response = client.get("/assessments/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["user_id"] == 1


def test_get_assessment_denies_other_users(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        assessments_api,
        "get_assessment",
        lambda db, assessment_id: SimpleNamespace(
            **sample_assessment(
                assessment_id,
                user_id=999,
            )
        ),
    )

    response = client.get("/assessments/1")

    assert response.status_code == 403
    assert response.json()["detail"] == "Access denied"


def test_create_assessment_rejects_invalid_max_score():
    client = create_test_client()

    response = client.post(
        "/assessments",
        json={
            "title": "Python Assessment",
            "max_score": 0,
        },
    )

    assert response.status_code == 422
