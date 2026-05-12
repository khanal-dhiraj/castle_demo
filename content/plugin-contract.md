---
title: Plugin Contract
order: 4
date: 2026-05-12
tags: [ssg, internals]
---

# Plugin Contract

This site is built by a tiny static site generator that lives in the same repository as the agent automation. Its design encodes a single hypothesis: a project whose features live in physically separate files is a project that AFK agents can work on in parallel without stepping on each other.

## The shape of a plugin

Every feature is a Python file in `plugins/` matching `NN_name.py`. Each file exports one function:

```python
def apply(site: Site) -> None:
    ...
```

The numeric prefix is the position in the Pipeline. The core loads plugins by sorting filenames alphabetically. So `10_load.py` runs before `30_markdown.py` runs before `90_write.py`.

## What plugins do

Plugins mutate a shared `Site` object in place. The `Site` holds a list of `Page`s and a dictionary of output paths to bytes. A plugin might:

- Walk `content/` and create `Page`s.
- Parse frontmatter and strip it from a body.
- Render Markdown into HTML.
- Wrap HTML in a Jinja template.
- Highlight code blocks.
- Emit a feed.

Each is a single file. Each is a single issue.

## Why numbered files

A registry with phases and decorators would be more "engineering-correct." We chose numbered files because the directory listing is the pipeline — an audience watching a pull request land can read one file and understand exactly where it sits. Gaps of ten leave room for newcomers; the writer is pinned at `90`.

The full reasoning is in `docs/adr/0001-plugin-contract.md`.
