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
- `GET /` reindirizza alla UI se imposti `FRONTEND_URL`; in alternativa reindirizza a `/docs`.


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
4. (Consigliato) Se il frontend è su un servizio separato, imposta `FRONTEND_URL` nel backend per aprire la UI direttamente da `/`.

## Quick start Codex + Railway (Express + Postgres)
Se vuoi creare un nuovo progetto Express deployato su Railway con Postgres usando Codex, segui la guida dedicata:

- `docs_railway_codex_express.md`


## Verifica online su Railway
Dopo il deploy, verifica che il servizio sia realmente online:

```bash
curl https://<tuo-dominio>.up.railway.app/health
curl https://<tuo-dominio>.up.railway.app/db/health
```

Risultati attesi:
- `/health` => `{"status":"ok","service":"project-jtea-api"}`
- `/db/health` => `{"db":"ok"}`

Se `/db/health` fallisce, controlla che `DATABASE_URL` (oppure variabili `PG*`) sia configurata nel servizio Railway.
