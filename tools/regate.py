# -*- coding: utf-8 -*-
# Remove existing writing gates + un-gate sections, so add_gate.py can re-place
# them at the new (later) position. Safe now that autosave uses stable keys.
import re, sys
F = sys.argv[1]
h = open(F, encoding="utf-8").read()
n0 = h.count('class="panel writing-gate"')
# remove the gate sections
h = re.sub(r'<section class="panel writing-gate">.*?</section>', '', h, flags=re.S)
# un-gate: strip the gating classes back off
h = h.replace(' gated locked-hidden', '')
open(F, "w", encoding="utf-8").write(h)
print("removed", n0, "gates; remaining writing-gate:", h.count('class="panel writing-gate"'), "| gated classes left:", h.count('gated locked-hidden'))
