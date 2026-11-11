import importlib

import pytest
from pydantic import ValidationError


def test_settings_default_to_sqlite(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    import app.config as config

    importlib.reload(config)

    assert config.settings.DATABASE_URL == "sqlite:///./skillforge.db"


def test_gemini_service_without_key_falls_back_cleanly(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    import app.ai.gemini_service as gemini_service

    importlib.reload(gemini_service)

    assert gemini_service.api_key is None
    assert "not configured" in gemini_service.generate_response("hello").lower()


def test_production_settings_reject_placeholder_secret():
    from app.config import Settings

    with pytest.raises(ValidationError):
        Settings(
            ENVIRONMENT="production",
            DATABASE_URL="postgresql://user:pass@db.example.net/skillforge",
            SECRET_KEY="replace-with-a-strong-random-secret",
            ALLOWED_ORIGINS="https://app.skillforge.example",
        )


def test_production_settings_reject_placeholder_database_url():
    from app.config import Settings

    with pytest.raises(ValidationError):
        Settings(
            ENVIRONMENT="production",
            DATABASE_URL="postgresql://USER:PASSWORD@DB_HOST:5432/skillforge",
            SECRET_KEY="a-secure-random-secret-that-is-long-enough-123456",
            ALLOWED_ORIGINS="https://app.skillforge.io",
        )
