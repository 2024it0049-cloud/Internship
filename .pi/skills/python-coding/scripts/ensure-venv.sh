#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
if [[ "$(uname -s)" == Linux* ]] || [[ "$(uname -s)" == Darwin* ]]; then
  PYTHON="$ROOT/.venv/bin/python"
else
  PYTHON="$ROOT/.venv/Scripts/python.exe"
fi

if [ -f "$PYTHON" ]; then
  echo "Virtual environment already exists: $ROOT/.venv"
  exit 0
fi

if command -v uv >/dev/null 2>&1 && [ -f "$ROOT/pyproject.toml" ]; then
  echo "Creating environment with uv..."
  (cd "$ROOT" && uv sync)
else
  echo "Creating Python virtual environment..."
  python -m venv "$ROOT/.venv"
fi

echo "Done: $ROOT/.venv"