# Getting Started

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- [geno-tools](https://github.com/42euge/geno-tools) installed (`pipx install geno-tools`)

## Install

```bash
geno-tools install dev
```

Or from within a Claude Code session:

```
/gt-install dev
```

This clones the repo, registers all skills with Claude Code, and sets up the `~/.geno/geno-dev/` directory.

## First use

Once installed, the skills are available as slash commands in any Claude Code session:

| Command | What it does |
|---|---|
| `/geno-dev-tasks-start` | Pick up a task from lab notes and execute it |
| `/geno-dev-commits-rewrite` | Rewrite messy git history into clean narrative commits |
| `/geno-dev-worktrees-manage` | List, create, switch, or prune git worktrees |
| `/geno-dev-workspaces-init` | Create an isolated workspace from an issue, ticket, or idea |
| `/geno-dev-sessions-fork` | Fork a Claude Code session to continue in a new one |

## Example: rewrite commit history

In a Claude Code session inside a git repo:

```
/geno-dev-commits-rewrite
```

The skill will analyze your commit history, propose a clean narrative, and — after your approval — rewrite the commits into logical chapters.

## Example: create a workspace

```
/geno-dev-workspaces-init https://github.com/42euge/geno-dev/issues/42
```

This fetches the issue, generates a workspace name, clones the relevant repos into a color-coded folder, and sets up metadata tracking.

## Runtime

geno-dev is a pure markdown skillset — no Python venv, no scripts. All functionality is implemented as skill instructions that guide the agent.
