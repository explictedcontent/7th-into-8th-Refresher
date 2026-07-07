# -*- coding: utf-8 -*-
"""
postprocess.py — run AFTER inserting a new (plaintext) lesson into the
already-locked deliverable. It:
  1. Hashes any remaining plaintext answer keys:
       data-answer="X"   -> data-k="<hash>"
       data-answers="a|b" -> data-ks="<hash>|<hash>"
       data-why="..."      -> data-w="<base64>"
     (existing lessons are already hashed, so only the new lesson is affected)
  2. Shuffles the option order of every quiz/checkbox group and drop-down so the
     correct answer is never fixed in one position ("all A").

It does NOT touch the JS engine — the one-time lockdown JS surgery (see
lockdown.py) has already been applied to the deliverable.

Usage:  python3 tools/postprocess.py path/to/deliverable.html
Grading is by hashed VALUE, not position, so shuffling never affects correctness.
"""
import re, sys, base64, html, random

def nz(s):
    s = str(s).strip().lower()
    if re.match(r'^[-+]?[0-9.]+$', s):
        try:
            f = float(s); return str(int(f)) if f == int(f) else repr(f)
        except Exception: pass
    return s

def H(s):
    s = nz(s); h = 5381
    for ch in s: h = ((h * 33) ^ ord(ch)) & 0xFFFFFFFF
    return format(h, 'x')

def hash_keys(h):
    h = re.sub(r'data-answers="([^"]*)"',
               lambda m: 'data-ks="%s"' % '|'.join(H(html.unescape(p)) for p in m.group(1).split('|') if p != ''), h)
    h = re.sub(r'data-answer="([^"]*)"',
               lambda m: 'data-k="%s"' % H(html.unescape(m.group(1))), h)
    h = re.sub(r'data-why="([^"]*)"',
               lambda m: 'data-w="%s"' % base64.b64encode(html.unescape(m.group(1)).encode('utf-8')).decode('ascii'), h)
    return h

def shuffle_positions(h, seed=1):
    random.seed(seed)
    def shuf_opts(m):
        labels = re.findall(r'<label>.*?</label>', m.group(1), re.S)
        if len(labels) > 1: random.shuffle(labels)
        return '<div class="options">' + ''.join(labels) + '</div>'
    h = re.sub(r'<div class="options">(.*?)</div>', shuf_opts, h, flags=re.S)
    def shuf_sel(m):
        opts = re.findall(r'<option.*?</option>', m.group(2), re.S)
        empty = [o for o in opts if 'value=""' in o]; rest = [o for o in opts if 'value=""' not in o]
        if len(rest) > 1: random.shuffle(rest)
        return m.group(1) + ''.join(empty + rest) + '</select>'
    return re.sub(r'(<select\b[^>]*>)(.*?)</select>', shuf_sel, h, flags=re.S)

if __name__ == '__main__':
    f = sys.argv[1]
    h = open(f, encoding='utf-8').read()
    plain = h.count('data-answer=') + h.count('data-answers=') + h.count('data-why=')
    h = hash_keys(h)
    h = shuffle_positions(h)
    open(f, 'w', encoding='utf-8').write(h)
    assert 'data-answer=' not in h and 'data-why=' not in h, "plaintext key still present"
    print("hashed %d plaintext keys; positions shuffled; 0 plaintext keys remain" % plain)
