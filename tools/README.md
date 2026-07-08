# Build & verify tools

These scripts build and check the deliverable,
`../8th-grade-refresher-ONE-FILE.html` — one self-contained HTML file (inline
CSS/JS, no external links) that pastes into the school Chromebook's online HTML
viewer. **The tools are dev-only. Never link or inline them into the HTML file.**

> These live in the repo so the pipeline survives a fresh cloud session (the
> container is ephemeral — anything not committed is lost).

## What the deliverable already has

- **6 subjects × 12 lessons.** Newer lessons are ~38 graded "steps": drop-downs,
  select-all (multi), typed practice, and multiple choice, plus one mid-lesson
  writing gate.
- **No per-question checking for the student.** All Check/score/feedback UI is
  CSS-hidden. She sees only a neutral "Answered X of N" bar — no correctness
  signal to brute-force.
- **Parent-only report** behind a PIN (created on first open; key
  `refresher_parent_pin_v1`). The 🔒 Parent button opens a per-lesson table
  (answered / correct / writing / status) computed from the hashed keys.
- **Writing gates.** Each lesson has a 60-word writing checkpoint placed
  mid-lesson (`.writing-gate`); sections after it are `.gated .locked-hidden`
  until the word count hits 60. A popup nudges her to finish it first.
- **Durable autosave** (`refresher_answers_v2`): keyed per control by
  `lessonPartId#index`, so adding a lesson doesn't wipe prior progress.
- **Anti-cheat baked in:** hashed answer key (`data-k`/`data-ks`/`data-w`
  base64) — nothing readable in the source — and shuffled option order.
- Art lessons include drawing studios (colour wheel, shade slider, blend/smudge
  brush).

## The hash (keep JS and Python in sync)

Grading compares a one-way hash of the student's input to the stored key, so
option **position never matters** — that's why shuffling is safe.

```
normalize(s): trim + lowercase; if numeric, canonical number (3.0 -> "3")
hash(s):      djb2 over normalize(s): h=5381; h=((h*33) ^ char) & 0xFFFFFFFF
```

Implemented as `_nz`/`_h` in the HTML's quiz engine, and mirrored in
`postprocess.py` (Python) and `verify.js` (JS). If you change one, change all three.

## Add a lesson (Lesson N for all six subjects)

1. Copy `lesson_builder_template.py` (the Lesson 12 build). Set `N` and
   `PREV = N-1`, and replace the six subject bodies with new topics. `SRC`/`OUT`
   point at the deliverable, so it appends in place. Target is **38 graded
   steps** and there are **no writebox() calls** (writing is a gate, added later).
2. `python3 your_lesson_N.py` — inserts the new lesson (with **plaintext**
   answers; that's expected).
3. `python3 tools/postprocess.py ../8th-grade-refresher-ONE-FILE.html`
   — hashes the new plaintext keys and re-shuffles option positions.
4. `python3 tools/add_gate.py ../8th-grade-refresher-ONE-FILE.html`
   — inserts one mid-lesson **writing gate** into each new lesson-part (skips any
   part that already has one).
5. Verify in jsdom (see below) — no JS errors, gate locks/unlocks, and the parent
   report scores a fully-correct lesson as all-correct.
6. Commit, push to branch `claude/eighth-grade-curriculum-arts-jnshgy`, send the
   file in chat.

Keep math **gentle** (whole numbers, worked examples, calculator OK). Keep the
other subjects normal, not dumbed down.

## Files

| File | Purpose |
|------|---------|
| `lesson_builder_template.py` | Reference builder (Lesson 12) + all builder helpers. Copy → edit → run to add a lesson. |
| `postprocess.py` | Run after inserting a new lesson: hashes plaintext keys + shuffles positions. Reusable. |
| `add_gate.py` | Run after postprocess: inserts a mid-lesson writing gate into each new lesson-part (skips parts that already have one). |
| `verify.js` | jsdom check: no JS errors; a writing gate hides then unlocks at 60 words; the student bar reads "Answered X of N"; the parent report scores a fully-correct lesson as all-correct. Pass the lesson id to spot-check as `node tools/verify.js <file> <lessonId>`. |
| `lockdown.py` | The **one-time** transform (hash keys + JS surgery) that first locked the file. Reference only. Do **not** re-run on the current file — its JS anchors are gone. |

## Verifying needs jsdom (dev only)

`verify.js` requires `jsdom` (e.g. `npm i jsdom` in a scratch dir, then run with
`NODE_PATH` pointing at its `node_modules`). jsdom stubs `<canvas>`, so studio
drawing isn't exercised there — only grading, the tracker, and JS errors are.
