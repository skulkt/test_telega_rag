from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str


@lru_cache
def get_settings() -> Settings:
    return Settings()


Settings.model_rebuild()
