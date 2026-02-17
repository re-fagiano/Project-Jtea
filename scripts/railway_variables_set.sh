#!/usr/bin/env bash
set -euo pipefail

# Set Railway environment variables for the configured project/service/env.
# Usage:
#   bash scripts/railway_variables_set.sh KEY VALUE
#   bash scripts/railway_variables_set.sh --required-defaults
#   PROJECT_ID=... SERVICE_ID=... ENVIRONMENT_ID=... bash scripts/railway_variables_set.sh KEY VALUE
#   APPLY_DEPLOY=1 bash scripts/railway_variables_set.sh --required-defaults

PROJECT_ID="${PROJECT_ID:-e9c06cf5-a20b-440f-92c5-a165ff996232}"
SERVICE_ID="${SERVICE_ID:-be554fa7-7c1c-480e-adfb-6a19e37618e5}"
ENVIRONMENT_ID="${ENVIRONMENT_ID:-294682c0-50e3-4792-8913-87516a279aca}"
APPLY_DEPLOY="${APPLY_DEPLOY:-0}"

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

set_required_defaults() {
  : "${SECRET_KEY:?Imposta SECRET_KEY nell'ambiente prima di usare --required-defaults}"

  railway variables set ENVIRONMENT production --environment "$ENVIRONMENT_ID"
  railway variables set SECRET_KEY "$SECRET_KEY" --environment "$ENVIRONMENT_ID"
  railway variables set ALGORITHM HS256 --environment "$ENVIRONMENT_ID"
  railway variables set ACCESS_TOKEN_EXPIRE_MINUTES 30 --environment "$ENVIRONMENT_ID"
  railway variables set APP_NAME "Project Jtea API" --environment "$ENVIRONMENT_ID"
  railway variables set DEBUG false --environment "$ENVIRONMENT_ID"
  railway variables set AUTO_CREATE_TABLES true --environment "$ENVIRONMENT_ID"

  if [[ -n "${CORS_ORIGINS:-}" ]]; then
    railway variables set CORS_ORIGINS "$CORS_ORIGINS" --environment "$ENVIRONMENT_ID"
  else
    echo "[WARN] CORS_ORIGINS non impostato: configurarlo manualmente con il dominio frontend." >&2
  fi

  echo "[OK] Variabili backend obbligatorie impostate." 
  echo "[NOTE] DATABASE_URL viene iniettata automaticamente se il servizio Postgres è collegato." 
}

if [[ $# -eq 1 && "$1" == "--required-defaults" ]]; then
  set_required_defaults
elif [[ $# -eq 2 ]]; then
  KEY="$1"
  VALUE="$2"
  railway variables set "$KEY" "$VALUE" --environment "$ENVIRONMENT_ID"
  echo "[OK] Variabile aggiornata: $KEY"
else
  echo "Usage:" >&2
  echo "  bash scripts/railway_variables_set.sh <KEY> <VALUE>" >&2
  echo "  SECRET_KEY=... CORS_ORIGINS=https://frontend.example.com bash scripts/railway_variables_set.sh --required-defaults" >&2
  exit 1
fi

if [[ "$APPLY_DEPLOY" == "1" ]]; then
  echo "[INFO] Avvio deploy (railway up)"
  railway up
fi
