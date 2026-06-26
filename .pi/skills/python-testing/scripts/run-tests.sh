#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
if [[ "$(uname -s)" == Linux* ]] || [[ "$(uname -s)" == Darwin* ]]; then
  PYTHON="$ROOT/.venv/bin/python"
else
  PYTHON="$ROOT/.venv/Scripts/python.exe"
fi

if [ ! -f "$PYTHON" ]; then
  echo "Virtual environment not found at $ROOT/.venv" >&2
  echo "Create one with: python -m venv .venv" >&2
  exit 1
fi

if ! "$PYTHON" -m pytest --version >/dev/null 2>&1; then
  echo "pytest is not installed in the virtual environment." >&2
  echo "Install with: uv add --dev pytest   (or pip install pytest)" >&2
  exit 1
fi

cd "$ROOT"
exec "$PYTHON" -m pytest "$@"
