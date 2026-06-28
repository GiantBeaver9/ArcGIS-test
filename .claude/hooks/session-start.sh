#!/bin/bash
# SessionStart hook: install dependencies for every package in the monorepo so
# tests (and tools) work in Claude Code on the web sessions.
#
# Synchronous by design: the session waits until deps are installed, avoiding
# races where Claude runs tests before the environment is ready.
set -euo pipefail

# Only run in the remote (Claude Code on the web) environment. Local users
# manage their own virtualenvs / node_modules.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$ROOT"

echo "[session-start] Installing dependencies for ArcGIS monorepo..."

# --- Python packages (editable installs with dev/test extras) ---------------
PY="$(command -v python3 || command -v python)"
echo "[session-start] Using Python: $("$PY" --version 2>&1)"
# Best-effort pip upgrade; ignore failures (e.g. OS-managed pip).
"$PY" -m pip install --upgrade pip >/dev/null 2>&1 || true

for pkg in python rest; do
  if [ -f "packages/$pkg/pyproject.toml" ]; then
    echo "[session-start] pip install -e packages/$pkg[dev]"
    "$PY" -m pip install -e "packages/$pkg[dev]"
  fi
done

# --- JavaScript package -----------------------------------------------------
# npm install (not ci) so the cached container layer can be reused/updated.
if [ -f "packages/js/package.json" ]; then
  echo "[session-start] npm install (packages/js)"
  ( cd packages/js && npm install --no-audit --no-fund )
fi

echo "[session-start] Done."
