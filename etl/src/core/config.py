from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    tmdb_api_key: str
    tmdb_language_code: str

    elasticsearch_url: str
    elasticsearch_index: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Config()