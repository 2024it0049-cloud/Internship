"""Tests for the generic multiples-to-word generator."""

from itertools import islice

import pytest

from fizzbuzz import word_sequence


@pytest.fixture
def first_n():
    """Return the first ``n`` values of a configured word sequence."""

    def _first(mappings, n):
        return list(islice(word_sequence(mappings), n))

    return _first


class TestSingleMapping:
    """Behavior with exactly one (multiple, word) pair."""

    @pytest.mark.parametrize(
        "number, expected",
        [
            (2, "Boom"),
            (4, "Boom"),
            (6, "Boom"),
        ],
    )
    def test_multiple_of_two_replaced_with_word(self, first_n, number, expected):
        """Every multiple of 2 yields the configured word."""
        result = first_n([(2, "Boom")], 6)
        assert result[number - 1] == expected

    @pytest.mark.parametrize(
        "number, expected",
        [
            (1, "1"),
            (3, "3"),
            (5, "5"),
        ],
    )
    def test_non_multiple_yields_number_string(self, first_n, number, expected):
        """Non-multiples yield the integer as a string."""
        result = first_n([(2, "Boom")], 6)
        assert result[number - 1] == expected


class TestMultipleMappings:
    """Behavior with more than one mapping."""

    def test_two_mappings_concatenate_in_input_order(self, first_n):
        """Words concatenate according to the order mappings were supplied."""
        result = first_n([(2, "Boom"), (7, "Baz")], 14)
        assert result[13] == "BoomBaz"

    def test_reversing_mappings_reverses_concatenation(self, first_n):
        """Same numbers but reversed input order produce reversed output."""
        result = first_n([(7, "Baz"), (2, "Boom")], 14)
        assert result[13] == "BazBoom"

    def test_overlapping_multiples_concatenate_in_order(self, first_n):
        """A number divisible by several multiples concatenates all words."""
        result = first_n([(2, "Boom"), (3, "Bam"), (5, "Bing")], 30)
        assert result[29] == "BoomBamBing"

    def test_example_sequence_from_requirement(self, first_n):
        """The exact sample from the requirement is reproduced."""
        result = first_n([(2, "Boom"), (7, "Baz"), (9, "Bam")], 21)
        assert result == [
            "1",
            "Boom",
            "3",
            "Boom",
            "5",
            "Boom",
            "Baz",
            "Boom",
            "Bam",
            "Boom",
            "11",
            "Boom",
            "13",
            "BoomBaz",
            "15",
            "Boom",
            "17",
            "BoomBam",
            "19",
            "Boom",
            "Baz",
        ]


class TestEmptyAndLazyBehavior:
    """Edge cases around empty configuration and infinite generation."""

    def test_empty_mappings_yields_plain_numbers(self, first_n):
        """With no mappings, the sequence is just natural numbers as strings."""
        result = first_n([], 5)
        assert result == ["1", "2", "3", "4", "5"]

    def test_sequence_is_lazy_and_unbounded(self, first_n):
        """The generator can produce values far beyond any reasonable limit."""
        result = first_n([(2, "Boom")], 1_000)
        assert result[999] == "Boom"


class TestInvalidInput:
    """Validation rules for malformed mappings."""

    def test_zero_multiple_raises_value_error(self):
        """A multiple of zero is not allowed."""
        with pytest.raises(ValueError, match="must be positive"):
            next(word_sequence([(0, "Boom")]))

    def test_negative_multiple_raises_value_error(self):
        """Negative multiples are not allowed."""
        with pytest.raises(ValueError, match="must be positive"):
            next(word_sequence([(-2, "Boom")]))

    def test_non_integer_multiple_raises_value_error(self):
        """Non-integer multiples are not allowed."""
        with pytest.raises(ValueError, match="must be an integer"):
            next(word_sequence([("two", "Boom")]))

    def test_non_string_word_raises_value_error(self):
        """Words must be strings."""
        with pytest.raises(ValueError, match="must be a string"):
            next(word_sequence([(2, 123)]))

    def test_non_tuple_mapping_raises_value_error(self):
        """Each mapping must be a two-element tuple."""
        with pytest.raises(ValueError, match=r"must be a \(multiple, word\) tuple"):
            next(word_sequence([2, "Boom"]))  # type: ignore[arg-type]
