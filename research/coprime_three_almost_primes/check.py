#!/usr/bin/env python3
"""Finite check of the coprime odd E_3 square-window conjecture."""

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


def coprime_pair(xs: list[int]) -> tuple[int, int] | None:
    for i, a in enumerate(xs):
        for b in xs[i + 1:]:
            if gcd(a, b) == 1:
                return a, b
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=3000)
    args = parser.parse_args()
    if args.bound < 23:
        parser.error("--bound must be at least 23")

    omega = omega_table((args.bound + 1) ** 2)
    for m in range(1, min(len(omega), 10001)):
        assert omega[m] == trial_omega(m), m

    failures = []
    least_count = (10**20, None)
    examples = {}
    for n in range(2, args.bound + 1):
        xs = [m for m in range(n * n + 1, (n + 1) ** 2)
              if m & 1 and omega[m] == 3]
        pair = coprime_pair(xs)
        if pair is None:
            failures.append(n)
        if n >= 23 and len(xs) < least_count[0]:
            least_count = (len(xs), n)
        if n in (23, args.bound):
            examples[n] = pair

    print(f"Checked n=2..{args.bound}; trial division cross-check m<=10000")
    print(f"Failures: {failures}")
    print(f"Least number of odd Omega=3 candidates for n>=23: {least_count}")
    print(f"Example coprime pairs: {examples}")
    assert all(n < 23 for n in failures)


if __name__ == "__main__":
    main()
