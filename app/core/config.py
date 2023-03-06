import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Chat"
    PROJECT_DESCRIPTION: str = "A FastAPI chat application"
    PROJECT_VERSION: str = "0.1.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DB_URL: str = os.getenv("DB_URL")


@lru_cache()
def get_settings():
    return Settings()
