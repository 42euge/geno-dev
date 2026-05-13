---
name: geno-dev-feature-ship
description: >-
  End-to-end feature shipping — discuss scope, create a GitHub issue, branch,
  implement, and open a PR. Use when user says /geno-dev-feature-ship.
argument-hint: "<feature description or issue URL>"
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
observability:
  success_signal: "PR created and URL presented to user"
  failure_signals:
    - "no GitHub remote available"
    - "implementation blocked"
  knowledge_reads:
    - "GitHub issues (via gh CLI)"
  knowledge_writes:
    - "GitHub issue (created)"
    - "GitHub PR (created)"
---

# Ship Feature

Take a feature idea from discussion through to a pull request: scope the work with the user, create a GitHub issue, branch, implement, and open a PR.

## Input

`$ARGUMENTS` is either a freeform feature description or an existing GitHub issue URL. If empty, ask the user what they want to build.

## Workflow

### 1. Scope the feature

If `$ARGUMENTS` is a GitHub issue URL, fetch it with `gh issue view` and skip to step 2.

Otherwise, start a conversation with the user to understand what they want:

- Ask clarifying questions to nail down the requirements
- Identify the target repo (use `git remote -v` in the current directory, or ask)
- Agree on the approach before moving forward

Do not rush past this step. The goal is a shared understanding of what "done" looks like.

### 2. Create a GitHub issue

Draft the issue based on the scoping conversation:

- Title: concise, under 70 characters
- Body: problem statement, proposed approach, scope (what's in / what's out)

Present the draft to the user with `AskUserQuestion` for approval. Create with `gh issue create`. Record the issue number for the branch name and PR.

Skip this step if `$ARGUMENTS` was already an issue URL.

### 3. Create a branch

Create a feature branch from the current default branch:

```
git checkout -b <descriptive-branch-name>
```

Branch name should reflect the feature (e.g., `add-dep-management`, `fix-auth-token`). Push with `-u` to set up tracking.

### 4. Implement

- Explore the codebase to understand the relevant code
- For non-trivial work, use `EnterPlanMode` to design the approach and get user approval, then `ExitPlanMode` to execute
- Implement the feature, committing logical units as you go
- Update documentation (CLAUDE.md, README, etc.) if the feature changes public behavior
- Run any available tests or linters to verify correctness

### 5. Open a pull request

Create the PR with `gh pr create`:

- Title: short, matches the feature
- Body: summary bullets, link to the issue (`Closes #N`), test plan
- Target the default branch

Present the PR URL to the user.

### 6. Wrap up

Summarize what was shipped: the issue, branch, PR, and key implementation decisions. If there are follow-up items (future scope from step 1), mention them so nothing is lost.

## Completion

When this skill finishes, emit a trace:

```bash
geno-trace emit \
  --skill geno-dev-feature-ship \
  --status <success|failure|abandoned> \
  --tool-calls <approximate count> \
  --errors <count of tool/command errors> \
  --produced "github-issue github-pr"
```

- `success` = PR created
- `failure` = could not complete implementation
- `abandoned` = user stopped before PR
