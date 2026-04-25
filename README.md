# geno-dev

Developer and infrastructure skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Task execution from lab notes, git commit history rewriting, worktree management, and workspace creation.

## Install

```bash
npx skills add 42euge/geno-dev
```

## Commands

| Command | Description |
|---|---|
| `/gt-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/gt-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup branch + soft reset + restage) |
| `/gt-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees — list, create, switch, and prune |
| `/gt-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |

## Repository structure

```
geno-dev/
├── package.json          # Vercel Skills manifest
├── .geno-agents          # agent identity for auto-registration
├── skills/
│   ├── geno-dev/         # umbrella skill
│   │   └── SKILL.md
│   ├── geno-dev-commits-rewrite/
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

## Runtime

No venv, no scripts.

## License

MIT
