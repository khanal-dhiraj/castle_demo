"""Write: materialize Site state to the Output directory.

For each Page, emit either `page.html` (set by an earlier Plugin) or
`page.body` (untransformed) at `page.output_path` (or a default of
`source_path.with_suffix('.html')` if no routing Plugin has set one).

Also flushes any extra entries plugins added directly to `site.output`
(e.g. an RSS Plugin writing `feed.xml`).
"""

from pathlib import Path

from insta_engineer.core import Site


def apply(site: Site) -> None:
    for page in site.pages:
        out_rel = page.output_path or page.source_path.with_suffix(".html")
        body = page.html if page.html is not None else page.body
        site.output[out_rel] = body.encode("utf-8")

    for rel, data in site.output.items():
        dst = site.output_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
