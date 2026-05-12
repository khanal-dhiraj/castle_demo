---
title: The State Machine
order: 2
date: 2026-05-12
tags: [agent-flow]
---

# The State Machine

Every issue Insta-Engineer touches passes through four labels. At any moment, an issue carries exactly one of them.

| Label | Set by | Meaning |
|---|---|---|
| `ready-for-agent` | Triage skill or a human | Queued; the daemon will pick it up. |
| `agent-working` | Daemon | A run is in flight. |
| `agent-pr-open` | Daemon | A draft pull request is ready for human review. |
| `agent-failed` | Daemon | Run errored or produced no commits; relabel `ready-for-agent` to retry. |

The transitions are deliberately one-directional. A human can re-label `agent-failed` back to `ready-for-agent` to retry, but the daemon never reverses its own moves.

## Where labels come from

The `ready-for-agent` label is borrowed from the triage skill's vocabulary of roles like `needs-triage`, `needs-info`, and `ready-for-agent`. Insta-Engineer extends that vocabulary with three agent-state labels (`agent-working`, `agent-pr-open`, `agent-failed`) and a polling daemon that observes the first and produces the rest.

## What humans do, what the daemon does

Humans label issues. The daemon labels runs. The boundary is sharp: every state transition is the responsibility of exactly one actor, and the label set tells you whose turn it is at any moment.
