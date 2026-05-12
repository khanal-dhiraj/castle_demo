# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repo hosts **Insta-Engineer**: a self-working software engineer demo. It has two halves under one name.

- **The agent automation** (`.sandcastle/`) — a Sandcastle-driven, label-triggered flow that polls GitHub for issues labeled `ready-for-agent`, runs a Claude Code agent in a Docker sandbox, and opens a draft PR.
- **The product** (`insta_engineer/`, `plugins/`, `content/`) — a plugin-based Python static site generator whose generated site documents the agent automation. New features land as numbered plugin files in `plugins/NN_name.py` (see [`docs/adr/0001-plugin-contract.md`](docs/adr/0001-plugin-contract.md)).

When the user asks to "run sandcastle" or "process issues", they mean starting `.sandcastle/daemon.mts`. When they ask to add product code, the SSG is the target — and the plugin contract is the convention. See [`CONTEXT.md`](CONTEXT.md) for the domain glossary.

## Common commands

```bash
# Agent automation
npm run sandcastle:labels          # Seed/update GitHub labels.
npm run sandcastle:daemon          # Long-running daemon (60s polling).
npm run sandcastle:once            # One-shot: process the oldest ready issue.

# SSG (run from the repo root)
python3 -m insta_engineer.cli build    # Build content/ → dist/. No install needed.
pytest                                  # Run the sanity test.
```

The Docker sandbox ships with `python3`, a pre-baked venv on PATH containing `markdown-it-py`, `python-frontmatter`, `jinja2`, `pygments`, and `pytest`. Agents inside the sandbox can run `pytest` directly without setup.

## Label state machine

Labels are the source of truth for issue state. The trigger label (`ready-for-agent`) comes from Matt Pocock's [triage skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/triage/SKILL.md); the `agent-*` states are extensions for the agent's own lifecycle.

| Label | Who sets | Meaning |
|---|---|---|
| `ready-for-agent` | triage skill / human | Queued for the daemon to pick up. |
| `agent-working` | daemon | Sandcastle run is in flight. |
| `agent-pr-open` | daemon | Draft PR opened; awaiting review/merge. |
| `agent-failed` | daemon | Run errored or produced no commits. Relabel `ready-for-agent` to retry. |

Flow: `... → ready-for-agent → agent-working → (agent-pr-open | agent-failed)`. Each transition removes the prior agent-state label and adds the new one, preserving the triage skill's "exactly one state at a time" invariant.

Full label set (categories + triage states + agent states) is defined in `.sandcastle/labels.json` and seeded by `npm run sandcastle:labels`.

## Sandcastle architecture

`.sandcastle/main.mts` exports `runIssue(issue)` — the per-issue execution. Calls `sandcastle.run()` with:
- `agent: claudeCode("claude-opus-4-7")` — **model ID is hard-coded; keep it as `claude-opus-4-7`**.
- `sandbox: docker()` — uses the image built from `.sandcastle/Dockerfile`.
- `branchStrategy: { type: "branch", branch }` where `branch = sandcastle/issue-<N>` — one branch per issue.
- `promptFile: .sandcastle/issue-prompt.md` with `{{TASK_ID}}`/`{{ISSUE_TITLE}}`/`{{ISSUE_BODY}}`/`{{BRANCH}}` substitution.

When `main.mts` is invoked as a CLI (via `sandcastle:once`), it picks the oldest open `ready-for-agent` issue and calls `runIssue` once with no label transitions.

`.sandcastle/daemon.mts` is the long-running orchestrator:
1. Every 60s, fetch the oldest open `ready-for-agent` issue.
2. Transition label to `agent-working`.
3. `runIssue(issue)`.
4. On success with commits: `git push -u origin <branch>` from the repo root (the worktree gets torn down after a clean run, but the branch ref persists in `.git/`), `gh pr create --draft` with `Closes #N` in the body, then transition to `agent-pr-open`.
5. On error or no-commits: transition to `agent-failed` and post a comment explaining how to retry.
6. If a PR already exists for the branch (re-run case), re-use it instead of erroring.

Existing template prompts `plan-prompt.md` / `implement-prompt.md` / `merge-prompt.md` come from the upstream `parallel-planner` scaffold and are **not wired into anything** — they're kept as reference for a future multi-agent planner/merger flow. Our daemon uses `issue-prompt.md` exclusively.

## Docker sandbox

`.sandcastle/Dockerfile` builds the per-run sandbox image:

- Base: `node:22-bookworm` with `git`, `curl`, `jq`, and the GitHub CLI.
- UID/GID alignment via `AGENT_UID`/`AGENT_GID` build args (defaulted by Sandcastle to the host user) so bind-mounted files share an owner without runtime chown. The macOS-specific groupdel dance handles GID 20 colliding with Debian's `dialout` group — don't remove it.
- Renames the base `node` user to `agent`, installs Claude Code CLI under `/home/agent/.local/bin`.
- Sandcastle bind-mounts the git worktree at `/home/agent/workspace` at container start, so the project root inside the container is `/home/agent/workspace`.

## Required environment

`.sandcastle/.env` (gitignored; example in `.sandcastle/.env.example`) must contain:

- `ANTHROPIC_API_KEY` — for the Claude Code agent.
- `GH_TOKEN` — for the `gh` calls inside `main.mts` and `daemon.mts`, plus the agent's own `gh` use inside the sandbox.

The host process running the daemon also needs `gh` authenticated (`gh auth status`) since it shells out for label transitions, issue lookup, branch push, and PR creation.

## Working with issues

1. Create a GitHub issue.
2. Apply `ready-for-agent` (manually or via the triage skill).
3. If the daemon is running (`npm run sandcastle:daemon`), it'll pick the issue up within 60s. Otherwise run `npm run sandcastle:once` for a one-off.
4. On success, you'll see the issue transition to `agent-pr-open` with a draft PR linked via `Closes #N`. Review, mark ready, merge — the issue auto-closes.
5. On `agent-failed`, read the comment posted by the daemon, then re-label `ready-for-agent` to retry.
