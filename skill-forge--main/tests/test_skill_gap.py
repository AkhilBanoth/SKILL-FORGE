
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import skill_gap as skill_gap_api
from app.database.postgres import get_db
from app.dependencies import get_current_user


def create_test_client():
    app = FastAPI()
    app.include_router(skill_gap_api.router)

    test_user = SimpleNamespace(id=1)

    app.dependency_overrides[get_current_user] = lambda: test_user
    app.dependency_overrides[get_db] = lambda: object()

    return TestClient(app)


def test_get_skill_gap_success(monkeypatch):
    client = create_test_client()

    mock_result = {
        "career_id": 10,
        "user_id": 1,
        "skills": [
            {
                "skill_id": 1,
                "required_weight": 5.0,
                "current_level": 3.0,
                "gap": 2.0,
            },
            {
                "skill_id": 2,
                "required_weight": 4.0,
                "current_level": 2.0,
                "gap": 2.0,
            },
        ],
        "overall_gap": 40.0,
    }

    monkeypatch.setattr(
        skill_gap_api,
        "calculate_skill_gap",
        lambda **kwargs: mock_result,
    )

    response = client.get("/skill-gap/10")

    assert response.status_code == 200
    assert response.json() == mock_result


def test_get_skill_gap_returns_404_for_missing_career(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        skill_gap_api,
        "calculate_skill_gap",
        lambda **kwargs: None,
    )

    response = client.get("/skill-gap/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Career not found"


def test_get_skill_gap_passes_correct_parameters(monkeypatch):
    client = create_test_client()
    captured = {}

    def mock_calculate_skill_gap(**kwargs):
        captured.update(kwargs)
        return None

    monkeypatch.setattr(
        skill_gap_api,
        "calculate_skill_gap",
        mock_calculate_skill_gap,
    )

    response = client.get("/skill-gap/15")

    assert response.status_code == 404
    assert captured["user_id"] == 1
    assert captured["career_id"] == 15
    assert "db" in captured


def test_get_skill_gap_rejects_invalid_career_id():
    client = create_test_client()

    response = client.get("/skill-gap/not-a-number")

    assert response.status_code == 422


def test_get_skill_gap_accepts_integer_career_id(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        skill_gap_api,
        "calculate_skill_gap",
        lambda **kwargs: None,
    )

    response = client.get("/skill-gap/20")

    assert response.status_code == 404
