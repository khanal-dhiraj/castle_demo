// Idempotently create the labels defined in .sandcastle/labels.json on the
// current GitHub repo (resolved by `gh` from the working directory's git remote).
// Usage: npx tsx .sandcastle/seed-labels.mts

import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

interface Label {
  name: string;
  color: string;
  description: string;
}

interface LabelsFile {
  categories: Label[];
  triageStates: Label[];
  agentStates: Label[];
}

const here = dirname(fileURLToPath(import.meta.url));
const labels: LabelsFile = JSON.parse(
  readFileSync(resolve(here, "labels.json"), "utf8"),
);

const all = [...labels.categories, ...labels.triageStates, ...labels.agentStates];

for (const label of all) {
  try {
    execFileSync(
      "gh",
      [
        "label",
        "create",
        label.name,
        "--color",
        label.color,
        "--description",
        label.description,
        "--force", // updates if it already exists
      ],
      { stdio: ["ignore", "inherit", "inherit"] },
    );
    console.log(`✓ ${label.name}`);
  } catch (err) {
    console.error(`✗ ${label.name}: ${(err as Error).message}`);
    process.exitCode = 1;
  }
}
