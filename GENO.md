# geno-dev — developer utilities skillset

Developer and infrastructure skills for AI coding agents: task execution from lab notes, git commit history rewriting, worktree management, workspace creation, and session forking.

## Skills

| Skill name | Sub-skillset | Skill | Slash command |
|-----------|-------------|-------|---------------|
| `geno-dev` | — | — | — (umbrella) |
| `geno-dev-tasks-start` | tasks | start | `/geno-dev-tasks-start` |
| `geno-dev-commits-rewrite` | commits | rewrite | `/geno-dev-commits-rewrite` |
| `geno-dev-worktrees-manage` | worktrees | manage | `/geno-dev-worktrees-manage` |
| `geno-dev-workspaces-init` | workspaces | init | `/geno-dev-workspaces-init` |
| `geno-dev-sessions-fork` | sessions | fork | `/geno-dev-sessions-fork` |

## Repo structure

```
geno-dev/
├── GENO.md              # agent instructions (this file)
├── SKILL.md             # umbrella skill manifest (symlink to skills/geno-dev/SKILL.md)
├── genotools.yaml       # geno-tools manifest
├── skills/              # skill definitions
│   ├── geno-dev/        #   umbrella
│   ├── geno-dev-commits-rewrite/
│   ├── geno-dev-sessions-fork/
│   ├── geno-dev-tasks-start/
│   ├── geno-dev-workspaces-init/
│   └── geno-dev-worktrees-manage/
├── docs/                # MkDocs Material site
├── config/defaults/     # default configuration files
│   └── colab.json
└── package.json         # npm/skills manifest
```

## Conventions

- Skill directories live under `skills/` and each contains a `SKILL.md`.
- The umbrella skill at `skills/geno-dev/SKILL.md` lists all available commands.
- See the [geno-tools nomenclature spec](https://42euge.github.io/geno-tools/skillsets/nomenclature/) for naming rules.

## Runtime

No venv or scripts — pure markdown workflows.
