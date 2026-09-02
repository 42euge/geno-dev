# Getting Started

## Prerequisites

- [geno-tools](https://github.com/42euge/geno-tools)

## Install

```bash
geno-tools install geno-dev
```

## Current surface

Explicit invocation depends on the agent hosting the session:

| Agent | Syntax | Umbrella example |
|---|---|---|
| Codex | `$skill-name` | `$geno-dev` |
| Claude Code | `/skill-name` | `/geno-dev` |

Invoke `feature-acceptance-test` after implementation when you want to:

- exercise the exact branch or artifact through its real user-facing entry point;
- receive a brief Markdown runbook with actions and expected observations;
- test a shared or hardware environment with explicit safety and cleanup gates.

The skill automatically records its invocation through `geno-dev usage`.

Invoke `iterative-ui-design` when you know the product surface that needs work
but expect to recognize the right design more easily than you can specify it:

Codex:

```text
$iterative-ui-design Show me several browser-reviewable directions for this editor and refine my selection over multiple rounds
```

Claude Code:

```text
/iterative-ui-design Show me several browser-reviewable directions for this editor and refine my selection over multiple rounds
```

The skill keeps mockups isolated from production code and stops at an approved
prototype and decision summary unless implementation is also requested.

Skills can record invocations through the installed CLI:

```bash
geno-dev usage record example-skill --trigger explicit
geno-dev usage report example-skill --days 30
```

The local database at `~/.geno/skill-usage.sqlite3` stores only skill name, UTC
timestamp, and whether the skill was invoked explicitly, selected
automatically, or could not determine its trigger.

Invoke `meta-mine-skill-creator` when you want to analyze local Claude Code and Codex sessions for:

- repeatable workflows that should become skills;
- repeated corrections that should patch a skill or repository rule;
- broader agent or product improvements that do not belong in a skill.

Target a pattern you already remember:

Codex:

```text
$meta-mine-skill-creator I repeatedly ask agents to test features through the real user path
```

Claude Code:

```text
/meta-mine-skill-creator I repeatedly ask agents to test features through the real user path
```

Or leave it empty to find the next best candidate:

Codex:

```text
$meta-mine-skill-creator
```

Claude Code:

```text
/meta-mine-skill-creator
```

Mining is read-only. The skill asks which candidates to materialize before editing the repository.

New capabilities belong in independent `skills/<skill-name>/SKILL.md` leaf directories and should be added to the umbrella skill and repository documentation.
