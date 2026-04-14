from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Surveyor Backend"
    API_V1_STR: str = "/api/v1"
    
    # In a real app, these would be loaded from .env
    SECRET_KEY: str = "your-secret-key-for-jwt-change-it"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        case_sensitive = True

settings = Settings()
