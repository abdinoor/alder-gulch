#!/usr/bin/env python3
"""Self-contained smoke tests for deterministic novel project tools."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(script: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(HERE / script), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"{script} returned {result.returncode}, expected {expected}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def fixture(root: Path) -> None:
    config = {
        "manuscript_dir": "manuscript",
        "scene_index": "planning/scene-index.yaml",
        "story_bible": "canon/story-bible.md",
        "timeline": "canon/timeline.yaml",
        "characters_dir": "canon/characters",
        "style_guide": "canon/style-and-voice.md",
        "evidence_ledger": "research/evidence-ledger.md",
        "invention_register": "research/invention-register.md",
        "author_decisions": "editorial/author-decisions.md",
        "revision_log": "editorial/revision-log.md",
        "intake_pending": "intake/pending",
        "intake_processed": "intake/processed",
    }
    config_text = "schema_version: 1\napproval_mode: \"review-then-apply\"\n" + "".join(
        f'{key}: "{value}"\n' for key, value in config.items()
    )
    write(root / ".novel/config.yaml", config_text)
    write(root / "AGENTS.md", "# Test instructions\n")
    write(
        root / "planning/scene-index.yaml",
        "schema_version: 1\nscenes:\n"
        "  - id: \"01.01\"\n    file: \"manuscript/ch-01/01.01-opening.md\"\n"
        "  - id: \"01.02\"\n    file: \"manuscript/ch-01/01.02-meeting.md\"\n",
    )
    for scene_id, name in (("01.01", "opening"), ("01.02", "meeting")):
        write(
            root / f"manuscript/ch-01/{scene_id}-{name}.md",
            f"---\nscene_id: \"{scene_id}\"\n---\n\nScene {scene_id}.\n",
        )
    write(root / "canon/story-bible.md", "# Story Bible\n")
    write(root / "canon/timeline.yaml", "schema_version: 1\nevents: []\n")
    write(root / "canon/style-and-voice.md", "# Style\n")
    write(root / "canon/characters/character-a.md", "# Character A\n")
    write(root / "research/evidence-ledger.md", "# Evidence\n")
    write(root / "research/invention-register.md", "# Inventions\n")
    (root / "research/sources").mkdir(parents=True)
    write(root / "editorial/author-decisions.md", "# Decisions\n")
    write(root / "editorial/revision-log.md", "# Revisions\n")
    (root / "intake/pending").mkdir(parents=True)
    (root / "intake/processed").mkdir(parents=True)
    (root / "templates").mkdir(parents=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="novel-tools-") as directory:
        root = Path(directory)
        fixture(root)
        root_arg = str(root)
        run("validate-project.py", "--root", root_arg)
        run("validate-scene-index.py", "--root", root_arg)
        packet = run(
            "assemble-context.py",
            "--root",
            root_arg,
            "--scene-id",
            "01.02",
            "--character",
            "character-a",
        ).stdout
        assert "Scene 01.01" in packet
        assert "Scene 01.02" in packet
        assert "Character: character-a" in packet
        run(
            "record-revision.py",
            "--root",
            root_arg,
            "--operation-id",
            "smoke-1",
            "--description",
            "Smoke test",
            "--approval-mode",
            "auto-integrate",
            "--target",
            "01.02",
            "--specialist",
            "writer",
            "--change",
            "Inserted test prose",
        )
        assert "smoke-1" in (root / "editorial/revision-log.md").read_text(encoding="utf-8")
        run(
            "record-revision.py",
            "--root",
            root_arg,
            "--operation-id",
            "smoke-2",
            "--description",
            "Must fail",
            "--approval-mode",
            "suggest",
            "--target",
            "01.02",
            expected=1,
        )
    print("OK: all novel tool smoke tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
