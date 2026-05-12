"""CLI entry point: `insta-engineer build`."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from .core import Site
from .plugin_loader import load_plugins


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="insta-engineer")
    sub = parser.add_subparsers(dest="command", required=True)

    build_p = sub.add_parser("build", help="Run the Pipeline against content/ → dist/")
    build_p.add_argument("--content", type=Path, default=Path("content"))
    build_p.add_argument("--output", type=Path, default=Path("dist"))
    build_p.add_argument("--plugins", type=Path, default=Path("plugins"))

    args = parser.parse_args(argv)
    if args.command == "build":
        return build(args.content, args.output, args.plugins)
    return 1


def build(content_dir: Path, output_dir: Path, plugins_dir: Path) -> int:
    if not content_dir.exists():
        print(f"error: content directory {content_dir} not found", file=sys.stderr)
        return 1
    if not plugins_dir.exists():
        print(f"error: plugins directory {plugins_dir} not found", file=sys.stderr)
        return 1

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    site = Site(content_dir=content_dir, output_dir=output_dir)
    plugins = load_plugins(plugins_dir)
    print(f"insta-engineer build: {len(plugins)} plugins")
    for name, apply in plugins:
        print(f"  → {name}")
        apply(site)

    print(f"insta-engineer build: wrote {len(site.output)} files to {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
