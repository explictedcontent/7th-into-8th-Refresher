# 🚀 8th Grade Launchpad — A 7th → 8th Grade Refresher

An interactive, browser-based summer review course for a student finishing 7th
grade and heading into 8th. Everything runs locally in any web browser — no
internet, login, or install required.

## ▶️ How to start

1. Download/clone this folder.
2. Double-click **`index.html`** — it opens in your web browser.
3. Pick a subject and work through Lesson 1. Click **Check my answers** on each
   quiz for instant feedback.

> Tip: works fully offline. Nothing is uploaded anywhere — the optional name you
> enter is saved only in your own browser.

## ⏱️ Built for a *real* 30 minutes

Every lesson is paced to a genuine **30 minutes** of work (not 15!):

- A **pacing timer** at the top of each lesson counts up to 30:00 and shows
  which segment to work on. Press **▶ Start lesson** to begin.
- The timer **auto-pauses when you switch tabs**, so only real on-task time
  counts — no rushing through.
- It **remembers your time** if the page is refreshed.
- At 30 minutes a **🎉 Break screen** appears: take 10–15 minutes, then come
  back for a second lesson. Two lessons + a break ≈ **one hour**.

## 📚 What's included (Lesson 1 for each subject)

Each lesson is broken into timed segments — warm-up, learn, lots of practice,
a create/apply task, and a quiz — with self-checking throughout.

| Subject | Lesson 1 topic | Interactive work (~30 min) |
|---|---|---|
| 🎨 **Art** *(her favorite — featured first)* | Elements of Art, Value & Color Theory | Element-spotting, color-mixer, and a guided **"Complementary Sunset" studio challenge** you paint & save |
| 🔢 **Math** | Integers, PEMDAS & Algebra Preview | Mental-math warm-up + 4 graded practice sets (integers, PEMDAS, substitution, word problems) + 6-question quiz |
| 📖 **English / Language Arts** | Parts of Speech & Strong Sentences | Word-tagging, fix-the-sentence, a **reading passage with comprehension**, and a **writing task** with self-check |
| 🔬 **Science** | Scientific Method & Lab Safety | Variable-tagging, a **design-your-own-experiment** planner, a **data-table** reading, and safety quiz |
| 🗺️ **Social Studies** | Map Skills, Continents & Coordinates | Continent matching, map-scale math, latitude/longitude practice, and a **reading passage** |

Every lesson has clear goals, worked examples, memory tricks, and self-checking
practice that explains *why* each answer is right.

## 🗂️ Project structure

```
index.html                 ← home page (start here)
lessons/
  art.html                 ← 🎨 Art + drawing studio
  math.html
  english.html
  science.html
  social-studies.html
assets/
  css/styles.css           ← shared look & feel
  js/quiz.js               ← shared quiz engine + name greeting
  js/activities.js         ← practice sets, word-tagging, writing word-count
  js/timer.js              ← 30-minute pacing timer + break screen
  js/studio.js             ← drawing-canvas logic for Art
```

## 🧩 Designed to grow

The lessons all share the same quiz engine, so adding **Lesson 2, 3, …** is easy:
copy a lesson page, change the content, and the quizzes "just work."

Made with ❤️ for a soon-to-be 8th grader.
