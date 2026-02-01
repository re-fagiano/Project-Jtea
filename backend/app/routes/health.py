from fastapi import APIRouter
from sqlalchemy import create_engine, text
import os

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"message": "API running"}


@router.get("/db/health")
def db_health():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return {"db": "error", "detail": "DATABASE_URL not set"}

    try:
        # pool_pre_ping evita connessioni "morte" dopo sleep/redeploy
        engine = create_engine(db_url, pool_pre_ping=True)

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as e:
        # Non loggare mai l'intero DATABASE_URL (contiene password)
        return {"db": "error", "detail": str(e)}
