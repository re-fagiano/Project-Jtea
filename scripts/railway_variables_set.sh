#!/usr/bin/env bash
set -euo pipefail

# Set a Railway environment variable for the configured project/service/env.
# Usage:
#   bash scripts/railway_variables_set.sh KEY VALUE
#   PROJECT_ID=... SERVICE_ID=... ENVIRONMENT_ID=... bash scripts/railway_variables_set.sh KEY VALUE
#   APPLY_DEPLOY=1 bash scripts/railway_variables_set.sh KEY VALUE

PROJECT_ID="${PROJECT_ID:-e9c06cf5-a20b-440f-92c5-a165ff996232}"
SERVICE_ID="${SERVICE_ID:-be554fa7-7c1c-480e-adfb-6a19e37618e5}"
ENVIRONMENT_ID="${ENVIRONMENT_ID:-294682c0-50e3-4792-8913-87516a279aca}"
APPLY_DEPLOY="${APPLY_DEPLOY:-0}"

if [[ $# -ne 2 ]]; then
  echo "Usage: bash scripts/railway_variables_set.sh <KEY> <VALUE>" >&2
  exit 1
fi

KEY="$1"
VALUE="$2"

if ! command -v railway >/dev/null 2>&1; then
  echo "[ERROR] Railway CLI non trovata. Esegui: bash scripts/railway_cli_bootstrap.sh" >&2
  exit 2
fi

if ! railway whoami >/dev/null 2>&1; then
  if [[ -t 0 ]]; then
    railway login
  else
    echo "[ERROR] Non autenticato e shell non interattiva. Imposta RAILWAY_TOKEN." >&2
    exit 3
  fi
fi

railway link --project "$PROJECT_ID" --service "$SERVICE_ID" --environment "$ENVIRONMENT_ID" >/dev/null
railway variables set "$KEY" "$VALUE" --environment "$ENVIRONMENT_ID"

echo "[OK] Variabile aggiornata: $KEY"

if [[ "$APPLY_DEPLOY" == "1" ]]; then
  echo "[INFO] Avvio deploy (railway up)"
  railway up
fi
