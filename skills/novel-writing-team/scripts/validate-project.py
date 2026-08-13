#!/usr/bin/env python3
"""Validate required novel project structure and configured paths."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from novel_common import project_root, scalar_config


REQUIRED_DIRS = (
    "manuscript",
    "planning",
    "canon/characters",
    "research/sources",
    "editorial",
    "intake/pending",
    "intake/processed",
    "templates",
)

REQUIRED_CONFIG_KEYS = (
    "manuscript_dir",
    "scene_index",
    "story_bible",
    "timeline",
    "characters_dir",
    "style_guide",
    "evidence_ledger",
    "invention_register",
    "author_decisions",
    "revision_log",
    "intake_pending",
    "intake_processed",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    try:
        root = project_root(args.root)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    errors: list[str] = []
    if not (root / "AGENTS.md").is_file():
        errors.append("missing AGENTS.md")
    for relative in REQUIRED_DIRS:
        if not (root / relative).is_dir():
            errors.append(f"missing directory: {relative}")

    config = scalar_config(root / ".novel" / "config.yaml")
    for key in REQUIRED_CONFIG_KEYS:
        relative = config.get(key)
        if not relative:
            errors.append(f"missing config key: {key}")
        elif not (root / relative).exists():
            errors.append(f"configured path does not exist: {key}={relative}")

    if config.get("approval_mode") not in {
        "suggest",
        "review-then-apply",
        "auto-integrate",
    }:
        errors.append("approval_mode must be suggest, review-then-apply, or auto-integrate")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: valid novel project at {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
