"""
Configurazione database SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

database_url = settings.DATABASE_URL

if database_url and not database_url.startswith("sqlite"):
    url = make_url(database_url)
    if url.drivername.startswith("postgresql") and "sslmode" not in url.query:
        url = url.set(query={**url.query, "sslmode": "require"})
    database_url = str(url)

# Crea engine SQLAlchemy
# SQLite non supporta pool_size, quindi configurazione diversa
if database_url.startswith("sqlite"):
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}  # Necessario per SQLite
    )
else:
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base per i modelli
Base = declarative_base()


def get_db():
    """
    Dependency che fornisce una sessione database.
    Usare con: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
