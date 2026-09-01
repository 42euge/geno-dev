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
