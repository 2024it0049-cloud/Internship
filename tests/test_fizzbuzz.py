import pytest

from vidgen.fizzbuzz import fizzbuzz


@pytest.fixture
def run_fizzbuzz(capsys):
    """Return a helper that runs fizzbuzz(n) and yields its output lines."""

    def _run(n: int = 100):
        fizzbuzz(n)
        captured = capsys.readouterr()
        return captured.out.strip().splitlines()

    return _run


@pytest.mark.parametrize("n", [1, 3, 5, 15, 100])
def test_outputs_exactly_n_lines(n, run_fizzbuzz):
    assert len(run_fizzbuzz(n)) == n


def test_defaults_to_one_hundred_lines(run_fizzbuzz):
    assert len(run_fizzbuzz()) == 100


@pytest.mark.parametrize(
    "n,expected_last",
    [
        (1, "1"),
        (3, "Fizz"),
        (5, "Buzz"),
        (7, "7"),
        (15, "FizzBuzz"),
        (30, "FizzBuzz"),
    ],
)
def test_last_line_matches_expected_value(n, expected_last, run_fizzbuzz):
    assert run_fizzbuzz(n)[-1] == expected_last


@pytest.mark.parametrize(
    "n,expected_sequence",
    [
        (
            15,
            [
                "1",
                "2",
                "Fizz",
                "4",
                "Buzz",
                "Fizz",
                "7",
                "8",
                "Fizz",
                "Buzz",
                "11",
                "Fizz",
                "13",
                "14",
                "FizzBuzz",
            ],
        ),
    ],
)
def test_full_sequence_matches_expected_values(n, expected_sequence, run_fizzbuzz):
    assert run_fizzbuzz(n) == expected_sequence
