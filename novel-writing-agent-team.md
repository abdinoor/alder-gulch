# Novel Writing Agent Team

## Design Principle

Roles are responsibilities, not necessarily independent agents. The system preserves three distinct modes of judgment while avoiding the cost of running a large team:

- **Evidentiary:** What does the available evidence support?
- **Narrative:** Does the story work, and why?
- **Creative and linguistic:** Does the prose express the story effectively, consistently, and in the correct voices?

The author retains final creative authority. A lightweight Lead / Managing Agent coordinates three specialists and invokes only those needed for a particular request.

## Team Structure

```text
Author
  └── Lead / Managing Agent and sole manuscript integrator
        ├── Research & Verification Agent
        ├── Story Editor
        └── Writer, Prose & Continuity Agent
```

The specialist perspectives are implemented as reference protocols within one repeatable orchestration skill. Separate specialist agents are created only when a task is substantial, parallelizable, or benefits from independent judgment.

## Lead / Managing Agent

Coordination is a function rather than a fourth specialist role. The Lead:

- Interprets the author's request and identifies the required workflow.
- Selects the appropriate skills or specialist agents.
- Retrieves only the relevant manuscript, research, character, and continuity context.
- Sequences work so structural decisions precede detailed drafting or polishing.
- Reconciles conflicting recommendations.
- Protects the author's intent and voice.
- Surfaces consequential creative decisions to the author.
- Determines the appropriate location for new or revised material.
- Acts as the sole writer to canonical manuscript files.
- Applies changes transactionally and reports the resulting diff.

The Lead should not automatically invoke the entire team. A factual question may require only Research & Verification; a structural review only the Story Editor; and a straightforward dialogue edit only the Writer, Prose & Continuity specialist.

## 1. Research & Verification Agent

### Responsibilities

- Discover primary and reliable secondary sources.
- Answer factual and historical questions.
- Verify claims appearing in drafted or submitted prose.
- Assess broader historical plausibility.
- Check period vocabulary, institutions, customs, objects, and behavior.
- Track citations, provenance, uncertainty, and conflicting accounts.

### Working method

Research and verification occur as distinct passes:

1. Collect relevant evidence without forcing it to support the manuscript.
2. Audit manuscript claims against that evidence.
3. Search deliberately for contradictory or complicating evidence.

Every material finding is classified as one of:

- Documented fact
- Disputed claim
- Reasonable inference
- Authorial invention

The agent returns evidence and constraints rather than silently rewriting uncertainty into certainty.

### Primary output

An evidence ledger containing sources, concise findings, confidence levels, contradictions, and implications for the manuscript.

## 2. Story Editor

### Responsibilities

- Develop and assess story architecture.
- Perform developmental editing.
- Evaluate plot, chronology, point of view, and character arcs.
- Analyze motivation, relationships, dialogue, and subtext.
- Review scene purpose, sequence, pacing, setup, and payoff.
- Determine or assess where submitted or generated material belongs.
- Convert an author's generative prompt into a scene contract.
- Independently assess whether a draft fulfills its intended narrative function.

The Story Editor works at the scale of the complete novel, acts or parts, chapters, scenes, and individual character arcs. It normally diagnoses problems and offers alternatives before rewriting. This keeps editorial judgment distinct from unrequested co-authorship.

### Scene contract

For prompt-driven drafting, the Story Editor may create a compact brief containing:

```yaml
target_scene: "07.03"
placement: "After the warning arrives, before the meeting adjourns"
length: "300-400 words"
pov: "Character A"
participants:
  - "Character A"
  - "Character B"
immediate_situation: "Armed supporters may intervene"
character_goals:
  character_a: "Persuade B to postpone the confrontation"
  character_b: "Argue that delay will embolden their opponents"
conflict: "Prudence versus loss of authority"
subtext: "A is partly motivated by fear but will not admit it"
required_information:
  - "A gunfight could turn public opinion against them"
turn: "B realizes A doubts their allies' discipline"
exit_state: "They proceed, but agree to add guards"
must_not_reveal:
  - "Character C has already betrayed them"
```

The author's prompt remains authoritative. The contract fills operational gaps from established canon without casually inventing major plot decisions.

### Primary output

An editorial memo, placement recommendation, or scene contract with prioritized findings and the tradeoffs of major recommendations.

## 3. Writer, Prose & Continuity Agent

This agent has separate working modes so creation and evaluation do not collapse into a single undifferentiated pass.

### Scene-drafting mode

- Draft new scenes or passages from an approved scene contract.
- Match the novel's narrative voice and established character voices.
- Give each character an immediate objective.
- Use conflict, evasion, and subtext rather than exposition between characters who already share information.
- Maintain point of view and the current knowledge state.
- Avoid introducing unsupported canon.
- Mark unresolved factual details instead of fabricating them.
- End with the required change in the scene's state.

### Dialogue-editing mode

- Preserve the author's intended meaning and scene outcome by default.
- Adjust delivery to match each speaker's worldview, vocabulary, syntax, status, emotional state, relationships, and current arc stage.
- Distinguish what a character says from what the character wants, conceals, or cannot admit.
- Ensure characters do not reveal information they do not yet know.
- Avoid interchangeable dialogue and exaggerated verbal tics.
- Flag revisions that would materially change meaning, motivation, subtext, or plot information.

### Prose-and-continuity mode

- Edit prose for clarity, rhythm, precision, imagery, and emotional effect.
- Preserve and strengthen narrative and character voice.
- Correct grammar, punctuation, spelling, usage, and typography.
- Enforce the project's house style.
- Track internal continuity across characters, locations, objects, dates, and events.
- Produce a clean proposed passage plus author queries and required canon updates.

For generated prose, drafting and editing are separate passes. The Story Editor may independently review a consequential draft between them.

### Primary output

A proposed draft or revision, material-change notes, continuity queries, and proposed updates to the story bible. The agent does not directly edit canonical manuscript files.

## Character and Voice Canon

Character understanding lives in durable project files rather than an agent's conversational memory. Each significant character should have a structured record containing:

- Story function and archetype
- Individual contradictions and blind spots
- Worldview, desires, fears, and forbidden admissions
- Vocabulary, register, syntax, directness, humor, and conversational strategies
- Conditional verbal or physical habits
- Relationships and power dynamics with other characters
- Current knowledge, suspicions, misunderstandings, and secrets
- Current position in the character arc
- Facts or behaviors that must not appear yet
- Approved dialogue examples from multiple emotional and social situations

Archetype is a starting point, not a voice specification. The goal is an individual whose speech changes appropriately with audience, pressure, status, deception, and development.

Peculiarities should be recorded as conditional tendencies with frequency limits, not mandatory catchphrases. For example:

```yaml
habit:
  behavior: "Uses 'reckon' when making a deliberately modest claim"
  frequency: "At most once in an ordinary scene"
  avoid_when: "Speaking formally or issuing a direct order"
```

## Shared Project Structure

```text
novel/
├── AGENTS.md
├── manuscript/
│   ├── ch-01/
│   │   ├── 01.01-arrival.md
│   │   └── 01.02-first-meeting.md
│   └── ch-02/
├── planning/
│   ├── premise.md
│   ├── outline.md
│   ├── character-arcs.md
│   └── scene-index.yaml
├── canon/
│   ├── story-bible.md
│   ├── timeline.md
│   ├── characters/
│   ├── locations.md
│   └── style-and-voice.md
├── research/
│   ├── evidence-ledger.md
│   ├── sources/
│   ├── open-questions.md
│   └── invention-register.md
├── editorial/
│   ├── developmental-memos/
│   ├── author-decisions.md
│   ├── continuity-issues.md
│   └── revision-log.md
└── skills/
    └── novel-writing-team/
        ├── SKILL.md
        ├── references/
        │   ├── research-verification.md
        │   ├── story-editor.md
        │   ├── writer-prose-continuity.md
        │   └── integration-protocol.md
        └── scripts/
```

The most important durable records are:

- `author-decisions.md`, which prevents settled creative choices from being repeatedly reopened.
- `evidence-ledger.md`, which separates fact, dispute, inference, and invention.
- `story-bible.md` and the character files, which define fictional canon.
- `style-and-voice.md`, which protects the author's prose from generic improvement.
- `scene-index.yaml`, which makes placement reliable.
- `revision-log.md`, which records what changed and why.

## Stable Placement

Every scene should have a stable ID and a separate file where practical. The scene index should record information such as:

```yaml
- id: "02.01"
  file: "manuscript/ch-02/02.01-hearing.md"
  title: "The Hearing"
  date: "1864-01-12"
  pov: "Elias"
  location: "Territorial courtroom"
  purpose: "Expose the conflict between Elias and Bell"
  begins_with: "Elias enters the crowded courtroom"
  ends_with: "Bell recognizes the witness"
  status: "draft"
```

Longer scene files may contain stable beat anchors:

```markdown
<!-- beat: jurors-enter -->
...
<!-- beat: testimony-begins -->
```

When placement is inferred:

- A high-confidence placement may be applied and reported.
- A moderate-confidence placement should be proposed for review.
- Materially different plausible placements should be presented to the author for a decision.

## Integration Protocol

Specialists analyze and propose; the Lead is the sole manuscript integrator. For every applied change, the Lead:

1. Re-reads the current target file to avoid editing stale text.
2. Inserts or replaces material at a stable scene or beat location.
3. Adjusts transitions into and out of the passage.
4. Preserves recoverability through version history or an intake archive.
5. Updates the scene index when structure changes.
6. Updates character, story-bible, and timeline records when new canon is established.
7. Updates the evidence or invention ledger when historical material is added.
8. Records the operation in the revision log.
9. Shows the author the result, material changes, and unresolved questions.

No two specialist agents should edit the same canonical manuscript files concurrently.

## Core Workflows

### Processing prose supplied by the author

```text
Author's prose
  -> Lead identifies placement and relevant context
  -> Story assessment when structure or placement is uncertain
  -> Research check when external facts are involved
  -> Prose and continuity revision
  -> Lead integrates and updates project records
```

### Generating prose from guidance

```text
Author's prompt
  -> Lead retrieves relevant context
  -> Story Editor creates a scene contract
  -> Research supplies necessary factual constraints
  -> Writer drafts
  -> Story Editor reviews consequential drafts
  -> Writer revises in prose-and-continuity mode
  -> Lead integrates and updates project records
```

### Improving character dialogue

```text
Author's dialogue
  -> Lead identifies speakers, scene state, and placement
  -> Load character profiles and approved examples
  -> Writer diagnoses and revises voice, subtext, and continuity
  -> Story Editor reviews if meaning or relationships changed
  -> Lead integrates and updates canon as needed
```

## Approval Modes

The author may select:

- **Suggest:** Return proposed prose and placement without writing files.
- **Review then apply:** Prepare the change and wait for approval.
- **Auto-integrate:** Apply high-confidence changes, then show the diff and retain recoverability.

Review should normally be required when a change:

- Moves material between scenes.
- Changes plot, motivation, or scene outcome.
- Removes substantial author-written content.
- Establishes a new historical claim.
- Contradicts established canon.
- Alters point of view or chronology.
- Requires choosing among materially different placements.

## Implementation Architecture

### One orchestration skill defines the workflow

Implement the team as one reusable `novel-writing-team` skill. Its concise `SKILL.md` routes requests and owns the end-to-end workflow. Separate reference protocols define Research & Verification, Story Editing, Writer / Prose / Continuity, schemas, and canonical integration.

This avoids competing triggers and duplicated handoff rules while retaining three distinct specialist perspectives. The repository copy under `skills/novel-writing-team/` is the source of truth; an installation script synchronizes it to the personal Codex skills directory.

### Agents provide independent judgment

The Lead may apply a skill directly for routine work. It creates a separate specialist agent when:

- The work is large enough to justify a separate context.
- An independent or adversarial assessment is valuable.
- Unrelated workstreams can safely proceed in parallel.
- A fresh verification pass should not inherit the researcher's assumptions.

### Tools provide bounded capabilities

Tools should retrieve or manipulate information rather than impersonate editorial roles. Useful capabilities include:

- Manuscript and scene search
- Character-context retrieval
- Story-bible and timeline lookup
- Web, archive, catalog, OCR, and PDF search
- Citation capture
- Timeline and continuity validation
- File patching and diff generation

Begin with ordinary file and search capabilities. Add a custom tool only after repeated use reveals a stable, deterministic operation worth automating.

### Files preserve state

Agent conversations are working memory. Manuscript, canon, evidence, decisions, and revision records in the project are authoritative.

## Cost-Conscious Routing

| Request | Normal execution |
|---|---|
| Find historical descriptions of jurors | Research & Verification |
| Establish the probable trial audience size | Research & Verification |
| Diagnose a slow second act | Story Editor |
| Evaluate a character's motivation or arc | Story Editor |
| Polish a passage with clear placement | Lead using Writer / Prose skill |
| Place and revise supplied prose | Story skill if needed, then Writer / Prose skill |
| Draft a straightforward passage with no factual issue | Lead prepares context; Writer drafts and edits |
| Draft a structurally important scene | Story Editor, Writer, Story review, Writer revision |
| Draft a historically consequential scene | Story Editor and Research, then Writer and review |
| Improve dialogue without changing meaning | Writer in dialogue-editing mode |
| Change dialogue subtext, motivation, or relationship dynamics | Writer plus Story Editor review |
| Check dates, ages, objects, or character knowledge | Writer / Continuity, consulting Research for external facts |
| Review a complete draft | Story Editor first; Research and Prose / Continuity afterward |

## Workflow Boundaries

Some responsibilities share an agent but remain separate stages:

1. **Structure before prose:** Structural revisions precede detailed drafting or line editing.
2. **Drafting before certification:** Creative fluency and factual skepticism are evaluated independently.
3. **Creation before editing:** The Writer drafts against a scene contract, then edits in a separate pass.
4. **Recommendations before authorial decisions:** Major choices involving theme, characterization, voice, or historical departure remain with the author.
5. **Research before historical judgment:** Plausibility claims are grounded in evidence with uncertainty made explicit.
6. **Proposal before integration:** Specialists return proposed changes; only the Lead writes canonical manuscript files.

## Final Operating Principle

The system is not three agents running on every paragraph. It is one controlled editorial pipeline with three available specialist perspectives. Skills make those perspectives reusable, separate agents supply independence when it matters, tools provide bounded capabilities, and project files preserve the evolving novel.
