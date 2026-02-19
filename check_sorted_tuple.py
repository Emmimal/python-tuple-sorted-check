# check_sorted_tuple.py
# Complete code collection from https://emitechlogic.com/check-if-a-tuple-is-sorted-in-python/
# Author: Emmimal Alexander
# Date: February 19, 2026
# Updated: Fixed tuple formatting error in print statements

from itertools import pairwise
import operator
import timeit


# ────────────────────────────────────────────────
# Method 1: all() with zip() — Recommended
# ────────────────────────────────────────────────
def is_sorted_zip(t, strict=False):
    """Non-decreasing (default) or strictly increasing check using zip()."""
    op = operator.lt if strict else operator.le
    return all(op(x, y) for x, y in zip(t, t[1:]))


# ────────────────────────────────────────────────
# Method 2: For Loop — clearest for interviews
# ────────────────────────────────────────────────
def is_sorted_loop(t, strict=False):
    """Index-based loop. Returns False on first violation."""
    op = operator.lt if strict else operator.le
    for i in range(len(t) - 1):
        if not op(t[i], t[i + 1]):
            return False
    return True


# ────────────────────────────────────────────────
# Method 3: all() with range()
# ────────────────────────────────────────────────
def is_sorted_range(t, strict=False):
    """One-liner with index access using range()."""
    op = operator.lt if strict else operator.le
    return all(op(t[i], t[i + 1]) for i in range(len(t) - 1))


# ────────────────────────────────────────────────
# Method 4: itertools.pairwise() — Python 3.10+
# ────────────────────────────────────────────────
def is_sorted_pairwise(t, strict=False):
    """Memory-efficient pairwise iterator (no slice)."""
    op = operator.lt if strict else operator.le
    return all(op(x, y) for x, y in pairwise(t))


# Polyfill for Python < 3.10
def pairwise_polyfill(iterable):
    it = iter(iterable)
    a = next(it, None)
    if a is None:
        return
    for b in it:
        yield a, b
        a = b


def is_sorted_pairwise_polyfill(t, strict=False):
    op = operator.lt if strict else operator.le
    return all(op(x, y) for x, y in pairwise_polyfill(t))


# ────────────────────────────────────────────────
# Method 5: Compare with sorted() — least efficient
# ────────────────────────────────────────────────
def is_sorted_sorted(t, reverse=False):
    """Simple but O(n log n) — use only for small tuples."""
    return t == tuple(sorted(t, reverse=reverse))


# ────────────────────────────────────────────────
# Descending order variants
# ────────────────────────────────────────────────
def is_non_increasing(t):
    return all(x >= y for x, y in zip(t, t[1:]))


def is_strictly_decreasing(t):
    return all(x > y for x, y in zip(t, t[1:]))


# ────────────────────────────────────────────────
# Key-based sorting check (e.g. records by salary)
# ────────────────────────────────────────────────
def is_sorted_by_key(t, key_func, strict=False):
    """Check sorted by a key function or itemgetter."""
    op = operator.lt if strict else operator.le
    return all(op(key_func(x), key_func(y)) for x, y in zip(t, t[1:]))


# Example convenience function
def is_sorted_by_salary(records):
    return is_sorted_by_key(records, operator.itemgetter(2))  # salary at index 2


# ────────────────────────────────────────────────
# Safe version (handles TypeError for mixed types)
# ────────────────────────────────────────────────
def is_sorted_safe(t, strict=False):
    try:
        return is_sorted_zip(t, strict=strict)
    except TypeError:
        return False


# ────────────────────────────────────────────────
# Example usage & test cases
# ────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        (1, 2, 3, 4, 5),
        (1, 3, 2, 4),
        (5, 5, 5),
        (1, 2, 2, 3),
        (),
        (7,),
        (10, 8, 8, 5, 2),
        (10, 8, 5, 2),
    ]

    print("Testing non-decreasing checks:")
    for t in tests:
        print(f"{str(t):<35} → {is_sorted_zip(t)}")

    print("\nTesting strictly increasing:")
    for t in tests:
        print(f"{str(t):<35} → {is_sorted_zip(t, strict=True)}")

    print("\nTesting non-increasing (descending with equals):")
    print(f"{str((10, 8, 8, 5, 2)):<35} → {is_non_increasing((10, 8, 8, 5, 2))}")
    print(f"{str((10, 8, 5, 2)):<35} → {is_non_increasing((10, 8, 5, 2))}")

    # Key-based example
    records = (
        ("Alice", 28, 72000),
        ("Bob",   34, 85000),
        ("Priya", 31, 91000),
    )
    print("\nRecords sorted by salary:", is_sorted_by_salary(records))  # True

    # Benchmark example (large mostly-sorted tuple with one violation)
    print("\nRunning quick benchmark (1 million elements)...")
    base = list(range(1_000_000))
    base[500_000] = 0  # violation in the middle → early exit for good methods
    t_large = tuple(base)

    print("zip method:   ", timeit.timeit(lambda: is_sorted_zip(t_large), number=3))
    print("loop method:  ", timeit.timeit(lambda: is_sorted_loop(t_large), number=3))
    print("sorted method:", timeit.timeit(lambda: is_sorted_sorted(t_large), number=1))  # much slower
