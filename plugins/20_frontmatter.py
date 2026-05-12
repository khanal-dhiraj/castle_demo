"""Frontmatter: parse and strip the YAML block at the top of each page.

Runs before Markdown rendering so downstream plugins see clean Markdown
with parsed metadata available on `page.frontmatter`.
"""

import frontmatter

from insta_engineer.core import Site


def apply(site: Site) -> None:
    for page in site.pages:
        if page.body.startswith("---\n") or page.body.startswith("---\r\n"):
            post = frontmatter.loads(page.body)
            page.frontmatter = dict(post.metadata)
            page.body = post.content
        else:
            page.frontmatter = {}
