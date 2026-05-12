# castle_demo

Demo repo for testing Sandcastle parallel-planner-with-review orchestration.

## Getting started

Run the following once to build the Docker image:

```bash
npx sandcastle docker build-image
```

Then start the orchestrator:

```bash
npx tsx .sandcastle/main.mts
```

## How it works

- **Plan**: An initial planning phase breaks the work into discrete, parallelizable tasks.
- **Execute + Review**: Tasks run in parallel, with each execution reviewed for quality.
- **Merge**: Reviewed results are merged back together into the final outcome.
