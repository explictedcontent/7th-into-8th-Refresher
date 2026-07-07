# Build & verify tools

These scripts build and check the deliverable,
`../8th-grade-refresher-ONE-FILE.html` — one self-contained HTML file (inline
CSS/JS, no external links) that pastes into the school Chromebook's online HTML
viewer. **The tools are dev-only. Never link or inline them into the HTML file.**

> These live in the repo so the pipeline survives a fresh cloud session (the
> container is ephemeral — anything not committed is lost).

## What the deliverable already has

- **6 subjects × 11 lessons.** Newer lessons (7–11) are ~38 graded "steps":
  drop-downs, select-all (multi), typed practice, and multiple choice. Writing
  tasks were removed at the parent's request.
- **Completion tracker** per lesson: the bar only says "Lesson complete!" when
  **every answer is correct** (not merely filled in).
- **Anti-cheat**, all baked into the one file:
  - **Hashed answer key.** `data-k` (single), `data-ks` (pipe-joined, multi),
    `data-w` (base64 explanation). No readable answer in the source.
  - **No answer leak.** Wrong/blank feedback never shows the answer or the
    explanation; the explanation appears only after a correct answer.
  - **Shuffled option order**, so the correct choice isn't always first.
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

1. Copy `lesson_builder_template.py` (it's the Lesson 11 build). Set `N` and
   `PREV = N-1`, and replace the six subject bodies with new topics. `SRC`/`OUT`
   point at the locked deliverable, so it appends in place.
2. `python3 your_lesson_N.py` — inserts the new lesson (with **plaintext**
   answers; that's expected).
3. `python3 tools/postprocess.py ../8th-grade-refresher-ONE-FILE.html`
   — hashes the new plaintext keys and re-shuffles option positions.
4. `NODE_PATH=<path-to-jsdom> node tools/verify.js ../8th-grade-refresher-ONE-FILE.html`
   — expect `RESULT: PASS`.
5. Commit, push to branch `claude/eighth-grade-curriculum-arts-jnshgy`, send the
   file in chat.

Keep math **gentle** (whole numbers, worked examples, calculator OK). Keep the
other subjects normal, not dumbed down.

## Files

| File | Purpose |
|------|---------|
| `lesson_builder_template.py` | Reference builder (Lesson 11) + all builder helpers. Copy → edit → run to add a lesson. |
| `postprocess.py` | Run after inserting a new lesson: hashes plaintext keys + shuffles positions. Reusable. |
| `verify.js` | jsdom end-to-end check: fills correct answers via the page hash, asserts no JS errors, all non-practice lessons complete, garbage stays locked. |
| `lockdown.py` | The **one-time** full transform (hash keys + JS surgery) that first locked the file. Kept for reference / rebuilding from a plaintext master. Do **not** re-run on the already-locked file — its JS anchors are gone. |

## Verifying needs jsdom (dev only)

`verify.js` requires `jsdom` (e.g. `npm i jsdom` in a scratch dir, then run with
`NODE_PATH` pointing at its `node_modules`). jsdom stubs `<canvas>`, so studio
drawing isn't exercised there — only grading, the tracker, and JS errors are.
