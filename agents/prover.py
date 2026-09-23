"""Proof search stage."""


def attempt_proof(candidate, attack):
    return {
        "status": "not_attempted",
        "methods": [
            "elementary construction",
            "known theorem composition",
            "lemma reduction",
        ],
    }
