---
title: Skills
order: 5
date: 2026-05-12
tags: [tools]
---

# Skills

Insta-Engineer doesn't replace humans — it concentrates their time on the parts of engineering that are still hard: deciding what to build, sharpening the problem, and reviewing the result.

Four human-facing skills exist to make that concentration sharper.

## /to-prd

Turns a conversation about a feature into a written PRD posted to the issue tracker. The PRD is the durable artifact; the chat history is not.

## /grill-with-docs

A relentless interview that stress-tests a plan against the project's existing glossary and architectural decision records. The output is alignment, plus updates to `CONTEXT.md` and `docs/adr/` captured as decisions crystallize.

## /to-issues

Breaks a plan or PRD into independently-grabbable issues using tracer-bullet vertical slices. Each issue is small enough to ship and self-contained enough to run alongside others.

## /triage

Moves an issue through a small state machine of triage roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. Once an issue is `ready-for-agent`, the daemon takes over.

## The handoff

Together the four skills form a pipeline of their own: PRD → grilling → issues → triage → agent. The agent is the last link in the chain, and the only link that does not sleep.
