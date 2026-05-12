"""Routes: assign each Page a pretty-URL output_path.

Convention:
- `index.md` → `index.html` (root stays flat, no nested directory)
- `<stem>.md` → `<stem>/index.html`

Paths are kept relative to `site.output_dir`; the writer plugin handles I/O.
"""

from pathlib import Path

from insta_engineer.core import Site


def apply(site: Site) -> None:
    for page in site.pages:
        src = page.source_path
        if src.name == "index.md":
            page.output_path = src.with_name("index.html")
        else:
            page.output_path = src.parent / src.stem / "index.html"
