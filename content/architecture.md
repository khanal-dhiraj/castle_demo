---
title: Architecture
order: 3
date: 2026-05-12
tags: [internals]
---

# Architecture

Insta-Engineer runs three components in concert.

## The daemon

A long-running process that polls GitHub every sixty seconds for issues carrying `ready-for-agent`. When it finds one, it transitions the label to `agent-working`, hands the issue to the Sandcastle library, then either opens a draft pull request on success or comments a retry hint on failure.

The daemon is intentionally simple: a single `while true` loop. It currently processes one issue per tick. Concurrency is a future enhancement — the underlying library already supports it.

## The Sandcastle library

Sandcastle is the engine that turns "an issue and a branch name" into "an agent making commits on that branch." It spins up a Docker container, mounts a fresh git worktree inside, drops the agent in, hands it a prompt, and waits for the completion signal.

Each run is hermetic. The agent's filesystem changes are confined to a worktree. When the run finishes, Sandcastle pushes the branch if commits were produced and tears the worktree down.

## The sandbox

The container is a Node base image with Python, the GitHub CLI, and the Claude Code CLI pre-installed. The agent inside has its own GitHub token and acts as itself — reading the issue, exploring the repo, running tests, committing, and signaling completion.

The image runs as a non-root user whose UID and GID are aligned with the host's user. That's why bind-mounted files don't need a runtime ownership fix.
