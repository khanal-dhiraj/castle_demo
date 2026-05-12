// Single-issue runner. Exports runIssue() for the daemon; when invoked as a
// CLI, picks the oldest open `ready-for-agent` issue and runs once.
// Usage: npx tsx .sandcastle/main.mts

import * as sandcastle from "@ai-hero/sandcastle";
import { docker } from "@ai-hero/sandcastle/sandboxes/docker";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

export interface Issue {
  number: number;
  title: string;
  body: string;
}

const here = dirname(fileURLToPath(import.meta.url));
const PROMPT_FILE = resolve(here, "issue-prompt.md");

/** Resolve the branch name used for a given issue. */
export function branchForIssue(issue: Issue): string {
  return `sandcastle/issue-${issue.number}`;
}

/** Run the Sandcastle agent against a single issue on its own branch. */
export async function runIssue(issue: Issue) {
  const branch = branchForIssue(issue);
  console.log(`→ Running issue #${issue.number} on branch ${branch}`);

  return sandcastle.run({
    agent: sandcastle.claudeCode("claude-opus-4-7"), // always use claude-opus-4-7
    sandbox: docker(),
    branchStrategy: { type: "branch", branch },
    name: `issue-${issue.number}`,
    promptFile: PROMPT_FILE,
    promptArgs: {
      TASK_ID: String(issue.number),
      ISSUE_TITLE: issue.title,
      ISSUE_BODY: issue.body || "(no body)",
      BRANCH: branch,
    },
    maxIterations: 30,
  });
}

/** Fetch the oldest open issue carrying the given label. Returns null if none. */
export function pickOldestIssueWithLabel(label: string): Issue | null {
  const json = execFileSync(
    "gh",
    [
      "issue",
      "list",
      "--state",
      "open",
      "--label",
      label,
      "--json",
      "number,title,body",
      "--limit",
      "1",
    ],
    { encoding: "utf8" },
  );
  const issues = JSON.parse(json) as Issue[];
  return issues[0] ?? null;
}

// CLI entry: one-shot picker, useful for manual runs / smoke tests.
const isMain = process.argv[1] === fileURLToPath(import.meta.url);
if (isMain) {
  const issue = pickOldestIssueWithLabel("ready-for-agent");
  if (!issue) {
    console.error("No open issues labeled `ready-for-agent`.");
    process.exit(1);
  }
  const result = await runIssue(issue);
  console.log("\n--- Run result ---");
  console.log("Branch:           ", result.branch);
  console.log("Iterations used:  ", result.iterations.length);
  console.log("Completion signal:", result.completionSignal);
  console.log("Commits:          ", result.commits.map((c) => c.sha));
  console.log("Log file:         ", result.logFilePath);
}
