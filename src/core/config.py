import logging

from functools import lru_cache
from pydantic_settings import BaseSettings

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] — [%(levelname)s] — [%(module)s] — [%(funcName)s]:  %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    GIGACHAT_CLIENT_ID: str
    GIGACHAT_CLIENT_SECRET: str
    GIGACHAT_SCOPE: str

    LLM_HISTORY_TTL: int = 3600

    TELEGRAM_TOKEN: str

    REDIS_HOST: str
    REDIS_PORT: int

    LLM_AGENT_NAME: str
    SENTENCES_MODEL_DIR: str

    @property
    def get_redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()


Settings.model_rebuild()
