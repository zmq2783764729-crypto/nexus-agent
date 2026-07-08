from functools import lru_cache
from pathlib import Path
from typing import Literal
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=False)


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return int(value)


class Settings(BaseModel):
    app_name: str = Field(default_factory=lambda: os.getenv("APP_NAME", "NexusAgent Core"))
    app_env: Literal["local", "dev", "test", "prod"] = Field(
        default_factory=lambda: os.getenv("APP_ENV", "local")
    )
    debug: bool = Field(default_factory=lambda: _get_bool("DEBUG", True))

    mysql_host: str = Field(default_factory=lambda: os.getenv("MYSQL_HOST", "127.0.0.1"))
    mysql_port: int = Field(default_factory=lambda: _get_int("MYSQL_PORT", 3306))
    mysql_user: str = Field(default_factory=lambda: os.getenv("MYSQL_USER", "root"))
    mysql_password: str = Field(default_factory=lambda: os.getenv("MYSQL_PASSWORD", ""))
    mysql_database: str = Field(default_factory=lambda: os.getenv("MYSQL_DATABASE", "agent01"))
    mysql_charset: str = Field(default_factory=lambda: os.getenv("MYSQL_CHARSET", "utf8mb4"))

    llm_provider: str = Field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai"))
    llm_model: str = Field(default_factory=lambda: os.getenv("LLM_MODEL", "qwen3.7-plus"))
    llm_api_key: str = Field(default_factory=lambda: os.getenv("LLM_API_KEY", ""))
    llm_base_url: str = Field(default_factory=lambda: os.getenv("LLM_BASE_URL", ""))

    redis_url: str = Field(default_factory=lambda: os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"))

    @property
    def database_url(self) -> str:
        return (
            f"mysql+asyncmy://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            f"?charset={self.mysql_charset}"
        )

    @property
    def is_local(self) -> bool:
        return self.app_env == "local"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
