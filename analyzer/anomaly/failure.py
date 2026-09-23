import random
from datetime import datetime

def generate_failure_metrics():
    timestamp = datetime.utcnow().isoformat()

    return [
        {"timestamp": timestamp, "service": "payment", "metric": "error_rate", "value": 0.85},
        {"timestamp": timestamp, "service": "payment", "metric": "request_latency_ms", "value": 2500},
        {"timestamp": timestamp, "service": "inventory", "metric": "request_count", "value": 850},
        {"timestamp": timestamp, "service": "inventory", "metric": "cpu_usage", "value": 92},
        {"timestamp": timestamp, "service": "inventory", "metric": "error_rate", "value": 0.18},
        {"timestamp": timestamp, "service": "checkout", "metric": "request_count", "value": 120},
        {"timestamp": timestamp, "service": "checkout", "metric": "error_rate", "value": 0.12}
    ]

if __name__ == "__main__":
    print("Generating failure scenario metrics...")
    metrics = generate_failure_metrics()

    for metric in metrics:
        print(metric)
