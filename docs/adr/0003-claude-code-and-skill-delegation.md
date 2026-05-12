# Claude Code as v1 implementer; skills as the architectural source

The v1 scaffold's implementation agent is Claude Code (via `sandcastle.claudeCode(...)`) and architectural discipline (TDD habits, deep-module enforcement, diagnostic rigor) is delegated to Matt Pocock's slash-invoked skills — `/tdd`, `/improve-codebase-architecture`, `/diagnose` — rather than duplicated as prose in `.sandcastle/` prompts.

Sandcastle supports four agent factories (`claudeCode`, `codex`, `opencode`, `pi`); we picked Claude Code because skills are a Claude Code primitive — Codex has no equivalent and would require inlining each skill's content into our prompts. The lock-in is real but bounded: porting to Codex later is mechanical (copy SKILL.md bodies into the prompts), in the same shape as the GitHub→Linear port.

Skills as the source of truth eliminates a duplication problem: writing our own Ousterhout / red-green-refactor guidance in `CODING_STANDARDS.md` would either drift from Matt's evolving library or become stale. `CODING_STANDARDS.md` is repurposed for project-specific overrides only (naming, error handling, repo conventions). Skills are prebaked into the sandbox Docker image so every container has them available without a runtime install.

The known gap: skills do not pre-commit to interface shape before TDD begins — `/improve-codebase-architecture` is a *post*-implementation skill. v1 mitigates by adding "is this interface deep?" check inside the implement-prompt's TDD cycle (cheap, weak). v2 closes the gap with an "architect-first" orchestration variant that invokes `/grill-with-docs` against the issue + codebase to lock the interface shape before the implementer runs `/tdd`.
