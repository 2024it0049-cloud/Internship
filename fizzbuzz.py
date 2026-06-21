"""Configurable multiples-to-word generator using stream addition.

This module replaces the original hardcoded FizzBuzz implementation with a
lazy, generator-based design. Each configured (multiple, word) pair is
treated as an infinite stream; the final sequence is the element-wise
concatenation (addition) of those streams.
"""

from __future__ import annotations

from itertools import count, islice
from typing import Iterable, Iterator, Tuple


Mapping = Tuple[int, str]


def _validate_mappings(mappings: Iterable[Mapping]) -> list[Mapping]:
    """Validate and freeze the user-supplied mappings.

    Each mapping must be a pair of (positive integer, string). The order of
    the input iterable is preserved so that stream addition reflects the
    user's intent.
    """
    validated: list[Mapping] = []
    for index, item in enumerate(mappings, start=1):
        if not (isinstance(item, tuple) and len(item) == 2):
            raise ValueError(
                f"Mapping at position {index} must be a (multiple, word) tuple, "
                f"got {type(item).__name__}"
            )
        multiple, word = item
        if not isinstance(multiple, int) or isinstance(multiple, bool):
            raise ValueError(
                f"Multiple at position {index} must be an integer, "
                f"got {type(multiple).__name__}"
            )
        if multiple <= 0:
            raise ValueError(
                f"Multiple at position {index} must be positive, got {multiple}"
            )
        if not isinstance(word, str):
            raise ValueError(
                f"Word at position {index} must be a string, got {type(word).__name__}"
            )
        validated.append((multiple, word))
    return validated


def _mapping_stream(multiple: int, word: str) -> Iterator[str]:
    """Yield a word stream for a single mapping.

    At each integer starting from 1, yield ``word`` when the integer is
    divisible by ``multiple``; otherwise yield the empty string.
    """
    for n in count(1):
        yield word if n % multiple == 0 else ""


def word_sequence(mappings: Iterable[Mapping]) -> Iterator[str]:
    """Yield the multiples-to-word sequence as a lazy stream.

    For every positive integer starting at 1, the value is the concatenation
    of all words whose multiple divides the integer. Concatenation follows the
    order in which mappings were supplied. If no word matches, the integer
    itself (as a string) is yielded.

    Args:
        mappings: An iterable of ``(multiple, word)`` pairs.

    Yields:
        The next string in the sequence.

    Raises:
        ValueError: If a mapping is malformed, its multiple is not a positive
            integer, or its word is not a string.
    """
    ordered = _validate_mappings(mappings)

    if not ordered:
        # No mappings -> stream of natural numbers as strings.
        for n in count(1):
            yield str(n)
        return

    streams = [_mapping_stream(multiple, word) for multiple, word in ordered]

    for n, parts in enumerate(zip(*streams), start=1):
        result = "".join(parts)
        yield result if result else str(n)


def print_sequence(mappings: Iterable[Mapping], n: int = 100) -> None:
    """Print the first ``n`` values of the configured sequence."""
    for value in islice(word_sequence(mappings), n):
        print(value)


def fizzbuzz(n: int = 100) -> None:
    """Print the classic FizzBuzz sequence from 1 to ``n``.

    This is a backward-compatible wrapper around ``print_sequence`` using the
    traditional mappings ``3 -> "Fizz"`` and ``5 -> "Buzz"``.
    """
    print_sequence([(3, "Fizz"), (5, "Buzz")], n)
