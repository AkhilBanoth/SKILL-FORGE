
from datetime import datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import users as users_api
from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User


def create_test_client():
    app = FastAPI()
    app.include_router(users_api.router)

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


def test_get_my_profile():
    client = create_test_client()

    response = client.get("/users/me")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "testuser@example.com"


def test_add_my_skill(monkeypatch):
    client = create_test_client()

    def fake_add_skill_to_user(db, user_id, skill_id, level):
        return {
            "id": 1,
            "user_id": user_id,
            "skill_id": skill_id,
            "level": level,
        }

    monkeypatch.setattr(
        users_api,
        "add_skill_to_user",
        fake_add_skill_to_user,
    )

    response = client.post(
        "/users/me/skills",
        json={"skill_id": 1, "level": 75},
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == 1
    assert response.json()["skill_id"] == 1
    assert response.json()["level"] == 75.0


def test_get_my_skills(monkeypatch):
    client = create_test_client()

    def fake_list_user_skills(db, user_id):
        return [
            {
                "id": 1,
                "user_id": user_id,
                "skill_id": 1,
                "level": 75.0,
            }
        ]

    monkeypatch.setattr(
        users_api,
        "list_user_skills",
        fake_list_user_skills,
    )

    response = client.get("/users/me/skills")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["skill_id"] == 1
    assert response.json()[0]["level"] == 75.0
