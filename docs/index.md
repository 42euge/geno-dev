# geno-dev

Developer workflow skills for coding agents.

## Installation

```bash
geno-tools install geno-dev
```

## Skills

### `meta-mine-skill-creator`

Mines local Claude Code and Codex session history for recurring successful workflows and places where the user corrected the agent. It produces evidence-backed candidates and does not change the repository until the user selects one.

## Local usage recording

The `geno-dev usage` CLI records skill invocations in a privacy-minimal local
SQLite database so adoption can be measured without storing prompts, paths, or
project data.

See [Getting Started](getting-started.md) for usage and the repository contract.

## Skill evaluations

The `geno-dev eval` CLI replays a scenario against a candidate skill with an
Anthropic-powered actor and independent structured judge. It produces JSON and
process exit statuses suitable for local iteration and CI.

See [Skill evaluations](skill-evals.md) for the case format and execution model.
