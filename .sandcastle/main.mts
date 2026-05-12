// Smoke test — one agent, one sandbox, one tiny task.
// Usage: npx tsx .sandcastle/main.mts

import * as sandcastle from "@ai-hero/sandcastle";
import { docker } from "@ai-hero/sandcastle/sandboxes/docker";

const result = await sandcastle.run({
  agent: sandcastle.claudeCode("claude-sonnet-4-6"),
  sandbox: docker(),
  branchStrategy: { type: "branch", branch: "sandcastle/hello-demo" },
  name: "hello-demo",
  prompt: [
    "Create a file named hello.txt in the current directory.",
    "Its contents should be a single line: a friendly one-sentence greeting from the agent.",
    "Then run `git add hello.txt && git commit -m 'add hello.txt'`.",
    "When the commit is done, output <promise>COMPLETE</promise> on its own line.",
  ].join("\n"),
  // Default file logging writes to .sandcastle/logs/<run>.log
});

console.log("\n--- Run result ---");
console.log("Branch:           ", result.branch);
console.log("Iterations:       ", result.iterations.length);
console.log("Completion signal:", result.completionSignal);
console.log("Commits:          ", result.commits);
console.log("Log file:         ", result.logFilePath);
