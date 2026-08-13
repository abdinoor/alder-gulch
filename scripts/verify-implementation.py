#!/usr/bin/env python3
"""Verify the repository-owned novel team implementation end to end."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


def run(command: list[str], cwd: Path) -> bool:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    label = " ".join(command)
    if result.returncode:
        print(f"FAIL: {label}")
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())
        return False
    print(f"PASS: {label}")
    if result.stdout:
        print(result.stdout.rstrip())
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-installed-skill", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    skill = root / "skills" / "novel-writing-team"
    creator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    commands = [
        [sys.executable, str(creator), str(skill)],
        [sys.executable, str(skill / "scripts" / "validate-project.py"), "--root", str(root)],
        [sys.executable, str(skill / "scripts" / "validate-scene-index.py"), "--root", str(root)],
        [sys.executable, str(skill / "scripts" / "test_novel_tools.py")],
    ]
    if not args.skip_installed_skill:
        commands.append([sys.executable, str(root / "scripts" / "install-novel-writing-team.py"), "--check"])
    success = all(run(command, root) for command in commands)
    if success:
        print("PASS: full deterministic implementation verification")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
