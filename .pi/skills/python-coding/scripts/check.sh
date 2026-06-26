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
  echo "Run: uv sync   (or python -m venv .venv)" >&2
  exit 1
fi

cd "$ROOT"

if ! "$PYTHON" -m ruff --version >/dev/null 2>&1; then
  echo "ruff not installed in the virtual environment." >&2
  echo "Install with: uv add --dev ruff   (or pip install ruff)" >&2
  exit 1
fi

echo "==> ruff check"
"$PYTHON" -m ruff check .

echo "==> ruff format --check"
"$PYTHON" -m ruff format --check .
