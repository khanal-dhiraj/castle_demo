# TASK

For each branch listed below, push it to `origin` and open a pull request
against `main`. Do not merge anything locally — humans review and merge the
PRs themselves.

Branches:

{{BRANCHES}}

Issues:

{{ISSUES}}

Each branch is named `sandcastle/issue-{id}-{slug}`, so the `{id}` in the
branch name maps to the issue ID in the list above.

# SETUP

Run this once before pushing so `git push` over HTTPS can use `$GH_TOKEN`:

```
gh auth setup-git
```

# FOR EACH BRANCH

1. `git push origin <branch>` — publish the work done in the sandbox.
2. `gh pr create --base main --head <branch> --title "<issue title>" --body "<body>"`
   where the body starts with `Closes #<id>` (GitHub then auto-closes the
   issue when the PR merges) and includes a short summary of what changed.
3. Swap the issue's labels so the planner skips it on the next run:
   `gh issue edit <id> --remove-label insta-engineer --add-label agent-pr-open`

Do NOT run `git merge`. Do NOT run `gh issue close` — the `Closes #<id>`
keyword in the PR body handles that automatically on merge.

If a step fails (e.g. push rejected, PR already exists), continue with the
remaining branches and note the failure in your final output.

Once you've opened a PR for every branch you can, output
<promise>COMPLETE</promise>.
