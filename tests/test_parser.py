"""Tests for log line and file parsing."""

from datetime import datetime

import pytest

from logalert.parser import LogEntry, parse_file, parse_line


def test_parse_line_returns_entry_for_valid_line():
    line = "2026-08-03 10:14:02 ERROR Database connection failed"
    entry = parse_line(line)

    assert isinstance(entry, LogEntry)
    assert entry.timestamp == datetime(2026, 8, 3, 10, 14, 2)
    assert entry.level == "ERROR"
    assert entry.message == "Database connection failed"


def test_parse_line_keeps_spaces_in_message():
    line = "2026-08-03 10:14:02 INFO User 42 logged in from home"
    entry = parse_line(line)

    assert entry.message == "User 42 logged in from home"


@pytest.mark.parametrize(
    "bad_line",
    [
        "not a log line",
        "2026-08-03 10:14:02 BANANA Unknown level",
        "2026-13-45 99:99:99 INFO Impossible date",
        "",
    ],
)
def test_parse_line_returns_none_for_malformed(bad_line):
    assert parse_line(bad_line) is None

def test_parse_file_counts_malformed_lines(tmp_path):
    log = tmp_path / "mixed.log"
    log.write_text(
        "2026-08-03 10:00:00 INFO Started\n"
        "garbage line here\n"
        "2026-08-03 10:00:05 ERROR Boom\n"
        "\n"
        "another bad one\n"
    )

    entries, malformed = parse_file(log)

    assert len(entries) == 2
    assert malformed == 2


def test_parse_file_handles_empty_file(tmp_path):
    log = tmp_path / "empty.log"
    log.write_text("")

    entries, malformed = parse_file(log)

    assert entries == []
    assert malformed == 0


def test_parse_file_raises_when_missing(tmp_path):
    missing = tmp_path / "does_not_exist.log"

    with pytest.raises(FileNotFoundError):
        parse_file(missing)


def test_parse_file_raises_on_directory(tmp_path):
    with pytest.raises(IsADirectoryError):
        parse_file(tmp_path)