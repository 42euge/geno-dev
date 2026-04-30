# Getting Started

## Prerequisites

- A supported coding CLI (Claude Code, Gemini CLI, Codex, or OpenCode)
- [geno-tools](https://42euge.github.io/geno-tools) installed

### Optional (for specific skills)

| Tool | Needed by | What it is | Install |
|------|-----------|-----------|---------|
| [geno-notes](https://github.com/42euge/geno-notes) | `/geno-dev-tasks-start` | Project journal — tasks, notes, plans | `geno-tools install geno-notes` |
| [geno-mon](https://github.com/42euge/geno-mon) | `/geno-dev-sessions-fork` | Session monitor for Claude Code | See [geno-mon docs](https://github.com/42euge/geno-mon) |

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

## What's next

- [Concepts](concepts.md) — understand workspaces, worktrees, and tasks
- [Workflows](workflows.md) — end-to-end examples
- [Commands](commands.md) — detailed reference for each slash command
- [geno-tools docs](https://42euge.github.io/geno-tools) — the broader ecosystem
