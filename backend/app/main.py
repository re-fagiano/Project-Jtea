"""
Entry point FastAPI - Project Jtea.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from .config import get_settings
from .database import Base, engine
from .routes.health import router as health_router
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

app.include_router(health_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    if settings.FRONTEND_URL:
        return RedirectResponse(url=settings.FRONTEND_URL, status_code=307)
    if settings.ENVIRONMENT.lower() == "production":
        # In produzione, se il frontend non è configurato, mostriamo la docs API
        # invece del payload JSON grezzo per un atterraggio più utile.
        return RedirectResponse(url="/docs", status_code=307)
    return {"status": "ok", "service": "project-jtea-api"}


app.include_router(auth)
app.include_router(clienti, prefix="/api")
app.include_router(richieste, prefix="/api")
