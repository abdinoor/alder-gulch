# Alder Gulch Novel Project

## Authority

- The author has final authority over plot, character, theme, voice, historical departures, and publication text.
- Treat files in `manuscript/`, `canon/`, `planning/`, `research/`, and `editorial/author-decisions.md` as canonical project state.
- Treat conversation context and agent memory as temporary working state.

## Required workflow

- Use the `novel-writing-team` skill for novel research, verification, story editing, drafting, dialogue editing, continuity work, placement, or manuscript integration.
- Treat `skills/novel-writing-team/` as the version-controlled source of truth for that skill. Use `scripts/install-novel-writing-team.py --check` to confirm the installed personal skill matches it.
- Identify the smallest sufficient specialist workflow. Do not run all specialists by default.
- Resolve structural questions before detailed prose polishing.
- Preserve the author's meaning, voice, and scene outcome unless the request explicitly authorizes changing them.
- Never turn uncertainty, inference, or invention into documented fact.
- Check character knowledge, chronology, and relevant canon before drafting or revising dialogue.

## Manuscript writes

- The primary agent is the sole integrator of canonical manuscript files.
- Subagents may research, diagnose, draft, review, and propose patches, but must not edit files under `manuscript/`, `canon/`, `planning/scene-index.yaml`, or `editorial/revision-log.md`.
- Re-read a target file immediately before applying a patch.
- Use stable scene IDs and beat anchors for placement. Do not rely only on matching prose that may later change.
- Never allow concurrent writes to the same canonical file.
- Preserve submitted prose under `intake/` before materially transforming or integrating it.
- Update all affected canon, scene-index, research, and revision records in the same task.

## Approval policy

- Default to `review-then-apply` unless the author explicitly requests suggestion-only or automatic integration.
- `suggest`: inspect and propose, but do not change canonical files.
- `review-then-apply`: prepare the proposed change and obtain approval before editing canonical files.
- `auto-integrate`: apply in-scope changes, validate them, and show a concise summary and diff.
- Require review for materially ambiguous placement, plot or motivation changes, substantial deletion, new historical assertions, canon conflicts, chronology changes, or point-of-view changes unless the author explicitly authorized them.

## File conventions

- Name scene files `<chapter>.<scene>-<slug>.md`, such as `02.01-hearing.md`.
- Give every scene corresponding metadata in `planning/scene-index.yaml`.
- Maintain characters in `canon/characters/<slug>.md` using `templates/character.md`.
- Record evidence using `templates/evidence-entry.md` and revisions using `templates/revision-entry.md`.
- Run the project and scene-index validators after structural or canonical edits.
- Run validators from `skills/novel-writing-team/scripts/` so a fresh checkout is self-contained.
