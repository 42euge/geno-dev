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
| `meta-mine-skill-creator` | Mine Claude Code and Codex sessions for candidate skills and system improvements. |

Route requests to the narrowest matching skill. Do not mine session history merely because a request mentions a past interaction; use the focused skill only when the user wants history analyzed for durable improvements.
