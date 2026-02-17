#!/usr/bin/env bash
set -euo pipefail

# Railway diagnostics for Codex/local shells.
# Helps identify why Railway commands fail in CI/Codespaces/containers.

PROJECT_ID="${PROJECT_ID:-e9c06cf5-a20b-440f-92c5-a165ff996232}"
SERVICE_ID="${SERVICE_ID:-be554fa7-7c1c-480e-adfb-6a19e37618e5}"
ENVIRONMENT_ID="${ENVIRONMENT_ID:-294682c0-50e3-4792-8913-87516a279aca}"

say() { printf '%s\n' "$*"; }
warn() { printf '[WARN] %s\n' "$*" >&2; }
err() { printf '[ERROR] %s\n' "$*" >&2; }

say "== Railway Doctor =="
say "project=$PROJECT_ID"
say "service=$SERVICE_ID"
say "environment=$ENVIRONMENT_ID"

say ""; say "[1/8] Git branch + script version"
current_branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"
say "branch=$current_branch"
if [[ -f scripts/railway_codex_setup.sh ]]; then
  if rg -n "\[1/5\]" scripts/railway_codex_setup.sh >/dev/null 2>&1; then
    say "setup-script-version=latest"
  else
    warn "setup-script-version=legacy (non latest). Pull/merge latest branch before continuing."
  fi
else
  err "scripts/railway_codex_setup.sh missing"
  exit 1
fi

say ""; say "[2/8] CLI availability"
if ! command -v railway >/dev/null 2>&1; then
  err "Railway CLI not found. Install: npm install -g @railway/cli"
  exit 2
fi
railway --version || true

say ""; say "[3/8] Network reachability"
if ! curl -fsSI --max-time 10 https://railway.com >/dev/null 2>&1; then
  err "Cannot reach https://railway.com from this environment."
  exit 3
fi
if ! curl -fsSI --max-time 10 https://registry.npmjs.org/@railway%2fcli >/dev/null 2>&1; then
  warn "Cannot reach npm registry endpoint for @railway/cli (may affect install/update)."
fi
say "network=ok"

say ""; say "[4/8] Token sanity"
if [[ -n "${RAILWAY_TOKEN:-}" ]]; then
  if railway whoami >/dev/null 2>&1; then
    say "token=valid"
  else
    err "RAILWAY_TOKEN is set but invalid/unauthorized."
    err "Hint: unset RAILWAY_TOKEN to use interactive login, or regenerate a valid token."
    exit 4
  fi
else
  warn "RAILWAY_TOKEN not set (this is fine if interactive login works)."
fi

say ""; say "[5/8] Auth check"
if railway whoami >/dev/null 2>&1; then
  say "auth=ok"
else
  warn "Not logged in. Starting interactive login..."
  railway login
fi

say ""; say "[6/8] Link check"
if railway link --project "$PROJECT_ID" --service "$SERVICE_ID" --environment "$ENVIRONMENT_ID" >/dev/null 2>&1; then
  say "link=ok"
else
  warn "Could not link using IDs directly. Falling back to interactive railway link..."
  railway link
fi

say ""; say "[7/8] Variables pull test"
tmp_file="$(mktemp)"
if railway variables --environment "$ENVIRONMENT_ID" > "$tmp_file" 2>/dev/null; then
  lines="$(wc -l < "$tmp_file" | tr -d ' ')"
  say "variables=ok lines=$lines"
else
  err "Failed to read variables for environment ID=$ENVIRONMENT_ID"
  rm -f "$tmp_file"
  exit 5
fi
rm -f "$tmp_file"

say ""; say "[8/8] Status"
railway status || warn "railway status failed (CLI/version-specific)."
say ""; say "Diagnosis complete."
