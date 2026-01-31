"""
Configurazione applicazione FastAPI.
"""
from __future__ import annotations

from functools import lru_cache
from typing import List
from urllib.parse import quote_plus

from pydantic import field_validator, model_validator  # noqa: F401
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurazione caricata da variabili d'ambiente e file .env."""

    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = ""
    PGHOST: str = ""
    PGPORT: str = ""
    PGUSER: str = ""
    PGPASSWORD: str = ""
    PGDATABASE: str = ""

    # JWT
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    APP_NAME: str = "Project Jtea API"
    DEBUG: bool = False
    AUTO_CREATE_TABLES: bool = True
    CORS_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, value: str, info) -> str:
        """Costruisce DATABASE_URL da variabili PG* se necessario."""
        values = info.data
        db_url = value or ""
        if (not db_url or "localhost" in db_url) and all(
            values.get(k) for k in ["PGHOST", "PGPORT", "PGUSER", "PGPASSWORD", "PGDATABASE"]
        ):
            user = values["PGUSER"]
            password = quote_plus(values["PGPASSWORD"])
            host = values["PGHOST"]
            port = values["PGPORT"]
            db = values["PGDATABASE"]
            return f"postgresql://{user}:{password}@{host}:{port}/{db}?sslmode=require"
        return db_url

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
