#!/usr/bin/env python3
"""Shared, dependency-free helpers for the novel-writing-team skill."""

from __future__ import annotations

from pathlib import Path
import re


def project_root(value: str) -> Path:
    root = Path(value).expanduser().resolve()
    if not (root / ".novel" / "config.yaml").is_file():
        raise ValueError(f"Not a novel project root: {root}")
    return root


def scalar_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        if value and not value.startswith("[") and not value.startswith("{"):
            values[key.strip()] = value
    return values


def scene_records(path: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    field = re.compile(r"^\s{2,4}([a-z_]+):\s*(.*?)\s*$")
    first = re.compile(r"^\s*-\s+id:\s*(.*?)\s*$")
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = first.match(raw)
        if match:
            if current:
                records.append(current)
            current = {"id": unquote(match.group(1))}
            continue
        if current:
            match = field.match(raw)
            if match:
                current[match.group(1)] = unquote(match.group(2))
    if current:
        records.append(current)
    return records


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value in {"null", "~"}:
        return ""
    return value
