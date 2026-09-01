---
name: geno-dev
description: >-
  Use when the user invokes /geno-dev to inspect available developer workflows
  or route a request to a focused skill in this skillset.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# geno-dev

This is the umbrella skill for `geno-dev`.

## Skills

| Skill | Use when |
|---|---|
| `feature-acceptance-test` | Validate an implemented feature through its real UI, CLI, hardware, or user workflow. |
| `meta-mine-skill-creator` | Mine Claude Code and Codex sessions for candidate skills and system improvements. |

Route requests to the narrowest matching skill. Use `feature-acceptance-test`
after implementation or review when the real user path still needs proof. Do
not mine session history merely because a request mentions a past interaction;
use the focused mining skill only when the user wants history analyzed for
durable improvements.
