# geno-dev

Developer and infrastructure skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Task execution from lab notes, git commit history rewriting, and Google Colab upload plumbing.

Part of the [geno-tools](https://github.com/42euge/geno-tools) ecosystem.

## Install

```bash
geno-tools install dev                       # from registry
geno-tools dev dev /path/to/local/checkout   # for local dev
```

## Commands

| Command | Description |
|---|---|
| `/gt-dev-task-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/gt-dev-commit-rewrite` | Rewrite git commit history into a clean narrative (backup branch + soft reset + restage) |
| `/gt-dev-colab-config` | Configure the Google Drive account used for Colab notebook uploads |
| `/gt-dev-colab-upload <notebook>` | Copy a `.ipynb` to Google Drive for Colab access |

## Repository structure

```
geno-dev/
├── SKILL.md              # umbrella (discovered by geno-tools)
├── genotools.yaml        # install manifest
├── commands/             # slash-command .md files
│   └── gt-dev-*.md
└── config/defaults/
    └── colab.json        # copied once → ~/.geno-tools/geno-dev/configs/colab.json
```

## Runtime

No venv, no scripts. Runtime state lives at:
- `~/.geno-tools/geno-dev/configs/colab.json` — Colab account config, copied from `config/defaults/colab.json` on install, user-editable.

## License

MIT
