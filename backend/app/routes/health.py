import os

from fastapi import APIRouter
from sqlalchemy import create_engine, text

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "service": "project-jtea-api"}


def _check_db_connection() -> dict:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return {"db": "error", "detail": "DATABASE_URL not set"}

    try:
        # pool_pre_ping evita connessioni "morte" dopo sleep/redeploy
        engine = create_engine(db_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as exc:
        # Non loggare mai l'intero DATABASE_URL (contiene password)
        return {"db": "error", "detail": str(exc)}


@router.get("/db/health")
def db_health():
    return _check_db_connection()


@router.get("/db-test", include_in_schema=False)
def db_test_legacy_alias():
    """Compatibilità con endpoint storico usato durante il deploy su Railway."""
    return _check_db_connection()
