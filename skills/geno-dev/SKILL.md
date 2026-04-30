---
name: geno-dev
description: >-
  Developer and infrastructure utilities — task execution from lab notes,
  git commit history rewriting, worktree management, workspace creation,
  and session forking.
  Use when user says /geno-dev-tasks-start, /geno-dev-commits-rewrite,
  /geno-dev-worktrees-manage, /geno-dev-workspaces-init, /geno-dev-sessions-fork,
  or /geno-dev-prs-check.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# geno-dev — Developer Utilities

Dev and infrastructure skills for Claude Code. Task execution, git history rewriting, worktree management, workspace creation, session forking, and PR checking.

## Commands

| Command | Description |
|---|---|
| `/geno-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |
| `/geno-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees — list, create, switch, and prune |
| `/geno-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |
| `/geno-dev-sessions-fork [session]` | Fork a Claude Code session — extract context to continue in a new session |
| `/geno-dev-prs-check [repo\|--all]` | Check open PRs and flag ones that may need closing |

## Runtime

No venv or scripts — pure markdown workflows.
