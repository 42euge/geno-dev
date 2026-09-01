# geno-dev

`geno-dev` is a geno-tools skillset for focused developer workflows. Add capabilities as independent leaf skills when their interfaces are defined.

## Skills

| Skill | Purpose |
|---|---|
| `geno-dev` | Umbrella entry point for the skillset. |
| `meta-mine-skill-creator` | Mine coding-agent sessions for candidate skills and system improvements. |

## Structure

```text
geno-dev/
├── AGENTS.md
├── SKILL.md -> skills/geno-dev/SKILL.md
├── genotools.yaml
├── skills/geno-dev/SKILL.md
├── skills/meta-mine-skill-creator/
│   ├── SKILL.md
│   └── references/
├── docs/index.md
├── docs/getting-started.md
└── mkdocs.yml
```

## Repository rules

- Put each focused capability in `skills/<skill-name>/SKILL.md`.
- Keep every skill directory a leaf; do not nest another `SKILL.md` below it.
- Start descriptions with the conditions that should trigger the skill.
- Use canonical source command names, never installation-specific aliases.
- Keep `.geno/` and `CLAUDE.local.md` untracked.
- Add runtime code only when a workflow needs deterministic reusable behavior, and add tests with it.

## Verification

```bash
geno-tools audit check .
mkdocs build --strict
```
