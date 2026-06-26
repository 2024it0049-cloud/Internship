#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
if [[ "$(uname -s)" == Linux* ]] || [[ "$(uname -s)" == Darwin* ]]; then
  PYTHON="$ROOT/.venv/bin/python"
else
  PYTHON="$ROOT/.venv/Scripts/python.exe"
fi

if [ $# -eq 0 ]; then
  echo "Usage: $0 <script.py|module.name> [args...]" >&2
  exit 1
fi

if [ ! -f "$PYTHON" ]; then
  echo "Virtual environment not found at $ROOT/.venv" >&2
  echo "Run: uv sync   (or python -m venv .venv)" >&2
  exit 1
fi

target="$1"
shift

if [[ "$target" == *.py ]]; then
  exec "$PYTHON" "$target" "$@"
else
  exec "$PYTHON" -m "$target" "$@"
fi
