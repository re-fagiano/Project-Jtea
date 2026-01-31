# Project-Jtea (Ticket Platform)

Backend FastAPI + frontend Next.js.

## Avvio in locale

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Endpoint utili:
- `GET /health` per verificare lo stato dell'API.
- `GET /docs` per la documentazione Swagger.
- La rotta `/` non è definita e restituisce `404` per design.

(Facoltativo) Se vuoi una root route, aggiungi in `backend/app/main.py`:
```python
@app.get("/", include_in_schema=False)
def root():
    return {"message": "API running"}
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Se il frontend deve comunicare con il backend, imposta `NEXT_PUBLIC_API_URL`
(ad esempio in `frontend/.env.local`) con l'URL del backend.

## Variabili d'ambiente
Copia `.env.example` in `.env` (backend) oppure configura le variabili nel servizio Railway.
Le variabili principali sono:
- `DATABASE_URL` (oppure `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`).
- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` per i token JWT.
- `REDIS_URL` per Celery (se usato).
- Parametri SMTP se invii email (`SMTP_*`, `EMAIL_FROM`).

## Deploy su Railway
1. Collega il repo a Railway.
2. Railway userà `railway.json` (Nixpacks) e avvierà `bash start.sh`.
3. Imposta le variabili d'ambiente richieste (vedi tabella nella documentazione o `.env.example`).
