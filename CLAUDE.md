# geno-dev — developer utilities skillset

Developer and infrastructure skills for Claude Code: task execution from lab notes, git commit history rewriting, worktree management, and workspace creation.

## Skills

| Skill name | Sub-skillset | Skill | Slash command |
|-----------|-------------|-------|---------------|
| `geno-dev` | — | — | — (umbrella) |
| `geno-dev-tasks-start` | tasks | start | `/geno-dev-tasks-start` |
| `geno-dev-commits-rewrite` | commits | rewrite | `/geno-dev-commits-rewrite` |
| `geno-dev-worktrees-manage` | worktrees | manage | `/geno-dev-worktrees-manage` |
| `geno-dev-workspaces-init` | workspaces | init | `/geno-dev-workspaces-init` |

## Compliance

This repo follows geno-ecosystem conventions. All contributors and agents must adhere to:

### Nomenclature

Skill names follow: `{skillset}-{sub-skillset}-{skill-slug}`

- **Skillset** = this repo's name: `geno-dev`
- **Sub-skillset** = always a **pluralized noun** (e.g., `tasks`, `commits`)
- **Skill slug** = action verb (e.g., `start`, `rewrite`)
- **Umbrella** = just `geno-dev`

When adding a new skill, pick the sub-skillset group it belongs to (create a new one if needed, must be a pluralized noun), then name the folder `geno-dev-{sub-skillset}-{skill-slug}`.

Full spec: https://42euge.github.io/geno-tools/skillsets/nomenclature/

### Repo structure

Every geno-ecosystem repo must have:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project instructions for agents (this file) |
| `package.json` | Skills manifest with name, version, skills map |
| `.geno-agents` | Agent identity: role, description, capabilities |
| `skills/geno-{name}/SKILL.md` | Umbrella skill |
| `README.md` | Human-facing docs: install, commands table, repo tree |

### SKILL.md frontmatter

Every SKILL.md must include:

```yaml
---
name: geno-dev-{sub-skillset}-{skill-slug}   # must match folder name
description: >-
  What this skill does.
  Use when user says /geno-dev-{sub-skillset}-{skill-slug}.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---
```

### Adding a new skill

1. Create `skills/geno-dev-{sub-skillset}-{skill}/SKILL.md` with compliant frontmatter
2. Update the umbrella `skills/geno-dev/SKILL.md` — add the new command to the description and table
3. Update `README.md` — command table and repo tree
4. Update `docs/commands.md` — add a section for the new command
5. Update this file's Skills table
