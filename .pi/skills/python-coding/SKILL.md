---
name: python-coding
description: Write, run, lint, and test Python code for this project. Use whenever you need to create, edit, execute, or validate a Python file.
---

# Python Coding

This skill helps you write idiomatic Python in the current project. It assumes a virtual environment managed with `uv` (and a fallback to a plain `.venv`).

## Setup

From the project root:

```bash
# Ensure dependencies are installed and a virtual environment exists
./scripts/ensure-venv.sh
if [ -f uv.lock ] || [ -f pyproject.toml ]; then
  uv sync
fi
```

## Run a Python file or module

```bash
# Run a file
./scripts/run.sh src/my_module.py arg1 arg2

# Run a module
./scripts/run.sh my_package.module arg1
```

If no module or file is specified, the script prints usage.

## Lint and format

```bash
./scripts/check.sh
```

This runs the project's `ruff` linter and format checker from the virtual environment.

## Run tests

```bash
./scripts/test.sh [pytest-args]
```

This runs `pytest` from the virtual environment.

## Conventions

- Target Python version follows `.python-version` / `requires-python` in `pyproject.toml`.
- Use type hints for public functions and classes.
- Write docstrings in the Google style for non-trivial modules/functions.
- Keep top-level side effects minimal; guard executable code with `if __name__ == "__main__":`.
- Use `pathlib` over raw `os.path` manipulation when possible.
- Format code with `ruff format` and lint with `ruff check` before marking a task complete.
- When adding dependencies, update `pyproject.toml` and run `uv sync` (or `pip install -e .` if not using `uv`).
