---
name: geno-dev
description: >-
  Developer and infrastructure utilities — task execution from lab notes,
  git commit history rewriting, worktree management, and workspace creation.
  Use when user says /gt-dev-tasks-start, /gt-dev-commits-rewrite,
  /gt-dev-worktrees-manage, or /gt-dev-workspaces-init.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# geno-dev — Developer Utilities

Dev and infrastructure skills for Claude Code. Task execution, git history rewriting, worktree management, and workspace creation.

## Commands

| Command | Description |
|---|---|
| `/gt-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/gt-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |
| `/gt-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees — list, create, switch, and prune |
| `/gt-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |

## Runtime

No venv or scripts — pure markdown workflows.
