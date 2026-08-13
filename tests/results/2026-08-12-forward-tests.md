# Forward-Test Results — 2026-08-12

All tests used fresh isolated agents, the repository-owned `skills/novel-writing-team` skill, raw files under `tests/fixtures/sample-project/`, suggestion-only mode, and an explicit prohibition on file edits.

## Prompt-driven dialogue — PASS

The run produced a normalized work order, scene contract, approximately 250 words of proposed dialogue, placement at Scene `01.02` between `warning-received` and `guards-ordered`, continuity checks, consulted files, and unresolved questions.

Verified invariants:

- Both speakers had distinct immediate objectives.
- Elias framed fear as procedural and public-legitimacy concerns.
- Bell remained terse, concrete, and oppositional.
- Neither character revealed the unknown financiers.
- The exchange ended with the hearing continuing and guards being posted.
- Shared facts were dramatized through conflict rather than simply explained.
- No files were edited.

## Character-voice editing — PASS

The run revised `dialogue-to-edit.md` while preserving its meaning and scene outcome.

Verified invariants:

- Elias's direct admission of fear was removed without removing his concern.
- Elias used measured procedural language.
- Bell used short, consequence-driven statements.
- The speakers remained distinguishable.
- No new canon or unavailable character knowledge was introduced.
- No file edits or Story review were required.

## Supplied-prose placement — PASS

The run selected Scene `01.02`, immediately after the sentence about Bell testing his bandage and before the `guards-ordered` anchor, with high confidence.

Verified invariants:

- The passage was classified as extending rather than replacing or conflicting.
- The revision matched Elias's voice and knowledge state.
- The placement connected the warning to Bell's subsequent guard order.
- No external historical claim requiring verification was introduced.
- No files were edited.

## Remaining acceptance cases

The deterministic smoke suite verifies scene-index integrity, context assembly, revision logging, and rejection of suggestion-only revision records. The project constitution and skill protocol reserve canonical writes for the Lead. Historical-source quality must continue to be checked on each real research request because no static fixture can validate arbitrary external evidence.
