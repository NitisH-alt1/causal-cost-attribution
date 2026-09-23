import json
from pathlib import Path

def calculate_anomaly_scores(baseline, failure):
    scores = {}

    for service, metrics in failure.items():
        scores[service] = {}

        for metric, failure_value in metrics.items():
            baseline_value = baseline.get(service, {}).get(metric)

            if baseline_value is None:
                continue

            if baseline_value == 0:
                score = 1.0 if failure_value > 0 else 0.0
            else:
                score = abs(failure_value - baseline_value) / abs(baseline_value)

            scores[service][metric] = round(min(score, 100.0), 4)

    return scores


if __name__ == "__main__":
    baseline = json.loads(
        Path("data/baseline.json").read_text()
    )

    failure = json.loads(
        Path("data/failure.json").read_text()
    )

    scores = calculate_anomaly_scores(
        baseline,
        failure
    )

    Path("data/anomaly_scores.json").write_text(
        json.dumps(scores, indent=2)
    )

    print("ANOMALY SCORES")
    print("================")

    for service, metrics in scores.items():
        print(f"\n{service}")

        for metric, score in metrics.items():
            print(f"  {metric}: {score}")
