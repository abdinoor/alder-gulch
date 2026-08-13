# Workflow Schemas

## Normalized work order

```yaml
operation: research | verify | story-review | process-prose | draft | dialogue-edit | continuity-review | integrate
approval_mode: suggest | review-then-apply | auto-integrate
target:
  mode: explicit | infer
  scene_id: null
  beat: null
author_prompt: ""
submitted_text: null
requested_length_words: null
specialists: []
constraints: []
success_conditions: []
```

## Context packet

```yaml
work_order: {}
target_scene: {}
neighbor_scenes: []
characters: []
timeline_events: []
author_decisions: []
style_guidance: []
evidence_constraints: []
missing_context: []
```

## Scene contract

Use the project's `templates/scene-contract.yaml` when available. Include target, placement, word length, point of view, participants, immediate situation, character goals, conflict, subtext, required information, turn, exit state, prohibited revelations, continuity constraints, and research constraints.

## Specialist handoff

```yaml
specialist: research | story | writer
assignment: ""
files_consulted: []
findings: []
proposal: null
confidence: high | medium | low
uncertainties: []
author_decisions_required: []
affected_files: []
```

## Revision result

```yaml
operation_id: ""
status: proposed | integrated | blocked
approval_mode: ""
target: ""
material_changes: []
canon_updates: []
research_updates: []
validation: []
unresolved_questions: []
```
