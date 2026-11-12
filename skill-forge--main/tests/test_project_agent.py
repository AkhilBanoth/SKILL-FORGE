
from unittest.mock import patch

import pytest

from app.agents import project_agent


def test_ask_project_agent_success(monkeypatch):
    monkeypatch.setattr(
        project_agent,
        "read_project_sources",
        lambda question: "SkillForge uses FastAPI.",
    )

    captured = {}

    def fake_generate_response(prompt):
        captured["prompt"] = prompt
        return "SkillForge is built with FastAPI."

    monkeypatch.setattr(
        project_agent,
        "generate_response",
        fake_generate_response,
    )

    answer = project_agent.ask_project_agent("What is SkillForge?")

    assert answer == "SkillForge is built with FastAPI."
    assert "What is SkillForge?" in captured["prompt"]
    assert "SkillForge uses FastAPI." in captured["prompt"]
    assert "Answer the user's question directly" in captured["prompt"]


@pytest.mark.parametrize("question", ["", "   ", "\n\t"])
def test_ask_project_agent_rejects_empty_question(question):
    with pytest.raises(ValueError, match="Question cannot be empty"):
        project_agent.ask_project_agent(question)


def test_ask_project_agent_passes_learner_context(monkeypatch):
    monkeypatch.setattr(
        project_agent,
        "read_project_sources",
        lambda question: "Test source",
    )

    monkeypatch.setattr(
        project_agent,
        "generate_response",
        lambda prompt: "Here is your answer.",
    )

    answer = project_agent.ask_project_agent(
        "Explain my project",
        learner_context={"level": "beginner"},
    )

    assert answer == "Here is your answer."


def test_ask_project_agent_propagates_gemini_failure(monkeypatch):
    monkeypatch.setattr(
        project_agent,
        "read_project_sources",
        lambda question: "Test source",
    )

    def fake_generate_response(prompt):
        raise RuntimeError("Gemini service unavailable")

    monkeypatch.setattr(
        project_agent,
        "generate_response",
        fake_generate_response,
    )

    with pytest.raises(RuntimeError, match="Gemini service unavailable"):
        project_agent.ask_project_agent("What is SkillForge?")


def test_ask_project_agent_returns_generated_answer(monkeypatch):
    monkeypatch.setattr(
        project_agent,
        "read_project_sources",
        lambda question: "Test source",
    )

    monkeypatch.setattr(
        project_agent,
        "generate_response",
        lambda prompt: "  SkillForge helps learners.  ",
    )

    answer = project_agent.ask_project_agent("What is SkillForge?")

    assert answer == "SkillForge helps learners."
