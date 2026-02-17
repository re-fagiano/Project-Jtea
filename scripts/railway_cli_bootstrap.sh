#!/usr/bin/env bash
set -euo pipefail

# Bootstrap Railway CLI in constrained environments.
# Tries multiple install strategies and verifies authentication prerequisites.
# Usage:
#   bash scripts/railway_cli_bootstrap.sh
#   DRY_RUN=1 bash scripts/railway_cli_bootstrap.sh
#   NPM_REGISTRY_MIRROR=https://registry.npmmirror.com bash scripts/railway_cli_bootstrap.sh

DRY_RUN="${DRY_RUN:-0}"
NPM_REGISTRY_MIRROR="${NPM_REGISTRY_MIRROR:-https://registry.npmmirror.com}"

say() { printf '%s\n' "$*"; }
warn() { printf '[WARN] %s\n' "$*" >&2; }
err() { printf '[ERROR] %s\n' "$*" >&2; }

run() {
  if [[ "$DRY_RUN" == "1" ]]; then
    say "[DRY-RUN] $*"
    return 0
  fi
  "$@"
}

has_railway() {
  command -v railway >/dev/null 2>&1
}

say "== Railway CLI bootstrap =="

if has_railway; then
  say "railway-cli=present"
  railway --version || true
else
  say "railway-cli=missing"

  say "[1/3] Tentativo installazione standard npm"
  if run npm install -g @railway/cli; then
    say "npm-install=ok"
  else
    warn "Installazione standard fallita (tipicamente E403 su registry aziendale)."

    say "[2/3] Tentativo installazione via mirror npm"
    if run npm install -g @railway/cli --registry "$NPM_REGISTRY_MIRROR"; then
      say "mirror-install=ok"
    else
      err "Installazione CLI fallita anche via mirror ($NPM_REGISTRY_MIRROR)."
      err "Configura un registry npm consentito o installa la CLI in una macchina/runner con accesso pieno."
      exit 1
    fi
  fi
fi

say "[3/3] Verifica operativa"
if [[ "$DRY_RUN" == "1" ]]; then
  say "[DRY-RUN] verifica finale saltata"
  exit 0
fi

if ! has_railway; then
  err "Railway CLI ancora non disponibile nel PATH dopo installazione."
  exit 2
fi
railway --version

if [[ -n "${RAILWAY_TOKEN:-}" ]]; then
  say "RAILWAY_TOKEN=set"
  if run railway whoami >/dev/null 2>&1; then
    say "auth=ok (token)"
  else
    warn "RAILWAY_TOKEN presente ma non valido/non autorizzato."
  fi
else
  warn "RAILWAY_TOKEN non impostato. In shell non interattiva, imposta un token per poter modificare Railway."
fi

say "Bootstrap completato."
