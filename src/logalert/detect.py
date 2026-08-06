"""Detect error patterns and anomalies in parsed log entries."""

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import timedelta

#config
BUCKET_MINUTES = 5
ERROR_THRESHOLD = 10
REPEAT_THRESHOLD = 15


@dataclass
class Alert:
    """One detected problem."""
    rule: str
    detail: str
    count: int


def bucket_key(timestamp, minutes=BUCKET_MINUTES):
    """Round a timestamp down to the start of its time bucket."""
    discard = timedelta(
        minutes=timestamp.minute % minutes,
        seconds=timestamp.second,
        microseconds=timestamp.microsecond,
    )
    return timestamp - discard


def count_by_bucket(entries, level="ERROR", minutes=BUCKET_MINUTES):
    """Count entries of one level per time bucket."""
    counts = defaultdict(int)
    for entry in entries:
        if entry.level == level:
            counts[bucket_key(entry.timestamp, minutes)] += 1
    return dict(counts)


def find_error_spikes(entries, threshold=ERROR_THRESHOLD, minutes=BUCKET_MINUTES):
    """Alert on any time bucket exceeding the error threshold."""
    alerts = []
    for bucket, count in sorted(count_by_bucket(entries, "ERROR", minutes).items()):
        if count > threshold:
            alerts.append(
                Alert(
                    rule="error_spike",
                    detail=f"{count} errors in {minutes}min window from {bucket}",
                    count=count,
                )
            )
    return alerts


def find_repeated_messages(entries, threshold=REPEAT_THRESHOLD):
    """Alert on any message repeating more than the threshold."""
    counts = Counter(e.message for e in entries if e.level == "ERROR")
    return [
        Alert(rule="repeated_message", detail=f'"{msg}" seen {n} times', count=n)
        for msg, n in counts.most_common()
        if n > threshold
    ]


def detect_all(entries):
    """Run every detection rule. Return a list of alerts."""
    return find_error_spikes(entries) + find_repeated_messages(entries)