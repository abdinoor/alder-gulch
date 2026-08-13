#!/usr/bin/env python3
"""Assemble a bounded Markdown context packet from canonical project files."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from novel_common import project_root, scalar_config, scene_records


def section(title: str, path: Path) -> str:
    if not path.is_file():
        return f"## {title}\n\n_Missing: {path}_\n"
    return f"## {title}\n\nSource: `{path}`\n\n{path.read_text(encoding='utf-8').strip()}\n"


def character_path(directory: Path, name: str) -> Path:
    direct = directory / f"{name}.md"
    if direct.is_file():
        return direct
    slug = "-".join(name.lower().replace("_", " ").split())
    return directory / f"{slug}.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--character", action="append", default=[])
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        root = project_root(args.root)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    config = scalar_config(root / ".novel" / "config.yaml")
    index_path = root / config["scene_index"]
    records = scene_records(index_path)
    position = next((i for i, item in enumerate(records) if item.get("id") == args.scene_id), None)
    if position is None:
        print(f"ERROR: scene not found: {args.scene_id}")
        return 1

    chosen = records[position]
    parts = [f"# Context Packet: Scene {args.scene_id}\n"]
    parts.append(section("Project instructions", root / "AGENTS.md"))
    parts.append(section("Style and voice", root / config["style_guide"]))
    parts.append(section("Author decisions", root / config["author_decisions"]))

    for label, index in (("Previous scene", position - 1), ("Target scene", position), ("Next scene", position + 1)):
        if 0 <= index < len(records):
            record = records[index]
            parts.append(section(f"{label} {record.get('id', '')}", root / record["file"]))

    characters_dir = root / config["characters_dir"]
    for name in args.character:
        parts.append(section(f"Character: {name}", character_path(characters_dir, name)))

    packet = "\n".join(parts).rstrip() + "\n"
    if args.output:
        output = Path(args.output).expanduser()
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(packet, encoding="utf-8")
        print(f"OK: wrote context packet to {output}")
    else:
        print(packet, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
