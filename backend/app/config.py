"""
Configurazione applicazione FastAPI
"""
from pydantic_settings import BaseSettings
from pydantic import model_validator
from urllib.parse import quote_plus
from functools import lru_cache


class Settings(BaseSettings):
    """Configurazione caricata da .env"""

    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = ""
    PGHOST: str = ""
    PGPORT: str = ""
    PGUSER: str = ""
    PGPASSWORD: str = ""
    PGDATABASE: str = ""
    
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
    DEBUG: bool = False
    AUTO_CREATE_TABLES: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @model_validator(mode="before")
    def assemble_db_url(cls, values: dict) -> dict:
        db_url = values.get("DATABASE_URL") or ""
        if ("localhost" in db_url or not db_url) and all(
            values.get(k) for k in ["PGHOST", "PGPORT", "PGUSER", "PGPASSWORD", "PGDATABASE"]
        ):
            user = values["PGUSER"]
            password = quote_plus(values["PGPASSWORD"])
            host = values["PGHOST"]
            port = values["PGPORT"]
            db = values["PGDATABASE"]
            values["DATABASE_URL"] = (
                f"postgresql://{user}:{password}@{host}:{port}/{db}?sslmode=require"
            )
        return values

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        """Valida impostazioni critiche in produzione."""
        if self.ENVIRONMENT.lower() == "production":
            if self.DEBUG:
                raise ValueError("DEBUG non può essere True in produzione")
            if self.SECRET_KEY == "your-super-secret-key-change-in-production":
                raise ValueError("SECRET_KEY deve essere impostata in produzione")
            if not self.DATABASE_URL or "localhost" in self.DATABASE_URL:
                raise ValueError(
                    "DATABASE_URL deve essere impostato in produzione (o definire PGHOST/PGPORT/PGUSER/PGPASSWORD/PGDATABASE)"
                )
        return self


@lru_cache()
def get_settings() -> Settings:
    """Singleton per le impostazioni"""
    return Settings()
