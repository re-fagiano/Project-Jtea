"""
Entry point FastAPI - Project Jtea.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from .config import get_settings
from .database import Base, engine
from .routers import auth, clienti, richieste

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.AUTO_CREATE_TABLES:
        try:
            Base.metadata.create_all(bind=engine)
        except SQLAlchemyError as exc:
            print(f"Errore inizializzazione DB: {exc}")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="API per la gestione ticket (MVP)",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    return {"message": "API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(auth)
app.include_router(clienti, prefix="/api")
app.include_router(richieste, prefix="/api")
