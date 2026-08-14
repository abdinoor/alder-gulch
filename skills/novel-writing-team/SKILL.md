---
name: novel-writing-team
description: Route and execute file-centered novel research, fact verification, story editing, prompt-driven scene drafting, character-specific dialogue editing, prose and continuity revision, placement, and controlled manuscript integration. Use when Codex works on a novel project or is asked to research, verify, plan, draft, revise, place, or integrate novel content while preserving canon, character knowledge, authorial voice, and revision history.
---

# Novel Writing Team

Act as the Lead / Managing Agent and sole canonical manuscript integrator. Treat project files as durable memory and agent conversations as temporary working state.

## Start every task

1. Locate the project root by finding `.novel/config.yaml` and `AGENTS.md`.
2. Read the root `AGENTS.md`, `.novel/config.yaml`, and the smallest relevant set of canonical files.
3. Normalize the request into: operation, approval mode, target or placement mode, author constraints, submitted text, required specialists, and success conditions.
4. Select the smallest sufficient workflow below.
5. State the active protocol or protocols briefly before using them.

## Route the request

- For evidence discovery, external facts, historical plausibility, or claim auditing, read [research-verification.md](references/research-verification.md).
- For structure, placement, scene purpose, character motivation, pacing, arcs, or a drafting contract, read [story-editor.md](references/story-editor.md).
- For new prose, line editing, dialogue voice, grammar, continuity, voice matching, tonal range, or requests for “more life,” read [writer-prose-continuity.md](references/writer-prose-continuity.md).
- Before any canonical write, read [integration-protocol.md](references/integration-protocol.md).
- For work orders, context packets, scene contracts, findings, and handoffs, read [schemas.md](references/schemas.md).

Use protocols sequentially when one output constrains the next. Do not launch specialists merely to simulate a team.

## Choose direct work or a subagent

Apply a protocol directly for routine paragraph- or scene-level work. Use a specialist subagent only when the work is substantial, an independent assessment is valuable, a fresh verifier should not inherit prior assumptions, or workstreams are genuinely independent.

Tell every subagent:

- Return analysis, evidence, a draft, or a proposed patch only.
- Do not edit canonical project files.
- Identify sources and files consulted.
- State uncertainty and unresolved questions.

Do not delegate integration. Do not run unrelated specialists in parallel when their outputs are sequential dependencies.

## Core workflows

### Process author-supplied prose

1. Preserve the submission under `intake/pending/` before materially transforming it.
2. Determine placement from the scene index, neighboring prose, and story purpose.
3. Use Story Editor when placement, structure, or scene effect is not obvious.
4. Use Research & Verification only for material external claims.
5. Use Writer / Prose / Continuity to revise in context.
6. Follow the integration protocol according to approval mode.

### Draft prose from guidance

1. Retrieve the likely target scene, neighbors, participating character records, relevant arc state, canonical style guidance, approved exemplars, and evidence constraints.
2. Create a scene contract. For consequential work, have the Story Editor create or assess it.
3. Resolve only factual questions that constrain the draft.
4. Draft against the contract.
5. Independently review consequential drafts for narrative function.
6. Revise in prose-and-continuity mode.
7. Integrate only through the Lead.

### Revise voice or add life

1. Read the canonical style guide and approved exemplars before proposing changes.
2. Diagnose whether the deficiency is structural, scene-level, paragraph-level, or sentence-level.
3. Preserve effective prose unless a specific defect is identified.
4. Add culture, emotion, humor, pleasure, and particularity through researched practices, relationships, perception, and action; do not manufacture narrator personality.
5. Compare before and after for meaning, cadence, implication, historical scale, and emotional pressure. Reject a revision that becomes smaller, glibber, or more conspicuous.
6. Follow the configured approval mode before integration.

### Improve dialogue

1. Identify the scene, speakers, immediate objectives, emotional states, relationships, knowledge states, and approved voice exemplars.
2. Diagnose interchangeability, exposition, voice, subtext, and continuity issues.
3. Preserve meaning and scene outcome unless authorized otherwise.
4. Revise peculiarities as conditional tendencies, not mandatory catchphrases.
5. Request Story review if meaning, motivation, relationship dynamics, or scene outcome changes.
6. Integrate only through the Lead.

### Verify or research

1. Separate discovery from verification.
2. Seek contradictory evidence.
3. Classify each finding as documented fact, disputed claim, reasonable inference, or authorial invention.
4. Record sources, confidence, contradictions, and manuscript implications.

## Context discipline

Retrieve only what the task needs: the target scene and neighbors, participating character files, relevant timeline events, applicable author decisions, style guidance, and relevant evidence. Prefer structured indexes and exact search over loading the full novel.

Use `scripts/assemble-context.py` for deterministic collection after a scene ID and participating characters are known. Use its output as a packet, then inspect any missing context directly.

## Approval modes

- `suggest`: propose content, placement, and affected files; do not change canonical files.
- `review-then-apply`: prepare the exact change and obtain author approval before canonical writes.
- `auto-integrate`: apply the authorized change, validate, update records, and report the diff.

Default to the project configuration. Do not interpret a request to draft or edit as automatic permission to integrate when the configured mode requires review.

## Validation

Before reporting an integration complete:

1. Run `scripts/validate-project.py --root <project-root>`.
2. Run `scripts/validate-scene-index.py --root <project-root>` after scene or index changes.
3. Inspect the resulting diff.
4. Confirm that manuscript, canon, evidence, and revision records agree.

Stop and report a concrete blocker when validation fails and the safe correction would require an unapproved creative decision.
