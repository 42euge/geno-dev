# geno-dev — developer utilities skillset

@import SKILL.md from skills/geno-dev/SKILL.md

Developer and infrastructure skills for coding agents: task execution from lab notes, git commit history rewriting, worktree management, workspace creation, and session forking.

## Skills

| Skill name | Slash command | Description |
|-----------|---------------|-------------|
| `geno-dev` | — (umbrella) | Umbrella skill for all geno-dev utilities |
| `geno-dev-tasks-start` | `/geno-dev-tasks-start` | Pick up a task from lab notes, plan if needed, execute, and mark done |
| `geno-dev-commits-rewrite` | `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative |
| `geno-dev-worktrees-manage` | `/geno-dev-worktrees-manage` | Manage git worktrees — list, create, switch, and prune |
| `geno-dev-workspaces-init` | `/geno-dev-workspaces-init` | Create development workspaces from issues, tickets, repos, or ideas |
| `geno-dev-sessions-fork` | `/geno-dev-sessions-fork` | Fork a Claude Code session to continue in a new session |

## Repo structure

```
geno-dev/
├── package.json          # Skills manifest
├── .geno-agents          # Agent identity for auto-registration
├── skills/
│   ├── geno-dev/         # Umbrella skill
│   │   └── SKILL.md
│   ├── geno-dev-commits-rewrite/
│   │   └── SKILL.md
│   ├── geno-dev-sessions-fork/
│   │   └── SKILL.md
│   ├── geno-dev-tasks-start/
│   │   └── SKILL.md
│   ├── geno-dev-workspaces-init/
│   │   └── SKILL.md
│   └── geno-dev-worktrees-manage/
│       └── SKILL.md
└── config/defaults/
    └── colab.json
```

## Compliance

This repo follows geno-ecosystem conventions. Skill names follow: `{skillset}-{sub-skillset}-{skill-slug}`.

- **Skillset** = `geno-dev`
- **Sub-skillset** = pluralized noun (e.g., `tasks`, `commits`)
- **Skill slug** = action verb (e.g., `start`, `rewrite`)

## Runtime

No venv, no scripts — pure markdown workflows.
