# Plugin contract: numbered filename + `apply(site)`

Every SSG feature is a **Plugin** at `plugins/NN_name.py` exporting `def apply(site: Site) -> None`. The core sorts plugins alphabetically by filename and invokes each in turn against a shared mutable **Site**. Numeric prefixes use gaps of 10 (`10`, `20`, `30`, ...) so new plugins can slot in without renumbering.

We chose this over (β) a decorator-based phased-hook registry and (γ) typed plugin base classes because the project is a demo of AFK-agent parallelism: each plugin issue must be writable and reviewable in isolation, and the contract had to fit on one line so the agent doesn't second-guess it. Numbered files also make the **Pipeline** legible at a glance — the directory listing *is* the execution order. The trade-off is that two plugins competing for the same slot require a rename (a shared-file edit), which is why we space slots by 10 and reserve `90` for the writer.
