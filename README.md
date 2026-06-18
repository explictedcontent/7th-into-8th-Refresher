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

## 📚 What's included (Lesson 1 for each subject)

| Subject | Lesson 1 topic | Interactive bits |
|---|---|---|
| 🎨 **Art** *(her favorite — featured first)* | Elements of Art & Color Theory | Real **drawing studio** (paint, brush sizes, save your art) + color-mixer |
| 🔢 **Math** | Integers & Order of Operations (PEMDAS) | "Try it" calculators + 4-question quiz |
| 📖 **English / Language Arts** | Parts of Speech & Strong Sentences | Find-the-verb practice + quiz |
| 🔬 **Science** | Scientific Method & Lab Safety | Spot-the-variable practice + quiz |
| 🗺️ **Social Studies** | Map Skills, Continents & Coordinates | Latitude/longitude practice + quiz |

Every lesson has clear goals, worked examples, memory tricks, and a
self-checking quiz that explains *why* each answer is right.

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
  js/studio.js             ← drawing-canvas logic for Art
```

## 🧩 Designed to grow

The lessons all share the same quiz engine, so adding **Lesson 2, 3, …** is easy:
copy a lesson page, change the content, and the quizzes "just work."

Made with ❤️ for a soon-to-be 8th grader.
