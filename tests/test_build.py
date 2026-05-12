"""Sanity test: scaffold runs end-to-end against the repo's own content/."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_build_runs_and_produces_output(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable, "-m", "insta_engineer.cli", "build",
            "--content", str(REPO_ROOT / "content"),
            "--output", str(tmp_path / "dist"),
            "--plugins", str(REPO_ROOT / "plugins"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"build failed.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    dist = tmp_path / "dist"
    html_files = list(dist.rglob("*.html"))
    assert html_files, "build produced no HTML output"

    content_md_files = list((REPO_ROOT / "content").rglob("*.md"))
    assert len(html_files) >= len(content_md_files), (
        f"expected at least {len(content_md_files)} html files (one per content md), "
        f"got {[p.name for p in html_files]}"
    )
