# Insta-Engineer

**Insta-Engineer** is a self-working software engineer: an AFK-agent automation whose label state machine drives issue → branch → PR with no human in the implementation loop. This repo also hosts a Python static site generator that builds the documentation site explaining that automation. The recursion is the point: agents build the site that describes the system they're part of.

## Language

**Insta-Engineer**:
The brand and identity of the entire system — the agent automation plus the docs site that explains it. Use the dashed form in prose and content; the Python package uses the underscore form `insta_engineer`.

**Site**:
The in-memory model of what's being built — a collection of **Pages** plus a map of paths to bytes that will be written to disk during a **Build**.
_Avoid_: "project", "blog"

**Page**:
A single piece of content flowing through the **Pipeline**. Carries its source path, parsed **Frontmatter**, raw body text, rendered HTML, and destination path.
_Avoid_: "post", "article", "document"

**Content**:
The directory of source Markdown files under `content/`. For this demo, the **Content** describes **Insta-Engineer** itself — the **State Machine**, the daemon, the **Plugin** contract, and the supporting skills.
_Avoid_: "src", "input", "sources"

**Output**:
The directory of generated files written to `dist/`. Discarded and rebuilt on every **Build**.
_Avoid_: "build" (as a noun for the directory), "dist" (as a noun in prose)

**Frontmatter**:
YAML metadata at the top of a **Content** file, delimited by `---`. Becomes a dict on the **Page**. Conventional fields: `title`, `date`, `order`, `tags`.
_Avoid_: "metadata", "header", "yaml block"

**Plugin**:
A Python file under `plugins/` matching `NN_name.py` (e.g. `30_markdown.py`) that exports `def apply(site: Site) -> None`. Plugins mutate the **Site** in place. The numeric prefix encodes the position in the **Pipeline** (see [ADR-0001](docs/adr/0001-plugin-contract.md)).
_Avoid_: "extension", "hook", "module"

**Pipeline**:
The ordered sequence of **Plugins** invoked during a **Build**. Order is determined by sorting plugin filenames alphabetically.
_Avoid_: "chain", "pass", "stages"

**Build**:
One end-to-end run of the **Pipeline** that consumes **Content** and produces **Output**. Invoked via `insta-engineer build`.
_Avoid_: "compile", "generate", "render" (overloaded — see ambiguities)

**State Machine**:
The label-driven lifecycle that moves an issue from `ready-for-agent` to `agent-working` to `agent-pr-open` or `agent-failed`. Owned by the Sandcastle daemon (see `CLAUDE.md`). The **Site** has a Page describing it.
_Avoid_: "workflow", "pipeline" (collides with the SSG's **Pipeline**)

## Relationships

- An **Insta-Engineer** demo run consists of: human creates issues → daemon picks them up via the **State Machine** → each issue produces one **Plugin** → cumulative **Builds** of the **Site** progressively improve how the **Content** about **Insta-Engineer** itself renders.
- A **Build** runs the **Pipeline** against the **Site**.
- The **Pipeline** is a list of **Plugins** ordered by filename.
- Each **Plugin** mutates the **Site** in place.
- The **Site** holds many **Pages**; each **Page** originates from one **Content** file (except synthetic Pages like the index, created by **Plugins**).

## Example dialogue

> **Engineer (audience):** "So the page I'm reading about the **State Machine** — that was rendered by a **Plugin** an agent wrote?"
> **Demo presenter:** "Yes. The agent that landed `plugins/30_markdown.py` is the one that turned this **Content** from raw Markdown into HTML. The headings you see came from `plugins/50_templates.py`, written by a different run."
>
> **Engineer:** "And the agent reads this very page to learn the **State Machine**?"
> **Demo presenter:** "In principle. The agent's prompt points at `CONTEXT.md` and the **Content**; nothing stops an agent from reading the rendered docs. The interesting part isn't that it does — it's that the **Content**, the **State Machine**, and the tool that built the page are all the same project."

## Flagged ambiguities

- "pipeline" — overloaded. The **State Machine** is *not* the **Pipeline**. The **State Machine** governs issue lifecycle (an agent-flow concept); the **Pipeline** is the ordered list of **Plugins** in a **Build** (an SSG concept). Use the bolded term to disambiguate.
- "render" was used to mean both "convert Markdown to HTML" and "apply a Jinja template" — resolved: avoid "render" as a noun. The Markdown step transforms `page.body` → `page.html`; the template step wraps `page.html` in a layout.
- "insta-engineer" (the brand) vs. "insta_engineer" (the Python package) — same thing, two casings dictated by Python naming. Prefer the dashed form in **Content** and prose; the underscore form only inside Python imports.
