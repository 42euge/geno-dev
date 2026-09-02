# geno-dev

Developer workflow skills for coding agents.

## Installation

```bash
geno-tools install geno-dev
```

## Skills

| Skill | Purpose |
|---|---|
| `meta-mine-skill-creator` | Mine local Claude Code and Codex sessions for reusable workflows, user corrections, candidate skills, and system improvements. |

## CLI

The `geno-dev usage` commands provide a shared local invocation recorder for
skills. Record and inspect an invocation with:

```bash
geno-dev usage record example-skill --trigger explicit
geno-dev usage report example-skill --days 30
```

The SQLite ledger at `~/.geno/skill-usage.sqlite3` contains only the skill name,
UTC timestamp, and explicit, implicit, or unknown trigger. It never uploads
usage data.

The `geno-dev eval` commands replay a behavioral case against a skill through
an Anthropic-powered actor and independent judge:

```bash
geno-dev eval validate docs/examples/branch-after-selection.eval.json --json
geno-dev eval run docs/examples/branch-after-selection.eval.json \
  --skill path/to/SKILL.md --model claude-sonnet-5 --json
```

Live runs require `ANTHROPIC_API_KEY`. See [Skill evaluations](docs/skill-evals.md)
for the case format, thresholds, exit statuses, and privacy boundary.

Installing the skillset with `geno-tools` installs the `geno-dev` command in
the managed runtime.

## Development

```bash
python3 -m pip install -e '.[test]'
pytest
geno-tools audit check .
mkdocs build --strict
```

## Documentation

See [Getting Started](docs/getting-started.md).

## License

MIT
