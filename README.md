# geno-dev

Developer and infrastructure skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Task execution from lab notes, git commit history rewriting, worktree management, workspace creation, and session forking.

## Install

```bash
geno-tools install dev
```

Or from within a Claude Code session:

```
/gt-install dev
```

## Commands

| Command | Description |
|---|---|
| `/geno-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup branch + soft reset + restage) |
| `/geno-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees — list, create, switch, and prune |
| `/geno-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |
| `/geno-dev-sessions-fork [session]` | Fork a Claude Code session — extract context to continue in a new session |

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

## Runtime

No venv, no scripts.

## License

MIT
