
from fastapi import FastAPI
from fastapi.testclient import TestClient
from types import SimpleNamespace

from app.api import ai as ai_api
from app.dependencies import get_current_user


def create_test_client():
    app = FastAPI()
    app.include_router(ai_api.router)

    test_user = SimpleNamespace(id=1)

    app.dependency_overrides[get_current_user] = lambda: test_user

    return TestClient(app)


def test_generate_questions_success(monkeypatch):
    client = create_test_client()

    mock_questions = [
        {
            "question": "What is Python?",
            "options": {
                "A": "A programming language",
                "B": "A database",
                "C": "An operating system",
                "D": "A browser",
            },
            "correct_answer": "A",
            "explanation": "Python is a programming language.",
        }
    ]

    monkeypatch.setattr(
        ai_api,
        "generate_questions",
        lambda **kwargs: mock_questions,
    )

    response = client.get(
        "/ai/generate-questions",
        params={
            "topic": "Python",
            "difficulty": "easy",
            "number_of_questions": 1,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["topic"] == "Python"
    assert data["difficulty"] == "easy"
    assert data["total_questions"] == 1
    assert data["questions"] == mock_questions


def test_generate_questions_rejects_invalid_difficulty():
    client = create_test_client()

    response = client.get(
        "/ai/generate-questions",
        params={
            "topic": "Python",
            "difficulty": "expert",
        },
    )

    assert response.status_code == 422


def test_generate_questions_rejects_invalid_question_count():
    client = create_test_client()

    response = client.get(
        "/ai/generate-questions",
        params={
            "topic": "Python",
            "number_of_questions": 25,
        },
    )

    assert response.status_code == 422


def test_analyze_skill_gaps_success(monkeypatch):
    client = create_test_client()

    mock_analysis = {
        "missing_skills": ["FastAPI"],
        "matched_skills": ["Python"],
        "recommendations": ["Learn FastAPI basics"],
    }

    monkeypatch.setattr(
        ai_api,
        "analyze_skill_gaps",
        lambda **kwargs: mock_analysis,
    )

    response = client.get(
        "/ai/analyze-skill-gaps",
        params=[
            ("current_skills", "Python"),
            ("required_skills", "Python"),
            ("required_skills", "FastAPI"),
            ("target_career", "Backend Developer"),
        ],
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["missing_skills"] == ["FastAPI"]
    assert data["matched_skills"] == ["Python"]
    assert data["recommendations"] == ["Learn FastAPI basics"]


def test_analyze_skill_gaps_requires_parameters():
    client = create_test_client()

    response = client.get("/ai/analyze-skill-gaps")

    assert response.status_code == 422
