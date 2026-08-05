"""Command-line entry point."""

import sys
from collections import Counter

from logalert.parser import parse_file


def summarize(entries, malformed):
    """Print a basic breakdown of the parsed log."""
    counts = Counter(entry.level for entry in entries)
    print(f"Parsed:    {len(entries)} lines")
    print(f"Malformed: {malformed} lines")
    for level in ("INFO", "WARN", "ERROR"):
        print(f"  {level:5} {counts[level]}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/sample.log"

    try:
        entries, malformed = parse_file(path)
    except (FileNotFoundError, IsADirectoryError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2
    except PermissionError:
        print(f"Error: no permission to read {path}", file=sys.stderr)
        return 2

    if not entries:
        print(f"Warning: no valid log entries found in {path}", file=sys.stderr)

    summarize(entries, malformed)
    return 0


if __name__ == "__main__":
    sys.exit(main())