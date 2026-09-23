def calculate_resource_cost(
    cpu_usage: float,
    memory_usage: float,
    replicas: int,
    cost_per_cpu_unit: float = 0.01,
    cost_per_memory_unit: float = 0.005,
    cost_per_replica: float = 0.02,
) -> float:
    cpu_cost = max(0.0, cpu_usage) * cost_per_cpu_unit
    memory_cost = max(0.0, memory_usage) * cost_per_memory_unit
    replica_cost = max(0, replicas) * cost_per_replica

    return round(cpu_cost + memory_cost + replica_cost, 6)


def calculate_cost_increase(
    baseline_cost: float,
    current_cost: float,
) -> float:
    if baseline_cost <= 0:
        return 0.0

    return round(
        max(0.0, current_cost - baseline_cost),
        6,
    )


def cost_anomaly_score(
    baseline_cost: float,
    current_cost: float,
) -> float:
    if baseline_cost <= 0:
        return 0.0

    increase = (current_cost - baseline_cost) / baseline_cost

    return round(
        max(0.0, min(1.0, increase)),
        3,
    )
