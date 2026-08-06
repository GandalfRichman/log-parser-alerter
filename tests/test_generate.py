"""Tests for synthetic log generation."""

from logalert.generate import build_log
from logalert.parser import parse_line


def test_build_log_is_reproducible_with_same_seed():
    first = build_log(seed=42, normal_count=50, burst_count=10)
    second = build_log(seed=42, normal_count=50, burst_count=10)

    assert first == second


def test_build_log_differs_with_different_seed():
    a = build_log(seed=1, normal_count=50, burst_count=10)
    b = build_log(seed=2, normal_count=50, burst_count=10)

    assert a != b


def test_every_generated_line_is_parseable():
    lines = build_log(seed=7, normal_count=100, burst_count=20)

    assert all(parse_line(line) is not None for line in lines)


def test_burst_produces_expected_error_count():
    lines = build_log(seed=42, normal_count=0, burst_count=25)

    assert len(lines) == 25
    assert all(" ERROR " in line for line in lines)