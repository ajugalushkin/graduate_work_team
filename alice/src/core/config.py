from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки."""

    model_config = SettingsConfigDict(
        env_file=(".env"),
    )


settings = Settings()
