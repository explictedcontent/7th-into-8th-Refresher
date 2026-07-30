/*
 * verify.js — jsdom smoke test for the deliverable's current architecture.
 * Checks, on one lesson (default a non-math lesson so answers are hash-fillable):
 *   - no JS errors on load
 *   - the writing gate hides sections, then UNLOCKS them once 60 words are typed
 *   - the student progress bar reads "Answered X of N" (no correctness leak)
 *   - the PIN-gated parent report scores a fully-correct lesson as all-correct
 *
 * Usage:  node tools/verify.js <file> [lessonId]      (default lessonId: social-12)
 * Requires: npm i jsdom   (dev-only; run with NODE_PATH pointing at node_modules)
 */
const fs = require('fs');
const { JSDOM } = require('jsdom');
const file = process.argv[2] || '8th-grade-refresher-ONE-FILE.html';
const LID = process.argv[3] || 'social-12';
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://x.test/' });
const { window } = dom, d = window.document;
window.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, { get: () => () => ({ data: [0,0,0,0] }) });
window.HTMLElement.prototype.scrollIntoView = function(){};
const errs = []; window.addEventListener('error', e => errs.push(e.message));
function nz(s){s=(''+s).trim().toLowerCase();if(/^[-+]?[0-9.]+$/.test(s)){var f=parseFloat(s);if(!isNaN(f)){if(f===Math.floor(f)&&isFinite(f))return ''+Math.round(f);return ''+f;}}return s;}
function H(s){s=nz(s);var h=5381;for(var i=0;i<s.length;i++){h=((h*33)^s.charCodeAt(i))>>>0;}return h.toString(16);}

window.addEventListener('DOMContentLoaded', () => window.setTimeout(() => {
  const part = d.getElementById(LID);
  if (!part) { console.log('lesson not found:', LID); process.exit(1); }
  const bar = (part.querySelector('.lp-label') || {}).textContent || '';
  const gatedTotal = part.querySelectorAll('.gated').length;
  const hiddenBefore = part.querySelectorAll('.gated.locked-hidden').length;
  const ta = part.querySelector('.writing-gate textarea');
  ta.value = Array.from({length:62},(_,i)=>'w'+i).join(' ');
  ta.dispatchEvent(new window.Event('input', { bubbles:true }));
  const hiddenAfter = part.querySelectorAll('.gated.locked-hidden').length;
  part.querySelectorAll('form.quiz .question').forEach(q => {
    if (q.classList.contains('multi')) { const ks=(q.getAttribute('data-ks')||'').split('|'); q.querySelectorAll('.options input').forEach(i=>i.checked=ks.indexOf(H(i.value))>=0); }
    else { const k=q.getAttribute('data-k'); q.querySelectorAll('.options input').forEach(i=>i.checked=(H(i.value)===k)); }
  });
  part.querySelectorAll('[data-tagging] select[data-k]').forEach(s => { const k=s.getAttribute('data-k'); [...s.options].forEach(o=>{ if(o.value&&H(o.value)===k) s.value=o.value; }); });
  const probs = part.querySelectorAll('[data-practice] .prob').length;
  d.querySelector('[data-parent]').click();
  d.querySelector('[data-pin-input]').value = '4428';
  d.querySelector('[data-pin-go]').click();
  const repEl = d.querySelector('.parent-report');
  // new report format: each lesson is a .rep-line (div or <details>) whose text is "Lesson N · Title ... status"
  const norm = s => (''+s).replace(/[^a-z0-9]/gi,'').toLowerCase();
  const titleKey = norm((part.querySelector('h1')||{}).textContent||'').slice(0,14);
  const line = [...repEl.querySelectorAll('.rep-line')].find(el => titleKey && norm(el.textContent).includes(titleKey));
  const row = line ? [line.textContent.replace(/\s+/g,' ').trim().slice(0,90)] : [];
  const barOk = /^Answered \d+ of \d+/.test(bar);
  const gateOk = hiddenBefore>0 && hiddenAfter===0;
  const allCorrect = probs>0 ? true : (!!line && /all correct/.test(line.textContent));
  console.log('file:', file, '| lesson:', LID);
  console.log('JS errors:', errs.length ? errs.slice(0,3) : 'NONE');
  console.log('student bar:', JSON.stringify(bar), barOk?'✓':'✗');
  console.log('writing gate: gated', gatedTotal, '| hidden before', hiddenBefore, '| after 62 words', hiddenAfter, gateOk?'✓':'✗');
  console.log('typed-practice probs (not hash-fillable):', probs);
  console.log('parent report row:', row[0] || '(none)');
  const ok = errs.length===0 && barOk && gateOk && allCorrect;
  console.log(ok ? '\nRESULT: PASS' : '\nRESULT: FAIL');
  process.exit(ok?0:1);
}, 480));
