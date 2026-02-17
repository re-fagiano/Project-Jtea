#!/usr/bin/env bash
set -euo pipefail

# Bootstrap script for connecting this repository to Railway from Codex/local shell.
# Usage:
#   bash scripts/railway_codex_setup.sh
#   RAILWAY_TOKEN=<token> bash scripts/railway_codex_setup.sh
#   PROJECT_ID=<id> SERVICE_ID=<id> ENVIRONMENT_ID=<id> bash scripts/railway_codex_setup.sh

PROJECT_ID="${PROJECT_ID:-e9c06cf5-a20b-440f-92c5-a165ff996232}"
SERVICE_ID="${SERVICE_ID:-be554fa7-7c1c-480e-adfb-6a19e37618e5}"
ENVIRONMENT_ID="${ENVIRONMENT_ID:-294682c0-50e3-4792-8913-87516a279aca}"
OUT_FILE="${OUT_FILE:-backend/.env.railway}"

check_https_reachability() {
  local host="$1"
  if ! curl -fsSI --max-time 10 "https://${host}" >/dev/null 2>&1; then
    echo "[ERROR] HTTPS verso ${host} non raggiungibile da questo ambiente." >&2
    echo "        Verifica proxy/firewall (es. CONNECT 403) o whitelist dei domini Railway/NPM." >&2
    return 1
  fi
}

if ! command -v railway >/dev/null 2>&1; then
  echo "[ERROR] Railway CLI non trovata. Installa con: npm install -g @railway/cli" >&2
  echo "        Se npm è bloccato dal proxy, abilita accesso a: registry.npmjs.org" >&2
  exit 1
fi

# Fast-fail con messaggio utile quando il problema è rete/proxy
check_https_reachability "railway.com"

if [[ -n "${RAILWAY_TOKEN:-}" ]]; then
  echo "[1/5] Uso autenticazione con RAILWAY_TOKEN (non interattiva)."
else
  echo "[1/5] Verifica login Railway..."
  if ! railway whoami >/dev/null 2>&1; then
    echo "Non risulti autenticato. Avvio login interattivo..."
    railway login
  fi
fi

echo "[2/5] Context progetto"
echo "- project:     $PROJECT_ID"
echo "- service:     $SERVICE_ID"
echo "- environment: $ENVIRONMENT_ID"

echo "[3/5] Link progetto e servizio"
railway link --project "$PROJECT_ID" --service "$SERVICE_ID" --environment "$ENVIRONMENT_ID"

echo "[4/5] Pull variabili in $OUT_FILE"
mkdir -p "$(dirname "$OUT_FILE")"
railway variables --environment "$ENVIRONMENT_ID" > "$OUT_FILE"

echo "[5/5] Done"
echo "- File generato: $OUT_FILE"
echo "- Avvio locale con variabili Railway:"
echo "  set -a; source $OUT_FILE; set +a; cd backend; uvicorn app.main:app --host 0.0.0.0 --port 8000"
