"""Command-line interface for geno-dev runtime capabilities."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
import json
from pathlib import Path
import sqlite3
import sys
from typing import Any

from geno_dev.evals import EvalAgent, EvalConfig, SkillEvaluator, load_eval_case
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

    evaluate = commands.add_parser("eval", help="evaluate skill behavior")
    eval_commands = evaluate.add_subparsers(dest="eval_command", required=True)

    validate = eval_commands.add_parser(
        "validate", help="validate an evaluation case"
    )
    validate.add_argument("case", type=Path)
    validate.add_argument("--json", action="store_true")

    run = eval_commands.add_parser("run", help="run an actor/judge evaluation")
    run.add_argument("case", type=Path)
    run.add_argument("--skill", type=Path, required=True)
    run.add_argument("--model", default="claude-sonnet-5")
    run.add_argument("--judge-model")
    run.add_argument("--runs", type=int, default=1)
    run.add_argument("--minimum-pass-rate", type=float, default=1.0)
    run.add_argument("--actor-max-tokens", type=int, default=2048)
    run.add_argument("--judge-max-tokens", type=int, default=1024)
    run.add_argument("--json", action="store_true")
    return parser


def _run_usage(args: argparse.Namespace) -> int:
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


def _default_eval_agent() -> EvalAgent:
    from anthropic import Anthropic

    from geno_dev.anthropic_eval import AnthropicEvalAgent

    return AnthropicEvalAgent(Anthropic())


def _print_eval_report(report: dict[str, Any]) -> None:
    status = "PASS" if report["passed"] else "FAIL"
    print(f"{status}: {report['case']}")
    print(f"Pass rate: {report['pass_rate']:.0%}")
    for trial in report["trials"]:
        trial_status = "PASS" if trial["passed"] else "FAIL"
        print(f"Trial {trial['number']}: {trial_status} ({trial['score']:.0%})")
        print(f"  {trial['summary']}")


def _run_eval(
    args: argparse.Namespace,
    eval_agent_factory: Callable[[], EvalAgent],
) -> int:
    try:
        case = load_eval_case(args.case)
        if args.eval_command == "run":
            config = EvalConfig(
                actor_model=args.model,
                judge_model=args.judge_model or args.model,
                runs=args.runs,
                minimum_pass_rate=args.minimum_pass_rate,
                actor_max_tokens=args.actor_max_tokens,
                judge_max_tokens=args.judge_max_tokens,
            )
            report = SkillEvaluator(eval_agent_factory()).evaluate(
                skill_path=args.skill,
                case=case,
                config=config,
            )
    except (OSError, ValueError) as error:
        print(f"geno-dev: {error}", file=sys.stderr)
        return 2
    except RuntimeError as error:
        print(f"geno-dev: evaluation failed: {error}", file=sys.stderr)
        return 2

    if args.eval_command == "validate":
        validation = case.validation_report()
        if args.json:
            print(json.dumps(validation, sort_keys=True))
        else:
            print(f"valid: {case.name}")
            print(f"criteria: {len(case.criteria)}")
            print(f"minimum score: {case.minimum_score:.2f}")
        return 0

    serialized = report.to_dict()
    if args.json:
        print(json.dumps(serialized, sort_keys=True))
    else:
        _print_eval_report(serialized)
    return 0 if report.passed else 1


def main(
    argv: Sequence[str] | None = None,
    *,
    eval_agent_factory: Callable[[], EvalAgent] | None = None,
) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "usage":
        return _run_usage(args)
    return _run_eval(args, eval_agent_factory or _default_eval_agent)


if __name__ == "__main__":
    raise SystemExit(main())
