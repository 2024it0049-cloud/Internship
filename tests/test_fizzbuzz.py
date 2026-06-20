"""Unit tests for fizzbuzz.py.

These tests verify the console output of the fizzbuzz() function.
"""

import pytest
from fizzbuzz import fizzbuzz


@pytest.fixture
def run_fizzbuzz(capsys):
    """Run fizzbuzz(n) and return the printed lines as a list."""
    def _run(n=100):
        fizzbuzz(n)
        out, _ = capsys.readouterr()
        return out.strip().splitlines()
    return _run


def test_fizzbuzz_default_runs_to_one_hundred(run_fizzbuzz):
    """Default call prints exactly 100 lines."""
    lines = run_fizzbuzz()
    assert len(lines) == 100


@pytest.mark.parametrize("number", [3, 6, 9, 12])
def test_multiple_of_three_prints_fizz(run_fizzbuzz, number):
    """Multiples of 3 should print Fizz."""
    lines = run_fizzbuzz(number)
    assert lines[number - 1] == "Fizz"


@pytest.mark.parametrize("number", [5, 10, 20, 25])
def test_multiple_of_five_prints_buzz(run_fizzbuzz, number):
    """Multiples of 5 should print Buzz."""
    lines = run_fizzbuzz(number)
    assert lines[number - 1] == "Buzz"


@pytest.mark.parametrize("number", [15, 30, 45])
def test_multiple_of_both_three_and_five_prints_fizzbuzz(run_fizzbuzz, number):
    """Multiples of both 3 and 5 should print FizzBuzz."""
    lines = run_fizzbuzz(number)
    assert lines[number - 1] == "FizzBuzz"


@pytest.mark.parametrize(
    "number, expected",
    [
        (1, "1"),
        (2, "2"),
        (4, "4"),
        (7, "7"),
        (11, "11"),
        (13, "13"),
    ],
)
def test_non_multiple_prints_number(run_fizzbuzz, number, expected):
    """Numbers not divisible by 3 or 5 should print the number itself."""
    lines = run_fizzbuzz(number)
    assert lines[number - 1] == expected


@pytest.mark.parametrize(
    "index, expected",
    [
        (2, "Fizz"),
        (4, "Buzz"),
        (14, "FizzBuzz"),
        (0, "1"),
    ],
)
def test_fizzbuzz_first_fifteen_outputs(run_fizzbuzz, index, expected):
    """Specific positions in the first fifteen lines should be correct."""
    lines = run_fizzbuzz(15)
    assert lines[index] == expected
