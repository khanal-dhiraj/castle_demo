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

`npm test` and `npm run typecheck` are stub scripts that print a placeholder and exit 0, so the prompt steps that run them are real (not pretend). Wiring in real test/typecheck infrastructure is each adopter's responsibility.

Secrets live in `.sandcastle/.env` (`ANTHROPIC_API_KEY`, `GH_TOKEN`). `.sandcastle/.env` is gitignored; `.env.example` is the template.

## Architecture

`main.mts` runs an outer loop (up to `MAX_ITERATIONS = 10`) with three phases per iteration:

1. **Plan** — one Opus agent reads `gh issue list --label Sandcastle`, builds a dependency graph, and emits a `<plan>{...}</plan>` JSON block listing only *unblocked* issues with assigned branch names (`sandcastle/issue-{id}-{slug}`). The orchestrator parses that tag — if it's missing, the run throws.
2. **Execute + Review** — each issue runs in its own Docker sandbox via `sandcastle.createSandbox({ branch, ... })`, concurrently under `Promise.allSettled`. Inside each sandbox: implementer (up to 100 iterations) commits to the issue's branch, then if any commits were made, a reviewer (1 iteration) refines on the same branch. `copyToWorktree: ["node_modules"]` skips reinstalling deps per worktree.
3. **Open PR** — a single merger agent on the host branch pushes every branch that produced commits to `origin` and opens a PR per branch with a `Closes #<id>` body. It also swaps the issue's `ready-for-agent` label for `agent-pr-open` so the planner skips it on the next run. Issues auto-close when humans merge the PR.

The outer loop repeats so that issues unblocked by a prior merge get picked up next round. The loop exits early when the planner returns zero issues.

## Prompt files (the "source code")

- `plan-prompt.md` — defines the blocking rules and the `<plan>` output contract `main.mts` parses.
- `implement-prompt.md` — required commit prefix is `RALPH:`; agent must emit `<promise>COMPLETE</promise>` when done; must not close the issue (`Closes #<id>` in the PR body does that on merge).
- `review-prompt.md` — loads `@.sandcastle/CODING_STANDARDS.md` so the standards apply at review time only (saves tokens during implementation). Review commits prefix is `RALPH: Review -`.
- `merge-prompt.md` — `{{BRANCHES}}` and `{{ISSUES}}` are templated from `main.mts`. The merger runs `gh auth setup-git` (so `git push` over HTTPS uses `$GH_TOKEN`), then per branch: pushes to `origin`, opens a PR with `Closes #<id>` in the body, and relabels the issue `ready-for-agent` → `agent-pr-open`.

When changing prompts, keep the contracts `main.mts` depends on: the `<plan>` tag and `issues[].{id,title,branch}` shape, the `RALPH:` commit prefix, and the merger's `<promise>COMPLETE</promise>` terminator.

## Dockerfile notes

`AGENT_UID`/`AGENT_GID` build args default to the host user's UID/GID. On macOS the host GID is often 20, which collides with Debian's `dialout` group — the Dockerfile drops the colliding group before renaming `node` → `agent`. The sandbox bind-mounts the worktree at `/home/agent/workspace` and overrides the working directory there at container start.
