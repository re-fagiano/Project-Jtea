# Project-Jtea

Repository con backend FastAPI e frontend Next.js + Tailwind.

```
project-jtea/
  backend/
  frontend/
  railway.json
```

## Backend (FastAPI)

### Setup locale
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copia il file `.env.example` in `.env` e personalizzalo.

Variabili essenziali:
- `DATABASE_URL` **oppure** `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`.
- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` per i token JWT.

Avvio:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Endpoint utili:
- `GET /health` per verificare lo stato dell'API (ritorna `{"status":"ok"}`).
- `GET /docs` per la documentazione Swagger.
- `GET /` restituisce uno status rapido del servizio.


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
- `FRONTEND_URL` per reindirizzare `/` al frontend deployato.

## Deploy su Railway
1. Collega il repo a Railway.
2. Railway userà `railway.json` (Nixpacks) e avvierà `bash start.sh`.
3. Imposta le variabili d'ambiente richieste (vedi tabella nella documentazione o `.env.example`).

### Railway: variabili da impostare (backend)

Obbligatorie:
- `ENVIRONMENT=production`
- `SECRET_KEY=<chiave-lunga-casuale>`
- `ALGORITHM=HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`
- `APP_NAME=Project Jtea API`
- `DEBUG=false`
- `AUTO_CREATE_TABLES=true`
- `CORS_ORIGINS=https://<dominio-frontend>`

Database (scegli una sola modalità):
- Modalità A (consigliata Railway): `DATABASE_URL` (iniettata dal servizio PostgreSQL collegato).
- Modalità B (fallback): `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`.

Opzionali:
- `SMTP_HOST`, `SMTP_PORT`, `EMAIL_FROM`
- `REDIS_URL`

### Railway: variabili frontend

- `NEXT_PUBLIC_API_URL=https://<dominio-backend-railway>`

### Collegamento rapido Codex ↔ Railway (questo progetto)
Per collegare velocemente il repository al progetto Railway indicato e scaricare le variabili del servizio backend:

```bash
bash scripts/railway_codex_setup.sh
```

Lo script usa di default questi ID (sovrascrivibili via env):
- `PROJECT_ID=e9c06cf5-a20b-440f-92c5-a165ff996232`
- `SERVICE_ID=be554fa7-7c1c-480e-adfb-6a19e37618e5`
- `ENVIRONMENT_ID=294682c0-50e3-4792-8913-87516a279aca`

Esempio con override:

```bash
PROJECT_ID=<project-id> SERVICE_ID=<service-id> ENVIRONMENT_ID=<environment-id> bash scripts/railway_codex_setup.sh
```

### Verifica rapida post deploy

```bash
curl https://<dominio-backend-railway>/health
```

Output atteso:

```json
{"status":"ok"}
```

## Quick start Codex + Railway (Express + Postgres)
Se vuoi creare un nuovo progetto Express deployato su Railway con Postgres usando Codex, segui la guida dedicata:

- `docs_railway_codex_express.md`
