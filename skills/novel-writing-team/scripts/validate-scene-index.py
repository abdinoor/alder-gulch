#!/usr/bin/env python3
"""Validate scene IDs, files, and front-matter correspondence."""

from __future__ import annotations

import argparse
import re
import sys

from novel_common import project_root, scalar_config, scene_records


SCENE_ID = re.compile(r"^\d{2,3}\.\d{2,3}$")


def frontmatter_scene_id(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    for line in text.splitlines()[1:]:
        if line == "---":
            break
        if line.startswith("scene_id:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    try:
        root = project_root(args.root)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    config = scalar_config(root / ".novel" / "config.yaml")
    index = root / config.get("scene_index", "planning/scene-index.yaml")
    if not index.is_file():
        print(f"ERROR: missing scene index: {index}")
        return 1

    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_files: set[str] = set()
    records = scene_records(index)
    for number, record in enumerate(records, start=1):
        scene_id = record.get("id", "")
        relative = record.get("file", "")
        if not SCENE_ID.fullmatch(scene_id):
            errors.append(f"record {number}: invalid scene id {scene_id!r}")
        if scene_id in seen_ids:
            errors.append(f"duplicate scene id: {scene_id}")
        seen_ids.add(scene_id)
        if not relative:
            errors.append(f"scene {scene_id}: missing file")
            continue
        if relative in seen_files:
            errors.append(f"duplicate scene file: {relative}")
        seen_files.add(relative)
        path = root / relative
        if not path.is_file():
            errors.append(f"scene {scene_id}: missing file {relative}")
            continue
        declared = frontmatter_scene_id(path.read_text(encoding="utf-8"))
        if declared != scene_id:
            errors.append(
                f"scene {scene_id}: front matter declares {declared!r} in {relative}"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(records)} scene record(s) validated in {index}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
