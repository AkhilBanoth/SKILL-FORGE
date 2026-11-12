
from datetime import datetime
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import certifications as certifications_api
from app.database.postgres import get_db
from app.dependencies import get_current_user
from app.models.user import User


def create_test_client(role="learner", user_id=1):
    app = FastAPI()
    app.include_router(certifications_api.router)

    test_user = User(
        id=user_id,
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


def sample_certification(certification_id=1, **overrides):
    certification = {
        "id": certification_id,
        "user_id": 1,
        "title": "Python Certification",
        "description": "Python fundamentals certification",
        "certificate_code": "CERT-TEST-001",
        "issued_at": datetime(2026, 1, 1),
        "expires_at": None,
        "is_revoked": False,
    }

    certification.update(overrides)
    return certification


def test_create_certification_as_admin(monkeypatch):
    client = create_test_client(role="admin")

    def fake_issue_certification(db, certification_data):
        return sample_certification(
            user_id=certification_data.user_id,
            title=certification_data.title,
            description=certification_data.description,
            expires_at=certification_data.expires_at,
        )

    monkeypatch.setattr(
        certifications_api,
        "issue_certification",
        fake_issue_certification,
    )

    response = client.post(
        "/certifications/",
        json={
            "user_id": 1,
            "title": "Python Certification",
            "description": "Python fundamentals certification",
        },
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == 1
    assert response.json()["title"] == "Python Certification"
    assert response.json()["certificate_code"] == "CERT-TEST-001"


def test_create_certification_denied_for_learner():
    client = create_test_client(role="learner")

    response = client.post(
        "/certifications/",
        json={
            "user_id": 1,
            "title": "Python Certification",
            "description": "Python fundamentals certification",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_get_my_certifications(monkeypatch):
    client = create_test_client(user_id=1)

    monkeypatch.setattr(
        certifications_api,
        "list_user_certifications",
        lambda db, user_id: [
            sample_certification(user_id=user_id)
        ],
    )

    response = client.get("/certifications/my")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == 1
    assert response.json()[0]["title"] == "Python Certification"


def test_verify_certification(monkeypatch):
    client = create_test_client()

    monkeypatch.setattr(
        certifications_api,
        "verify_certification",
        lambda db, certificate_code: sample_certification()
        if certificate_code == "CERT-TEST-001"
        else (_ for _ in ()).throw(
            ValueError("Certificate not found")
        ),
    )

    response = client.get(
        "/certifications/verify/CERT-TEST-001"
    )

    assert response.status_code == 200
    assert response.json()["certificate_code"] == "CERT-TEST-001"


def test_verify_invalid_certification_returns_404(monkeypatch):
    client = create_test_client()

    def fake_verify_certification(db, certificate_code):
        raise ValueError("Certificate not found")

    monkeypatch.setattr(
        certifications_api,
        "verify_certification",
        fake_verify_certification,
    )

    response = client.get(
        "/certifications/verify/INVALID-CODE"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Certificate not found"


def test_list_all_certifications_as_admin(monkeypatch):
    client = create_test_client(role="admin")

    monkeypatch.setattr(
        certifications_api,
        "list_all_certifications",
        lambda db: [sample_certification()],
    )

    response = client.get("/certifications/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["certificate_code"] == "CERT-TEST-001"


def test_list_all_certifications_denied_for_learner():
    client = create_test_client(role="learner")

    response = client.get("/certifications/")

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_get_own_certification(monkeypatch):
    client = create_test_client(role="learner", user_id=1)

    monkeypatch.setattr(
        certifications_api,
        "get_certification",
        lambda db, certification_id: SimpleNamespace(
            **sample_certification(certification_id, user_id=1)
        ),
    )

    response = client.get("/certifications/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["user_id"] == 1


def test_get_other_users_certification_denied(monkeypatch):
    client = create_test_client(role="learner", user_id=1)

    monkeypatch.setattr(
        certifications_api,
        "get_certification",
        lambda db, certification_id: SimpleNamespace(
            **sample_certification(certification_id, user_id=999)
        ),
    )

    response = client.get("/certifications/1")

    assert response.status_code == 403
    assert response.json()["detail"] == "Access denied"


def test_revoke_certification_as_admin(monkeypatch):
    client = create_test_client(role="admin")

    monkeypatch.setattr(
        certifications_api,
        "revoke_user_certification",
        lambda db, certification_id: sample_certification(
            certification_id,
            is_revoked=True,
        ),
    )

    response = client.patch("/certifications/1/revoke")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["is_revoked"] is True


def test_revoke_certification_denied_for_learner():
    client = create_test_client(role="learner")

    response = client.patch("/certifications/1/revoke")

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_create_certification_rejects_invalid_user_id():
    client = create_test_client(role="admin")

    response = client.post(
        "/certifications/",
        json={
            "user_id": 0,
            "title": "Python Certification",
            "description": "Python fundamentals certification",
        },
    )

    assert response.status_code == 422
