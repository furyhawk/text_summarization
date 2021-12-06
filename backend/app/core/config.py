from pydantic import BaseSettings, BaseModel
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "textsum"
    MODELS: List[str] = ['Headline', 'Transformer',
                         'TFIDF', 'T5', 'Finetuned']
    MIN_LENGTH: int = 15
    MAX_LENGTH: int = 150
    HEADLINE_MIN_LENGTH = 7
    HEADLINE_MAX_LENGTH = 20

    class Config:
        env_prefix = ""


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "app"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


@lru_cache()
def get_settings():
    return Settings()
