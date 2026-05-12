"""Plugin discovery: import every `plugins/*.py` in filename order."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Callable

from .core import Site

PluginFunc = Callable[[Site], None]


def load_plugins(plugins_dir: Path) -> list[tuple[str, PluginFunc]]:
    plugin_files = sorted(
        p for p in plugins_dir.glob("*.py")
        if p.name != "__init__.py" and not p.name.startswith(".")
    )
    plugins: list[tuple[str, PluginFunc]] = []
    for path in plugin_files:
        module = _load_module(path)
        apply = getattr(module, "apply", None)
        if not callable(apply):
            raise RuntimeError(
                f"Plugin {path.name} is missing a top-level `apply(site)` function."
            )
        plugins.append((path.stem, apply))
    return plugins


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        f"insta_engineer_plugin_{path.stem}", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load plugin from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
