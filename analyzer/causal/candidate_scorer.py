import json
from pathlib import Path

DEPENDENCIES = [
    ("checkout", "inventory"),
    ("inventory", "payment")
]

def load_json(path):
    return json.loads(Path(path).read_text())

def normalize_score(score):
    return score / (1.0 + score)

def build_candidates(anomalies):
    candidates = []

    for parent, child in DEPENDENCIES:
        parent_metrics = anomalies.get(parent, {})
        child_metrics = anomalies.get(child, {})

        parent_score = max(
            [normalize_score(v) for v in parent_metrics.values()],
            default=0.0
        )

        child_score = max(
            [normalize_score(v) for v in child_metrics.values()],
            default=0.0
        )

        candidates.append({
            "cause_service": child,
            "affected_service": parent,
            "dependency": f"{parent} -> {child}",
            "anomaly_strength": round(child_score, 4),
            "propagation_strength": round(parent_score, 4),
            "causal_candidate_score": round(
                (child_score * 0.6) + (parent_score * 0.4),
                4
            )
        })

    return candidates


if __name__ == "__main__":
    anomalies = load_json("data/anomaly_scores.json")

    candidates = build_candidates(anomalies)

    candidates.sort(
        key=lambda x: x["causal_candidate_score"],
        reverse=True
    )

    Path("data/causal_candidates.json").write_text(
        json.dumps(candidates, indent=2)
    )

    print("CAUSAL CANDIDATES")
    print("=================")

    for candidate in candidates:
        print()
        print(f"Dependency: {candidate['dependency']}")
        print(f"Anomaly strength: {candidate['anomaly_strength']}")
        print(f"Propagation strength: {candidate['propagation_strength']}")
        print(
            f"Causal candidate score: "
            f"{candidate['causal_candidate_score']}"
        )
