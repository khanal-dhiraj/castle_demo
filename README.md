# Insta-Engineer

A self-working software engineer demo. AFK agents drive GitHub issues to merged pull requests, building a Python static site whose content documents the very system that built it.

## Two halves

- **The agent automation** (`.sandcastle/`, `CLAUDE.md`) — a polling daemon watches GitHub for issues labeled `ready-for-agent`, runs a Claude Code agent inside a Docker sandbox, and opens a draft pull request when it's done.
- **The site** (`insta_engineer/`, `plugins/`, `content/`) — a plugin-based static site generator whose generated site explains the agent automation. Every plugin lives in its own file and is added by a single AFK-agent run.

The recursion is the demo: agents build a site that explains the system they're part of.

## Quick start

```bash
# Build the site (no install required when run from the repo root).
python3 -m insta_engineer.cli build

# Or, if you want the `insta-engineer` command on PATH:
pip install -e .
insta-engineer build

# Run the sanity test.
pytest
```

The build reads `content/`, walks `plugins/` in filename order, and writes to `dist/`.

## Layout

```
.sandcastle/         Agent automation: daemon, prompt, Dockerfile.
insta_engineer/      Static site generator (Site, Page, plugin loader, CLI).
plugins/             Numbered plugin files; the directory listing is the Pipeline.
content/             Source Markdown for the docs site.
docs/adr/            Architecture decision records.
tests/               Pytest sanity tests.
CONTEXT.md           Glossary and relationships.
CLAUDE.md            Agent-facing repo orientation.
```

## See also

- `CONTEXT.md` for the domain glossary.
- `docs/adr/0001-plugin-contract.md` for the rationale behind the plugin shape.
- `CLAUDE.md` for the agent-automation overview.
