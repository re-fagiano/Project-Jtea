"""
Configurazione applicazione FastAPI
"""
from pydantic_settings import BaseSettings
from pydantic import model_validator
from functools import lru_cache


class Settings(BaseSettings):
    """Configurazione caricata da .env"""

    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ticket_platform"
    
    # JWT Auth
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email SMTP
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@example.com"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # App
    APP_NAME: str = "Ticket Platform API"
    DEBUG: bool = True
    AUTO_CREATE_TABLES: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        """Valida impostazioni critiche in produzione."""
        if self.ENVIRONMENT.lower() == "production":
            if self.DEBUG:
                raise ValueError("DEBUG non può essere True in produzione")
            if self.SECRET_KEY == "your-super-secret-key-change-in-production":
                raise ValueError("SECRET_KEY deve essere impostata in produzione")
            if self.DATABASE_URL == "postgresql://postgres:password@localhost:5432/ticket_platform":
                raise ValueError("DATABASE_URL deve essere impostato in produzione")
        return self


@lru_cache()
def get_settings() -> Settings:
    """Singleton per le impostazioni"""
    return Settings()
