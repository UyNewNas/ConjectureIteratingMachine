#!/usr/bin/env python3
"""Finite check of odd composite Liouville-negative square windows."""

from array import array
from math import isqrt
import argparse
import json


def trial_data(n):
    rest = n
    omega = 0
    d = 2
    while d * d <= rest:
        while rest % d == 0:
            omega += 1
            rest //= d
        d += 1
    if rest > 1:
        omega += 1
    return omega, omega > 1


def run(bound):
    limit = (bound + 2) ** 2
    spf = array("I", [0]) * (limit + 1)
    for p in range(2, isqrt(limit) + 1):
        if spf[p] == 0:
            for multiple in range(p * p, limit + 1, p):
                if spf[multiple] == 0:
                    spf[multiple] = p

    liouville = array("b", [0]) * (limit + 1)
    liouville[1] = 1
    for m in range(2, limit + 1):
        p = spf[m] or m
        liouville[m] = -liouville[m // p]

    # Independent trial division checks the two sieve-derived properties.
    for m in range(3, min(limit, 10000) + 1, 2):
        omega, composite = trial_data(m)
        assert liouville[m] == (-1 if omega % 2 else 1)
        assert (spf[m] != 0) == composite

    counts = []
    witnesses = {}
    for n in range(5, bound + 2):
        found = [m for m in range(n * n + 1, (n + 1) ** 2)
                 if m % 2 and spf[m] != 0 and liouville[m] == -1]
        counts.append(len(found))
        if n in (5, 6, 17, 18):
            witnesses[n] = found[:10]

    one_window_failures = [n for n in range(5, bound + 1) if counts[n - 5] == 0]
    two_window_failures = [n for n in range(5, bound + 1)
                           if counts[n - 5] + counts[n - 4] == 0]
    small_primes = (3, 5, 7, 11, 13, 17, 19)
    square_family_failures = []
    for n in range(5, bound + 1):
        covered = False
        for p in small_primes:
            q = max(3, isqrt(n * n // p) + 1)
            if q % 2 == 0:
                q += 1
            if p * q * q < (n + 2) ** 2:
                covered = True
                break
        if not covered:
            square_family_failures.append(n)
    return {
        "n_range": [5, bound],
        "one_window_failures": one_window_failures,
        "two_window_failures": two_window_failures,
        "minimum_two_window_count": min(counts[i] + counts[i + 1]
                                        for i in range(len(counts) - 1)),
        "small_square_family": list(small_primes),
        "small_square_family_failure_count": len(square_family_failures),
        "small_square_family_first_failures": square_family_failures[:12],
        "sample_witnesses": witnesses,
        "independent_trial_division_checked_through": min(limit, 10000),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=3000)
    args = parser.parse_args()
    if args.bound < 18:
        parser.error("bound must be at least 18")
    print(json.dumps(run(args.bound), ensure_ascii=False, indent=2))
