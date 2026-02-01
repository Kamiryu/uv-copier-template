"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from environment variables and optional .env file."""

    environment: str = "development"
    log_level: str = "info"
    log_file: str = "logs/app.log"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="")


settings = Settings()
