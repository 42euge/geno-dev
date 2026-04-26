# geno-dev

Developer and infrastructure skills for AI coding agents. Task execution from lab notes, git commit history rewriting, worktree management, and workspace creation.

Part of the [geno-tools](https://42euge.github.io/geno-tools) ecosystem.

## Features

- **Task execution** — pick up tasks from lab notes, assess scope, plan if needed, execute, and mark done
- **Commit rewriting** — rewrite messy git history into a clean narrative with backup, soft reset, and restage
- **Worktree management** — manage git worktrees: create for feature branches, list with status, and prune stale ones
- **Workspace creation** — create isolated development workspaces from GitHub issues, JIRA tickets, or feature ideas

## Install

```bash
geno-tools install dev
```

## Commands

| Command | Description |
|---|---|
| `/geno-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |
| `/geno-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees — list, create, switch, and prune |
| `/geno-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |

## Runtime

No venv, no scripts — pure markdown workflows.
