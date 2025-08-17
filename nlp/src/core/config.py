"""Configuration settings for the application."""

from functools import lru_cache

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    module_name: str = "nlp-module"
    api_v1_prefix: str = "/api/v1"
    environment: str = Field(default="production")
    log_level: str = "INFO"
    
    # Patterns
    patterns_path: str = "patterns.json"

    # Elasticsearch
    elasticsearch_host: str = "elasticsearch"
    elasticsearch_port: int = 9200
    elasticsearch_username: str = ""
    elasticsearch_password: str = ""

    # CORS
    cors_origins: list[AnyHttpUrl] | list[str] = []

    @field_validator("cors_origins", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse string CORS origins into list of URLs."""
        if isinstance(v, str) and not v.startswith("["):
            # Return as strings to avoid validation issues
            origins = [url.strip() for url in v.split(",")]
            # Ensure each URL has a scheme
            for i, origin in enumerate(origins):
                if not origin.startswith(("http://", "https://")):
                    origins[i] = f"http://{origin}"
            return origins
        elif isinstance(v, list):
            return v
        raise ValueError("CORS_ORIGINS should be a comma-separated string of URLs")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()  # type: ignore
