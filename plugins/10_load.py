"""Load: walk content/ and create a Page per .md file with raw body text.

Later plugins parse frontmatter, render Markdown, wrap in templates, etc.
"""

from insta_engineer.core import Page, Site


def apply(site: Site) -> None:
    for md_path in sorted(site.content_dir.rglob("*.md")):
        rel = md_path.relative_to(site.content_dir)
        page = Page(
            source_path=rel,
            body=md_path.read_text(encoding="utf-8"),
        )
        site.pages.append(page)
