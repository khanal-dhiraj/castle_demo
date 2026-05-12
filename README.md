# Insta-engineer

A deployable scaffold built on [sandcastle](https://github.com/mattpocock/sandcastle) that turns labeled GitHub issues into PRs. TDD and deep-module architectural discipline are baked in by way of slash-invoked skills (`/tdd`, `/improve-codebase-architecture`) prebaked into the agent sandbox. See [`CONTEXT.md`](CONTEXT.md) for the project's vocabulary and [PRD #19](https://github.com/khanal-dhiraj/castle_demo/issues/19) for the v1 design.

## Prerequisites

- A GitHub account.
- An Anthropic API key with billing enabled.
- A GitHub repository you control to deploy onto (created from this scaffold via "Use this template").

## Setup

Target: under 10 minutes, including the first Action's cold-start.

1. Click **Use this template** on this repo and create a new repository under your account.
2. In the new repo, go to **Settings → Secrets and variables → Actions → New repository secret** and add two secrets:
   - `ANTHROPIC_API_KEY` — your Anthropic API key.
   - `GH_TOKEN` — a fine-grained personal access token (**Settings → Developer settings → Personal access tokens → Fine-grained tokens**) scoped to the new repo with the following repository permissions: `Issues: Read and write`, `Contents: Read and write`, `Pull requests: Read and write`.
3. Confirm the `insta-engineer` label exists on the repo (**Issues → Labels**). If not, create it — name must match exactly.

## Triggering a run

1. Open a new issue or pick an existing one.
2. Apply the `insta-engineer` label.
3. Watch the run in the **Actions** tab. The workflow is `insta-engineer`; the job builds the sandbox image (cold-start 3–5 min on first run, layer-cached after) and then runs the orchestrator.
4. On completion, a PR appears against the default branch. Review and merge using your normal workflow.

## What good tickets look like

The agent works best with issues that are:

- **Clearly scoped** — one slice of work, one deliverable.
- **Self-contained** — acceptance criteria you can check by reading the diff, not by tracing hidden dependencies across other files or systems.
- **Specific about acceptance** — explicit success conditions in the issue body. "Add a `greet(name)` function with one passing test" beats "improve greeting logic."

v1 does not ship an issue template. Authoring conventions are yours to define.

## Troubleshooting

- **First run is slow.** The initial workflow run builds the sandbox Docker image (3–5 min). Subsequent runs reuse cached layers and start the orchestrator within ~30s of the label event. This is expected.
- **UID / file-ownership issues.** Only relevant if you fork the `.sandcastle/Dockerfile`. The sandcastle CLI auto-passes `AGENT_UID=$(id -u)` and `AGENT_GID=$(id -g)`; on `ubuntu-latest` that resolves to `1001 / 127`. The Dockerfile already handles the macOS GID-20 / `dialout` collision for local dev. Leave the existing handling in place.
- **Missing secrets.** The orchestrator step fails immediately with `ANTHROPIC_API_KEY` or `GH_TOKEN` undefined. Recheck **Settings → Secrets and variables → Actions** — both must be set as *repository* secrets (not environment secrets) and the names must match exactly.
- **Running locally instead of via the Action.** Copy `.sandcastle/.env.example` to `.sandcastle/.env`, fill in the same two values, then `npx sandcastle docker build-image && npx tsx .sandcastle/main.mts`. Useful when iterating on prompts. The Action and the local CLI run the same orchestrator.

## Architectural discipline

The implementer agent invokes `/tdd` for its inner red-green-refactor loop. The reviewer agent invokes `/improve-codebase-architecture` against the diff to surface shallow modules and refactor toward narrow-interface / broad-behavior shape. Both skills are sourced from `mattpocock/skills` and prebaked into the sandbox image, so they fire without a runtime install. Project-specific overrides — naming, error handling, repo layout — live in [`.sandcastle/CODING_STANDARDS.md`](.sandcastle/CODING_STANDARDS.md); the reviewer loads them after running the architecture skill. See [ADR-0003](docs/adr/0003-claude-code-and-skill-delegation.md) for the rationale.

## Graduation paths

### v2 architect-first orchestration

When `/improve-codebase-architecture`'s *post-hoc* refactoring becomes a bottleneck, add a sibling `.sandcastle/main-architect.mts` that runs `/grill-with-docs` against the issue + codebase to lock the interface shape before `/tdd` begins. Adopt by renaming files; the trigger stays the same. Scope and rationale: [ADR-0003](docs/adr/0003-claude-code-and-skill-delegation.md) and the "Out of Scope" section of [PRD #19](https://github.com/khanal-dhiraj/castle_demo/issues/19).

### Linear substrate

Replace `gh` CLI calls in the prompts with Linear MCP equivalents. Skills are already substrate-pluggable. Roughly a day's work. Rationale: [ADR-0001](docs/adr/0001-github-as-v1-substrate.md); v1 deferral noted in [PRD #19](https://github.com/khanal-dhiraj/castle_demo/issues/19).

### Webhook + always-on worker

When the GitHub Action's 6-hour job ceiling or per-minute billing starts to bite, replace the `.github/workflows/insta-engineer.yml` trigger with a webhook handler on Fly / Modal / Render that runs the same `npx tsx .sandcastle/main.mts`. Orchestrator code is unchanged. Rationale: [ADR-0002](docs/adr/0002-github-action-as-v1-trigger.md); v1 deferral noted in [PRD #19](https://github.com/khanal-dhiraj/castle_demo/issues/19).

## Cost expectations

Per labeled issue, order-of-magnitude:

- **Anthropic billing:** roughly $1–$3 per issue, from 4–8 Opus calls (1 planner + 1–N implementer + 1–N reviewer + 1 merger).
- **GitHub Actions minutes:** 3–5 minutes per issue, dominated by the Docker image build on a cold cache.

Both figures scale with issue complexity. Budget accordingly before bulk-labeling.

## Links

- [`CONTEXT.md`](CONTEXT.md) — project vocabulary.
- [ADR-0001](docs/adr/0001-github-as-v1-substrate.md) — GitHub as v1 substrate.
- [ADR-0002](docs/adr/0002-github-action-as-v1-trigger.md) — GitHub Action as v1 trigger.
- [ADR-0003](docs/adr/0003-claude-code-and-skill-delegation.md) — Claude Code + skill delegation.
- [PRD #19](https://github.com/khanal-dhiraj/castle_demo/issues/19) — v1 ship plan.
