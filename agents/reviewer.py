"""Research evaluation stage."""


def review_candidate(candidate, attack, proof):
    return {
        "classification": "unreviewed",
        "scores": {
            "difficulty": None,
            "novelty": None,
            "depth": None,
        },
        "rule": "No proof does not automatically imply hard conjecture.",
    }
