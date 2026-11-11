
from datetime import datetime, timezone
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import admin as admin_api
from app.api import ai_learning_recommendations as learning_recs_api
from app.api import ai_mentor as mentor_api
from app.api import analytics as analytics_api
from app.api import assessment_skills as assessment_skills_api
from app.api import careers as careers_api
from app.api import courses as courses_api
from app.api import lessons as lessons_api
from app.api import notifications as notifications_api
from app.api import project_submissions as submissions_api
from app.api import quizzes as quizzes_api
from app.api import recommendations as recommendations_api
from app.api import resources as resources_api

from app.database.postgres import get_db
from app.dependencies import get_current_user, get_admin_user


NOW = datetime.now(timezone.utc)


# ---------------- SHARED TEST SETUP ----------------

def create_client(router, user=None, admin=None, role="learner"):
    app = FastAPI()
    app.include_router(router)

    test_user = user or SimpleNamespace(
        id=1,
        role=role,
        is_active=True,
    )

    test_admin = admin or SimpleNamespace(
        id=99,
        role="admin",
        is_active=True,
    )

    app.dependency_overrides[get_db] = lambda: object()
    app.dependency_overrides[get_current_user] = lambda: test_user
    app.dependency_overrides[get_admin_user] = lambda: test_admin

    return TestClient(app)


# ---------------- ADMIN ----------------

class FakeQuery:
    def __init__(self, records=None, count=0):
        self.records = records or []
        self.count_value = count

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def all(self):
        return self.records

    def count(self):
        return self.count_value

    def first(self):
        return self.records[0] if self.records else None


class FakeDB:
    def __init__(self, mapping=None):
        self.mapping = mapping or {}

    def query(self, model):
        return self.mapping.get(model, FakeQuery())

    def commit(self):
        pass

    def refresh(self, obj):
        pass


def test_admin_dashboard_stats():
    from app.models.user import User
    from app.models.course import Course
    from app.models.assessment import Assessment
    from app.models.project import Project

    db = FakeDB({
        User: FakeQuery(count=3),
        Course: FakeQuery(count=4),
        Assessment: FakeQuery(count=5),
        Project: FakeQuery(count=6),
    })

    db.query(User).records = [
        SimpleNamespace(is_active=True),
        SimpleNamespace(is_active=False),
        SimpleNamespace(is_active=True),
    ]

    client = create_client(admin_api.router)
    client.app.dependency_overrides[get_db] = lambda: db

    response = client.get("/admin/dashboard/stats")

    assert response.status_code == 200
    assert response.json() == {
        "total_users": 3,
        "active_users": 3,
        "total_courses": 4,
        "total_assessments": 5,
        "total_projects": 6,
    }


def test_admin_user_details_not_found():
    client = create_client(admin_api.router)
    client.app.dependency_overrides[get_db] = lambda: FakeDB()

    response = client.get("/admin/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_course_creation_requires_admin():
    app = FastAPI()
    app.include_router(courses_api.router)
    app.dependency_overrides[get_db] = lambda: FakeDB()

    client = TestClient(app)
    response = client.post(
        "/courses",
        json={
            "title": "Advanced Python",
            "description": "Python fundamentals",
            "skill_id": 1,
            "level": "Intermediate",
            "duration_hours": 5,
        },
    )

    assert response.status_code == 401


# ---------------- AI LEARNING RECOMMENDATIONS ----------------

def test_ai_learning_recommendations_success(monkeypatch):
    client = create_client(learning_recs_api.router)
    expected = {"recommendations": ["Python", "SQL"]}

    def fake_service(db, user_id):
        assert user_id == 1
        return expected

    monkeypatch.setattr(
        learning_recs_api,
        "generate_learning_recommendations",
        fake_service,
    )

    response = client.get("/ai-learning-recommendations/me")

    assert response.status_code == 200
    assert response.json() == expected


# ---------------- AI MENTOR ----------------

def test_ai_mentor_learning_guidance_success(monkeypatch):
    client = create_client(mentor_api.router)
    expected = {"guidance": "Practice Python daily."}

    def fake_service(db, user_id):
        assert user_id == 1
        return expected

    monkeypatch.setattr(
        mentor_api,
        "generate_ai_learning_guidance",
        fake_service,
    )

    response = client.get("/ai-mentor/learning-guidance")

    assert response.status_code == 200
    assert response.json() == expected


# ---------------- ANALYTICS ----------------

def test_analytics_dashboard_success(monkeypatch):
    client = create_client(analytics_api.router)

    expected = {
        "courses": {
            "total_courses": 3,
            "completed_courses": 1,
            "in_progress_courses": 2,
            "average_progress": 60.0,
        },
        "assessments": {
            "total_attempts": 4,
            "average_score": 75.0,
        },
        "projects": {
            "total_submissions": 2,
            "reviewed_submissions": 1,
        },
    }

    monkeypatch.setattr(
        analytics_api,
        "get_learning_dashboard",
        lambda db, user_id: expected,
    )

    response = client.get("/analytics/my-dashboard")

    assert response.status_code == 200
    assert response.json() == expected


# ---------------- ASSESSMENT SKILLS ----------------

def test_assessment_skill_evaluation_success(monkeypatch):
    client = create_client(assessment_skills_api.router)
    expected = {"attempt_id": 10, "skills": []}

    def fake_service(db, attempt_id, user_id):
        assert attempt_id == 10
        assert user_id == 1
        return expected

    monkeypatch.setattr(
        assessment_skills_api,
        "evaluate_assessment_skill",
        fake_service,
    )

    response = client.get("/assessment-skills/10/evaluate")

    assert response.status_code == 200
    assert response.json() == expected


# ---------------- CAREERS ----------------

def test_create_career_success(monkeypatch):
    client = create_client(careers_api.router, role="admin")

    expected = {
        "id": 1,
        "title": "Backend Developer",
        "description": "Build APIs",
        "created_at": NOW.isoformat(),
    }

    monkeypatch.setattr(
        careers_api,
        "create_new_career",
        lambda **kwargs: expected,
    )

    response = client.post(
        "/careers",
        json={
            "title": "Backend Developer",
            "description": "Build APIs",
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Backend Developer"


def test_create_career_rejects_short_title():
    client = create_client(careers_api.router, role="admin")

    response = client.post(
        "/careers",
        json={"title": "A"},
    )

    assert response.status_code == 422


def test_list_careers_success(monkeypatch):
    client = create_client(careers_api.router)

    expected = [{
        "id": 1,
        "title": "Backend Developer",
        "description": None,
        "created_at": NOW.isoformat(),
    }]

    monkeypatch.setattr(
        careers_api,
        "list_careers",
        lambda db: expected,
    )

    response = client.get("/careers")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "Backend Developer"


# ---------------- LESSONS ----------------

def test_create_lesson_success(monkeypatch):
    client = create_client(lessons_api.router, role="admin")

    expected = {
        "id": 1,
        "module_id": 2,
        "title": "Python Basics",
        "content": "Variables and data types",
        "order_index": 1,
        "duration_minutes": 20,
        "created_at": NOW.isoformat(),
    }

    monkeypatch.setattr(
        lessons_api,
        "create_new_lesson",
        lambda **kwargs: expected,
    )

    response = client.post(
        "/modules/2/lessons",
        json={
            "title": "Python Basics",
            "content": "Variables and data types",
            "order_index": 1,
            "duration_minutes": 20,
        },
    )

    assert response.status_code == 201
    assert response.json()["module_id"] == 2


def test_create_lesson_rejects_invalid_duration():
    client = create_client(lessons_api.router, role="admin")

    response = client.post(
        "/modules/2/lessons",
        json={
            "title": "Python Basics",
            "order_index": 1,
            "duration_minutes": 0,
        },
    )

    assert response.status_code == 422


# ---------------- NOTIFICATIONS ----------------

def test_get_my_notifications_success(monkeypatch):
    client = create_client(notifications_api.router)

    expected = [{
        "id": 1,
        "user_id": 1,
        "title": "Welcome",
        "message": "Welcome to SkillForge",
        "is_read": False,
        "created_at": NOW.isoformat(),
    }]

    monkeypatch.setattr(
        notifications_api,
        "list_user_notifications",
        lambda db, user_id: expected,
    )

    response = client.get("/notifications/my")

    assert response.status_code == 200

    actual = response.json()

    assert len(actual) == 1
    assert actual[0]["id"] == 1
    assert actual[0]["user_id"] == 1
    assert actual[0]["title"] == "Welcome"
    assert actual[0]["message"] == "Welcome to SkillForge"
    assert actual[0]["is_read"] is False

    actual_created_at = datetime.fromisoformat(
        actual[0]["created_at"].replace("Z", "+00:00")
    )

    assert actual_created_at == NOW


def test_create_notification_denied_for_learner():
    learner = SimpleNamespace(
        id=1,
        role="learner",
        is_active=True,
    )

    client = create_client(
        notifications_api.router,
        user=learner,
    )

    response = client.post(
        "/notifications/",
        json={
            "user_id": 2,
            "title": "Notice",
            "message": "A new update",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_mark_notification_not_found(monkeypatch):
    client = create_client(notifications_api.router)

    def fake_mark(db, notification_id, user_id):
        raise ValueError("Notification not found")

    monkeypatch.setattr(
        notifications_api,
        "mark_user_notification_as_read",
        fake_mark,
    )

    response = client.patch("/notifications/999/read")

    assert response.status_code == 404
    assert response.json()["detail"] == "Notification not found"


# ---------------- PROJECT SUBMISSIONS ----------------

def test_create_project_submission_success(monkeypatch):
    client = create_client(submissions_api.router)

    expected = {
        "id": 1,
        "project_id": 2,
        "user_id": 1,
        "repository_url": "https://github.com/example/project",
        "demo_url": None,
        "description": "My submission",
        "status": "submitted",
        "score": None,
        "feedback": None,
        "submitted_at": NOW.isoformat(),
        "reviewed_at": None,
    }

    monkeypatch.setattr(
        submissions_api,
        "create_new_submission",
        lambda **kwargs: expected,
    )

    response = client.post(
        "/project-submissions",
        json={
            "project_id": 2,
            "repository_url": "https://github.com/example/project",
            "description": "My submission",
        },
    )

    assert response.status_code == 201
    assert response.json()["project_id"] == 2


def test_list_my_project_submissions(monkeypatch):
    client = create_client(submissions_api.router)

    monkeypatch.setattr(
        submissions_api,
        "get_my_submissions",
        lambda **kwargs: [],
    )

    response = client.get("/project-submissions/my")

    assert response.status_code == 200
    assert response.json() == []


def test_project_submission_invalid_id():
    client = create_client(submissions_api.router)

    response = client.get("/project-submissions/not-a-number")

    assert response.status_code == 422


# ---------------- QUIZZES ----------------

def test_create_quiz_success(monkeypatch):
    client = create_client(quizzes_api.router, role="admin")

    expected = {
        "id": 1,
        "lesson_id": 3,
        "title": "Python Quiz",
        "description": None,
        "passing_score": 60.0,
        "is_active": True,
        "created_at": NOW.isoformat(),
    }

    monkeypatch.setattr(
        quizzes_api,
        "create_new_quiz",
        lambda **kwargs: expected,
    )

    response = client.post(
        "/lessons/3/quizzes",
        json={
            "title": "Python Quiz",
            "passing_score": 60,
        },
    )

    assert response.status_code == 201
    assert response.json()["lesson_id"] == 3


def test_create_quiz_rejects_invalid_score():
    client = create_client(quizzes_api.router, role="admin")

    response = client.post(
        "/lessons/3/quizzes",
        json={
            "title": "Python Quiz",
            "passing_score": 120,
        },
    )

    assert response.status_code == 422


# ---------------- CAREER RECOMMENDATIONS ----------------

def test_career_recommendations_success(monkeypatch):
    client = create_client(recommendations_api.router)

    expected = {
        "user_id": 1,
        "recommendations": [{
            "career_id": 10,
            "career_title": "Backend Developer",
            "match_score": 85.0,
        }],
    }

    monkeypatch.setattr(
        recommendations_api,
        "calculate_career_recommendations",
        lambda **kwargs: expected,
    )

    response = client.get("/recommendations/careers")

    assert response.status_code == 200
    assert response.json() == expected


# ---------------- RESOURCES ----------------

def test_create_resource_success(monkeypatch):
    client = create_client(resources_api.router, role="admin")

    expected = {
        "id": 1,
        "lesson_id": 3,
        "title": "Python Documentation",
        "resource_type": "documentation",
        "url": "https://docs.python.org/",
        "created_at": NOW.isoformat(),
    }

    monkeypatch.setattr(
        resources_api,
        "create_new_resource",
        lambda **kwargs: expected,
    )

    response = client.post(
        "/lessons/3/resources",
        json={
            "title": "Python Documentation",
            "resource_type": "documentation",
            "url": "https://docs.python.org/",
        },
    )

    assert response.status_code == 201
    assert response.json()["lesson_id"] == 3


def test_create_resource_rejects_short_title():
    client = create_client(resources_api.router, role="admin")

    response = client.post(
        "/lessons/3/resources",
        json={
            "title": "A",
            "resource_type": "documentation",
            "url": "https://docs.python.org/",
        },
    )

    assert response.status_code == 422


def test_create_career_denied_for_learner():
    client = create_client(careers_api.router)

    response = client.post(
        "/careers",
        json={"title": "Backend Developer"},
    )

    assert response.status_code == 403


def test_project_submission_review_denied_for_learner():
    client = create_client(submissions_api.router)

    response = client.put(
        "/project-submissions/1/review",
        json={"status": "approved", "score": 90},
    )

    assert response.status_code == 403


def test_mentor_can_reach_project_submission_review(monkeypatch):
    from fastapi import HTTPException

    client = create_client(submissions_api.router, role="mentor")

    def missing_submission(**kwargs):
        raise HTTPException(status_code=404, detail="Submission not found")

    monkeypatch.setattr(
        submissions_api,
        "review_project_submission",
        missing_submission,
    )

    response = client.put(
        "/project-submissions/1/review",
        json={"status": "approved", "score": 90},
    )

    assert response.status_code == 404