#!/usr/bin/env bash
set -euo pipefail

cd backend

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

if command -v uvicorn >/dev/null 2>&1; then
  exec uvicorn app.main:app --host "$HOST" --port "$PORT"
fi

if command -v python >/dev/null 2>&1 && python -c "import uvicorn" >/dev/null 2>&1; then
  exec python -m uvicorn app.main:app --host "$HOST" --port "$PORT"
fi

echo "Errore: uvicorn non trovato. Installa le dipendenze backend prima di avviare il progetto." >&2
echo "Suggerimento: cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
exit 127
