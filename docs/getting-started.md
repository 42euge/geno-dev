# Getting Started

## Prerequisites

- A supported coding CLI (Claude Code, Gemini CLI, Codex, or OpenCode)
- [geno-tools](https://42euge.github.io/geno-tools) installed

## Installation

```bash
geno-tools install geno-dev
```

Or from within an agent session:

```
/geno-tools install geno-dev
```

## First use

Once installed, the geno-dev skills are available as slash commands in your agent session:

- `/geno-dev-tasks-start` — pick up a task from lab notes and execute it
- `/geno-dev-commits-rewrite` — rewrite messy git history into a clean narrative
- `/geno-dev-worktrees-manage` — create, list, switch, and prune git worktrees
- `/geno-dev-workspaces-init` — create isolated development workspaces
- `/geno-dev-sessions-fork` — fork a session to continue work in a new context

## Runtime

geno-dev is a pure markdown skillset — no Python venv, no scripts, no external dependencies beyond git. All skills are self-contained SKILL.md files with structured agent instructions.
