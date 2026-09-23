def propagation_score(
    upstream_anomaly,
    downstream_anomaly
):
    if upstream_anomaly and downstream_anomaly:
        return 1.0

    if upstream_anomaly or downstream_anomaly:
        return 0.5

    return 0.0
