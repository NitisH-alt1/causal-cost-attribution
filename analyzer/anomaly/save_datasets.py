import json
from pathlib import Path

baseline = {
    "payment": {
        "error_rate": 0.012,
        "cpu_usage": 17
    },
    "inventory": {
        "error_rate": 0.006,
        "cpu_usage": 31,
        "request_count": 120
    },
    "checkout": {
        "error_rate": 0.005,
        "request_count": 82
    }
}

failure = {
    "payment": {
        "error_rate": 0.85,
        "request_latency_ms": 2500
    },
    "inventory": {
        "error_rate": 0.18,
        "cpu_usage": 92,
        "request_count": 850
    },
    "checkout": {
        "error_rate": 0.12,
        "request_count": 120
    }
}

Path("data/baseline.json").write_text(json.dumps(baseline, indent=2))
Path("data/failure.json").write_text(json.dumps(failure, indent=2))

print("Baseline and failure datasets saved.")
