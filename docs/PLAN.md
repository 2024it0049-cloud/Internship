# multiples-to-word Generator: Implementation Plan

## Step 1: Current Design Analysis

The repository currently contains a single-file, imperative FizzBuzz implementation:

- `fizzbuzz.py` hardcodes the pairs `3 -> "Fizz"` and `5 -> "Buzz"`.
- It prints directly to standard output.
- It supports only a fixed stop value `n`.
- The test file captures printed output and verifies a few hardcoded cases.

There is no separation between configuration (which multiples map to which words), the
lazy sequence generation, and the side effect of printing. The new requirement needs
an arbitrary, user-supplied list of `(multiple, word)` pairs while preserving input
order and supporting lazy, unbounded generation.

## Step 2: Core Concepts

### What are Python generators?

A Python generator is a function that uses `yield` to return one value at a time while
pausing its local state. On the next iteration, execution resumes immediately after the
last `yield`. This makes generators memory-efficient for large or even infinite
sequences, because they produce values lazily rather than building the whole sequence
up front.

Example relevant to this problem:

```python
def integers(start=1):
    n = start
    while True:
        yield n
        n += 1
```

Calling `integers()` returns a generator object that yields 1, 2, 3, … on demand.

### How can generators implement streams?

A *stream* is a lazily evaluated sequence of values, often conceptually infinite.
A generator is the natural Python implementation of a stream: each call to `next()`
consumes the next element of the stream. In this project, every configured
`(multiple, word)` pair defines a stream that emits either the word (when the current
integer is divisible by the multiple) or an empty string (otherwise).

Example stream for `2 -> "Boom"`:

```text
index:  1     2      3     4      5     6      7     8
value: ""  "Boom"  ""  "Boom"  ""  "Boom"  ""  "Boom"
```

### What does "addition of streams" mean?

Given two or more streams, *addition of streams* means taking the next element from
each stream and combining them with an associative operation. With numeric streams the
operation is ordinary addition; with string streams the natural operation is
concatenation. Formally, if `S1, S2, ...` are streams, then:

```text
(S1 + S2)[i] = S1[i] combined-with S2[i]
```

For our problem, "combined-with" is string concatenation. The concatenation order is
determined by the order of the streams, which in turn is determined by the order of
the user-supplied mappings.

### Applying addition of streams to this problem

1. For each mapping `(multiple, word)`, create a generator/stream that emits `""` at
   every index and `word` only when the index is divisible by `multiple`.
2. Align all streams so that the *i-th* `next()` call on each stream corresponds to
   the same integer `i`.
3. At each step, concatenate the values from all streams.
4. If the concatenated result is empty, fall back to the string representation of the
   current integer; otherwise yield the concatenated word(s).

This naturally satisfies the ordering requirement: because the streams are created in
the order the user provided the mappings, the concatenation produced by `zip(*streams)`
will follow that same order.

## Step 3: Implementation Plan

### File layout

```text
vidgen/
├── docs/
│   └── PLAN.md               # this document
├── fizzbuzz.py               # refactored into a configurable generator module
├── main.py                   # unchanged entry point
├── tests/
│   ├── test_fizzbuzz.py      # existing tests, kept passing for default behavior
│   └── test_multiples_to_word.py  # new tests for the generic generator
└── pyproject.toml
```

### API design

`fizzbuzz.py` will be refactored to expose:

- `word_sequence(mappings)` — generator that yields the configured sequence for all
  positive integers starting at 1.
- `print_sequence(mappings, n=100)` — convenience helper that prints the first `n`
  values of `word_sequence`.
- `fizzbuzz(n=100)` — backward-compatible wrapper that prints the classic FizzBuzz
  sequence using `[(3, "Fizz"), (5, "Buzz")]`.

`mappings` is an iterable of `(multiple, word)` tuples. Validation rules:

- `multiple` must be a positive integer (`> 0`).
- `word` must be a string.
- The iterable is converted to a list to preserve order and allow repeated iteration.

Invalid input raises `ValueError` with a clear message.

### Algorithm

```text
validate mappings -> list of tuples
if mappings is empty:
    yield str(1), str(2), str(3), ...
else:
    create one generator per mapping (each generator tracks its own index)
    for each tuple of values from zip(*streams):
        concatenated = join non-empty values in stream order
        yield concatenated if concatenated else str(current_index)
```

The `zip(*streams)` expression is the literal "addition of streams": it pulls the next
element from every stream at the same logical index and returns them as a tuple ready
for combination.

### Test plan

Use `pytest`, test functions only, fixtures, parametrization, and one assert per test.

Existing `test_fizzbuzz.py` tests will remain valid because the default `fizzbuzz(n)`
behavior is unchanged.

New `test_multiples_to_word.py` will cover:

1. Single mapping.
2. Multiple mappings with non-overlapping multiples.
3. Overlapping multiples and concatenation order.
4. Reversing input order changes concatenation order for the same number.
5. Empty mappings produce plain numbers.
6. Invalid multiple values (zero, negative, non-integer).
7. Invalid word values (non-string).
8. Infinite/lazy behavior via `itertools.islice`.

## Step 4: Verification

After implementation, run:

```bash
python -m pytest -q
```

All tests should pass.
