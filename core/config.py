from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str
    cors_allowed_origin: List[str]

    class Config:
        env_file = ".env"

settings = Settings()
