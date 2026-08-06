"""Tests for detection rules."""

from datetime import datetime, timedelta

from logalert.detect import bucket_key, detect_all, find_error_spikes
from logalert.parser import LogEntry


def make_entries(level, count, start=None, gap_seconds=10, message="Boom"):
    """Build a list of LogEntry objects for testing."""
    start = start or datetime(2026, 8, 3, 12, 0, 0)
    return [
        LogEntry(start + timedelta(seconds=i * gap_seconds), level, message)
        for i in range(count)
    ]


def test_bucket_key_rounds_down_to_window_start():
    assert bucket_key(datetime(2026, 8, 3, 12, 3, 47)) == datetime(2026, 8, 3, 12, 0)
    assert bucket_key(datetime(2026, 8, 3, 12, 7, 1)) == datetime(2026, 8, 3, 12, 5)


def test_error_spike_detected_when_over_threshold():
    entries = make_entries("ERROR", 20, gap_seconds=5)
    alerts = find_error_spikes(entries, threshold=10)

    assert len(alerts) >= 1
    assert alerts[0].rule == "error_spike"


def test_no_spike_when_errors_are_spread_out():
    entries = make_entries("ERROR", 20, gap_seconds=600)

    assert find_error_spikes(entries, threshold=10) == []


def test_quiet_log_produces_no_alerts():
    entries = make_entries("INFO", 100, gap_seconds=30)

    assert detect_all(entries) == []