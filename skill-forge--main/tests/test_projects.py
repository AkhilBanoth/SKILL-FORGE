
from datetime import datetime
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import projects as projects_api
from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User


def create_test_client(role="learner"):
    app = FastAPI()
    app.include_router(projects_api.router)

    test_user = User(
        id=1,
        full_name="Test User",
        email="testuser@example.com",
        hashed_password="test-password",
        role=role,
        is_active=True,
        created_at=datetime(2026, 1, 1),
    )

    app.dependency_overrides[get_current_user] = lambda: test_user
    app.dependency_overrides[get_db] = lambda: None

    return TestClient(app)


def sample_project(project_id=1, **overrides):
    project = {
        "id": project_id,
        "user_id": 1,
        "title": "Python Learning Project",
        "description": "Build a Python application",
        "difficulty": "Beginner",
        "required_skills": "Python, SQL",
        "instructions": "Complete the project tasks",
        "is_active": True,
        "created_at": datetime(2026, 1, 1),
    }

    project.update(overrides)
    return project


def test_create_project(monkeypatch):
    client = create_test_client()

    def fake_create_new_project(db, project_data, user_id):
        return sample_project(
            user_id=user_id,
            title=project_data.title,
            description=project_data.description,
            difficulty=project_data.difficulty,
            required_skills=project_data.required_skills,
            instructions=project_data.instructions,
        )

    monkeypatch.setattr(
        projects_api,
        "create_new_project",
        fake_create_new_project,
    )

    response = client.post(
        "/projects",
        json={
            "title": "Python Learning Project",
            "description": "Build a Python application",
            "difficulty": "Beginner",
            "required_skills": "Python, SQL",
            "instructions": "Complete the project tasks",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["user_id"] == 1
    assert response.json()["title"] == "Python Learning Project"


def test_list_projects(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        projects_api,
        "get_all_projects",
        lambda db, skip, limit: [
            sample_project(project_id=1),
            sample_project(
                project_id=2,
                title="SQL Project",
            ),
        ],
    )

    response = client.get("/projects")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Python Learning Project"
    assert response.json()[1]["title"] == "SQL Project"


def test_list_my_projects(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        projects_api,
        "get_projects_by_user",
        lambda db, user_id: [
            sample_project(user_id=user_id)
        ],
    )

    response = client.get("/projects/my")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == 1


def test_get_project(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        projects_api,
        "get_project_details",
        lambda db, project_id: sample_project(project_id),
    )

    response = client.get("/projects/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Python Learning Project"


def test_update_project(monkeypatch):
    client = create_test_client()

    def fake_update_existing_project(
        db, project_id, project_data, user_id, is_admin
    ):
        return sample_project(
            project_id=project_id,
            user_id=user_id,
            title=project_data.title or "Python Learning Project",
        )

    monkeypatch.setattr(
        projects_api,
        "update_existing_project",
        fake_update_existing_project,
    )

    response = client.put(
        "/projects/1",
        json={"title": "Updated Python Project"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Updated Python Project"


def test_delete_project(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        projects_api,
        "delete_existing_project",
        lambda db, project_id, user_id, is_admin: sample_project(
            project_id=project_id,
            user_id=user_id,
            is_active=False,
        ),
    )

    response = client.delete("/projects/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["is_active"] is False


def test_create_project_rejects_short_title():
    client = create_test_client()

    response = client.post(
        "/projects",
        json={
            "title": "AI",
            "description": "Build a Python application",
        },
    )

    assert response.status_code == 422


def test_update_passes_admin_permission(monkeypatch):
    client = create_test_client(role="admin")
    captured = {}

    def fake_update_existing_project(
        db, project_id, project_data, user_id, is_admin
    ):
        captured["user_id"] = user_id
        captured["is_admin"] = is_admin

        return sample_project(
            project_id=project_id,
            user_id=user_id,
            title=project_data.title or "Python Learning Project",
        )

    monkeypatch.setattr(
        projects_api,
        "update_existing_project",
        fake_update_existing_project,
    )

    response = client.put(
        "/projects/1",
        json={"title": "Admin Updated Project"},
    )

    assert response.status_code == 200
    assert captured["user_id"] == 1
    assert captured["is_admin"] is True
