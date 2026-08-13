#!/usr/bin/env python3
"""Append a normalized, human-readable revision-log entry."""

from __future__ import annotations

import argparse
from datetime import date
import sys

from novel_common import project_root, scalar_config


def bullets(values: list[str]) -> str:
    return "; ".join(values) if values else "None"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--operation-id", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--approval-mode", required=True, choices=("suggest", "review-then-apply", "auto-integrate"))
    parser.add_argument("--target", required=True)
    parser.add_argument("--source-intake", default="None")
    parser.add_argument("--specialist", action="append", default=[])
    parser.add_argument("--change", action="append", default=[])
    parser.add_argument("--updated", action="append", default=[])
    parser.add_argument("--unresolved", action="append", default=[])
    args = parser.parse_args()

    try:
        root = project_root(args.root)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    if args.approval_mode == "suggest":
        print("ERROR: suggestion-only work must not be recorded as an integrated revision")
        return 1

    config = scalar_config(root / ".novel" / "config.yaml")
    log = root / config["revision_log"]
    entry = (
        f"\n## {date.today().isoformat()} — {args.description}\n\n"
        f"- **Operation ID:** {args.operation_id}\n"
        f"- **Approval mode:** {args.approval_mode}\n"
        f"- **Target:** {args.target}\n"
        f"- **Source intake:** {args.source_intake}\n"
        f"- **Specialists used:** {bullets(args.specialist)}\n"
        f"- **Material changes:** {bullets(args.change)}\n"
        f"- **Canon/research files updated:** {bullets(args.updated)}\n"
        f"- **Unresolved questions:** {bullets(args.unresolved)}\n"
    )
    with log.open("a", encoding="utf-8") as handle:
        handle.write(entry)
    print(f"OK: appended revision {args.operation_id} to {log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
