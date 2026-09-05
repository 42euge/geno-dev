from pathlib import Path
import tempfile
import unittest

from geno_dev.evals import (
    EvalCase,
    EvalConfig,
    EvalCriterion,
    JudgeCriterion,
    JudgeVerdict,
    SkillEvaluator,
)


class FakeEvalAgent:
    def __init__(self) -> None:
        self.actor_calls: list[dict[str, object]] = []
        self.judge_calls: list[dict[str, object]] = []

    def respond(
        self, *, skill: str, prompt: str, model: str, max_tokens: int
    ) -> str:
        self.actor_calls.append(
            {
                "skill": skill,
                "prompt": prompt,
                "model": model,
                "max_tokens": max_tokens,
            }
        )
        return "Create C1, C2, and C3 with the watcher shared across each."

    def judge(
        self,
        *,
        case: EvalCase,
        response: str,
        model: str,
        max_tokens: int,
    ) -> JudgeVerdict:
        self.judge_calls.append(
            {
                "case": case,
                "response": response,
                "model": model,
                "max_tokens": max_tokens,
            }
        )
        return JudgeVerdict(
            criteria=(
                JudgeCriterion(
                    name="multiple-options",
                    passed=True,
                    evidence="The response names C1, C2, and C3.",
                ),
                JudgeCriterion(
                    name="shared-baseline",
                    passed=True,
                    evidence="The watcher is shared across each option.",
                ),
            ),
            summary="The response preserves branching and the locked watcher.",
        )


class SequencedEvalAgent:
    def __init__(self, outcomes: list[bool]) -> None:
        self.outcomes = outcomes
        self.response_count = 0

    def respond(
        self, *, skill: str, prompt: str, model: str, max_tokens: int
    ) -> str:
        self.response_count += 1
        return f"response {self.response_count}"

    def judge(
        self,
        *,
        case: EvalCase,
        response: str,
        model: str,
        max_tokens: int,
    ) -> JudgeVerdict:
        passed = self.outcomes.pop(0)
        return JudgeVerdict(
            criteria=(
                JudgeCriterion(
                    name=case.criteria[0].name,
                    passed=passed,
                    evidence=f"{response} {'passes' if passed else 'fails'}.",
                ),
            ),
            summary="Sequenced verdict.",
        )


class SkillEvaluatorTests(unittest.TestCase):
    def test_actor_and_judge_produce_computed_pass_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill_path = Path(directory) / "SKILL.md"
            skill_path.write_text("# Branch designs\nAlways offer three options.\n")
            case = EvalCase(
                name="branch after selection",
                prompt="C is closest. Keep the watcher.",
                criteria=(
                    EvalCriterion(
                        name="multiple-options",
                        description="Proposes at least three options.",
                    ),
                    EvalCriterion(
                        name="shared-baseline",
                        description="Carries the watcher into every option.",
                    ),
                ),
            )
            agent = FakeEvalAgent()

            report = SkillEvaluator(agent).evaluate(
                skill_path=skill_path,
                case=case,
                config=EvalConfig(
                    actor_model="claude-sonnet-5",
                    judge_model="claude-sonnet-5",
                ),
            )

        self.assertTrue(report.passed)
        self.assertEqual(report.pass_rate, 1.0)
        self.assertEqual(report.trials[0].score, 1.0)
        self.assertEqual(report.to_dict()["minimum_score"], 1.0)
        self.assertEqual(report.to_dict()["minimum_pass_rate"], 1.0)
        self.assertEqual(report.trials[0].response, "Create C1, C2, and C3 with the watcher shared across each.")
        self.assertEqual(agent.actor_calls[0]["model"], "claude-sonnet-5")
        self.assertEqual(agent.judge_calls[0]["response"], report.trials[0].response)

    def test_multiple_runs_use_aggregate_pass_rate_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill_path = Path(directory) / "SKILL.md"
            skill_path.write_text("# Branch designs\nAlways offer three options.\n")
            case = EvalCase(
                name="branch after selection",
                prompt="C is closest. Keep exploring.",
                criteria=(
                    EvalCriterion(
                        name="multiple-options",
                        description="Proposes at least three options.",
                    ),
                ),
            )
            agent = SequencedEvalAgent([True, False, True])

            report = SkillEvaluator(agent).evaluate(
                skill_path=skill_path,
                case=case,
                config=EvalConfig(
                    actor_model="claude-sonnet-5",
                    judge_model="claude-sonnet-5",
                    runs=3,
                    minimum_pass_rate=0.67,
                ),
            )

        self.assertEqual(len(report.trials), 3)
        self.assertAlmostEqual(report.pass_rate, 2 / 3)
        self.assertFalse(report.passed)


if __name__ == "__main__":
    unittest.main()
