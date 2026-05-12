# Task

Implement GitHub issue **#{{TASK_ID}}** on branch `{{BRANCH}}`.

## Issue title
{{ISSUE_TITLE}}

## Issue body
{{ISSUE_BODY}}

# Context

Recent commits on this repo:

<recent-commits>

!`git log -n 10 --format="%h %ad %s" --date=short`

</recent-commits>

# Exploration

Read the repo before writing code. Understand what exists and what convention to follow. If the issue is ambiguous, make the most reasonable interpretation and note your assumption in the commit message — do not stall.

# Execution

- Add only what the issue requires; do not invent unrelated scaffolding.
- If tests exist and are relevant to your change, run them and ensure they pass before committing.
- If a typecheck script exists (`npm run typecheck`), run it before committing.
- If this is a Python project (a `pyproject.toml` exists), run `pytest` from the repo root before committing. The sandbox already has the dependencies installed in a pre-baked venv on `PATH`, so no `pip install` is needed.
- Make ONE git commit per logical change with a clear message describing the change.

# Completion

Once the issue is implemented and committed on branch `{{BRANCH}}`, output `<promise>COMPLETE</promise>` on its own line.

# Rules

- ONLY work on this issue. Do not touch unrelated files.
- Do not close the issue — that happens automatically when the PR merges.
