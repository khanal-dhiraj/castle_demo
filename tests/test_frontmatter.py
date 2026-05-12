"""Unit tests for the 20_frontmatter plugin."""

import importlib.util
from pathlib import Path

from insta_engineer.core import Page, Site

PLUGIN_PATH = Path(__file__).resolve().parent.parent / "plugins" / "20_frontmatter.py"


def _load_plugin():
    spec = importlib.util.spec_from_file_location("plugin_20_frontmatter", PLUGIN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make_site(pages: list[Page]) -> Site:
    site = Site(content_dir=Path("/nonexistent"), output_dir=Path("/nonexistent"))
    site.pages = pages
    return site


def test_parses_and_strips_frontmatter() -> None:
    plugin = _load_plugin()
    body = "---\ntitle: Hello\norder: 1\ntags: [a, b]\n---\n\n# Heading\n\nBody text.\n"
    page = Page(source_path=Path("index.md"), body=body)
    site = _make_site([page])

    plugin.apply(site)

    assert page.frontmatter == {"title": "Hello", "order": 1, "tags": ["a", "b"]}
    assert not page.body.startswith("---")
    assert "title:" not in page.body
    assert "# Heading" in page.body
    assert "Body text." in page.body


def test_page_without_frontmatter_passes_through() -> None:
    plugin = _load_plugin()
    original_body = "# Just Markdown\n\nNo metadata here.\n"
    page = Page(source_path=Path("plain.md"), body=original_body)
    site = _make_site([page])

    plugin.apply(site)

    assert page.frontmatter == {}
    assert page.body == original_body
