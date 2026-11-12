from datetime import datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import auth as auth_api
from app.database.postgres import get_db


def create_test_client():
    app = FastAPI()
    app.include_router(auth_api.router)
    app.dependency_overrides[get_db] = lambda: None
    return TestClient(app)


def test_register_success(monkeypatch):
    client = create_test_client()

    def fake_register_user(**kwargs):
        return {
            "id": 1,
            "full_name": kwargs["full_name"],
            "email": kwargs["email"],
            "role": "learner",
            "is_active": True,
            "created_at": datetime(2026, 1, 1),
        }

    monkeypatch.setattr(auth_api, "register_user", fake_register_user)

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "email": "testuser@example.com",
            "password": "TestPass123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["role"] == "learner"


def test_login_success(monkeypatch):
    client = create_test_client()

    def fake_login_user(**kwargs):
        return {
            "access_token": "test-token",
            "token_type": "bearer",
        }

    monkeypatch.setattr(auth_api, "login_user", fake_login_user)

    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "TestPass123",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "test-token"
    assert response.json()["token_type"] == "bearer"


def test_register_rejects_invalid_email():
    client = create_test_client()

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Test User",
            "email": "not-an-email",
            "password": "TestPass123",
        },
    )

    assert response.status_code == 422