# Curriculum Notes

**Deliverable:** `8th-grade-refresher-ONE-FILE.html` — one self-contained HTML file
(works in the school Chromebook's online HTML viewer: open → Select All → Copy → paste).

## How checking works (parent-controlled)

The student gets **no per-question right/wrong feedback** — that's what let her
brute-force answers by checking one at a time. Instead:

- **She sees only** a neutral "Answered X of N — keep going" bar. No correctness
  signal anywhere she can watch.
- **The parent sees the real scores** behind a PIN. A discreet **🔒 Parent** button
  (bottom-right) opens a report of every lesson's *answered / correct / writing /
  status* across all subjects. The parent **creates the PIN on first open** — do
  this once before handing over the laptop. (Answer key is one-way hashed in the
  source, so nothing is readable there either.)

## Writing gates (must-do, mid-lesson)

Every lesson has a **writing checkpoint placed in the middle** (never at the end).
The rest of the lesson stays **hidden/locked until at least 60 words are written**,
and a popup nudges her to finish it before continuing — so she can't skip writing
and jump ahead. The parent report shows the word count per lesson.

## Persistence

Answers are saved per-control with **stable keys**, so **adding a new lesson no
longer wipes previous progress** (as long as she keeps using the same online
viewer). One growing master file — no separate download per day needed.

## What's included

- Six subjects: **Art, Math, English, Science, Anatomy, Social Studies**
- **12 lessons each** (~38 graded steps: drop-downs, select-all, typed practice,
  multiple choice) + one mid-lesson 60-word writing gate each
- Art's drawing studios include a colour wheel + a real blend/smudge tool
- Shuffled answer positions; hashed answer key; render-verified in jsdom (no JS errors)
