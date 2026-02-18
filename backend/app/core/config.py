from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AURORA CORE"
    environment: str = "dev"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field(default="change-me", min_length=16)
    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"

    database_url: str = "postgresql+psycopg://aurora:aurora@db:5432/aurora"
    redis_url: str = "redis://redis:6379/0"
    broker_url: str = "redis://redis:6379/1"
    result_backend: str = "redis://redis:6379/2"

    cors_origins: list[str] = ["http://localhost:3000"]

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_starter: str = ""
    stripe_price_pro: str = ""
    stripe_price_agency: str = ""

    openai_api_key: str = ""
    ollama_base_url: str = "http://ollama:11434"


@lru_cache
def get_settings() -> Settings:
    return Settings()
