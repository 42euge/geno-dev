---
name: geno-dev-issue-work
description: >-
  Select a GitHub issue or JIRA ticket and start working on it, with a choice
  of normal interactive mode or autonomous loop mode.
  Use when user says /geno-dev-issue-work.
argument-hint: "[issue number, JIRA key, search query, or URL]"
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# Work on Issue

Pick a GitHub issue or JIRA ticket and start working on it. Offers two execution modes: normal (interactive, back-and-forth with the user) or loop (autonomous work with periodic check-ins).

## Input

`$ARGUMENTS` is optional. Can be:

- A GitHub issue number (e.g., `42`)
- A JIRA ticket key (e.g., `PROJ-1234`)
- A URL to a GitHub issue or JIRA ticket
- A search query (e.g., `auth bug`)
- Empty — show open issues and let the user pick

## Workflow

### 1. Detect issue source

Determine whether we're working with GitHub or JIRA based on the input:

- **Bare number** (e.g., `42`) → GitHub issue in the current repo
- **JIRA key** (e.g., `PROJ-1234`, matches `[A-Z]+-\d+`) → JIRA ticket
- **URL containing `github.com`** → GitHub issue (extract owner/repo/number)
- **URL containing `atlassian.net` or `jira`** → JIRA ticket (extract key)
- **Text or empty** → GitHub issue search in the current repo

For GitHub: run `gh repo view --json nameWithOwner -q .nameWithOwner` to confirm the current repo. If not in a git repo or no GitHub remote, tell the user and stop.

For JIRA: the user must have the JIRA CLI (`jira`) or a configured MCP server. If neither is available, ask the user to provide the ticket details manually.

### 2. Select an issue

**GitHub path:**

If `$ARGUMENTS` is a number, fetch it directly with `gh issue view <number>`.

If `$ARGUMENTS` is text, search with `gh issue list --search "<query>" --json number,title,labels,assignees --limit 10`.

If no arguments, list open issues with `gh issue list --json number,title,labels,assignees --limit 15`.

Present the results to the user with `AskUserQuestion`. Each option shows the issue number, title, and labels. Let the user pick one.

**JIRA path:**

Fetch the ticket details. Try `jira issue view <KEY> --plain` if the CLI is available, or use the JIRA MCP server if configured.

If `$ARGUMENTS` is a search query with no matching JIRA key pattern, search with `jira issue list --query "text ~ '<query>'" --plain` or ask the user to provide the ticket key directly.

### 3. Understand the issue

**GitHub:** Read the full issue body and comments with `gh issue view <number>`.

**JIRA:** Read the ticket description, acceptance criteria, and comments.

Summarize the issue for the user: what needs to happen, any constraints or context from the comments.

### 4. Choose execution mode

Use `AskUserQuestion` to ask the user how they want to work on this:

- **Normal mode** — interactive back-and-forth. You implement, ask questions when stuck, and the user reviews as you go. Best for exploratory or ambiguous issues.
- **Loop mode** — autonomous execution with periodic status updates. You work independently, checking in at key milestones. Best for well-defined issues with clear acceptance criteria.

### 5. Set up the branch

Create a feature branch from the default branch:

- **GitHub:** `git checkout -b <number>-<slug>` (e.g., `19-add-dep-management`)
- **JIRA:** `git checkout -b <KEY>-<slug>` (e.g., `PROJ-1234-migrate-db-schema`)

Where `<slug>` is a short kebab-case summary of the issue title. Push with `-u` to set up tracking.

### 6a. Normal mode

Work interactively:

- Explore the codebase to understand the relevant code
- For non-trivial changes, use `EnterPlanMode` to propose an approach, get user approval, then `ExitPlanMode`
- Implement the fix or feature
- Ask the user when you hit ambiguity or need a decision
- When done, create a PR with `gh pr create`. For GitHub issues, link with `Closes #N`. For JIRA tickets, include the ticket key in the PR title (e.g., `PROJ-1234: Fix auth token`) and body. Present the URL.

### 6b. Loop mode

Work autonomously using `ScheduleWakeup` to self-pace:

**First iteration:**

- Explore the codebase and build context
- Draft a plan (save it as a comment on the issue or present it briefly)
- Start implementing

**Each subsequent iteration:**

- Continue where you left off
- Commit logical units as you go
- At each wake-up, assess: am I blocked? is there a decision the user needs to make?
- If blocked or need input, stop the loop and ask the user
- If making progress, schedule the next wake-up and keep going

**Finishing:**

- Run available tests or linters
- Create a PR with `gh pr create`. For GitHub issues, link with `Closes #N`. For JIRA, include the ticket key in the title and body.
- Stop the loop and present the PR URL to the user

Use `ScheduleWakeup` with the `/loop` prompt to continue each iteration. Choose delay based on the work: 60–90s for active implementation, 120–270s if waiting on a build or test run.
