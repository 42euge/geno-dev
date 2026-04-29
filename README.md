# geno-dev

Developer and infrastructure skills for AI coding agents. Task execution from lab notes, git commit history rewriting, worktree management, workspace creation, session forking, and agentic loops.

## Install

```bash
geno-tools install geno-dev
```

## Commands

| Command | Description |
|---|---|
| `/geno-dev-tasks-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/geno-dev-commits-rewrite` | Rewrite git commit history into a clean narrative (backup branch + soft reset + restage) |
| `/geno-dev-worktrees-manage [list\|create\|switch\|prune]` | Manage git worktrees — list, create, switch, and prune |
| `/geno-dev-workspaces-init [config\|list\|<text>]` | Create development workspaces from issues, tickets, repos, or ideas |
| `/geno-dev-sessions-fork [session]` | Fork an agent session — extract context to continue in a new session |
| `/geno-dev-loops-turbocharge [task] [--spec <file>]` | Spec-driven convergence loop — iterate until all acceptance criteria pass |
| `/geno-dev-loops-cruise [task] [--plan <file>]` | Plan-driven sequential loop — execute a plan one step at a time |

## Repository structure

```
geno-dev/
├── GENO.md               # agent instructions (single source of truth)
├── SKILL.md              # umbrella skill manifest
├── genotools.yaml        # geno-tools manifest
├── package.json          # npm/skills metadata
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
│   ├── geno-dev-worktrees-manage/
│   │   └── SKILL.md
│   ├── geno-dev-loops-turbocharge/
│   │   └── SKILL.md
│   └── geno-dev-loops-cruise/
│       └── SKILL.md
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   └── commands.md
└── config/defaults/
    └── colab.json
```

## Runtime

No venv, no scripts.

## License

MIT
