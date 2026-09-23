from datetime import datetime


def temporal_score(event_time, anomaly_time, window_seconds=30):
    if not event_time or not anomaly_time:
        return 0.0

    difference = abs(
        (anomaly_time - event_time).total_seconds()
    )

    if difference > window_seconds:
        return 0.0

    return round(
        1.0 - (difference / window_seconds),
        3
    )
