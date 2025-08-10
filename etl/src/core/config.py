from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    elastic_url: str
    elastic_index: str
    dump_file: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Config()