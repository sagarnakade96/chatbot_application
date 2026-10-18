from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo-root .env (shared with the other experiments in this repository).
ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    app_name: str = "Chatbot Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:8501"]

    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_region: str | None = None
    knowledge_base_id: str | None = None
    tavily_api_key: str | None = None


    model_config = SettingsConfigDict(
        env_file=ROOT_ENV, env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
