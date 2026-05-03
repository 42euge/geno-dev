# geno-dev — developer utilities skillset

Developer and infrastructure skills for AI coding agents: task execution from lab notes, git commit history rewriting, worktree management, workspace creation, session forking, end-to-end feature shipping, issue-driven development, agentic loops, PR and branch auditing, scheduled snoozing, and skill retrospectives.

## Skills

| Skill | Sub-skillset | Slash command |
|-------|-------------|---------------|
| geno-dev | — | — (umbrella) |
| geno-dev-tasks-start | tasks | /geno-dev-tasks-start |
| geno-dev-commits-rewrite | commits | /geno-dev-commits-rewrite |
| geno-dev-worktrees-manage | worktrees | /geno-dev-worktrees-manage |
| geno-dev-workspaces-init | workspaces | /geno-dev-workspaces-init |
| geno-dev-sessions-fork | sessions | /geno-dev-sessions-fork |
| geno-dev-loops-turbocharge | loops | /geno-dev-loops-turbocharge |
| geno-dev-loops-cruise | loops | /geno-dev-loops-cruise |
| geno-dev-loops-nos | loops | /geno-dev-loops-nos |
| geno-dev-loops-ignition | loops | /geno-dev-loops-ignition |
| geno-dev-prs-check | prs | /geno-dev-prs-check |
| geno-dev-branches-audit | branches | /geno-dev-branches-audit |
| geno-dev-scheduling-snooze | scheduling | /geno-dev-scheduling-snooze |
| geno-dev-feature-ship | feature-ship | /geno-dev-feature-ship |
| geno-dev-issue-work | issue-work | /geno-dev-issue-work |
| geno-dev-skills-retro | meta | /geno-dev-skills-retro |

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
│   ├── geno-dev-worktrees-manage/
│   ├── geno-dev-loops-turbocharge/
│   ├── geno-dev-loops-cruise/
│   ├── geno-dev-loops-nos/
│   ├── geno-dev-loops-ignition/
│   ├── geno-dev-prs-check/
│   ├── geno-dev-branches-audit/
│   ├── geno-dev-scheduling-snooze/
│   ├── geno-dev-feature-ship/
│   ├── geno-dev-issue-work/
│   └── geno-dev-skills-retro/
├── docs/                # MkDocs Material site
│   ├── index.md
│   ├── getting-started.md
│   ├── concepts.md
│   ├── workflows.md
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
- **loops-turbocharge**: Spec-driven convergence loop — iterates until all acceptance criteria pass.
- **loops-cruise**: Plan-driven sequential loop — executes a plan one step at a time via agent subagents.
- **loops-nos**: Burst parallel sprint — identifies independent items and spawns subagents in parallel.
- **loops-ignition**: Cold-start bootstrap loop — turns a high-level goal into a blueprint, scaffold, implementation, and verified first slice.
- **prs-check**: Checks open PRs, classifies by status (closeable/stale/blocked/draft/approved), renders a table with links.
- **branches-audit**: Audits all branches across a workspace or repo, classifying by PR status and suggesting next actions.
- **scheduling-snooze**: Delays session work until a specified time using natural language, with chained wakeups for long delays.
- **skills-retro**: Meta-harness — analyzes failed sessions, identifies root causes, and patches the responsible skill to prevent recurrence.

## Conventions

- Skill directories live under `skills/` and must contain a `SKILL.md` with valid frontmatter.
- The `.geno/` directory and `CLAUDE.local.md` are never committed — they hold machine-local state.
- This skill never modifies a project's `.gitignore` or tracked config files.
- **Prefix aliasing**: Slash commands use the canonical `geno-` prefix in source (e.g., `/geno-dev-tasks-start`). Short `/gt-` aliases are configured per-install by geno-tools and are not part of the skill source.
- **Adding a new skill**: Create a directory under `skills/` named after the skill, add a `SKILL.md` with valid frontmatter (name, description, argument-hint, license, metadata), then register the skill in the skills table and repo structure tree in this file.
