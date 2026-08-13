# Integration Protocol

The Lead is the only canonical manuscript integrator.

## Before a write

1. Confirm the active approval mode authorizes the write.
2. Preserve materially transformed author submissions in `intake/pending/`.
3. Resolve the exact target file and stable scene or beat anchor.
4. Re-read the target file immediately before patching.
5. Confirm no specialist or parallel task is editing the same canonical file.
6. List every manuscript, canon, planning, research, intake, and editorial file the transaction must update.

## Apply the transaction

1. Patch the manuscript at the stable anchor; do not use broad mechanical replacement.
2. Adjust only the transitions necessary to integrate the passage.
3. Update the scene index for structural or metadata changes.
4. Update character, story-bible, location, or timeline canon for deliberately established facts.
5. Update the evidence ledger or invention register for historical claims or deliberate departures.
6. Append a revision-log entry with operation ID, approval mode, target, source intake, specialists, material changes, affected records, and unresolved questions.
7. Move the intake item to `intake/processed/` only after successful integration and validation.

## Validate and report

Run both project validators when applicable. Inspect the exact diff. Confirm the passage appears once, no stable IDs were duplicated, referenced paths exist, character knowledge remains valid, and affected records agree.

Report the target, material changes, records updated, validation results, and unresolved questions. Preserve rollback through version control or the intake archive.

If any stage fails, do not claim completion. Leave the preserved intake in `pending`, identify partial changes, and repair or revert only the changes made by this transaction.
