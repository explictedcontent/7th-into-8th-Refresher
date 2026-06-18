/* ===========================================================
   Shared interactive quiz engine
   Works on any page that has:
     <form class="quiz"> ... </form>
   Each .question has data-answer="<value of correct input>"
   and an optional data-why="explanation".
   A button with [data-check] grades; [data-reset] clears.
   =========================================================== */

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("form.quiz").forEach(setupQuiz);
  setupGreeting();
});

function setupQuiz(form) {
  const questions = form.querySelectorAll(".question");
  const checkBtn = form.querySelector("[data-check]");
  const resetBtn = form.querySelector("[data-reset]");
  const scoreEl = form.querySelector(".score");

  if (checkBtn) {
    checkBtn.addEventListener("click", function () {
      let correct = 0;
      questions.forEach(function (q) {
        const answer = q.getAttribute("data-answer");
        const why = q.getAttribute("data-why") || "";
        const chosen = q.querySelector("input:checked");
        const feedback = q.querySelector(".feedback");

        // clear previous styling
        q.querySelectorAll(".options label").forEach(function (l) {
          l.classList.remove("correct", "wrong");
        });

        q.querySelectorAll(".options input").forEach(function (input) {
          const label = input.closest("label");
          if (input.value === answer) label.classList.add("correct");
        });

        if (feedback) {
          feedback.classList.add("show");
          if (chosen && chosen.value === answer) {
            correct++;
            feedback.className = "feedback show right";
            feedback.textContent = "✅ Correct! " + why;
          } else if (chosen) {
            chosen.closest("label").classList.add("wrong");
            feedback.className = "feedback show miss";
            feedback.textContent = "❌ Not quite. " + why;
          } else {
            feedback.className = "feedback show miss";
            feedback.textContent = "⚠️ You skipped this one. " + why;
          }
        }
      });

      if (scoreEl) {
        const total = questions.length;
        scoreEl.classList.add("show");
        let msg = "You got " + correct + " / " + total + ". ";
        const pct = correct / total;
        if (pct === 1) msg += "Perfect! 🌟 You're ready for 8th grade!";
        else if (pct >= 0.7) msg += "Great work! 💪 Review the misses and you've got it.";
        else msg += "Good start! 🌱 Re-read the lesson and try again.";
        scoreEl.textContent = msg;
        scoreEl.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      form.querySelectorAll("input").forEach(function (i) { i.checked = false; });
      form.querySelectorAll(".feedback").forEach(function (f) {
        f.classList.remove("show", "right", "miss");
        f.textContent = "";
      });
      form.querySelectorAll(".options label").forEach(function (l) {
        l.classList.remove("correct", "wrong");
      });
      if (scoreEl) { scoreEl.classList.remove("show"); scoreEl.textContent = ""; }
    });
  }
}

/* Friendly name greeting saved in the browser (optional, private to this PC) */
function setupGreeting() {
  const el = document.querySelector("[data-greeting]");
  if (!el) return;
  const saved = localStorage.getItem("learnerName");
  if (saved) el.textContent = "Welcome back, " + saved + "! 👋";
}

function saveName() {
  const input = document.getElementById("nameInput");
  const el = document.querySelector("[data-greeting]");
  if (input && input.value.trim()) {
    localStorage.setItem("learnerName", input.value.trim());
    if (el) el.textContent = "Welcome, " + input.value.trim() + "! 👋 Let's learn.";
  }
}
