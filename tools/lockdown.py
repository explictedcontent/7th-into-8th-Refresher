# -*- coding: utf-8 -*-
import re, base64, html

SRC = "/home/user/7th-into-8th-Refresher/8th-grade-refresher-ONE-FILE.html"
SHIP = SRC
VERIFY = "/tmp/htmltest/verify_copy.html"

raw = open(SRC, encoding="utf-8").read()

# ---------- hash + normalize (MUST match the JS _nz/_h exactly) ----------
def nz(s):
    s = str(s).strip().lower()
    if re.match(r'^[-+]?[0-9.]+$', s):
        try:
            f = float(s)
            if f == int(f):
                return str(int(f))
            return repr(f)
        except Exception:
            pass
    return s

def H(s):
    s = nz(s)
    h = 5381
    for ch in s:
        h = ((h * 33) ^ ord(ch)) & 0xFFFFFFFF
    return format(h, 'x')

def W(s):
    txt = html.unescape(s)
    return base64.b64encode(txt.encode('utf-8')).decode('ascii')

plain_single = []   # (hash, plaintext)
plain_multi  = []   # (hashjoined, plaintext_join)
plain_prob   = []

def build(with_vk):
    h = raw

    # data-answers -> data-ks   (multi)  -- do BEFORE data-answer
    def rep_answers(m):
        parts = [p for p in m.group(1).split('|') if p != '']
        hashed = '|'.join(H(html.unescape(p)) for p in parts)
        vk = ' data-vk="%s"' % html.escape('|'.join(parts), quote=True) if with_vk else ''
        return 'data-ks="%s"%s' % (hashed, vk)
    h = re.sub(r'data-answers="([^"]*)"', rep_answers, h)

    # data-answer -> data-k  (single quiz, tagging select, practice prob)
    def rep_answer(m):
        v = m.group(1)
        vk = ' data-vk="%s"' % html.escape(v, quote=True) if with_vk else ''
        return 'data-k="%s"%s' % (H(html.unescape(v)), vk)
    h = re.sub(r'data-answer="([^"]*)"', rep_answer, h)

    # data-why -> data-w  (base64)
    h = re.sub(r'data-why="([^"]*)"', lambda m: 'data-w="%s"' % W(m.group(1)), h)

    return h

# ---------- record plaintext for the verifier (from the ORIGINAL html) ----------
for m in re.finditer(r'data-answers="([^"]*)"', raw):
    parts = [p for p in m.group(1).split('|') if p != '']
    plain_multi.append(('|'.join(H(html.unescape(p)) for p in parts), '|'.join(parts)))
for m in re.finditer(r'data-answer="([^"]*)"', raw):
    plain_single.append((H(html.unescape(m.group(1))), m.group(1)))

ship = build(False)
vcopy = build(True)

# ---------- JS surgery (shared engine — each anchor appears once) ----------
def sub1(h, old, new, tag):
    assert h.count(old) == 1, "anchor %s count=%d" % (tag, h.count(old))
    return h.replace(old, new, 1)

HELPERS = (
"  /* ===== anti-cheat helpers ===== */\n"
"  function _nz(s){ s=(''+s).trim().toLowerCase();\n"
"    if(/^[-+]?[0-9.]+$/.test(s)){ var f=parseFloat(s); if(!isNaN(f)){ if(f===Math.floor(f)&&isFinite(f)) return ''+Math.round(f); return ''+f; } }\n"
"    return s; }\n"
"  function _h(s){ s=_nz(s); var h=5381; for(var i=0;i<s.length;i++){ h=((h*33)^s.charCodeAt(i))>>>0; } return h.toString(16); }\n"
"  function _dw(b){ try{ return decodeURIComponent(escape(atob(b))); }catch(e){ return ''; } }\n\n"
"  /* ===== Quiz engine ===== */\n")

def js_patch(h):
    h = sub1(h, "  /* ===== Quiz engine ===== */\n", HELPERS, "helpers")

    # quiz: why source
    h = sub1(h,
        "        var why=q.getAttribute('data-why')||'';",
        "        var why=_dw(q.getAttribute('data-w')||'');", "why-src")

    # multi: answers attr
    h = sub1(h,
        "          var ans=(q.getAttribute('data-answers')||'').split('|').filter(Boolean);",
        "          var ans=(q.getAttribute('data-ks')||'').split('|').filter(Boolean);", "multi-ans")
    # multi: picked hashed
    h = sub1(h,
        "          var picked=[]; q.querySelectorAll('.options input:checked').forEach(function(i){ picked.push(i.value); });",
        "          var picked=[]; q.querySelectorAll('.options input:checked').forEach(function(i){ picked.push(_h(i.value)); });", "multi-picked")
    # multi: reveal loop -> no correct highlight
    h = sub1(h,
        "          q.querySelectorAll('.options input').forEach(function(input){\n"
        "            var isAns=ans.indexOf(input.value)>=0;\n"
        "            if(isAns) input.closest('label').classList.add('correct');\n"
        "            if(input.checked && !isAns) input.closest('label').classList.add('wrong');\n"
        "          });",
        "          q.querySelectorAll('.options input').forEach(function(input){\n"
        "            if(input.checked && ans.indexOf(_h(input.value))<0) input.closest('label').classList.add('wrong');\n"
        "          });", "multi-reveal")
    # multi feedback: strip why on wrong/skip
    h = sub1(h,
        "            else if(picked.length){ q.classList.add('q-wrong'); feedback.className='feedback show miss'; feedback.textContent='❌ Not quite — pick ALL the right ones and none of the wrong ones. '+why; }",
        "            else if(picked.length){ q.classList.add('q-wrong'); feedback.className='feedback show miss'; feedback.textContent='❌ Not quite — re-check your picks, look back at the lesson, and try again.'; }", "multi-wrong")
    h = sub1(h,
        "            else { q.classList.add('q-wrong'); feedback.className='feedback show miss'; feedback.textContent='⚠️ You skipped this one. '+why; }\n"
        "          }\n"
        "          return;",
        "            else { q.classList.add('q-wrong'); feedback.className='feedback show miss'; feedback.textContent='⚠️ Pick your answers first.'; }\n"
        "          }\n"
        "          return;", "multi-skip")

    # single: answer attr
    h = sub1(h,
        "        var answer=q.getAttribute('data-answer');\n"
        "        var chosen=q.querySelector('input:checked');\n"
        "        q.querySelectorAll('.options input').forEach(function(input){\n"
        "          if(input.value===answer) input.closest('label').classList.add('correct'); });",
        "        var answer=q.getAttribute('data-k');\n"
        "        var chosen=q.querySelector('input:checked');", "single-attr+reveal")
    h = sub1(h,
        "          if(chosen&&chosen.value===answer){ correct++; q.classList.add('q-right'); feedback.className='feedback show right'; feedback.textContent='✅ Correct! '+why; }",
        "          if(chosen&&_h(chosen.value)===answer){ correct++; q.classList.add('q-right'); feedback.className='feedback show right'; feedback.textContent='✅ Correct! '+why; }", "single-ok")
    h = sub1(h,
        "          else if(chosen){ q.classList.add('q-wrong'); chosen.closest('label').classList.add('wrong'); feedback.className='feedback show miss'; feedback.textContent='❌ Not quite. '+why; }",
        "          else if(chosen){ q.classList.add('q-wrong'); chosen.closest('label').classList.add('wrong'); feedback.className='feedback show miss'; feedback.textContent='❌ Not quite — look back at the lesson and try again.'; }", "single-wrong")
    h = sub1(h,
        "          else { q.classList.add('q-wrong'); feedback.className='feedback show miss'; feedback.textContent='⚠️ You skipped this one. '+why; }\n"
        "        }\n"
        "      });\n"
        "      if(scoreEl){",
        "          else { q.classList.add('q-wrong'); feedback.className='feedback show miss'; feedback.textContent='⚠️ Pick an answer first.'; }\n"
        "        }\n"
        "      });\n"
        "      if(scoreEl){", "single-skip")

    # practice grader
    h = sub1(h,
        "        var ans=(p.getAttribute('data-answer')||'').trim().toLowerCase();\n"
        "        var input=p.querySelector('input'); var mark=p.querySelector('.mark');\n"
        "        var val=(input?input.value:'').trim().toLowerCase();\n"
        "        var ok=val===ans;\n"
        "        if(!ok&&val!==''&&!isNaN(parseFloat(ans))&&!isNaN(parseFloat(val))) ok=parseFloat(val)===parseFloat(ans);",
        "        var key=p.getAttribute('data-k')||'';\n"
        "        var input=p.querySelector('input'); var mark=p.querySelector('.mark');\n"
        "        var val=(input?input.value:'').trim();\n"
        "        var ok=val!=='' && _h(val)===key;", "practice")

    # tagging grader
    h = sub1(h,
        "      box.querySelectorAll('select[data-answer]').forEach(function(sel){\n"
        "        total++; var ok=sel.value===sel.getAttribute('data-answer');",
        "      box.querySelectorAll('select[data-k]').forEach(function(sel){\n"
        "        total++; var ok=_h(sel.value)===sel.getAttribute('data-k');", "tagging")

    # tracker steps() -> correctness-gated
    old_steps = (
"    function steps(part){\n"
"      var done=0,total=0;\n"
"      part.querySelectorAll('form.quiz .question').forEach(function(q){\n"
"        total++; if(q.querySelector('input:checked')) done++; });\n"
"      part.querySelectorAll('[data-practice] .prob input').forEach(function(inp){\n"
"        total++; if(inp.value.trim()!=='') done++; });\n"
"      part.querySelectorAll('[data-tagging] select[data-answer]').forEach(function(s){\n"
"        total++; if(s.value!=='') done++; });\n"
"      part.querySelectorAll('textarea.write[data-min]').forEach(function(t){\n"
"        total++; var mn=parseInt(t.getAttribute('data-min')||'0',10);\n"
"        var w=t.value.trim()?t.value.trim().split(/\\s+/).length:0; if(w>=mn) done++; });\n"
"      return {done:done,total:total};\n"
"    }")
    new_steps = (
"    function steps(part){\n"
"      var done=0,total=0;\n"
"      part.querySelectorAll('form.quiz .question').forEach(function(q){\n"
"        total++;\n"
"        if(q.classList.contains('multi')){\n"
"          var ans=(q.getAttribute('data-ks')||'').split('|').filter(Boolean);\n"
"          var picked=[]; q.querySelectorAll('.options input:checked').forEach(function(i){ picked.push(_h(i.value)); });\n"
"          if(ans.length>0 && picked.length===ans.length && ans.every(function(a){ return picked.indexOf(a)>=0; })) done++;\n"
"        } else {\n"
"          var c=q.querySelector('input:checked');\n"
"          if(c && _h(c.value)===q.getAttribute('data-k')) done++;\n"
"        }\n"
"      });\n"
"      part.querySelectorAll('[data-practice] .prob').forEach(function(p){\n"
"        total++; var inp=p.querySelector('input');\n"
"        if(inp && inp.value.trim()!=='' && _h(inp.value)===p.getAttribute('data-k')) done++; });\n"
"      part.querySelectorAll('[data-tagging] select[data-k]').forEach(function(s){\n"
"        total++; if(_h(s.value)===s.getAttribute('data-k')) done++; });\n"
"      part.querySelectorAll('textarea.write[data-min]').forEach(function(t){\n"
"        total++; var mn=parseInt(t.getAttribute('data-min')||'0',10);\n"
"        var w=t.value.trim()?t.value.trim().split(/\\s+/).length:0; if(w>=mn) done++; });\n"
"      return {done:done,total:total};\n"
"    }")
    h = sub1(h, old_steps, new_steps, "tracker-steps")

    # tracker label wording
    h = sub1(h,
        "          if(label) label.innerHTML='✅ <strong>Lesson complete!</strong> You answered every question and finished every writing task. Amazing work — you earned this one!'; }",
        "          if(label) label.innerHTML='✅ <strong>Lesson complete!</strong> Every answer is correct and every writing task is done. Amazing work — you earned this one!'; }", "done-msg")
    h = sub1(h,
        "          if(label) label.textContent=s.done+' of '+s.total+' steps done — finish them all to complete the lesson'; }",
        "          if(label) label.textContent=s.done+' of '+s.total+' correct — every answer must be right to complete the lesson'; }", "prog-msg")
    return h

ship = js_patch(ship)
vcopy = js_patch(vcopy)

# sanity: no plaintext answer keys left in the shipped file
assert 'data-answer=' not in ship, "data-answer leaked"
assert 'data-answers=' not in ship, "data-answers leaked"
assert 'data-why=' not in ship, "data-why leaked"
assert 'data-vk=' not in ship, "data-vk leaked into ship"
assert ship.count('function _h(') == 1

open(SHIP, "w", encoding="utf-8").write(ship)
open(VERIFY, "w", encoding="utf-8").write(vcopy)

import json
json.dump({"single": plain_single, "multi": plain_multi},
          open("/tmp/htmltest/answers.json", "w"))
print("data-k written:", ship.count('data-k='))
print("data-ks written:", ship.count('data-ks='))
print("data-w written:", ship.count('data-w='))
print("single answers:", len(plain_single), "multi:", len(plain_multi))
print("OK: no plaintext answer keys in ship file")
