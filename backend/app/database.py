"""
Configurazione database SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import get_settings

settings = get_settings()


database_url = settings.DATABASE_URL

if not database_url:
    database_url = "sqlite:///./data.db"

if database_url and not database_url.startswith("sqlite"):
    url = make_url(database_url)
    if url.drivername.startswith("postgresql") and "sslmode" not in url.query:
        url = url.set(query={**url.query, "sslmode": "require"})
    database_url = str(url)

if database_url.startswith("sqlite"):
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(database_url, pool_pre_ping=True, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
