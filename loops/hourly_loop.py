"""Hourly conjecture research pipeline.

Each stage is isolated so model providers, theorem provers and search tools can
be replaced without changing the audit format.
"""

from pathlib import Path
from datetime import datetime, timezone
import json

from agents.generator import generate_candidate
from agents.attacker import attack_candidate
from agents.prover import attempt_proof
from agents.reviewer import review_candidate

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "research" / "reports"


def run_loop():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    candidate = generate_candidate()
    attack = attack_candidate(candidate)
    proof = attempt_proof(candidate, attack)
    review = review_candidate(candidate, attack, proof)

    report = {
        "timestamp": now,
        "candidate": candidate,
        "attack": attack,
        "proof": proof,
        "review": review,
    }

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = REPORTS / f"loop-{now.replace(':', '').replace('-', '')}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run_loop(), indent=2, ensure_ascii=False))
