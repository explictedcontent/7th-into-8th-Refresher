/* ===========================================================
   Shared logic for the longer lessons' activities:
   - Practice sets (type-in answers, graded together)
   - Word-tagging exercises (label parts of speech, etc.)
   - Live word counters for writing tasks
   =========================================================== */

document.addEventListener("DOMContentLoaded", function () {

  /* ---- Practice sets ---- */
  document.querySelectorAll("[data-practice]").forEach(function (set) {
    const grade = set.querySelector("[data-grade]");
    if (!grade) return;
    grade.addEventListener("click", function () {
      let correct = 0, total = 0;
      set.querySelectorAll(".prob").forEach(function (p) {
        total++;
        const ans = (p.getAttribute("data-answer") || "").trim().toLowerCase();
        const input = p.querySelector("input");
        const mark = p.querySelector(".mark");
        const val = (input ? input.value : "").trim().toLowerCase();
        let ok = val === ans;
        if (!ok && val !== "" && !isNaN(parseFloat(ans)) && !isNaN(parseFloat(val))) {
          ok = parseFloat(val) === parseFloat(ans);
        }
        if (mark) {
          mark.textContent = val === "" ? "—" : (ok ? "✅" : "❌");
          mark.style.color = ok ? "var(--good)" : "var(--bad)";
        }
        if (ok) correct++;
      });
      const score = set.querySelector("[data-practice-score]");
      if (score) {
        score.classList.add("show");
        score.textContent = "You solved " + correct + " of " + total + " correctly"
          + (correct === total ? " — perfect! 🌟" : ". Fix the ❌ and try again.");
      }
    });
  });

  /* ---- Word-tagging exercises ---- */
  document.querySelectorAll("[data-tagging]").forEach(function (box) {
    const grade = box.querySelector("[data-grade]");
    if (!grade) return;
    grade.addEventListener("click", function () {
      let correct = 0, total = 0;
      box.querySelectorAll("select[data-answer]").forEach(function (sel) {
        total++;
        const ok = sel.value === sel.getAttribute("data-answer");
        sel.classList.remove("ok", "no");
        sel.classList.add(ok ? "ok" : "no");
        if (ok) correct++;
      });
      const score = box.querySelector("[data-tag-score]");
      if (score) {
        score.classList.add("show");
        score.textContent = "You labeled " + correct + " of " + total + " correctly"
          + (correct === total ? " — nice! 🌟" : ". Red ones need another look.");
      }
    });
  });

  /* ---- Live word counters ---- */
  document.querySelectorAll("textarea.write").forEach(function (t) {
    const out = t.getAttribute("data-count") ? document.querySelector(t.getAttribute("data-count")) : null;
    function update() {
      const words = t.value.trim() ? t.value.trim().split(/\s+/).length : 0;
      if (out) out.textContent = words + (words === 1 ? " word" : " words");
    }
    t.addEventListener("input", update);
    update();
  });

});
