from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from geno_dev.cli import main
from geno_dev.evals import EvalCase, JudgeCriterion, JudgeVerdict


class PassingEvalAgent:
    def respond(
        self, *, skill: str, prompt: str, model: str, max_tokens: int
    ) -> str:
        return "Create C1, C2, and C3."

    def judge(
        self,
        *,
        case: EvalCase,
        response: str,
        model: str,
        max_tokens: int,
    ) -> JudgeVerdict:
        return JudgeVerdict(
            criteria=tuple(
                JudgeCriterion(
                    name=criterion.name,
                    passed=True,
                    evidence="The response names three branches.",
                )
                for criterion in case.criteria
            ),
            summary="All criteria pass.",
        )


class FailingEvalAgent(PassingEvalAgent):
    def judge(
        self,
        *,
        case: EvalCase,
        response: str,
        model: str,
        max_tokens: int,
    ) -> JudgeVerdict:
        return JudgeVerdict(
            criteria=tuple(
                JudgeCriterion(
                    name=criterion.name,
                    passed=False,
                    evidence="The response offers only one direction.",
                )
                for criterion in case.criteria
            ),
            summary="The branching criterion fails.",
        )


class SkillEvalCliTests(unittest.TestCase):
    def test_validate_reports_normalized_case(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            case_path = Path(directory) / "branching.json"
            case_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "name": "branch after selection",
                        "prompt": "C is closest. Keep the watcher and continue.",
                        "criteria": [
                            {
                                "name": "multiple-options",
                                "description": "Proposes at least three next-round options.",
                            },
                            {
                                "name": "shared-baseline",
                                "description": "Carries the watcher into every option.",
                            },
                        ],
                    }
                )
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "geno_dev.cli",
                    "eval",
                    "validate",
                    str(case_path),
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["name"], "branch after selection")
        self.assertEqual(report["criteria_count"], 2)
        self.assertEqual(report["minimum_score"], 1.0)

    def test_run_emits_json_report_and_pass_exit_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_path = root / "SKILL.md"
            skill_path.write_text("# Explore\nAlways create branches.\n")
            case_path = root / "branching.json"
            case_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "name": "branch after selection",
                        "prompt": "C is closest. Keep exploring.",
                        "criteria": [
                            {
                                "name": "multiple-options",
                                "description": "Proposes at least three options.",
                            }
                        ],
                    }
                )
            )
            output = io.StringIO()

            with redirect_stdout(output):
                exit_status = main(
                    [
                        "eval",
                        "run",
                        str(case_path),
                        "--skill",
                        str(skill_path),
                        "--model",
                        "claude-sonnet-5",
                        "--json",
                    ],
                    eval_agent_factory=PassingEvalAgent,
                )

        self.assertEqual(exit_status, 0)
        report = json.loads(output.getvalue())
        self.assertTrue(report["passed"])
        self.assertEqual(report["pass_rate"], 1.0)
        self.assertEqual(report["trials"][0]["score"], 1.0)

    def test_run_returns_one_for_behavioral_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_path = root / "SKILL.md"
            skill_path.write_text("# Explore\nAlways create branches.\n")
            case_path = root / "branching.json"
            case_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "name": "branch after selection",
                        "prompt": "C is closest. Keep exploring.",
                        "criteria": [
                            {
                                "name": "multiple-options",
                                "description": "Proposes at least three options.",
                            }
                        ],
                    }
                )
            )
            output = io.StringIO()

            with redirect_stdout(output):
                exit_status = main(
                    [
                        "eval",
                        "run",
                        str(case_path),
                        "--skill",
                        str(skill_path),
                        "--json",
                    ],
                    eval_agent_factory=FailingEvalAgent,
                )

        self.assertEqual(exit_status, 1)
        report = json.loads(output.getvalue())
        self.assertFalse(report["passed"])
        self.assertEqual(report["pass_rate"], 0.0)

    def test_run_returns_two_for_invalid_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_path = root / "SKILL.md"
            skill_path.write_text("# Explore\nAlways create branches.\n")
            case_path = root / "branching.json"
            case_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "name": "branch after selection",
                        "prompt": "C is closest. Keep exploring.",
                        "criteria": [
                            {
                                "name": "multiple-options",
                                "description": "Proposes at least three options.",
                            }
                        ],
                    }
                )
            )
            errors = io.StringIO()

            with redirect_stderr(errors):
                exit_status = main(
                    [
                        "eval",
                        "run",
                        str(case_path),
                        "--skill",
                        str(skill_path),
                        "--runs",
                        "0",
                    ],
                    eval_agent_factory=PassingEvalAgent,
                )

        self.assertEqual(exit_status, 2)
        self.assertIn("runs must be positive", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
