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

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Variabili d'ambiente
Copia `.env.example` in `.env` (backend) oppure configura le variabili nel servizio Railway (DATABASE_URL o PGHOST/PGPORT/PGUSER/PGPASSWORD/PGDATABASE).

## Deploy su Railway
1. Collega il repo a Railway.
2. Railway userà `railway.json` (Nixpacks) e avvierà `bash start.sh`.
3. Imposta le variabili d'ambiente richieste (vedi tabella nella documentazione o `.env.example`).
