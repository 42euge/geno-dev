"""Anthropic Messages API adapter for skill evaluations."""

from __future__ import annotations

import json
from typing import Any

from geno_dev.evals import EvalCase, JudgeCriterion, JudgeVerdict


class AnthropicEvalAgent:
    def __init__(self, client: Any) -> None:
        self._client = client

    def _request(self, stage: str, **kwargs: Any) -> Any:
        try:
            return self._client.messages.create(**kwargs)
        except Exception as error:
            raise RuntimeError(
                f"Anthropic {stage} request failed: {error}"
            ) from error

    def respond(
        self, *, skill: str, prompt: str, model: str, max_tokens: int
    ) -> str:
        message = self._request(
            "actor",
            model=model,
            max_tokens=max_tokens,
            system=(
                "You are the candidate agent in a behavioral skill evaluation. "
                "Follow the supplied skill instructions exactly and respond to "
                "the user scenario as you would in a real session. Do not discuss "
                "the evaluation itself.\n\n<skill>\n"
                f"{skill}\n"
                "</skill>"
            ),
            messages=[{"role": "user", "content": prompt}],
        )
        text = "\n".join(
            block.text for block in message.content if block.type == "text"
        ).strip()
        if not text:
            raise RuntimeError("Anthropic actor returned no text")
        return text

    def judge(
        self,
        *,
        case: EvalCase,
        response: str,
        model: str,
        max_tokens: int,
    ) -> JudgeVerdict:
        criterion_names = [criterion.name for criterion in case.criteria]
        tool = {
            "name": "submit_skill_evaluation",
            "description": (
                "Submit the complete evidence-based verdict for every named "
                "criterion. Judge only the candidate response shown in the "
                "request. Do not infer unshown actions or give credit without "
                "specific evidence."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "criteria": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "enum": criterion_names,
                                },
                                "passed": {"type": "boolean"},
                                "evidence": {"type": "string"},
                            },
                            "required": ["name", "passed", "evidence"],
                            "additionalProperties": False,
                        },
                        "minItems": len(criterion_names),
                        "maxItems": len(criterion_names),
                    },
                    "summary": {"type": "string"},
                },
                "required": ["criteria", "summary"],
                "additionalProperties": False,
            },
        }
        message = self._request(
            "judge",
            model=model,
            max_tokens=max_tokens,
            system=(
                "You are an independent behavioral evaluator. Assess each "
                "criterion against the candidate response, cite concise direct "
                "evidence, and submit exactly one structured verdict."
            ),
            messages=[
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "case": case.name,
                            "scenario": case.prompt,
                            "criteria": [
                                {
                                    "name": criterion.name,
                                    "description": criterion.description,
                                }
                                for criterion in case.criteria
                            ],
                            "candidate_response": response,
                        },
                        sort_keys=True,
                    ),
                }
            ],
            tools=[tool],
            tool_choice={"type": "tool", "name": tool["name"]},
        )
        blocks = [
            block
            for block in message.content
            if block.type == "tool_use" and block.name == tool["name"]
        ]
        if len(blocks) != 1 or not isinstance(blocks[0].input, dict):
            raise RuntimeError("Anthropic judge returned no structured verdict")
        payload = blocks[0].input
        raw_criteria = payload.get("criteria")
        summary = payload.get("summary")
        if not isinstance(raw_criteria, list) or not isinstance(summary, str):
            raise RuntimeError("Anthropic judge returned an invalid verdict")
        criteria: list[JudgeCriterion] = []
        for item in raw_criteria:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("name"), str)
                or not isinstance(item.get("passed"), bool)
                or not isinstance(item.get("evidence"), str)
            ):
                raise RuntimeError("Anthropic judge returned an invalid criterion")
            criteria.append(
                JudgeCriterion(
                    name=item["name"],
                    passed=item["passed"],
                    evidence=item["evidence"],
                )
            )
        return JudgeVerdict(criteria=tuple(criteria), summary=summary)
