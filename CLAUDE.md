# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A demo of Sandcastle's parallel-planner-with-review orchestration. The "product" here is the orchestration itself: `.sandcastle/main.mts` plus the four prompt files in `.sandcastle/`. There is no application code — the agents it spawns produce code in response to GitHub issues labeled `Sandcastle`.

## Commands

```bash
# One-time: build the Docker image agents run inside.
# Uses the host UID/GID via build-args so bind-mounted files don't get root-owned.
npx sandcastle docker build-image

# Run the orchestrator loop.
npx tsx .sandcastle/main.mts
```

`npm test` is a placeholder that exits 1, and there is no `npm run typecheck`. The implementer/reviewer/merge prompts tell agents to run those commands — they will fail until real scripts are wired up. Treat that as a known gap, not a bug to fix unless asked.

Secrets live in `.sandcastle/.env` (`ANTHROPIC_API_KEY`, `GH_TOKEN`). `.sandcastle/.env` is gitignored; `.env.example` is the template.

## Architecture

`main.mts` runs an outer loop (up to `MAX_ITERATIONS = 10`) with three phases per iteration:

1. **Plan** — one Opus agent reads `gh issue list --label Sandcastle`, builds a dependency graph, and emits a `<plan>{...}</plan>` JSON block listing only *unblocked* issues with assigned branch names (`sandcastle/issue-{id}-{slug}`). The orchestrator parses that tag — if it's missing, the run throws.
2. **Execute + Review** — each issue runs in its own Docker sandbox via `sandcastle.createSandbox({ branch, ... })`, concurrently under `Promise.allSettled`. Inside each sandbox: implementer (up to 100 iterations) commits to the issue's branch, then if any commits were made, a reviewer (1 iteration) refines on the same branch. `copyToWorktree: ["node_modules"]` skips reinstalling deps per worktree.
3. **Merge** — a single merger agent on the host branch merges every branch that produced commits, runs typecheck/test, and closes the corresponding issues with `gh issue close`.

The outer loop repeats so that issues unblocked by a prior merge get picked up next round. The loop exits early when the planner returns zero issues.

## Prompt files (the "source code")

- `plan-prompt.md` — defines the blocking rules and the `<plan>` output contract `main.mts` parses.
- `implement-prompt.md` — required commit prefix is `RALPH:`; agent must emit `<promise>COMPLETE</promise>` when done; must not close the issue (merger does that).
- `review-prompt.md` — loads `@.sandcastle/CODING_STANDARDS.md` so the standards apply at review time only (saves tokens during implementation). Review commits prefix is `RALPH: Review -`.
- `merge-prompt.md` — `{{BRANCHES}}` and `{{ISSUES}}` are templated from `main.mts`.

When changing prompts, keep the contracts `main.mts` depends on: the `<plan>` tag and `issues[].{id,title,branch}` shape, and the `RALPH:` commit prefix that the merger relies on for `gh issue close` semantics.

## Dockerfile notes

`AGENT_UID`/`AGENT_GID` build args default to the host user's UID/GID. On macOS the host GID is often 20, which collides with Debian's `dialout` group — the Dockerfile drops the colliding group before renaming `node` → `agent`. The sandbox bind-mounts the worktree at `/home/agent/workspace` and overrides the working directory there at container start.
