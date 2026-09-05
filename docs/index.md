# geno-dev

Developer workflow skills for coding agents.

## Installation

```bash
geno-tools install geno-dev
```

## Skills

### `feature-acceptance-test`

Validates the exact feature branch or artifact through the UI, CLI, hardware,
or workflow a user will actually operate. It can run the acceptance path when
authorized and always writes a concise Markdown runbook the user can execute
independently.

### `meta-mine-skill-creator`

Mines local Claude Code and Codex session history for recurring successful workflows and places where the user corrected the agent. It produces evidence-backed candidates and does not change the repository until the user selects one.

Pass a remembered pattern to test it against session evidence, or leave the
argument empty to discover the next highest-ranked skill candidate.

### `iterative-ui-design`

Creates several distinct, browser-reviewable UI directions and carries the
user's selections through progressively narrower rounds. It preserves locked
and rejected decisions, adds interactivity only when needed for feedback, and
hands the approved prototype to the normal implementation workflow.

## Local usage recording

The `geno-dev usage` CLI records skill invocations in a privacy-minimal local
SQLite database so adoption can be measured without storing prompts, paths, or
project data.

See [Getting Started](getting-started.md) for usage and the repository contract.
