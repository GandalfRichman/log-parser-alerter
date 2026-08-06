"""Command-line entry point."""

import argparse
import sys
from collections import Counter
from pathlib import Path

from logalert.detect import detect_all
from logalert.parser import parse_file


def build_summary(entries, malformed, alerts, source):
    """Build the alert summary as Markdown text."""
    counts = Counter(e.level for e in entries)
    lines = [
        "# Log Alert Summary",
        "",
        f"**Source:** `{source}`  ",
        f"**Lines parsed:** {len(entries)} ({malformed} malformed)",
        "",
        "## Levels",
        "",
        "| Level | Count |",
        "| --- | --- |",
    ]
    for level in ("INFO", "WARN", "ERROR"):
        lines.append(f"| {level} | {counts[level]} |")

    lines += ["", "## Alerts", ""]
    if not alerts:
        lines.append("No alerts. All clear.")
    else:
        for alert in alerts:
            lines.append(f"- **{alert.rule}** — {alert.detail}")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Parse logs and report alerts.")
    parser.add_argument("path", nargs="?", default="data/sample.log")
    parser.add_argument("-o", "--output", help="write Markdown report to this file")
    args = parser.parse_args()

    try:
        entries, malformed = parse_file(args.path)
    except (FileNotFoundError, IsADirectoryError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2
    except PermissionError:
        print(f"Error: no permission to read {args.path}", file=sys.stderr)
        return 2

    alerts = detect_all(entries)
    report = build_summary(entries, malformed, alerts, args.path)
    print(report)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")

    return 1 if alerts else 0


if __name__ == "__main__":
    sys.exit(main())