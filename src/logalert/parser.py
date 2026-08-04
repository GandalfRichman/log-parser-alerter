"""Parse raw log lines into structured records."""

from dataclasses import dataclass
from datetime import datetime

VALID_LEVELS = {"INFO", "WARN", "ERROR"}


@dataclass
class LogEntry:
    """One parsed log line."""
    timestamp: datetime
    level: str
    message: str


def parse_line(line):
    """Parse one log line. Return a LogEntry, or None if malformed."""
    parts = line.strip().split(maxsplit=3)
    if len(parts) < 4:
        return None

    date_part, time_part, level, message = parts
    if level not in VALID_LEVELS:
        return None

    try:
        timestamp = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    return LogEntry(timestamp=timestamp, level=level, message=message)

def parse_file(path):
    """Parse a log file. Return (entries, malformed_count)."""
    entries = []
    malformed = 0

    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            entry = parse_line(line)
            if entry is None:
                malformed += 1
            else:
                entries.append(entry)

    return entries, malformed