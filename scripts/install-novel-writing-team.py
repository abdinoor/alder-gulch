#!/usr/bin/env python3
"""Install or check the repository-owned novel-writing-team Codex skill."""

from __future__ import annotations

import argparse
from datetime import datetime
import filecmp
from pathlib import Path
import shutil
import sys


def same_tree(source: Path, destination: Path) -> bool:
    if not destination.is_dir():
        return False
    comparison = filecmp.dircmp(source, destination, ignore=["__pycache__", ".DS_Store"])
    if comparison.left_only or comparison.right_only or comparison.diff_files or comparison.funny_files:
        return False
    return all(
        same_tree(source / name, destination / name)
        for name in comparison.common_dirs
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--install", action="store_true")
    parser.add_argument("--force", action="store_true", help="Back up and replace a differing installed skill")
    parser.add_argument("--destination", help="Override the default ~/.codex/skills/novel-writing-team path")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = root / "skills" / "novel-writing-team"
    destination = (
        Path(args.destination).expanduser().resolve()
        if args.destination
        else Path.home() / ".codex" / "skills" / "novel-writing-team"
    )
    if not (source / "SKILL.md").is_file():
        print(f"ERROR: repository skill source missing: {source}")
        return 1

    identical = same_tree(source, destination)
    if args.check:
        if identical:
            print(f"OK: installed skill matches repository source at {destination}")
            return 0
        print(f"ERROR: installed skill is missing or differs from {source}")
        return 1

    if identical:
        print(f"OK: installed skill already matches {source}")
        return 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if not args.force:
            print("ERROR: installed skill differs; rerun with --force to back it up and replace it")
            return 1
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = destination.with_name(f"{destination.name}.backup-{stamp}")
        destination.rename(backup)
        print(f"Backed up existing skill to {backup}")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    print(f"OK: installed skill from {source} to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
