"""Generate synthetic server logs for testing."""

import random
from datetime import datetime, timedelta

INFO_MESSAGES = [
    "User logged in",
    "Request handled",
    "Cache hit",
    "Health check passed",
]

WARN_MESSAGES = [
    "Slow query detected",
    "Retrying connection",
]

ERROR_MESSAGES = [
    "Database connection failed",
    "Timeout contacting service",
]


def format_line(moment, level, message):
    """Turn one event into a log line."""
    stamp = moment.strftime("%Y-%m-%d %H:%M:%S")
    return f"{stamp} {level} {message}"


def pick_message(level):
    """Choose a random message for the given level."""
    pools = {
        "INFO": INFO_MESSAGES,
        "WARN": WARN_MESSAGES,
        "ERROR": ERROR_MESSAGES,
    }
    return random.choice(pools[level])

def generate_normal_events(start, count):
    """Yield mostly-INFO events spread a few seconds apart."""
    moment = start
    for _ in range(count):
        level = random.choices(
            ["INFO", "WARN", "ERROR"],
            weights=[85, 12, 3],
        )[0]
        yield format_line(moment, level, pick_message(level))
        moment += timedelta(seconds=random.randint(1, 20))


def generate_error_burst(start, count):
    """Yield a tight cluster of ERROR lines — the anomaly to detect."""
    moment = start
    for _ in range(count):
        yield format_line(moment, "ERROR", "Database connection failed")
        moment += timedelta(seconds=random.randint(1, 4))


def build_log(seed=42, normal_count=500, burst_count=60):
    """Build a full log: normal traffic with one error burst in the middle."""
    random.seed(seed)
    start = datetime(2026, 8, 3, 9, 0, 0)

    first_half = list(generate_normal_events(start, normal_count // 2))
    burst_start = datetime(2026, 8, 3, 12, 0, 0)
    burst = list(generate_error_burst(burst_start, burst_count))
    second_start = datetime(2026, 8, 3, 13, 0, 0)
    second_half = list(generate_normal_events(second_start, normal_count // 2))

    return first_half + burst + second_half


def write_log(path="data/sample.log", **kwargs):
    """Write the generated log to disk."""
    lines = build_log(**kwargs)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines)


if __name__ == "__main__":
    count = write_log()
    print(f"Wrote {count} lines to data/sample.log")