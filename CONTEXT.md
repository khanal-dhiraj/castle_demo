# Insta-engineer

A cloud-deployable scaffold built on Sandcastle: users clone or fork the repo, customize orchestration + prompts, deploy somewhere, and then assign GitHub issues to it. The scaffold runs the orchestrator, which writes code + tests against the issue and opens a PR.

## Language

**Insta-engineer**:
The whole deployable system — scaffold + orchestrator + trigger + sandbox. Not a single agent.
_Avoid_: "the bot", "the agent" (those are sub-parts)

**Scaffold**:
The repo template a user clones to get Insta-engineer running on their own codebase. Includes `.sandcastle/`, deployment recipe, and conventions.
_Avoid_: "template" (sandcastle already uses "template" for its built-in starters)

**Orchestrator**:
The Node program at `.sandcastle/main.mts` that drives one or more agent runs per issue. **v1 ships a single flagship orchestration** — `parallel-planner-with-review` — not a config-switchable menu. "Swappable" means file replacement: adopters fork and edit, or copy a different sandcastle template. v2 adds an alternate `main-architect.mts` (architect-first variant invoking `/grill-with-docs` before TDD).
_Avoid_: "the runner", "the loop"

**Sandcastle template**:
A built-in starter (blank / simple-loop / sequential-reviewer / parallel-planner / parallel-planner-with-review) that sandcastle ships. The current scaffold is derived from `parallel-planner-with-review`.

**Implementation agent**:
The Claude Code instance that runs *inside* a sandbox during the Execute phase to actually write code for one issue. Distinct from the orchestrator. **v1 locked to Claude Code** — relies on slash-invoked **Skills** for architectural discipline. Codex support is a v2 port.

**Skill**:
A slash-invokable behavior pack the agent loads at runtime (Claude Code primitive). Insta-engineer leans on Matt Pocock's `tdd`, `improve-codebase-architecture`, `diagnose`, and `grill-with-docs` skills as the source of truth for "good code" — instead of duplicating that content in custom prompts. Skills are prebaked into the sandbox Docker image so every container is born skill-ready.

**Issue tracker substrate**:
The system of record for tickets. Locked to **GitHub** for v1. Linear is a planned port (Linear MCP is available; skills are already pluggable across substrates).

**Trigger**:
The mechanism that wakes the orchestrator when a new issue arrives. Not provided by sandcastle — Insta-engineer supplies it. **v1**: GitHub Action listening for `issues.labeled` where label == `insta-engineer`, running on a GH-hosted `ubuntu-latest` runner. Graduation path: same orchestrator behind a webhook + always-on worker (Fly/Modal/Render) when GH Action limits bite.

**Deep module** (Ousterhout):
A unit of code with lots of internal functionality behind a narrow interface. Cheap to test in isolation; hard for callers to misuse. Insta-engineer treats producing deep modules as a v1 hard constraint, not an aesthetic preference.

**Shallow module**:
A unit of code where the interface is nearly as wide as the implementation — thin wrappers, leaky abstractions, types-with-getters. Symptoms: tests need to mock many dependencies; small behavior changes ripple across many callers. Shallow modules erode the TDD feedback loop.

**Feedback rate**:
The wall-clock time from "agent makes a change" to "agent learns whether it was correct." The system's speed limit (Pragmatic Programmer's "don't outrun your headlights"). LLMs default to batching too much before checking; the scaffold's job is to enforce small steps so feedback stays tight.

## Relationships

- **Insta-engineer** = **Scaffold** + **Orchestrator** + **Trigger** + sandbox provider
- An **Orchestrator** invokes one or more **Implementation agent**s per issue
- An **Implementation agent** reads + writes the **Issue tracker substrate** via `gh` CLI
- A **Scaffold** is derived from a **Sandcastle template** plus Insta-engineer-specific conventions (commit prefix, label, branch naming)
- **Deep modules** preserve **feedback rate**; **shallow modules** degrade it
- **Skills** (`/tdd`, `/improve-codebase-architecture`) are the source of architectural discipline; **CODING_STANDARDS.md** holds only project-specific overrides
- **Implementation agent** invokes **Skills** at runtime; therefore v1 locks to Claude Code as the implementer

## Example dialogue

> **Dev:** "If I fork the **Scaffold** and change the **Orchestrator** to `simple-loop`, does the **Trigger** still work?"
> **Designer:** "Yes — the **Trigger** only needs to invoke `npx tsx .sandcastle/main.mts`. It doesn't care which **Sandcastle template** you derived from."

## Flagged ambiguities

_None yet._
