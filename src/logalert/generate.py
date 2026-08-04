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