"""Site and Page: the data model every Plugin mutates during a Build."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Page:
    source_path: Path
    body: str
    frontmatter: dict[str, Any] = field(default_factory=dict)
    html: str | None = None
    output_path: Path | None = None


@dataclass
class Site:
    content_dir: Path
    output_dir: Path
    pages: list[Page] = field(default_factory=list)
    output: dict[Path, bytes] = field(default_factory=dict)
