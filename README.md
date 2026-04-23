# geno-dev

Developer and infrastructure skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Task execution from lab notes and git commit history rewriting.

## Install

```bash
npx skills add 42euge/geno-dev
```

## Commands

| Command | Description |
|---|---|
| `/gt-dev-task-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/gt-dev-commit-rewrite` | Rewrite git commit history into a clean narrative (backup branch + soft reset + restage) |

## Repository structure

```
geno-dev/
├── package.json          # Vercel Skills manifest
├── .geno-agents          # agent identity for auto-registration
├── skills/
│   ├── geno-dev/         # umbrella skill
│   │   └── SKILL.md
│   ├── geno-dev-commit-rewrite/
│   │   └── SKILL.md
│   └── geno-dev-task-start/
│       └── SKILL.md
└── config/defaults/
    └── colab.json
```

## Runtime

No venv, no scripts.

## License

MIT
