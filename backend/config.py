"""
config.py
---------
Single source of truth for all environment variables.
Uses pydantic-settings so every value is type-checked at startup.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Always resolve .env from the project root (one level above this file)
_ENV_FILE = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── AI Provider ───────────────────────────────────────────────────────────
    active_ai_provider: str = Field("openai", description="'openai' or 'gemini'")

    openai_api_key: str = Field("", description="OpenAI secret key")
    openai_model: str = Field("gpt-4o", description="OpenAI model name")

    gemini_api_key: str = Field("", description="Google Gemini API key")
    gemini_model: str = Field("gemini-2.0-flash", description="Gemini model name")

    # ── Groq (free tier, OpenAI-compatible) ──────────────────────────────────
    groq_api_key: str = Field("", description="Groq API key (free tier available)")
    groq_model: str = Field("llama-3.3-70b-versatile", description="Groq model name")

    # ── Database ──────────────────────────────────────────────────────────────
    database_url: str = Field(
        "postgresql+asyncpg://user:password@localhost:5432/esa_db"
    )

    # ── Redis ─────────────────────────────────────────────────────────────────
    redis_url: str = Field("redis://localhost:6379")

    # ── Auth ──────────────────────────────────────────────────────────────────
    secret_key: str = Field("change-me", description="JWT signing secret")
    algorithm: str = Field("HS256")
    access_token_expire_minutes: int = Field(60)

    # ── Vector Store ──────────────────────────────────────────────────────────
    vector_store: str = Field("pgvector", description="'pgvector' or 'pinecone'")
    pinecone_api_key: str = Field("")
    pinecone_environment: str = Field("")
    pinecone_index_name: str = Field("esa-bc-docs")

    # ── App ───────────────────────────────────────────────────────────────────
    app_env: str = Field("development")
    cors_origins: str = Field("http://localhost:5173")

    @property
    def cors_origins_list(self) -> list[str]:
        """Split comma-separated CORS origins into a list."""
        return [o.strip() for o in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


# Single shared instance — import this everywhere
settings = Settings()
