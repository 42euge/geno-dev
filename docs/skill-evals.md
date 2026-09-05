# Skill evaluations

`geno-dev eval` replays a behavioral scenario against a `SKILL.md` and returns
a machine-readable pass or fail result. It is designed for corrections such as
“the agent refined one option when the skill should have branched again.”

## How it works

Each run makes two independent Anthropic Messages API calls:

1. The **actor** receives the candidate skill as instructions and responds to
   the case prompt as it would in a real session.
2. The **judge** receives the case, named criteria, and actor response. It must
   submit one schema-constrained tool call with pass/fail evidence for every
   criterion.

The engine—not either model—computes the criterion score, trial result,
aggregate pass rate, and process exit status.

This is a decision-trace evaluator. It does not provide a shell, browser, or
credentials to the actor. Put the relevant prior-turn context directly in the
case prompt, and evaluate the next decision before spending time on artifacts.

## Case format

Cases are versioned JSON files:

```json
{
  "schema_version": 1,
  "name": "branch after a non-final selection",
  "prompt": "You created A, B, and C. The user selects C and gives deltas.",
  "criteria": [
    {
      "name": "multiple-options",
      "description": "The next artifact set contains at least three options."
    }
  ],
  "minimum_score": 1.0
}
```

Criterion names must be unique. `minimum_score` is the fraction of criteria
that each trial must pass and defaults to `1.0`.

Validate a case without an API key:

```bash
geno-dev eval validate docs/examples/branch-after-selection.eval.json --json
```

## Run an evaluation

Set an Anthropic API key, then pass the skill and case to the CLI:

```bash
export ANTHROPIC_API_KEY=...
geno-dev eval run docs/examples/branch-after-selection.eval.json \
  --skill path/to/SKILL.md \
  --model claude-sonnet-5 \
  --runs 3 \
  --minimum-pass-rate 0.67 \
  --json
```

The actor model defaults to `claude-sonnet-5`. The judge uses the same model
unless `--judge-model` is supplied. Token ceilings are configurable with
`--actor-max-tokens` and `--judge-max-tokens`.

Exit statuses:

| Status | Meaning |
|---|---|
| `0` | The aggregate pass rate met the threshold. |
| `1` | The evaluation ran, but behavior missed the threshold. |
| `2` | The case, skill, configuration, credentials, or API call failed. |

JSON is written to stdout, so CI can archive it or compare results without a
second reporting format.

## Privacy and cost

Live runs send the full candidate skill, case prompt, criteria, and actor
response to Anthropic. Do not put credentials, private transcripts, personal
data, or proprietary code in cases unless that use is authorized. Each trial
makes one actor call and one judge call, so use `eval validate` and a single
trial while authoring before increasing `--runs`.

The engine never writes the API key or evaluation inputs to its own storage.
Redirected JSON output is controlled by the caller.

See the official [Anthropic Python SDK documentation](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python)
and [tool-use documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools).
