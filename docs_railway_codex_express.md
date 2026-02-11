# Interfacciarsi con Railway usando Codex (Express + Postgres)

Questa guida rapida ti permette di usare Codex per creare e deployare una API Express su Railway con database Postgres.

## 1) Prerequisiti

```bash
node -v
npm -v
```

## 2) Installa Codex CLI

```bash
npm install -g @openai/codex
```

## 3) Installa Railway CLI e fai login

```bash
npm install -g @railway/cli
railway login
```

## 4) Crea una cartella progetto e avvia Codex

```bash
mkdir express-railway-api && cd express-railway-api
codex
```

## 5) Prompt da dare a Codex

Incolla questo prompt dentro Codex:

```text
Create an Express API and deploy it to Railway with a Postgres database.
Requirements:
- Use Node.js + Express.
- Add endpoints:
  - GET /health -> {"status":"ok"}
  - GET /users
  - POST /users
- Use PostgreSQL with a users table (id, name, email unique, created_at).
- Add migrations or startup SQL.
- Read DB connection from DATABASE_URL.
- Add scripts in package.json for dev and start.
- Add a railway.json and Procfile if needed.
- Deploy to Railway and output the public URL.
```

## 6) Collegamento a Postgres su Railway

Dopo il deploy del servizio API:
1. In Railway crea un servizio **PostgreSQL** nel progetto.
2. Railway inietterà `DATABASE_URL` nelle variabili del servizio API (oppure aggiungila manualmente se necessario).
3. Riavvia/redeploy il servizio API.

## 7) Verifica rapida

```bash
curl https://<your-railway-domain>/health
```

Output atteso:

```json
{"status":"ok"}
```

## Note utili

- Se vuoi usare un DB locale in sviluppo, usa un file `.env` con `DATABASE_URL` e caricalo con `dotenv`.
- In produzione Railway gestisce URL e networking, quindi usa sempre le variabili d'ambiente del servizio.
- Per debug deployment:

```bash
railway logs
```
