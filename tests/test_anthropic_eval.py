from types import SimpleNamespace
import unittest

from geno_dev.anthropic_eval import AnthropicEvalAgent
from geno_dev.evals import EvalCase, EvalCriterion


class FakeMessages:
    def __init__(self, responses: list[object]) -> None:
        self.responses = responses
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> object:
        self.calls.append(kwargs)
        return self.responses.pop(0)


class FakeAnthropicClient:
    def __init__(self, responses: list[object]) -> None:
        self.messages = FakeMessages(responses)


class FailingMessages:
    def create(self, **kwargs: object) -> object:
        raise ConnectionError("network unavailable")


class FailingAnthropicClient:
    def __init__(self) -> None:
        self.messages = FailingMessages()


class AnthropicEvalAgentTests(unittest.TestCase):
    def test_actor_applies_skill_to_scenario(self) -> None:
        client = FakeAnthropicClient(
            [
                SimpleNamespace(
                    content=[
                        SimpleNamespace(type="text", text="Create C1, C2, and C3.")
                    ]
                )
            ]
        )
        agent = AnthropicEvalAgent(client)

        response = agent.respond(
            skill="# UI exploration\nAlways branch.",
            prompt="C is closest. Keep exploring.",
            model="claude-sonnet-5",
            max_tokens=1200,
        )

        self.assertEqual(response, "Create C1, C2, and C3.")
        call = client.messages.calls[0]
        self.assertEqual(call["model"], "claude-sonnet-5")
        self.assertEqual(call["max_tokens"], 1200)
        self.assertIn("Always branch", str(call["system"]))
        self.assertEqual(
            call["messages"],
            [{"role": "user", "content": "C is closest. Keep exploring."}],
        )

    def test_judge_returns_forced_structured_verdict(self) -> None:
        client = FakeAnthropicClient(
            [
                SimpleNamespace(
                    content=[
                        SimpleNamespace(
                            type="tool_use",
                            name="submit_skill_evaluation",
                            input={
                                "criteria": [
                                    {
                                        "name": "multiple-options",
                                        "passed": True,
                                        "evidence": "Names C1, C2, and C3.",
                                    }
                                ],
                                "summary": "The response branches correctly.",
                            },
                        )
                    ]
                )
            ]
        )
        agent = AnthropicEvalAgent(client)
        case = EvalCase(
            name="branch after selection",
            prompt="C is closest.",
            criteria=(
                EvalCriterion(
                    name="multiple-options",
                    description="Proposes at least three next-round options.",
                ),
            ),
        )

        verdict = agent.judge(
            case=case,
            response="Create C1, C2, and C3.",
            model="claude-sonnet-5",
            max_tokens=800,
        )

        self.assertTrue(verdict.criteria[0].passed)
        self.assertEqual(verdict.criteria[0].name, "multiple-options")
        call = client.messages.calls[0]
        self.assertEqual(
            call["tool_choice"],
            {"type": "tool", "name": "submit_skill_evaluation"},
        )
        self.assertEqual(call["tools"][0]["name"], "submit_skill_evaluation")

    def test_sdk_errors_become_evaluation_runtime_errors(self) -> None:
        agent = AnthropicEvalAgent(FailingAnthropicClient())

        with self.assertRaisesRegex(RuntimeError, "Anthropic actor request failed"):
            agent.respond(
                skill="# Explore",
                prompt="Show options.",
                model="claude-sonnet-5",
                max_tokens=800,
            )


if __name__ == "__main__":
    unittest.main()
