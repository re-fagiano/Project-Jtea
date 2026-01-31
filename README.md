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
- `GET /` ritorna `{"message": "Backend online"}`.
- `GET /health` per health check.
- `POST /login` per ottenere un token JWT.
- `GET /users/me` per l'utente autenticato.

## Frontend (Next.js + Tailwind)

### Setup locale
```bash
cd frontend
npm install
npm run dev
```

Configura `NEXT_PUBLIC_API_URL` in `frontend/.env.local` (vedi `.env.local.example`).

## Deploy su Railway

### Opzione consigliata: due servizi

**Backend**
- Collega il repo e seleziona la cartella `backend`.
- Abilita PostgreSQL: Railway imposterà `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`.
- Imposta manualmente `SECRET_KEY`.
- Usa `startCommand`: `bash start.sh`.

**Frontend**
- Collega la cartella `frontend`.
- Build command: `npm install && npm run build`.
- Start command: `npm start`.
- Imposta `NEXT_PUBLIC_API_URL` con l'URL pubblico del backend.

### Opzione alternativa: un solo servizio

1. Esegui `npm run build` e `npm run export` nel frontend.
2. Copia la cartella `out` in `backend/static`.
3. In FastAPI monta i file statici:

```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

### Verifica
- Frontend: `https://<nome-progetto>.up.railway.app`
- Backend: `https://<nome-progetto>.up.railway.app/health`
