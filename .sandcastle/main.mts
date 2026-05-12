// Single-issue runner: pick the oldest open Sandcastle-labeled issue,
// run one agent on it, commit on its own branch.
// Usage: npx tsx .sandcastle/main.mts

import * as sandcastle from "@ai-hero/sandcastle";
import { docker } from "@ai-hero/sandcastle/sandboxes/docker";
import { execSync } from "node:child_process";

// 1. Fetch the oldest open issue with the Sandcastle label.
const issuesJson = execSync(
  `gh issue list --state open --label Sandcastle --json number,title,body --limit 1`,
  { encoding: "utf8" },
);
const [issue] = JSON.parse(issuesJson) as {
  number: number;
  title: string;
  body: string;
}[];

if (!issue) {
  console.error("No open Sandcastle-labeled issues. Create one and rerun.");
  process.exit(1);
}

const branch = `sandcastle/issue-${issue.number}`;
console.log(`Picked issue #${issue.number}: ${issue.title}`);
console.log(`Working on branch: ${branch}\n`);

// 2. Run one agent on its own branch.
const result = await sandcastle.run({
  agent: sandcastle.claudeCode("claude-opus-4-7"), // always use claude-opus-4-7 
  sandbox: docker(),
  branchStrategy: { type: "branch", branch },
  name: `issue-${issue.number}`,
  prompt: [
    `# Task`,
    `Implement GitHub issue #${issue.number} on this branch.`,
    ``,
    `## Issue title`,
    issue.title,
    ``,
    `## Issue body`,
    issue.body || "(no body)",
    ``,
    `## Rules`,
    `- Read the repo structure first. It is a fresh TypeScript repo.`,
    `- Add only what the issue requires; do not invent unrelated scaffolding.`,
    `- If you create tests, run them and ensure they pass before committing.`,
    `- Make ONE git commit per logical change, with a clear message.`,
    `- When done, output <promise>COMPLETE</promise> on its own line.`,
  ].join("\n"),
  maxIterations: 30, // give it room to read, edit, test, iterate
});

console.log("\n--- Run result ---");
console.log("Branch:           ", result.branch);
console.log("Iterations used:  ", result.iterations.length);
console.log("Completion signal:", result.completionSignal);
console.log("Commits:          ", result.commits.map((c) => c.sha));
console.log("Log file:         ", result.logFilePath);
