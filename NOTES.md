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
  status*. The parent PIN is **4310** (checked as a one-way hash, so it is not readable in the source).
  **Each lesson expands to show exactly what was missed** — a Question / She put /
  Correct table (her answers in red, correct answers in green). Typed math answers
  stay hidden ("— (open lesson)") so they can't be extracted; everything else shows
  the correct answer. (Answer key is one-way hashed in the source, so nothing is
  readable there either.)

## Writing gates (must-do, mid-lesson)

Every lesson has a **writing checkpoint placed in the middle** (never at the end).
The rest of the lesson stays **hidden/locked until at least 60 words are written**,
and a popup nudges her to finish it before continuing — so she can't skip writing
and jump ahead. The parent report shows the word count per lesson.

## Persistence

Answers are saved per-control with **stable keys**, so **adding a new lesson no
longer wipes previous progress** (as long as she keeps using the same online
viewer). One growing master file — no separate download per day needed.

## Fun & engagement (global — auto-applies to every lesson)

Added a game layer that never weakens the anti-cheat (rewards are for *finishing*,
never for revealing answers). All of these are runtime modules that iterate every
lesson, so **new lessons get them automatically**:

- **🎉 Confetti + celebration** when a lesson is fully answered, and a confetti/
  "🔓 Unlocked!" toast when the writing gate is cleared.
- **⭐ XP, levels, badges & a daily streak**, shown on a **progress map** on the
  home screen (per-subject bars + earned badges). Keys: `rf_done`, `rf_streak`.
- **🎨 Avatar + colour-theme picker** on home (5 themes, 12 avatars).
  Keys: `rf_avatar`, `rf_theme`.
- **🕹️ Drag-and-drop / tap-to-place word matching** replaces the tagging
  drop-downs: word chips + inline blanks. It drives the same hidden `<select>`
  elements, so grading, autosave and the parent report are unchanged.
- Also removed the old top-bar **"Check all my answers"** button — it revealed
  the score to the student (now parent-report only).

## What's included

- Six subjects: **Art, Math, English, Science, Anatomy, Social Studies**
- **21 lessons each** (~38 graded steps: drop-downs, select-all, typed practice,
  multiple choice) + one mid-lesson 60-word writing gate each
- Art's drawing studios include a colour wheel + a real blend/smudge tool
- Shuffled answer positions; hashed answer key; render-verified in jsdom (no JS errors)
