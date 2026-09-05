"""Command-line interface for geno-dev runtime capabilities."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
from pathlib import Path
import sqlite3
import sys
from typing import Any

from geno_dev.usage import (
    DEFAULT_DATABASE,
    TRIGGERS,
    record_invocation,
    summarize_invocations,
)


def _print_usage_report(report: dict[str, Any]) -> None:
    print(f"{report['skill']} usage")
    print(f"Last {report['days']} days: {report['period_count']}")
    print(f"All time: {report['all_time_count']}")
    print(f"Active days: {report['active_days']}")
    trigger_counts = report["trigger_counts"]
    print(
        "Triggers: "
        f"explicit={trigger_counts['explicit']} "
        f"implicit={trigger_counts['implicit']} "
        f"unknown={trigger_counts['unknown']}"
    )
    if report["daily_counts"]:
        print("Daily:")
        for day, count in report["daily_counts"].items():
            print(f"  {day}: {count}")
    print(f"First: {report['first_invoked_at'] or '-'}")
    print(f"Last: {report['last_invoked_at'] or '-'}")
    print(f"Database: {report['database']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="geno-dev")
    commands = parser.add_subparsers(dest="command", required=True)

    usage = commands.add_parser("usage", help="record and report skill usage")
    usage_commands = usage.add_subparsers(dest="usage_command", required=True)

    record = usage_commands.add_parser("record", help="record one invocation")
    record.add_argument("skill")
    record.add_argument("--trigger", choices=TRIGGERS, default="unknown")
    record.add_argument("--database", type=Path, default=DEFAULT_DATABASE)

    report = usage_commands.add_parser("report", help="summarize invocations")
    report.add_argument("skill")
    report.add_argument("--days", type=int, default=30)
    report.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    report.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.usage_command == "record":
            invocation_id = record_invocation(
                args.database,
                skill_name=args.skill,
                trigger=args.trigger,
            )
            print(f"recorded {args.skill} invocation {invocation_id}")
            return 0

        report = summarize_invocations(
            args.database,
            skill_name=args.skill,
            days=args.days,
        )
    except (OSError, RuntimeError, sqlite3.Error, ValueError) as error:
        print(f"geno-dev: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        _print_usage_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
