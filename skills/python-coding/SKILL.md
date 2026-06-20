---
name: python-coding
description: Guidelines for writing, refactoring, explaining, and reviewing Python code in a clean, production-ready style.
---

# Python Coding

Use this skill for any task that involves Python source code.

## Core principles

- Write clear, readable, idiomatic Python 3 code.
- Follow PEP 8 for naming, spacing, line length, and imports.
- Prefer explicit over implicit. Avoid clever one-liners.
- Add docstrings to public modules, classes, and functions.
- Keep functions small and focused on a single responsibility.
- Use type hints where they improve clarity, but do not force them if they hurt readability.

## Code style

- Use `snake_case` for functions and variables, `PascalCase` for classes, `UPPER_CASE` for constants.
- Use list/dict comprehensions only when they make the code shorter and clearer.
- Avoid mutable default arguments (`def f(x=[])` is a bug).
- Prefer f-strings for string formatting.
- Group imports: stdlib first, third-party next, local last, separated by blank lines.
- Run `ruff` or `flake8` style checks when available.

## Refactoring

- When refactoring, preserve existing behavior.
- Extract helper functions to remove duplication.
- Rename confusing variables/functions to descriptive names.
- Add or update tests after refactoring.

## Explanation

- Explain code in simple language, focusing on intent and data flow.
- Mention any assumptions, edge cases, or trade-offs.
- Provide short examples if it helps.

## Production quality

- Handle edge cases (empty input, negative values, None, etc.).
- Raise appropriate exceptions with clear messages.
- Avoid silent failures.
- Prefer exceptions over returning special sentinel values.
