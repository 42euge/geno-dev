# Getting Started

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- [npx skills](https://github.com/nichochar/skills) available on your PATH
- Git installed

## Install

```bash
npx skills add 42euge/geno-dev
```

This registers all geno-dev skills with Claude Code (and other supported agents). No venv or runtime dependencies are needed — geno-dev is pure markdown workflows.

## First use

Once installed, the following slash commands are available in any Claude Code session:

| Command | What it does |
|---|---|
| `/geno-dev-tasks-start` | Pick up a task from lab notes and execute it |
| `/geno-dev-commits-rewrite` | Rewrite git history into a clean narrative |
| `/geno-dev-worktrees-manage` | Manage git worktrees (list, create, switch, prune) |
| `/geno-dev-workspaces-init` | Create development workspaces from issues, tickets, or ideas |
| `/geno-dev-sessions-fork` | Fork a session to continue in a new one |

## Quick example

Start a task from your lab notes:

```
/geno-dev-tasks-start fix the auth token bug
```

The skill will load your geno-notes tasks, find the matching task, assess its scope, plan if needed, execute, and mark it done.

## Workspace workflow

Create an isolated workspace for a GitHub issue:

```
/geno-dev-workspaces-init https://github.com/42euge/geno-dev/issues/42
```

Then use worktree management inside the workspace:

```
/geno-dev-worktrees-manage create feature/fix-auth
```

Workspaces and worktrees are designed to work together for branch-level isolation within project-level organization.

## What's next

- See [Commands](commands.md) for detailed usage of each slash command
- Check [geno-tools docs](https://42euge.github.io/geno-tools) for the broader ecosystem
