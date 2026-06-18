/* ===========================================================
   Lesson pacing timer — makes each lesson a REAL 30 minutes.

   A page opts in by defining, before this script loads:
     window.LESSON_PLAN = {
       minutes: 30,
       segments: [ { label: "Warm-up", min: 5 }, ... ]
     };
   and including the .pacer markup + #breakOverlay.

   Features:
   - Counts up to the target (default 30:00) and shows progress.
   - Auto-pauses when the tab is hidden, so only real on-task
     time counts (no "AI 30 minutes").
   - Remembers elapsed time on this computer (survives refresh).
   - Shows a Break screen at the target time.
   =========================================================== */

document.addEventListener("DOMContentLoaded", function () {
  const plan = window.LESSON_PLAN;
  const pacer = document.getElementById("pacer");
  if (!plan || !pacer) return;

  const targetSec = (plan.minutes || 30) * 60;
  const segs = plan.segments || [];
  let cum = 0;
  segs.forEach(function (s) { s.start = cum; cum += s.min * 60; s.end = cum; });

  const storeKey = "pace:" + location.pathname.split("/").pop();
  let elapsed = parseInt(localStorage.getItem(storeKey) || "0", 10);
  let running = false;
  let ticker = null;
  let breakShown = false;

  const timeEl = pacer.querySelector("[data-time]");
  const fillEl = pacer.querySelector("[data-fill]");
  const segEl = pacer.querySelector("[data-seg]");
  const toggleBtn = pacer.querySelector("[data-toggle]");
  const resetBtn = pacer.querySelector("[data-reset]");

  function fmt(s) {
    const m = Math.floor(s / 60);
    const ss = s % 60;
    return (m < 10 ? "0" : "") + m + ":" + (ss < 10 ? "0" : "") + ss;
  }

  function render() {
    timeEl.textContent = fmt(Math.min(elapsed, targetSec)) + " / " + fmt(targetSec);
    fillEl.style.width = Math.min(100, (elapsed / targetSec) * 100) + "%";
    const cur = segs.find(function (s) { return elapsed < s.end; }) || segs[segs.length - 1];
    if (cur && segEl) {
      segEl.innerHTML = "Spend about <b>" + cur.min + " min</b> here · Now on: <b>" + cur.label + "</b>";
    }
    if (elapsed >= targetSec && !breakShown) {
      breakShown = true;
      pause();
      showBreak();
    }
  }

  function persist() { localStorage.setItem(storeKey, String(elapsed)); }

  function start() {
    if (running) return;
    running = true;
    toggleBtn.textContent = "⏸ Pause";
    pacer.classList.add("running");
    ticker = setInterval(function () {
      elapsed++;
      persist();
      render();
    }, 1000);
  }

  function pause() {
    running = false;
    toggleBtn.textContent = elapsed > 0 ? "▶ Resume" : "▶ Start lesson";
    pacer.classList.remove("running");
    clearInterval(ticker);
  }

  toggleBtn.addEventListener("click", function () { running ? pause() : start(); });
  resetBtn.addEventListener("click", function () {
    pause();
    elapsed = 0;
    breakShown = false;
    persist();
    render();
  });

  // Only count REAL minutes: pause when the tab/window is hidden.
  document.addEventListener("visibilitychange", function () {
    if (document.hidden && running) pause();
  });

  // Break overlay
  function showBreak() {
    const ov = document.getElementById("breakOverlay");
    if (ov) {
      ov.classList.add("show");
    } else {
      alert("🎉 That's 30 minutes — great work! Take a 10–15 minute break, then come back for the next lesson.");
    }
  }
  const keepBtn = document.getElementById("breakKeep");
  if (keepBtn) keepBtn.addEventListener("click", function () {
    document.getElementById("breakOverlay").classList.remove("show");
  });

  if (elapsed > 0 && elapsed < targetSec) toggleBtn.textContent = "▶ Resume";
  render();
});
