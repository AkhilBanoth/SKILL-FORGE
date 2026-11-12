
from sqlalchemy.orm import Session

from app.models.course_progress import CourseProgress
from app.models.assessment_attempt import AssessmentAttempt
from app.models.user_skill import UserSkill


def generate_learning_recommendations(
    db: Session,
    user_id: int,
) -> dict:
    user_skills = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user_id)
        .all()
    )

    skill_gaps = []

    for user_skill in user_skills:
        level = float(user_skill.level or 0)

        if level < 5:
            skill_gaps.append({
                "skill_id": user_skill.skill_id,
                "current_level": level,
                "target_level": 5,
                "gap": round(5 - level, 2),
            })

    course_progress = (
        db.query(CourseProgress)
        .filter(CourseProgress.user_id == user_id)
        .all()
    )

    incomplete_courses = [
        {
            "course_id": item.course_id,
            "progress_percentage": float(
                item.progress_percentage or 0
            ),
        }
        for item in course_progress
        if not item.is_completed
    ]

    assessments = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.status == "submitted",
        )
        .order_by(AssessmentAttempt.submitted_at.desc())
        .limit(5)
        .all()
    )

    weak_assessments = [
        {
            "assessment_id": item.assessment_id,
            "score_percentage": round(
                float(item.score or 0) * 100
                / float(item.max_score),
                2,
            ),
        }
        for item in assessments
        if item.max_score and item.max_score > 0
        and item.score / item.max_score < 0.7
    ]

    recommendations = []

    for skill in sorted(
        skill_gaps,
        key=lambda item: item["gap"],
        reverse=True,
    )[:3]:
        recommendations.append({
            "type": "skill_improvement",
            "skill_id": skill["skill_id"],
            "reason": (
                f"Your current skill level is "
                f"{skill['current_level']}. "
                f"Work toward level {skill['target_level']}."
            ),
            "priority": "high",
        })

    for course in incomplete_courses[:3]:
        recommendations.append({
            "type": "continue_course",
            "course_id": course["course_id"],
            "progress_percentage": course[
                "progress_percentage"
            ],
            "reason": "Continue this course to improve your progress.",
            "priority": "medium",
        })

    for assessment in weak_assessments[:3]:
        recommendations.append({
            "type": "assessment_practice",
            "assessment_id": assessment["assessment_id"],
            "score_percentage": assessment[
                "score_percentage"
            ],
            "reason": "Review this assessment topic and practise again.",
            "priority": "high",
        })

    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "summary": {
            "skill_gaps_found": len(skill_gaps),
            "incomplete_courses": len(incomplete_courses),
            "weak_assessments": len(weak_assessments),
        },
    }