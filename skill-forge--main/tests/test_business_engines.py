
from app.business.skill_gap_engine import analyze_skill_gap
from app.business.career_matching_engine import match_careers
from app.business.readiness_engine import calculate_readiness
from app.business.roadmap_engine import generate_learning_roadmap
from app.business.certification_rules import check_certification_eligibility


def test_analyze_skill_gap():
    result = analyze_skill_gap(
        ["Python", "SQL", "FastAPI"],
        ["python", "SQL"],
    )

    assert result["matched_count"] == 2
    assert result["missing_count"] == 1
    assert result["gap_percentage"] == 33.33


def test_match_careers():
    result = match_careers(
        ["Python", "SQL"],
        [
            {
                "id": 1,
                "title": "Data Analyst",
                "required_skills": ["Python", "SQL", "Excel"],
            },
            {
                "id": 2,
                "title": "Backend Developer",
                "required_skills": ["Python", "FastAPI"],
            },
        ],
    )

    assert result[0]["career_id"] == 1
    assert result[0]["match_percentage"] == 66.67
    assert result[0]["missing_skills"] == ["excel"]


def test_calculate_readiness():
    result = calculate_readiness(
        ["Python", "SQL"],
        ["Python"],
        completed_projects=2,
        completed_assessments=3,
    )

    assert 0 <= result["readiness_score"] <= 100
    assert result["missing_skills"] == ["sql"]


def test_generate_learning_roadmap():
    result = generate_learning_roadmap(
        ["Python", "SQL", "FastAPI"],
        ["Python"],
    )

    assert result["total_steps"] == 2
    assert result["roadmap"][0]["skill"] == "SQL"
    assert result["roadmap"][1]["skill"] == "FastAPI"


def test_certification_eligibility():
    result = check_certification_eligibility(
        required_skills=["Python", "SQL"],
        user_skills=["Python", "SQL"],
        required_readiness_score=70,
        user_readiness_score=80,
        required_projects=2,
        completed_projects=2,
    )

    assert result["eligible"] is True
    assert result["missing_skills"] == []
