# Curriculum Notes

**Deliverable:** `8th-grade-refresher-ONE-FILE.html` — one self-contained HTML file
(works in the school Chromebook's online HTML viewer: open → Select All → Copy → paste).

## Lesson size — quadrupled for a real ~2 hours of work

The lessons were **quadrupled** from the early versions. Every lesson is now built to
**exactly 40 graded steps** (drop-downs, select-all questions, typed practice, multiple
choice, plus two ~100-word writing tasks), so a full pass adds up to a **real ~2 hours of
work** across the subjects — not a 10-minute click-through.

A sticky **completion tracker** at the top of each lesson only reads **"Lesson complete!"**
once every question is answered and every writing task hits its word minimum, so the work
can't be skipped to "finish" early.

## Anti-cheat lockdown

Closed the four ways the work could be skipped:

1. **The completion bar now counts CORRECT answers, not just filled-in ones.**
   A step only turns green when the answer is actually right, so clicking random
   options no longer reaches "Lesson complete!". The bar reads *"X of N correct —
   every answer must be right to complete the lesson."*
2. **Wrong/blank answers no longer reveal the answer.** Feedback on a miss just
   says "look back at the lesson and try again" — the explanation only appears
   once the answer is correct, and the correct option is never highlighted on a
   wrong try.
3. **The answer key is hashed in the source.** `data-answer`/`data-why` are gone;
   answers are stored as one-way hashes and explanations are base64-encoded, so
   reading the pasted source shows only gibberish — nothing to copy.

Verified end-to-end: filling every question with the correct answer grades 100%
and completes all 66 lessons; filling garbage leaves lessons locked. No JS errors.

## What's included

- Six subjects: **Art, Math, English, Science, Anatomy, Social Studies**
- **11 lessons each** (Art's drawing studios include a colour wheel + a real blend/smudge tool)
- Autosave/restore (survives closing, refresh, power loss) + clear wrong-answer marking
- Every exercise auto-graded and render-verified in a real browser (Chromium); no JS errors
