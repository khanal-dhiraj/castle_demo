"""Markdown: render `page.body` to HTML via markdown-it-py into `page.html`.

Runs after slot 20 (frontmatter stripping). `page.body` is left intact so
later plugins (e.g. excerpt generators) can still inspect the source text.
"""

from markdown_it import MarkdownIt

from insta_engineer.core import Site

_md = MarkdownIt("commonmark").enable("table")


def apply(site: Site) -> None:
    for page in site.pages:
        page.html = _md.render(page.body) if page.body else ""
