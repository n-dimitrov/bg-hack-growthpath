from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./growthpath.db"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LLM Farm Configuration - Bosch LLM Farm
    LLM_FARM_BASE_URL: str = "https://aoai-farm.bosch-temp.com/api/google/v1"
    LLM_FARM_API_KEY: str = ""
    LLM_DEFAULT_MODEL: str = "claude-sonnet-4-5@20250929"
    LLM_DEFAULT_MAX_TOKENS: int = 4096

    class Config:
        env_file = ".env"


settings = Settings()
