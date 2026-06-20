---
name: python-testing
description: Guidelines for generating and reviewing pytest-based unit tests for Python code.
---

# Python Testing

Use this skill whenever you need to generate, review, or improve Python tests.

Reference: https://docs.pytest.org/en/stable/

## Required framework

- Use **pytest** only. Do not use `unittest` test classes.

## Test style

- Write tests as **top-level functions**, not classes.
- Give each test a **descriptive name** that clearly states the condition being verified, e.g. `test_multiple_of_three_prints_fizz`.
- Include **only one `assert` per test function**.
- Keep tests small, readable, and focused on a single behavior.
- Do not add production code inside test files.

## pytest features

- Use **fixtures** to share setup logic, DRY up helper creation, or inject dependencies (`capsys`, `tmpdir`, etc.).
- Use **pytest.mark.parametrize** when the same logic needs to be verified against multiple inputs.
- Prefer `@pytest.fixture` functions defined in `conftest.py` or the test module itself.
- Use built-in fixtures (`capsys`, `monkeypatch`, `tmpdir`) where appropriate.

## Scope

- Prefer **unit tests** over integration tests unless the user explicitly asks for integration tests.
- Test edge cases explicitly: empty input, negative values, zero, boundaries, single element, maximum expected size.
- Do not test third-party libraries; test only the code under review.

## Assertions

- Use simple, direct assertions: `assert result == expected`.
- When testing console output, capture it with `capsys` and assert on the captured output.
- When testing exceptions, use `with pytest.raises(...):`.

## Running tests

- Tests should be discoverable by `pytest` from the project root.
- Generated tests should pass when run with `pytest -q`.
