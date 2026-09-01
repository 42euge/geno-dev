# Getting Started

## Prerequisites

- [geno-tools](https://github.com/42euge/geno-tools)

## Install

```bash
geno-tools install geno-dev
```

## Current surface

Invoke `/geno-dev` to inspect the skillset.

Run `/meta-mine-skill-creator` when you want to analyze local Claude Code and Codex sessions for:

- repeatable workflows that should become skills;
- repeated corrections that should patch a skill or repository rule;
- broader agent or product improvements that do not belong in a skill.

Mining is read-only. The skill asks which candidates to materialize before editing the repository.

New capabilities belong in independent `skills/<skill-name>/SKILL.md` leaf directories and should be added to the umbrella skill and repository documentation.
