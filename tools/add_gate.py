# -*- coding: utf-8 -*-
# Insert a mid-lesson writing gate into any lesson-part that doesn't have one.
import re, sys
F = sys.argv[1]
h = open(F, encoding="utf-8").read()

def gate_html(sub, n):
    wid = "wg-%s-%d" % (sub, n)
    return ('<section class="panel writing-gate"><h2>✍️ Writing checkpoint — finish this to keep going</h2>'
'<p>Before the rest of this lesson opens up, write <strong>at least 60 words</strong> in your own words: '
'explain what you have learned so far in this lesson and give one example. Take your time — real sentences count.</p>'
'<div class="tryit"><textarea class="write" data-count="#%s" data-min="60" placeholder="Write at least 60 words here…"></textarea>'
'<div class="wordcount" id="%s">0 / 60 words</div></div>'
'<p class="gate-status">🔒 Write at least 60 words to unlock the rest of this lesson.</p></section>') % (wid, wid)

sec_re = re.compile(r'<section class="panel[^"]*"[^>]*>.*?</section>', re.S)
added = [0]

def transform_part(m):
    inner = m.group('inner')
    if 'class="panel writing-gate"' in inner:
        return m.group(0)  # already has a gate — skip
    sub, n = m.group('sub'), int(m.group('n'))
    chunks = []; pos = 0
    for sm in sec_re.finditer(inner):
        if sm.start() > pos: chunks.append(('ws', inner[pos:sm.start()]))
        chunks.append(('sec', sm.group(0))); pos = sm.end()
    tail = inner[pos:]
    nsec = sum(1 for t,_ in chunks if t == 'sec')
    if nsec == 0: return m.group(0)
    gi = max(1, nsec // 2)
    if gi >= nsec: gi = nsec - 1 if nsec > 1 else nsec
    out = ''; si = 0; inserted = False
    for t, text in chunks:
        if t == 'sec':
            if si == gi and not inserted: out += gate_html(sub, n); inserted = True
            if si >= gi: text = text.replace('<section class="panel', '<section class="panel gated locked-hidden', 1)
            out += text; si += 1
        else: out += text
    if not inserted: out += gate_html(sub, n)
    tail = tail.replace('<div class="lesson-nav', '<div class="lesson-nav gated locked-hidden', 1)
    added[0] += 1
    return m.group('open') + out + tail + m.group('close')

part_re = re.compile(r'(?P<open><div class="lesson-part[^"]*" id="(?P<sub>[a-z]+)-(?P<n>\d+)">)(?P<inner>.*?)(?P<close></div><!-- /(?P=sub)-(?P=n) -->)', re.S)
h = part_re.sub(transform_part, h)
open(F, "w", encoding="utf-8").write(h)
print("gates added to", added[0], "parts; total writing-gate sections:", h.count('class="panel writing-gate"'))
