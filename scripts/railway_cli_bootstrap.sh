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

npm_install() {
  local mode="$1"
  shift

  case "$mode" in
    default)
      run npm install -g @railway/cli --fetch-timeout=10000 --fetch-retries=0 "$@"
      ;;
    no_proxy)
      run env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
        -u npm_config_http_proxy -u npm_config_https_proxy \
        npm install -g @railway/cli --fetch-timeout=10000 --fetch-retries=0 "$@"
      ;;
    *)
      err "Unknown install mode: $mode"
      return 2
      ;;
  esac
}

say "== Railway CLI bootstrap =="
if [[ -n "${HTTP_PROXY:-}${HTTPS_PROXY:-}${http_proxy:-}${https_proxy:-}" ]]; then
  say "proxy=detected"
else
  warn "proxy=not-detected"
fi

if has_railway; then
  say "railway-cli=present"
  railway --version || true
else
  say "railway-cli=missing"

  say "[1/4] Tentativo installazione standard npm"
  if npm_install default; then
    say "npm-install=ok"
  else
    warn "Installazione standard fallita (tipicamente E403 su proxy/registry)."

    say "[2/4] Tentativo installazione npm senza proxy"
    if npm_install no_proxy; then
      say "npm-install-no-proxy=ok"
    else
      warn "Installazione senza proxy fallita (rete diretta non raggiungibile o bloccata)."

      say "[3/4] Tentativo installazione via mirror npm"
      if npm_install default --registry "$NPM_REGISTRY_MIRROR"; then
        say "mirror-install=ok"
      else
        err "Installazione CLI fallita anche via mirror ($NPM_REGISTRY_MIRROR)."
        err "Serve un canale di rete autorizzato al download di @railway/cli (proxy allowlist o runner differente)."
        exit 1
      fi
    fi
  fi
fi

say "[4/4] Verifica operativa"
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
