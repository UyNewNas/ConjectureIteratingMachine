"""Counterexample search stage."""


def attack_candidate(candidate):
    return {
        "status": "not_run",
        "candidate": candidate.get("title"),
        "checks": [
            "small brute force",
            "boundary cases",
            "known theorem coverage",
        ],
    }
