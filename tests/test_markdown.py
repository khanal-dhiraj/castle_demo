"""Unit test for the 30_markdown plugin: synthetic Site, assert rendered HTML."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from insta_engineer.core import Page, Site

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_PATH = REPO_ROOT / "plugins" / "30_markdown.py"


def _load_plugin():
    spec = importlib.util.spec_from_file_location("plugin_30_markdown", PLUGIN_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make_site(*bodies: str) -> Site:
    site = Site(content_dir=Path("/tmp/in"), output_dir=Path("/tmp/out"))
    for i, body in enumerate(bodies):
        site.pages.append(Page(source_path=Path(f"p{i}.md"), body=body))
    return site


def test_renders_heading_list_and_fenced_code() -> None:
    body = """# Hello

A paragraph with `inline code` and a [link](https://example.com).

- one
- two
- three

```python
print("hi")
```
"""
    site = _make_site(body)
    _load_plugin().apply(site)

    html = site.pages[0].html
    assert html is not None
    assert "<h1>Hello</h1>" in html
    assert "<ul>" in html and "<li>one</li>" in html
    assert '<pre><code class="language-python">' in html
    assert 'print(&quot;hi&quot;)' in html
    assert '<a href="https://example.com">link</a>' in html
    assert "<code>inline code</code>" in html


def test_renders_table() -> None:
    body = """| col1 | col2 |
| ---- | ---- |
| a    | b    |
"""
    site = _make_site(body)
    _load_plugin().apply(site)

    html = site.pages[0].html
    assert html is not None
    assert "<table>" in html
    assert "<th>col1</th>" in html
    assert "<td>a</td>" in html


def test_empty_body_yields_empty_string() -> None:
    site = _make_site("")
    _load_plugin().apply(site)

    assert site.pages[0].html == ""


def test_preserves_body() -> None:
    body = "# Heading"
    site = _make_site(body)
    _load_plugin().apply(site)

    assert site.pages[0].body == body


def test_ordered_list() -> None:
    body = "1. first\n2. second\n"
    site = _make_site(body)
    _load_plugin().apply(site)

    html = site.pages[0].html
    assert html is not None
    assert "<ol>" in html
    assert "<li>first</li>" in html
