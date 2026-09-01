---
name: feature-acceptance-test
description: >-
  Use when an implemented feature or merge request needs validation through
  its real UI, CLI, hardware, or end-user workflow, or when the user asks how
  to test or dogfood it manually. Do not use for unit-test design or code
  review alone.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# Validate a feature through its real user path

Prove the exact implementation under review through the public surface a user
will actually operate, then leave a concise Markdown runbook the user can
follow independently. Automated tests and code review are prerequisites or
supporting evidence, not substitutes for acceptance.

## Record the invocation

At the start of every invocation, call the installed `geno-dev` CLI exactly
once. Set `trigger` to `explicit` when the user named this skill and to
`implicit` when the request triggered it automatically:

```bash
trigger=implicit
geno-dev usage record feature-acceptance-test --trigger "$trigger"
```

The recorder writes only the skill name, trigger, and UTC timestamp to the
local SQLite database. If the CLI is unavailable or recording fails, continue
the requested work and mention the failure briefly in the final response. Do
not replace the CLI call with direct database access.

## Acceptance contract

Before testing, establish:

- the exact branch, merge request, commit, package, or build being evaluated;
- the public entry point the user will operate;
- environment and hardware prerequisites;
- observable success and failure criteria;
- cleanup or rollback needed after the test.

Do not silently test a stale checkout, a different build, a private API, or a
test-only shortcut when the real path is available. State any unavoidable
substitution and what remains unproven.

## Choose the validation mode

- **Instructions:** When the user asks how to test, produce concise,
  copy-pasteable steps with expected observations and cleanup. Do not create a
  verification program when the user asked for a human runbook.
- **Agent-executed:** When execution is in scope, exercise the real entry point
  and capture observable evidence. Prefer the safest environment that still
  proves the behavior.
- **Guided:** When the user owns the UI, microphone, hardware, credentials, or
  physical setup, provide one coherent test sequence and use their observations
  to diagnose the result.

Automate setup and evidence collection where useful, but preserve the user
journey being tested.

## Required Markdown deliverable

Every invocation must create a manual acceptance runbook in the current
workspace. Use an existing documentation or test-plan location when the
repository has one; otherwise write `<feature-slug>-manual-acceptance.md` at the
workspace root. Do not commit the runbook unless the user asks.

Keep it brief and executable. Include:

- the exact artifact, commit, and environment it applies to;
- prerequisites and safety checks;
- numbered user actions with copy-pasteable commands where appropriate;
- the expected observation after each action;
- cleanup or rollback steps;
- known limitations and anything the procedure does not prove.

Do not substitute a verification program, test output, or a chat response for
the Markdown file. If the workspace is not writable, provide the complete
runbook in the final response and report that the file could not be created.

## Evaluate and finish

Treat unexpected behavior as evidence, not as a reason to switch to an easier
test path. If fixing it is already within the implementation request, make the
smallest scoped fix and repeat the same acceptance path. Otherwise report the
defect without changing code.

Finish with:

- `PASS`, `FAIL`, or `BLOCKED`;
- the exact artifact and environment tested;
- the observed evidence;
- a link to the manual acceptance Markdown file;
- cleanup performed and any remaining state.

## Authorization boundaries

Planning and local read-only inspection do not authorize deployment or hardware
changes. Require explicit current authorization before touching shared or
production environments, installing artifacts, changing hardware state, or
using credentials. Define rollback first and stop when the target environment
or artifact identity is uncertain.

## Usage report

To see how often the skill has been used, run:

```bash
geno-dev usage report feature-acceptance-test --days 30
```

The database defaults to `~/.geno/skill-usage.sqlite3`. No usage data is sent
off the machine.
