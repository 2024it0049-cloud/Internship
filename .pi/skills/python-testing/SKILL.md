---
name: python-testing
description: Write pytest-based unit tests for Python projects using test functions, fixtures, parametrization, single asserts, and descriptive names. Use whenever creating, reviewing, or refactoring tests.
---

# Python Testing

## Setup

From the project root:

```bash
# Ensure pytest is installed in the virtual environment
if command -v uv >/dev/null 2>&1 && [ -f pyproject.toml ]; then
  uv add --dev pytest
elif [ -f .venv/Scripts/python.exe ]; then
  .venv/Scripts/python.exe -m pip install pytest
else
  python -m pip install pytest
fi
```

## Run tests

```bash
# Run the full test suite
./scripts/run-tests.sh

# Run a specific file or directory
pytest tests/test_module.py
pytest tests/

# Run a specific test by name
pytest -k test_returns_zero_for_empty_input
```

## Rules

### Use test functions, not test classes

```python
# Good
def test_returns_zero_when_no_items():
    assert total([]) == 0

# Avoid
class TestTotal:
    def test_returns_zero(self):
        assert total([]) == 0
```

### Use fixtures for shared setup

Place reusable setup in `conftest.py` or in the test file.

```python
import pytest

@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Ada"}

def test_user_name_is_set(sample_user):
    assert sample_user["name"] == "Ada"
```

Prefer built-ins like `tmp_path`, `monkeypatch`, and `capsys` over manual cleanup.

### Use parametrization for multiple inputs

```python
@pytest.mark.parametrize("n,expected", [
    (1, 1),
    (5, 120),
    (0, 1),
])
def test_factorial_returns_expected_value(n, expected):
    assert factorial(n) == expected
```

### Only one assert per test

Each test should verify one logical condition.

```python
# Good
def test_greet_includes_name():
    assert "Ada" in greet("Ada")

def test_greet_starts_with_hello():
    assert greet("Ada").startswith("Hello")

# Avoid
def test_greet():
    result = greet("Ada")
    assert "Ada" in result
    assert result.startswith("Hello")
    assert len(result) > 0
```

If you need to assert multiple things about a single complex object, consider using `pytest.approx` or a dataclass comparison so there is still one logical assertion.

### Test names should explain the condition being tested

Name the test after the behavior and scenario, not the function under test.

```python
# Good
def test_raises_value_error_for_negative_timeout():
    with pytest.raises(ValueError):
        connect(timeout=-1)

def test_returns_empty_list_when_database_has_no_users():
    assert list_users() == []

# Avoid
def test_connect_raises():
    ...

def test_list_users():
    ...
```

## Project layout

```
project/
├── src/
│   └── my_package/
│       └── calculator.py
└── tests/
    ├── conftest.py
    └── test_calculator.py
```

Test files must be named `test_*.py` or `*_test.py` so pytest discovers them.

## Minimal example

`tests/test_calculator.py`:

```python
import pytest
from my_package.calculator import add, divide

@pytest.fixture
def positive_operands():
    return {"a": 2, "b": 3}

@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),
    (-1, 1, 0),
    (10, 5, 15),
])
def test_add_returns_sum_of_operands(a, b, expected):
    assert add(a, b) == expected

def test_add_returns_result_from_fixture(positive_operands):
    assert add(positive_operands["a"], positive_operands["b"]) == 5

def test_divide_raises_zero_division_error_for_zero_divisor():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```
