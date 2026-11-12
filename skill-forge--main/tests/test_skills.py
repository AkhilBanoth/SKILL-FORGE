
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.api import skills as skills_api
from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User


def create_test_client():
    app = FastAPI()
    app.include_router(skills_api.router)

    test_admin = User(
        id=1,
        full_name="Test Admin",
        email="admin@example.com",
        hashed_password="test-password",
        role="admin",
        is_active=True,
        created_at=datetime(2026, 1, 1),
    )

    app.dependency_overrides[get_db] = lambda: None
    app.dependency_overrides[get_current_user] = lambda: test_admin

    return TestClient(app)


def test_list_skills(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        skills_api,
        "list_skills",
        lambda db: [
            {
                "id": 1,
                "name": "Python",
                "category": "Programming",
                "description": "Python fundamentals",
                "created_at": datetime(2026, 1, 1),
            }
        ],
    )

    response = client.get("/skills")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Python"


def test_get_skill(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        skills_api,
        "get_skill",
        lambda db, skill_id: {
            "id": skill_id,
            "name": "Python",
            "category": "Programming",
            "description": "Python fundamentals",
            "created_at": datetime(2026, 1, 1),
        },
    )

    response = client.get("/skills/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Python"


def test_get_missing_skill(monkeypatch):
    client = create_test_client()

    def fake_get_skill(db, skill_id):
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    monkeypatch.setattr(
        skills_api,
        "get_skill",
        fake_get_skill,
    )

    response = client.get("/skills/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found"


def test_create_skill(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        skills_api,
        "create_new_skill",
        lambda db, name, category, description: {
            "id": 2,
            "name": name,
            "category": category,
            "description": description,
            "created_at": datetime(2026, 1, 1),
        },
    )

    response = client.post(
        "/skills",
        json={
            "name": "Java",
            "category": "Programming",
            "description": "Java fundamentals",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Java"
    assert response.json()["category"] == "Programming"


def test_create_skill_rejects_short_name():
    client = create_test_client()

    response = client.post(
        "/skills",
        json={
            "name": "J",
            "category": "Programming",
            "description": "Test skill",
        },
    )

    assert response.status_code == 422
