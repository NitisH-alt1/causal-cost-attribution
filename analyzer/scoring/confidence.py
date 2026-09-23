def calculate_confidence(
    temporal_score,
    dependency_score,
    anomaly_score,
    propagation_score
):
    scores = [
        temporal_score,
        dependency_score,
        anomaly_score,
        propagation_score
    ]

    confidence = sum(scores) / len(scores)

    return round(max(0.0, min(1.0, confidence)), 3)
