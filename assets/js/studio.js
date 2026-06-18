/* ===========================================================
   Mini Art Studio — a real paint canvas for the Art lesson.
   Mouse + touch drawing, color swatches, brush size,
   clear, and save-as-image.
   =========================================================== */

document.addEventListener("DOMContentLoaded", function () {
  const canvas = document.getElementById("artCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  // Crisp internal resolution
  canvas.width = 800;
  canvas.height = 480;
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.lineCap = "round";
  ctx.lineJoin = "round";

  let drawing = false;
  let color = "#8b5cf6";
  let size = 8;
  let last = { x: 0, y: 0 };

  function pos(e) {
    const rect = canvas.getBoundingClientRect();
    const point = e.touches ? e.touches[0] : e;
    return {
      x: (point.clientX - rect.left) * (canvas.width / rect.width),
      y: (point.clientY - rect.top) * (canvas.height / rect.height),
    };
  }

  function start(e) {
    drawing = true;
    last = pos(e);
    // a dot so a single tap leaves a mark
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.arc(last.x, last.y, size / 2, 0, Math.PI * 2);
    ctx.fill();
    e.preventDefault();
  }

  function move(e) {
    if (!drawing) return;
    const p = pos(e);
    ctx.strokeStyle = color;
    ctx.lineWidth = size;
    ctx.beginPath();
    ctx.moveTo(last.x, last.y);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
    last = p;
    e.preventDefault();
  }

  function end() { drawing = false; }

  canvas.addEventListener("mousedown", start);
  canvas.addEventListener("mousemove", move);
  window.addEventListener("mouseup", end);
  canvas.addEventListener("touchstart", start, { passive: false });
  canvas.addEventListener("touchmove", move, { passive: false });
  canvas.addEventListener("touchend", end);

  // Color swatches
  document.querySelectorAll(".swatch").forEach(function (s) {
    s.style.background = s.dataset.color;
    s.addEventListener("click", function () {
      color = s.dataset.color;
      document.querySelectorAll(".swatch").forEach(function (x) { x.classList.remove("active"); });
      s.classList.add("active");
    });
  });
  const first = document.querySelector(".swatch");
  if (first) first.classList.add("active");

  // Brush size
  const slider = document.getElementById("brushSize");
  const sizeLabel = document.getElementById("brushVal");
  if (slider) {
    slider.addEventListener("input", function () {
      size = parseInt(slider.value, 10);
      if (sizeLabel) sizeLabel.textContent = size + "px";
    });
  }

  // Clear
  const clearBtn = document.getElementById("clearBtn");
  if (clearBtn) clearBtn.addEventListener("click", function () {
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  });

  // Save
  const saveBtn = document.getElementById("saveBtn");
  if (saveBtn) saveBtn.addEventListener("click", function () {
    const link = document.createElement("a");
    link.download = "my-artwork.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
  });
});
