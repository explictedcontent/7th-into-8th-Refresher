/*
 * verify.js — self-contained end-to-end check of the deliverable.
 * Loads the file in jsdom, fills every quiz question and drop-down with the
 * CORRECT answer (found by matching the page's own hash — no answer key file
 * needed), clicks all Check buttons, and asserts:
 *   - no JS errors
 *   - every lesson WITHOUT typed-practice completes on correct answers
 *   - a garbage-filled lesson does NOT complete (anti-cheat still holds)
 * Practice (typed) answers can't be derived from a one-way hash, so lessons
 * containing .prob inputs are reported separately, not auto-completed.
 *
 * Usage:  node tools/verify.js path/to/deliverable.html
 * Requires: npm i jsdom   (dev-only; not shipped in the single HTML file)
 */
const fs = require('fs');
const { JSDOM } = require('jsdom');
const file = process.argv[2] || '8th-grade-refresher-ONE-FILE.html';
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), { runScripts: 'dangerously', pretendToBeVisual: true });
const { window } = dom, d = window.document;
window.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: () => () => ({ data: [0,0,0,0] }) });
const errs = []; window.addEventListener('error', e => errs.push(e.message));

// mirror of the page's _nz/_h (keep in sync with the quiz engine)
function nz(s){s=(''+s).trim().toLowerCase();if(/^[-+]?[0-9.]+$/.test(s)){var f=parseFloat(s);if(!isNaN(f)){if(f===Math.floor(f)&&isFinite(f))return ''+Math.round(f);return ''+f;}}return s;}
function H(s){s=nz(s);var h=5381;for(var i=0;i<s.length;i++){h=((h*33)^s.charCodeAt(i))>>>0;}return h.toString(16);}

function fillCorrect(root){
  root.querySelectorAll('form.quiz .question').forEach(q => {
    if (q.classList.contains('multi')) {
      const keys = (q.getAttribute('data-ks')||'').split('|');
      q.querySelectorAll('.options input').forEach(i => i.checked = keys.indexOf(H(i.value)) >= 0);
    } else {
      const k = q.getAttribute('data-k');
      q.querySelectorAll('.options input').forEach(i => i.checked = (H(i.value) === k));
    }
  });
  root.querySelectorAll('[data-tagging] select[data-k]').forEach(s => {
    const k = s.getAttribute('data-k');
    [...s.options].forEach(o => { if (o.value && H(o.value) === k) s.value = o.value; });
  });
}

window.addEventListener('DOMContentLoaded', () => window.setTimeout(() => {
  fillCorrect(d);
  d.querySelectorAll('[data-check],[data-grade]').forEach(b => b.click());
  d.dispatchEvent(new window.Event('input', { bubbles: true }));

  const parts = [...d.querySelectorAll('.lesson-part')];
  let noPractice = 0, done = 0, withPractice = 0, incomplete = [];
  parts.forEach(p => {
    const hasProb = p.querySelectorAll('[data-practice] .prob').length > 0;
    const complete = (p.querySelector('.lesson-progress')||{classList:{contains:()=>false}}).classList.contains('done');
    if (hasProb) { withPractice++; }
    else { noPractice++; if (complete) done++; else incomplete.push(p.id); }
  });

  const qwrong = d.querySelectorAll('.q-wrong').length;
  const swrong = d.querySelectorAll('select.no').length;

  // negative: garbage in one lesson must NOT complete
  const g = parts.find(p => p.querySelectorAll('form.quiz .question:not(.multi)').length >= 3);
  g.querySelectorAll('form.quiz .question').forEach(q => { const f=q.querySelector('.options input'); if(f){q.querySelectorAll('.options input').forEach(i=>i.checked=false); f.checked=true;} });
  g.querySelectorAll('[data-tagging] select').forEach(s => s.selectedIndex = s.options.length-1);
  g.querySelectorAll('[data-check],[data-grade]').forEach(b => b.click());
  d.dispatchEvent(new window.Event('input', { bubbles: true }));
  const garbageComplete = g.querySelector('.lesson-progress').classList.contains('done');

  console.log('file:', file);
  console.log('JS errors:', errs.length ? errs.slice(0,3) : 'NONE');
  console.log('quiz wrong on correct fill:', qwrong, '| dropdown wrong:', swrong, '(both should be 0)');
  console.log('lessons w/o practice:', noPractice, '| complete on correct answers:', done, incomplete.length?('| INCOMPLETE: '+incomplete.join(',')):'');
  console.log('lessons with typed practice (not auto-filled):', withPractice);
  console.log('NEGATIVE — garbage lesson', g.id, 'complete?', garbageComplete, '(should be false)');
  const ok = errs.length===0 && qwrong===0 && swrong===0 && incomplete.length===0 && !garbageComplete;
  console.log(ok ? '\nRESULT: PASS' : '\nRESULT: FAIL');
  process.exit(ok ? 0 : 1);
}, 400));
