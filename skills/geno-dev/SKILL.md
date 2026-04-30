---
name: geno-dev
description: >-
  Developer and infrastructure utilities — task execution from lab notes,
  git commit history rewriting, worktree management, workspace creation,
  session forking, end-to-end feature shipping, issue-driven development, and agentic loops.
  Use when user says /geno-dev-tasks-start, /geno-dev-commits-rewrite,
  /geno-dev-worktrees-manage, /geno-dev-workspaces-init, /geno-dev-sessions-fork,
  /geno-dev-feature-ship, /geno-dev-issue-work, /geno-dev-loops-turbocharge,
  /geno-dev-loops-cruise, or /geno-dev-prs-check.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# geno-dev — Developer Utilities

Dev and infrastructure skills for AI coding agents. Task execution, git history rewriting, worktree management, workspace creation, session forking, end-to-end feature shipping, issue-driven development, agentic loops, and PR checking.

## Commands

| Command | Description |
|---|---|
| `/geno-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |
| `/geno-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees — list, create, switch, and prune |
| `/geno-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |
| `/geno-dev-sessions-fork [session]` | Fork an agent session — extract context to continue in a new session |
| `/geno-dev-feature-ship [description\|issue URL]` | End-to-end: scope, issue, branch, implement, and PR |
| `/geno-dev-issue-work [number\|query\|URL]` | Pick a GitHub issue or JIRA ticket and work on it (normal or loop mode) |
| `/geno-dev-loops-turbocharge [task] [--spec <file>]` | Spec-driven convergence loop — iterate until all acceptance criteria pass |
| `/geno-dev-loops-cruise [task] [--plan <file>]` | Plan-driven sequential loop — execute a plan one step at a time |
| `/geno-dev-prs-check [repo\|--all]` | Check open PRs and flag ones that may need closing |

## Runtime

No venv or scripts — pure markdown workflows.
