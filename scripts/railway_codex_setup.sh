#!/usr/bin/env bash
set -euo pipefail

# Bootstrap script for connecting this repository to Railway from Codex/local shell.
# Usage:
#   bash scripts/railway_codex_setup.sh
#   PROJECT_ID=<id> SERVICE_ID=<id> ENVIRONMENT_ID=<id> bash scripts/railway_codex_setup.sh

PROJECT_ID="${PROJECT_ID:-e9c06cf5-a20b-440f-92c5-a165ff996232}"
SERVICE_ID="${SERVICE_ID:-be554fa7-7c1c-480e-adfb-6a19e37618e5}"
ENVIRONMENT_ID="${ENVIRONMENT_ID:-294682c0-50e3-4792-8913-87516a279aca}"

if ! command -v railway >/dev/null 2>&1; then
  echo "[ERROR] Railway CLI non trovata. Installa con: npm install -g @railway/cli" >&2
  exit 1
fi

echo "[1/4] Verifica login Railway..."
if ! railway whoami >/dev/null 2>&1; then
  echo "Non risulti autenticato. Avvio login interattivo..."
  railway login
fi

echo "[2/4] Link progetto e servizio"
railway link --project "$PROJECT_ID" --service "$SERVICE_ID" --environment "$ENVIRONMENT_ID"

echo "[3/4] Pull variabili in backend/.env.railway"
mkdir -p backend
railway variables --environment "$ENVIRONMENT_ID" > backend/.env.railway

echo "[4/4] Done"
echo "- File generato: backend/.env.railway"
echo "- Avvio locale con variabili Railway:"
echo "  set -a; source backend/.env.railway; set +a; cd backend; uvicorn app.main:app --host 0.0.0.0 --port 8000"
