---
name: geno-dev
description: >-
  Developer and infrastructure utilities — task execution from lab notes
  and git commit history rewriting.
  Use when user says /gt-dev-task-start or /gt-dev-commit-rewrite.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# geno-dev — Developer Utilities

Dev and infrastructure skills for Claude Code. Task execution and git history rewriting.

## Commands

| Command | Description |
|---|---|
| `/gt-dev-task-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/gt-dev-commit-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |

## Runtime

No venv or scripts — pure markdown workflows.
