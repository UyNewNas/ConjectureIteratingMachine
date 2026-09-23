#!/usr/bin/env python3
"""Finite check of the odd exact-three-almost-prime Goldbach candidate."""

import argparse
from array import array
from math import gcd, isqrt


def omega_table(limit: int) -> bytearray:
    spf = array("I", range(limit + 1))
    for p in range(2, isqrt(limit) + 1):
        if spf[p] == p:
            for m in range(p * p, limit + 1, p):
                if spf[m] == m:
                    spf[m] = p
    omega = bytearray(limit + 1)
    for m in range(2, limit + 1):
        omega[m] = omega[m // spf[m]] + 1
    return omega


def trial_omega(m: int) -> int:
    count = 0
    d = 2
    while d * d <= m:
        while m % d == 0:
            count += 1
            m //= d
        d += 1
    return count + (m > 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=1_000_000)
    parser.add_argument("--coprime-bound", type=int, default=100_000)
    args = parser.parse_args()
    if args.bound < 798 or args.bound % 2:
        parser.error("--bound must be even and at least 798")
    if args.coprime_bound < 0 or args.coprime_bound > args.bound:
        parser.error("--coprime-bound must lie between 0 and --bound")

    omega = omega_table(args.bound)
    for m in range(1, min(args.bound, 10_000) + 1):
        assert omega[m] == trial_omega(m), m

    candidates = [m for m in range(3, args.bound, 2) if omega[m] == 3]
    failures = []
    coprime_failures = []
    examples = {}
    largest_first_summand = (0, None)
    for even in range(6, args.bound + 1, 2):
        pair = None
        coprime_pair = None
        for a in candidates:
            if a > even // 2:
                break
            b = even - a
            if omega[b] == 3:
                if pair is None:
                    pair = (a, b)
                if even <= args.coprime_bound and gcd(a, b) == 1:
                    coprime_pair = (a, b)
                    break
                if even > args.coprime_bound:
                    break
        if pair is None:
            failures.append(even)
        else:
            if pair[0] > largest_first_summand[0]:
                largest_first_summand = (pair[0], even)
            if even in (798, 1000, args.bound):
                examples[even] = pair
        if even <= args.coprime_bound and coprime_pair is None:
            coprime_failures.append(even)

    print(f"Checked even N=6..{args.bound}; trial division cross-check m<=10000")
    print(f"Exact-three failures: count={len(failures)}, last={failures[-1]}")
    print(f"Coprime variant through {args.coprime_bound}: "
          f"count={len(coprime_failures)}, last={coprime_failures[-1] if coprime_failures else None}")
    print(f"Largest first summand of first found pair: {largest_first_summand}")
    print(f"Example pairs: {examples}")
    assert failures[-1] == 796
    assert all(even < 798 for even in failures)


if __name__ == "__main__":
    main()
