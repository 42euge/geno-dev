# geno-dev

Developer and infrastructure skills for AI coding agents. Task execution from lab notes, git commit history rewriting, worktree management, workspace creation, session forking, end-to-end feature shipping, issue-driven development, agentic loops, background monitoring, PR checking and branch auditing, scheduled snoozing, and skill retrospectives.

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
| `/geno-dev-feature-ship [description\|issue URL]` | End-to-end: scope, issue, branch, implement, and PR |
| `/geno-dev-issue-work [number\|query\|URL]` | Pick a GitHub issue or JIRA ticket and work on it (normal or loop mode) |
| `/geno-dev-loops-turbocharge [task] [--spec <file>]` | Spec-driven convergence loop — iterate until all acceptance criteria pass |
| `/geno-dev-loops-cruise [task] [--plan <file>]` | Plan-driven sequential loop — execute a plan one step at a time |
| `/geno-dev-loops-autopilot [task] [--watch <tests\|ci\|lint\|git\|all>]` | Background monitoring loop — watch CI, tests, lint, and git state |
| `/geno-dev-loops-boost [task]` | Pomodoro focus loop — time-boxed work blocks with reflection |
| `/geno-dev-loops-ignition [goal] [--blueprint <file>]` | Cold-start bootstrap loop — turn a high-level goal into a blueprint and verified first slice |
| `/geno-dev-prs-check [repo\|--all]` | Check open PRs and flag ones that may need closing |
| `/geno-dev-branches-audit [repo\|--all]` | Audit all branches — find ones needing PRs, ready to merge, or stale |
| `/geno-dev-scheduling-snooze <time> [prompt]` | Snooze session until a specified time, then execute a prompt |
| `/geno-dev-skills-retro [session] [--skill <name>]` | Meta-harness: analyze a failed session and patch the responsible skill |

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
│   ├── geno-dev-loops-cruise/
│   │   └── SKILL.md
│   ├── geno-dev-loops-autopilot/
│   │   └── SKILL.md
│   ├── geno-dev-loops-boost/
│   │   └── SKILL.md
│   ├── geno-dev-loops-ignition/
│   │   └── SKILL.md
│   ├── geno-dev-prs-check/
│   │   └── SKILL.md
│   ├── geno-dev-branches-audit/
│   │   └── SKILL.md
│   ├── geno-dev-scheduling-snooze/
│   │   └── SKILL.md
│   ├── geno-dev-feature-ship/
│   │   └── SKILL.md
│   ├── geno-dev-issue-work/
│   │   └── SKILL.md
│   └── geno-dev-skills-retro/
│       └── SKILL.md
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   ├── concepts.md
│   ├── workflows.md
│   └── commands.md
└── config/defaults/
    └── colab.json
```

## Runtime

No venv, no scripts.

## License

MIT
