import json
from pathlib import Path

import requests
import time

from analyzer.causal.causal_engine import analyze_causal_chain
from analyzer.cost.cost_model import (
    calculate_resource_cost,
    calculate_cost_increase,
    cost_anomaly_score,
)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

JAEGER_URL = "http://localhost:16686/api/traces"


def capture_trace():
    for attempt in range(10):
        response = requests.get(
            JAEGER_URL,
            params={
                "service": "checkout",
                "operation": "POST /checkout",
                "limit": 20,
            },
            timeout=10,
        )
        response.raise_for_status()
        trace_data = response.json()

        for trace in trace_data.get("data", []):
            services = {
                process.get("serviceName")
                for process in trace.get("processes", {}).values()
                if process.get("serviceName")
            }

            if {"checkout", "inventory", "payment"}.issubset(services):
                (DATA_DIR / "sample-trace.json").write_text(
                    json.dumps({"data": [trace]}, indent=2),
                    encoding="utf-8",
                )
                print(
                    "Captured distributed checkout trace:",
                    trace.get("traceID"),
                    "services=",
                    sorted(services),
                )
                return {"data": [trace]}

        if attempt < 9:
            time.sleep(2)

    raise RuntimeError(
        "No distributed POST /checkout trace containing "
        "checkout, inventory, and payment was found."
    )

def build_causal_chain():
    result = analyze_causal_chain("payment")

    (DATA_DIR / "causal_chain.json").write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    return result


def build_cost_data():
    baseline = {
        "checkout": {"cpu": 20.0, "memory": 256.0, "replicas": 1},
        "inventory": {"cpu": 31.0, "memory": 512.0, "replicas": 1},
        "payment": {"cpu": 17.0, "memory": 256.0, "replicas": 1},
    }

    current = {
        "checkout": {"cpu": 20.0, "memory": 256.0, "replicas": 1},
        "inventory": {"cpu": 92.0, "memory": 512.0, "replicas": 2},
        "payment": {"cpu": 85.0, "memory": 256.0, "replicas": 2},
    }

    services = {}
    total_increase = 0.0

    for service in baseline:
        b = baseline[service]
        c = current[service]

        baseline_cost = calculate_resource_cost(
            b["cpu"],
            b["memory"],
            b["replicas"],
        )

        current_cost = calculate_resource_cost(
            c["cpu"],
            c["memory"],
            c["replicas"],
        )

        increase = calculate_cost_increase(
            baseline_cost,
            current_cost,
        )

        services[service] = {
            "baseline_cost": baseline_cost,
            "current_cost": current_cost,
            "cost_increase": increase,
            "cost_anomaly_score": cost_anomaly_score(
                baseline_cost,
                current_cost,
            ),
        }

        total_increase += increase

    for service, values in services.items():
        values["attribution_share"] = round(
            values["cost_increase"] / total_increase,
            4,
        ) if total_increase > 0 else 0.0

    result = {
        "currency": "USD",
        "model": "resource-based estimated attribution",
        "total_cost_increase": round(total_increase, 6),
        "services": services,
    }

    (DATA_DIR / "cost_data.json").write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    return result


def main():
    print("CAPTURING TELEMETRY...")
    capture_trace()

    print("BUILDING CAUSAL CHAIN...")
    chain = build_causal_chain()

    print("BUILDING COST ATTRIBUTION...")
    cost = build_cost_data()

    print("\n=== PIPELINE COMPLETE ===")
    print(json.dumps({
        "causal_chain": chain,
        "cost": cost,
    }, indent=2))


if __name__ == "__main__":
    main()


