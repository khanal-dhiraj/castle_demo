# TASK

Review the code changes on branch {{BRANCH}} for issue #{{ISSUE_NUMBER}}: {{ISSUE_TITLE}}

# CONTEXT

Here are the last 10 commits:

<recent-commits>

!`git log -n 10 --format="%H%n%ad%n%B---" --date=short`

</recent-commits>

<issue>

!`gh issue view {{ISSUE_NUMBER}}`

</issue>

<diff-to-main>

!`git diff main..HEAD`

</diff-to-main>

# REVIEW PROCESS

1. **Architectural review (skill).** Run the `/improve-codebase-architecture` skill against the diff. Let it identify shallow modules, leaky interfaces, and refactoring opportunities. Apply its refactors (deepening shallow modules, narrowing interfaces) before approving.

2. **Project-specific overrides.** Then load `@.sandcastle/CODING_STANDARDS.md` and apply any rules the architecture skill does not already cover.

3. **Preserve functionality.** Never change what the code does — only how it does it. All original features, outputs, and behaviors must remain intact.

# EXECUTION

If you find improvements to make:

1. Make the changes directly on this branch.
2. Run `npm run typecheck` and `npm run test` to ensure nothing is broken.
3. Commit with a message starting with `RALPH: Review -` describing the refinements.

If the code is already clean and the skill surfaces no actionable refactors, do nothing.

Once complete, output <promise>COMPLETE</promise>.
