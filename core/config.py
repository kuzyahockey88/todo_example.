from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    cors_allowed_origin: list[str]

    class Config:
        env_file = ".env"


settings = Settings()
