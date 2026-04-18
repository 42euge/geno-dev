---
name: geno-dev
description: >-
  Developer and infrastructure utilities — task execution from lab notes,
  git commit history rewriting, Google Colab notebook uploads, and Colab
  account configuration. Use when user says /gt-dev-task-start,
  /gt-dev-commit-rewrite, /gt-dev-colab-config, or /gt-dev-colab-upload.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# geno-dev

Dev and infrastructure skills for Claude Code. Task execution, git history rewriting, and Colab upload plumbing.

Installed via [geno-tools](https://github.com/42euge/geno-tools):
```bash
geno-tools install dev
```

## Commands

| Command | Description |
|---|---|
| `/gt-dev-task-start [description]` | Pick up a task from lab notes, assess scope, plan if needed, execute, and mark done |
| `/gt-dev-commit-rewrite` | Rewrite git commit history into a clean narrative (backup + soft reset + restage) |
| `/gt-dev-colab-config` | Configure Google Drive account for Colab notebook uploads |
| `/gt-dev-colab-upload <notebook>` | Copy a `.ipynb` to Google Drive for Colab access |

## Runtime

No venv or scripts — pure markdown workflows. Colab account config lives at:
- `~/.geno-tools/geno-dev/configs/colab.json` — copied from `config/defaults/colab.json` on install, user-editable.
