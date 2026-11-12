
from fastapi import FastAPI
from fastapi.testclient import TestClient
from types import SimpleNamespace

from app.api import course_modules as course_modules_api
from app.database.postgres import get_db
from app.dependencies import get_current_user


def create_test_client():
    app = FastAPI()
    app.include_router(course_modules_api.router)

    app.dependency_overrides[get_db] = lambda: None
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=1, role="admin", is_active=True
    )

    return TestClient(app)


def sample_course_module(module_id=1, **overrides):
    module = {
        "id": module_id,
        "course_id": 1,
        "title": "Python Basics",
        "description": "Introduction to Python programming",
        "order_index": 1,
    }

    module.update(overrides)
    return module


def test_create_course_module(monkeypatch):
    client = create_test_client()

    def fake_create_new_course_module(
        db, course_id, title, description, order_index
    ):
        return sample_course_module(
            course_id=course_id,
            title=title,
            description=description,
            order_index=order_index,
        )

    monkeypatch.setattr(
        course_modules_api,
        "create_new_course_module",
        fake_create_new_course_module,
    )

    response = client.post(
        "/courses/1/modules",
        json={
            "title": "Python Basics",
            "description": "Introduction to Python programming",
            "order_index": 1,
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["course_id"] == 1
    assert response.json()["title"] == "Python Basics"
    assert response.json()["order_index"] == 1


def test_list_course_modules(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        course_modules_api,
        "list_course_modules",
        lambda db, course_id: [
            sample_course_module(course_id=course_id),
            sample_course_module(
                module_id=2,
                course_id=course_id,
                title="Python Functions",
                order_index=2,
            ),
        ],
    )

    response = client.get("/courses/1/modules")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Python Basics"
    assert response.json()[1]["title"] == "Python Functions"
    assert response.json()[1]["order_index"] == 2


def test_get_course_module(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        course_modules_api,
        "get_course_module",
        lambda db, module_id: sample_course_module(
            module_id=module_id
        ),
    )

    response = client.get("/courses/modules/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Python Basics"


def test_create_course_module_rejects_short_title():
    client = create_test_client()

    response = client.post(
        "/courses/1/modules",
        json={
            "title": "A",
            "description": "Introduction to Python",
            "order_index": 1,
        },
    )

    assert response.status_code == 422


def test_create_course_module_rejects_invalid_order_index():
    client = create_test_client()

    response = client.post(
        "/courses/1/modules",
        json={
            "title": "Python Basics",
            "description": "Introduction to Python",
            "order_index": 0,
        },
    )

    assert response.status_code == 422
