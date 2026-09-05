"""Behavioral evaluation contracts for agent skills."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Protocol


CASE_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class EvalCriterion:
    name: str
    description: str


@dataclass(frozen=True)
class EvalCase:
    name: str
    prompt: str
    criteria: tuple[EvalCriterion, ...]
    minimum_score: float = 1.0
    schema_version: int = CASE_SCHEMA_VERSION

    def validation_report(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "criteria_count": len(self.criteria),
            "minimum_score": self.minimum_score,
        }


@dataclass(frozen=True)
class JudgeCriterion:
    name: str
    passed: bool
    evidence: str


@dataclass(frozen=True)
class JudgeVerdict:
    criteria: tuple[JudgeCriterion, ...]
    summary: str


class EvalAgent(Protocol):
    def respond(
        self, *, skill: str, prompt: str, model: str, max_tokens: int
    ) -> str: ...

    def judge(
        self,
        *,
        case: EvalCase,
        response: str,
        model: str,
        max_tokens: int,
    ) -> JudgeVerdict: ...


@dataclass(frozen=True)
class EvalConfig:
    actor_model: str
    judge_model: str
    runs: int = 1
    minimum_pass_rate: float = 1.0
    actor_max_tokens: int = 2048
    judge_max_tokens: int = 1024

    def __post_init__(self) -> None:
        if not self.actor_model.strip() or not self.judge_model.strip():
            raise ValueError("actor and judge models must not be empty")
        if self.runs <= 0:
            raise ValueError("runs must be positive")
        if not 0 < self.minimum_pass_rate <= 1:
            raise ValueError("minimum_pass_rate must be greater than 0 and at most 1")
        if self.actor_max_tokens <= 0 or self.judge_max_tokens <= 0:
            raise ValueError("max token limits must be positive")


@dataclass(frozen=True)
class EvalTrial:
    number: int
    response: str
    criteria: tuple[JudgeCriterion, ...]
    score: float
    passed: bool
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "number": self.number,
            "response": self.response,
            "criteria": [
                {
                    "name": criterion.name,
                    "passed": criterion.passed,
                    "evidence": criterion.evidence,
                }
                for criterion in self.criteria
            ],
            "score": self.score,
            "passed": self.passed,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class EvalReport:
    case_name: str
    skill_path: Path
    actor_model: str
    judge_model: str
    trials: tuple[EvalTrial, ...]
    minimum_score: float
    minimum_pass_rate: float
    pass_rate: float
    passed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "case": self.case_name,
            "skill": str(self.skill_path),
            "actor_model": self.actor_model,
            "judge_model": self.judge_model,
            "minimum_score": self.minimum_score,
            "minimum_pass_rate": self.minimum_pass_rate,
            "trials": [trial.to_dict() for trial in self.trials],
            "pass_rate": self.pass_rate,
            "passed": self.passed,
        }


class SkillEvaluator:
    """Evaluate a skill through an actor/judge agent seam."""

    def __init__(self, agent: EvalAgent) -> None:
        self._agent = agent

    def evaluate(
        self, *, skill_path: Path, case: EvalCase, config: EvalConfig
    ) -> EvalReport:
        skill = skill_path.read_text()
        if not skill.strip():
            raise ValueError("skill file must not be empty")

        expected_names = tuple(criterion.name for criterion in case.criteria)
        trials: list[EvalTrial] = []
        for number in range(1, config.runs + 1):
            response = self._agent.respond(
                skill=skill,
                prompt=case.prompt,
                model=config.actor_model,
                max_tokens=config.actor_max_tokens,
            )
            if not response.strip():
                raise RuntimeError("actor returned an empty response")
            verdict = self._agent.judge(
                case=case,
                response=response,
                model=config.judge_model,
                max_tokens=config.judge_max_tokens,
            )
            by_name = {criterion.name: criterion for criterion in verdict.criteria}
            if len(by_name) != len(verdict.criteria) or set(by_name) != set(
                expected_names
            ):
                raise RuntimeError(
                    "judge criteria must match the evaluation case exactly"
                )
            ordered = tuple(by_name[name] for name in expected_names)
            score = sum(criterion.passed for criterion in ordered) / len(ordered)
            trials.append(
                EvalTrial(
                    number=number,
                    response=response,
                    criteria=ordered,
                    score=score,
                    passed=score >= case.minimum_score,
                    summary=verdict.summary,
                )
            )

        pass_rate = sum(trial.passed for trial in trials) / len(trials)
        return EvalReport(
            case_name=case.name,
            skill_path=skill_path,
            actor_model=config.actor_model,
            judge_model=config.judge_model,
            trials=tuple(trials),
            minimum_score=case.minimum_score,
            minimum_pass_rate=config.minimum_pass_rate,
            pass_rate=pass_rate,
            passed=pass_rate >= config.minimum_pass_rate,
        )


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def load_eval_case(path: Path) -> EvalCase:
    """Load and validate one versioned JSON evaluation case."""
    try:
        raw = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error.msg}") from error
    if not isinstance(raw, dict):
        raise ValueError("evaluation case must be a JSON object")
    if raw.get("schema_version") != CASE_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version must be {CASE_SCHEMA_VERSION}"
        )

    raw_criteria = raw.get("criteria")
    if not isinstance(raw_criteria, list) or not raw_criteria:
        raise ValueError("criteria must be a non-empty array")
    criteria: list[EvalCriterion] = []
    seen_names: set[str] = set()
    for index, item in enumerate(raw_criteria):
        if not isinstance(item, dict):
            raise ValueError(f"criteria[{index}] must be an object")
        name = _required_text(item.get("name"), f"criteria[{index}].name")
        if name in seen_names:
            raise ValueError(f"duplicate criterion name: {name}")
        seen_names.add(name)
        criteria.append(
            EvalCriterion(
                name=name,
                description=_required_text(
                    item.get("description"), f"criteria[{index}].description"
                ),
            )
        )

    minimum_score = raw.get("minimum_score", 1.0)
    if (
        not isinstance(minimum_score, (int, float))
        or isinstance(minimum_score, bool)
        or not 0 < float(minimum_score) <= 1
    ):
        raise ValueError("minimum_score must be greater than 0 and at most 1")

    return EvalCase(
        name=_required_text(raw.get("name"), "name"),
        prompt=_required_text(raw.get("prompt"), "prompt"),
        criteria=tuple(criteria),
        minimum_score=float(minimum_score),
    )
