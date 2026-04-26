# geno-dev — developer utilities skillset

Developer and infrastructure skills for AI coding agents: task execution from lab notes, git commit history rewriting, worktree management, workspace creation, and session forking.

## Skills

| Skill | Sub-skillset | Slash command |
|-------|-------------|---------------|
| geno-dev | — | — (umbrella) |
| geno-dev-tasks-start | tasks | /geno-dev-tasks-start |
| geno-dev-commits-rewrite | commits | /geno-dev-commits-rewrite |
| geno-dev-worktrees-manage | worktrees | /geno-dev-worktrees-manage |
| geno-dev-workspaces-init | workspaces | /geno-dev-workspaces-init |
| geno-dev-sessions-fork | sessions | /geno-dev-sessions-fork |

## Repo structure

```
geno-dev/
├── GENO.md              # agent instructions (this file)
├── SKILL.md             # umbrella skill manifest
├── genotools.yaml       # geno-tools manifest
├── package.json         # npm/skills metadata
├── .geno-agents         # agent identity for auto-registration
├── skills/              # skill definitions
│   ├── geno-dev/        #   umbrella
│   ├── geno-dev-commits-rewrite/
│   ├── geno-dev-sessions-fork/
│   ├── geno-dev-tasks-start/
│   ├── geno-dev-workspaces-init/
│   └── geno-dev-worktrees-manage/
├── docs/                # MkDocs Material site
│   ├── index.md
│   ├── getting-started.md
│   └── commands.md
├── config/defaults/     # default configuration files
│   └── colab.json
└── mkdocs.yml           # MkDocs configuration
```

## Architecture

Pure markdown skillset — no Python package, no venv, no scripts. Each skill is a SKILL.md file containing the full workflow as structured instructions for the agent.

### Key skills

- **tasks-start**: Integrates with geno-notes to pick up tasks, plan if needed, execute, and mark done.
- **commits-rewrite**: Rewrites messy git history into clean narrative commits using soft reset and selective restaging.
- **worktrees-manage**: Workspace-aware git worktree management with safety protections for Claude Code and geno-tools worktrees.
- **workspaces-init**: Creates isolated development workspaces from GitHub issues, JIRA tickets, repo names, or feature ideas, with color-coded folder organization.
- **sessions-fork**: Extracts full session context via geno-mon for continuation in a new session.

## Conventions

- Skill directories live under `skills/` and must contain a `SKILL.md` with valid frontmatter.
- The `.geno/` directory and `CLAUDE.local.md` are never committed — they hold machine-local state.
- This skill never modifies a project's `.gitignore` or tracked config files.
