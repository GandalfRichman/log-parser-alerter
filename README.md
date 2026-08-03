# Log Parser & Alerter

## Project brief
Server logs are high-volume and nobody reads them, so failures are noticed late.
This tool solves that by turning raw logs into a short, human-readable warning.
It consumes synthetic plain-text server logs (`data/sample.log`) in the format
`TIMESTAMP LEVEL MESSAGE`, parses each line into structured records, and applies
threshold and rate rules to detect error spikes and anomalous patterns.
The output is an alert summary printed to stdout (and written as a Markdown
report) listing which rules fired, the counts involved, and the time window
affected. Stretch goal: run on a schedule via GitHub Actions and alert only
when a threshold is breached.

## Status
In development — see the [v1.0 milestone](../../milestone/1).

## Quickstart
```bash
uv sync
uv run python -m logalert data/sample.log
```
