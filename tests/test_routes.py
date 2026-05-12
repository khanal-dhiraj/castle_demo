"""Unit test for the 40_routes plugin: pretty-URL output paths."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from insta_engineer.core import Page, Site

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_PATH = REPO_ROOT / "plugins" / "40_routes.py"


def _load_routes_apply():
    spec = importlib.util.spec_from_file_location("routes_plugin", PLUGIN_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.apply


def test_routes_assigns_pretty_output_paths(tmp_path: Path) -> None:
    apply = _load_routes_apply()
    site = Site(content_dir=tmp_path / "content", output_dir=tmp_path / "dist")
    site.pages = [
        Page(source_path=Path("index.md"), body=""),
        Page(source_path=Path("state-machine.md"), body=""),
        Page(source_path=Path("architecture.md"), body=""),
    ]

    apply(site)

    by_source = {p.source_path.name: p.output_path for p in site.pages}
    assert by_source["index.md"] == Path("index.html")
    assert by_source["state-machine.md"] == Path("state-machine/index.html")
    assert by_source["architecture.md"] == Path("architecture/index.html")

    for page in site.pages:
        assert page.output_path is not None
