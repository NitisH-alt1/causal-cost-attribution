import time
import random
from datetime import datetime

SERVICES = ["checkout", "inventory", "payment"]

def generate_metric(service, metric, value):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "service": service,
        "metric": metric,
        "value": value
    }

def generate_normal_metrics():
    return [
        generate_metric("checkout", "request_count", random.randint(80, 120)),
        generate_metric("inventory", "request_count", random.randint(80, 120)),
        generate_metric("payment", "request_count", random.randint(80, 120)),
        generate_metric("checkout", "error_rate", random.uniform(0.0, 0.02)),
        generate_metric("inventory", "error_rate", random.uniform(0.0, 0.02)),
        generate_metric("payment", "error_rate", random.uniform(0.0, 0.02)),
        generate_metric("inventory", "cpu_usage", random.uniform(20, 45)),
        generate_metric("payment", "cpu_usage", random.uniform(10, 30))
    ]

if __name__ == "__main__":
    print("Generating normal baseline metrics...")
    metrics = generate_normal_metrics()

    for metric in metrics:
        print(metric)
