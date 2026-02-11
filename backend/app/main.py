"""
Entry point FastAPI - Project Jtea.
"""
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
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
    """Apre il frontend se configurato, altrimenti mostra una landing diagnostica."""
    frontend_url = os.getenv("FRONTEND_URL", "").strip()
    if frontend_url:
        return RedirectResponse(url=frontend_url, status_code=307)

    return HTMLResponse(
        content=(
            "<h1>Project Jtea API online</h1>"
            "<p>Il backend è attivo, ma FRONTEND_URL non è configurata.</p>"
            "<ul>"
            "<li><a href='/docs'>Apri Swagger docs</a></li>"
            "<li><a href='/health'>Health check</a></li>"
            "<li><a href='/db/health'>DB health check</a></li>"
            "</ul>"
            "<p>Per avere una UI navigabile su / imposta la variabile FRONTEND_URL "
            "nel servizio backend Railway.</p>"
        )
    )


app.include_router(auth)
app.include_router(clienti, prefix="/api")
app.include_router(richieste, prefix="/api")
