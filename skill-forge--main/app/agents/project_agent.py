
from app.ai.gemini_service import generate_response
from app.agents.source_reader import read_project_sources
from app.agents.prompts import PROJECT_AGENT_SYSTEM_PROMPT


def ask_project_agent(
    question: str,
    learner_context: dict | None = None,
) -> str:
    """Answer SkillForge project questions using Gemini and project sources."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    source_context = read_project_sources(question)

    prompt = f"""
{PROJECT_AGENT_SYSTEM_PROMPT}

You are the AI project assistant for SkillForge.

Learner context:
{learner_context or {}}

Relevant project source code and documentation:
{source_context}

User question:
{question}

Instructions:
- Answer the user's question directly and clearly.
- Use the supplied project context when relevant.
- Do not invent files, functions, endpoints, or implementation details.
- If the supplied context does not contain the answer, explain what is missing.
- Never reveal API keys, passwords, tokens, or other secrets.
- Use simple English and provide practical steps when appropriate.
"""

    return generate_response(prompt).strip()
