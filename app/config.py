
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SkillForge"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///./skillforge.db"
    POSTGRES_DB: str = "skillforge"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DATABASE: str = "skillforge"

    SECRET_KEY: str = "change-this-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ALGORITHM: str = "HS256"

    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-3.6-flash"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.ENVIRONMENT.strip().lower() == "production":
            secret_key = self.SECRET_KEY.lower()
            if len(self.SECRET_KEY) < 32 or any(
                marker in secret_key
                for marker in ("change-this", "replace", "placeholder", "example")
            ):
                raise ValueError("Production requires a strong SECRET_KEY of at least 32 characters")
            if self.DATABASE_URL.startswith("sqlite"):
                raise ValueError("Production requires a PostgreSQL DATABASE_URL")
            if any(
                marker in self.DATABASE_URL.lower()
                for marker in ("db_host", "user:password", "replace", "placeholder")
            ):
                raise ValueError("Production DATABASE_URL must not contain placeholders")
            if not self.allowed_origins or "*" in self.allowed_origins:
                raise ValueError("Production requires explicit ALLOWED_ORIGINS")
            if any("your-" in origin or "example.com" in origin for origin in self.allowed_origins):
                raise ValueError("Production ALLOWED_ORIGINS must not contain placeholders")
        return self


settings = Settings()
