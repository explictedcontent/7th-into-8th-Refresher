# -*- coding: utf-8 -*-
"""
lesson_builder_template.py — reference builder for adding a lesson to ALL six
subjects. This is the Lesson 11 build, kept as a working template.

TO ADD LESSON N (the file is already anti-cheat "locked"):
  1. Copy this file. Set N and PREV (= N-1). SRC and OUT already point at the
     locked deliverable, so add() appends the new lesson in place.
  2. Replace the six subject bodies below with new topics. Keep the same
     structure so each lesson lands on ~38 graded steps (the assemble() pad
     asserts the count). Builders emit PLAINTEXT data-answer/data-answers/
     data-why — that is expected; postprocess.py hashes them next.
  3. Run:  python3 your_lesson.py
  4. Lock + shuffle the new answers:  python3 tools/postprocess.py <deliverable>
  5. Verify:  NODE_PATH=<jsdom> node tools/verify.js <deliverable>
  6. Commit, push, deliver.

Builder helpers: sel, prob, pset, tagblock, mquiz, quiz, panel, howto,
assemble (pads to 40 minus current via a review pool), add (inserts body +
rewrites the previous lesson's forward nav and adds the tab button).
Note: writing tasks (writebox) were removed from the deliverable at the
parent's request — do not re-add them unless asked.
"""
import re
SRC = "/home/user/7th-into-8th-Refresher/8th-grade-refresher-ONE-FILE.html"  # the locked deliverable
OUT = "/home/user/7th-into-8th-Refresher/8th-grade-refresher-ONE-FILE.html"  # write back in place; then run postprocess.py
h = open(SRC, encoding="utf-8").read()
N = 11
PREV = 10

def sel(ans,*opts):
    o='<option value="">choose…</option>'
    for v,l in opts: o+='<option value="%s">%s</option>'%(v,l)
    return '<select data-answer="%s">%s</select>'%(ans,o)
def prob(n,q,a):
    return ('<div class="prob" data-answer="%s"><span class="pnum">%d</span><span class="qtext">%s</span>'
            '<input type="text" inputmode="text" /><span class="mark"></span></div>')%(a,n,q)
def pset(title,intro,probs):
    return ('<section class="panel"><h2>%s</h2>%s<div data-practice><div class="practice-grid">%s</div>'
            '<div class="btn-row"><button type="button" class="btn" data-grade>Check answers</button>'
            '<span class="score" data-practice-score></span></div></div></section>')%(title,intro,"".join(probs))
def tagblock(title,intro,tl):
    return ('<section class="panel"><h2>%s</h2><p>%s</p><div data-tagging><p class="tagline">%s</p>'
            '<div class="btn-row"><button type="button" class="btn" data-grade>Check</button>'
            '<span class="score" data-tag-score></span></div></div></section>')%(title,intro,tl)
def example(t): return '<div class="callout"><span class="ico">💡</span><div><strong>How to do it:</strong> %s</div></div>'%t
def mquiz(qid,items):
    out=[]
    for i,(qq,opts,why) in enumerate(items,1):
        ans="|".join(v for (v,l,c) in opts if c)
        labels="".join('<label><input type="checkbox" name="%sm%d" value="%s" />%s</label>'%(qid,i,v,l) for (v,l,c) in opts)
        out.append('<div class="question multi" data-answers="%s" data-why="%s"><div class="q"><span class="num">%d</span>%s <span class="selhint">(tick every correct one)</span></div><div class="options">%s</div><div class="feedback"></div></div>'%(ans,why,i,qq,labels))
    return ('<section class="panel"><h2>☑️ Select ALL that apply</h2><p>These can have more than one right answer — tick every correct box.</p><form class="quiz">%s'
            '<div class="btn-row"><button type="button" class="btn" data-check>Check my answers</button>'
            '<button type="button" class="btn ghost" data-reset>Reset</button><span class="score"></span></div></form></section>')%"".join(out)
def quiz(qid,items,heading="✏️ Quick Check"):
    out=[]
    for i,(qq,opts,why) in enumerate(items,1):
        ans=[v for (v,l,c) in opts if c][0]
        labels="".join('<label><input type="radio" name="%sz%d" value="%s" />%s</label>'%(qid,i,v,l) for (v,l,c) in opts)
        out.append('<div class="question" data-answer="%s" data-why="%s"><div class="q"><span class="num">%d</span>%s</div><div class="options">%s</div><div class="feedback"></div></div>'%(ans,why,i,qq,labels))
    return ('<section class="panel"><h2>%s</h2><form class="quiz">%s'
            '<div class="btn-row"><button type="button" class="btn" data-check>Check my answers</button>'
            '<button type="button" class="btn ghost" data-reset>Reset</button><span class="score"></span></div></form></section>')%(heading,"".join(out))
def writebox(cid,mn,prompt,heading):
    return ('<section class="panel"><h2>%s</h2><p>%s</p><div class="tryit">'
            '<textarea class="write" data-count="#%s" data-min="%d" placeholder="Write your answer here…"></textarea>'
            '<div class="wordcount" id="%s">0 / %d words</div></div></section>')%(heading,prompt,cid,mn,cid,mn)
def panel(title,html): return '<section class="panel"><h2>%s</h2>%s</section>'%(title,html)
def goals(items): return '<ul class="goal-list">%s</ul>'%"".join('<li>%s</li>'%t for t in items)
def plan(items): return '<ul class="plan-strip">%s</ul>'%"".join('<li><b>%d.</b> %s</li>'%(i+1,t) for i,t in enumerate(items))
def howto():
    return panel('🧭 How this lesson works — read this first',
      goals(['Read each <strong>coloured box</strong> first — it teaches and shows you how.',
             'Drop-downs (▾): pick the <strong>one</strong> correct word.',
             '<strong>☑ Select-all boxes:</strong> tick <em>every</em> correct one, leave the wrong ones empty.',
             'Type-in boxes: work it out and type the answer.',
             'Writing boxes: keep writing until the counter turns <strong>green ✓</strong>.'])
      +'<div class="callout"><span class="ico">📊</span><div>The bar at the top fills as you get answers <strong>right</strong>. Keep going until it says <strong>“Lesson complete!”</strong></div></div>')
def head(s,klass,kicker,title,intro):
    return ('<div class="lesson-part" id="%s-%d">\n    <header class="lesson-head %s"><div class="kicker">%s</div>'
            '<h1>%s</h1><p>%s</p></header>\n')%(s,N,klass,kicker,title,intro)
def review(title,pairs):
    out=""
    for ci in range(0,len(pairs),8):
        chunk=pairs[ci:ci+8]
        items="".join("%s %s. "%(c,s) for c,s in chunk)
        t=title if ci==0 else title+" (cont.)"
        out+=('<section class="panel"><h2>⚡ %s</h2><p>Quick-fire review — get every blank right to finish the lesson.</p>'
            '<div data-tagging><p class="tagline">%s</p><div class="btn-row"><button type="button" class="btn" data-grade>Check</button>'
            '<span class="score" data-tag-score></span></div></div></section>')%(t,items)
    return out
def navp(s,fwd_onclick,fwd_label):
    return ('    <div class="lesson-nav"><span class="back-link" onclick="showPart(\'%s\',%d)">← %s · Lesson %d</span>\n'
            '      <span class="back-link" onclick="%s">%s</span></div>\n    </div><!-- /%s-%d -->')%(s,PREV,s.capitalize(),PREV,fwd_onclick,fwd_label,s,N)
def steps(frag):
    q=frag.count('class="question"')+frag.count('class="question multi"')
    p=frag.count('class="prob"'); t=len(re.findall(r'<select data-answer=',frag)); w=len(re.findall(r'data-min="\d+"',frag))
    return q+p+t+w
def assemble(s,klass,kicker,title,intro,planlist,body_mid,pool,fwd_onclick,fwd_label,revtitle):
    main=head(s,klass,kicker,title,intro)+howto()+panel('🎯 Today’s plan',plan(planlist))+body_mid
    cur=steps(main); pad=40-cur
    assert 0<=pad<=len(pool), "%s pad=%d (cur=%d, pool=%d)"%(s,pad,cur,len(pool))
    block=review(revtitle,pool[:pad]) if pad>0 else ""
    return main+block+navp(s,fwd_onclick,fwd_label)
def add(h,s,body):
    tab_old='<button class="lt" onclick="showPart(\'%s\',%d)">Lesson %d</button></div>'%(s,PREV,PREV)
    assert h.count(tab_old)==1, "tab %s x%d"%(s,h.count(tab_old))
    h=h.replace(tab_old, tab_old[:-6]+'<button class="lt" onclick="showPart(\'%s\',%d)">Lesson %d</button></div>'%(s,N,N),1)
    pat=re.compile(r'<span class="back-link" onclick="show[^"]*\([^)]*\)">[^<]*</span></div>\n    </div><!-- /'+s+r'-'+str(PREV)+r' -->')
    repl='<span class="back-link" onclick="showPart(\''+s+'\','+str(N)+')">Next: '+s.capitalize()+' · Lesson '+str(N)+' →</span></div>\n    </div><!-- /'+s+'-'+str(PREV)+' -->'
    assert len(pat.findall(h))==1, "prev fwd %s"%s
    h=pat.sub(lambda m: repl,h,count=1)
    mk='</div><!-- /%s-%d -->'%(s,PREV)
    h=h.replace(mk, mk+"\n\n"+body,1)
    return h

# ===================== ART L11: Colour Harmony & Schemes =====================
art_studio=('<section class="panel"><h2>🖌️ Studio · Build a colour scheme</h2>'
 '<p><strong>What to do:</strong> Pick ONE scheme and paint a simple shape or pattern using only those colours. <strong>How:</strong> for <em>analogous</em> use colours next to each other (blue → blue-green → green); for <em>complementary</em> use two opposites (blue &amp; orange); for <em>monochromatic</em> pick one colour and use the side bar to make lighter tints and darker shades. Use the <strong>Blend tool</strong> to mix neighbours smoothly.</p>'
 '<div class="studio"><div class="tools"><div class="swatches">'
 +"".join('<span class="swatch" data-color="%s" title="c"></span>'%c for c in ['#2d6cdf','#1fae8b','#8fce00','#f5c518','#f0883e','#e5484d','#8b5cf6','#ffffff'])
 +'</div><div class="wheel-wrap"><div class="color-wheel" title="Tap to blend a colour"></div><div class="wheel-side"><span class="color-current"></span><input type="range" class="shade-slider" min="8" max="92" value="50" /></div></div>'
 '<div class="brush-size"><label for="brushSize12">Brush</label><input type="range" id="brushSize12" min="2" max="60" value="16" /><span data-brushval>16px</span></div></div>'
 '<div class="canvas-wrap"><canvas id="artCanvas12" aria-label="Colour scheme studio"></canvas></div>'
 '<div class="btn-row"><button class="btn" data-save>💾 Save</button><button class="btn ghost" data-clear>🧽 Clear</button></div></div></section>')
art_mid=(panel('🎨 Colours that work together',
   '<p>A <strong>colour scheme</strong> is a planned set of colours that look good together. Here are the main ones:</p>'
   '<table class="tidy"><tr><th>Scheme</th><th>What it is</th></tr>'
   '<tr><td><strong>Monochromatic</strong></td><td>ONE colour, plus its lighter tints and darker shades</td></tr>'
   '<tr><td><strong>Analogous</strong></td><td>Colours that sit NEXT to each other on the wheel (calm, harmonious)</td></tr>'
   '<tr><td><strong>Complementary</strong></td><td>Two OPPOSITE colours (blue &amp; orange) — bold, high contrast</td></tr>'
   '<tr><td><strong>Triadic</strong></td><td>THREE colours evenly spaced on the wheel (red, yellow, blue)</td></tr>'
   '<tr><td><strong>Warm / cool</strong></td><td>Warm = reds/oranges/yellows; cool = blues/greens/purples</td></tr></table>'
   +example('For a calm, gentle picture, choose ANALOGOUS colours like blue, blue-green and green. For something that really pops, use COMPLEMENTARY opposites like blue and orange next to each other.'))
 + tagblock('🟢 Name the scheme','Fill each blank.',
   'One colour with its tints and shades is a ' + sel('mono',('mono','monochromatic'),('tri','triadic'),('comp','complementary'))
   + ' scheme. Colours next to each other on the wheel are ' + sel('anal',('anal','analogous'),('comp','complementary'),('mono','monochromatic'))
   + '. Two opposite colours are ' + sel('comp',('comp','complementary'),('anal','analogous'),('mono','monochromatic'))
   + '. Three evenly-spaced colours are ' + sel('tri',('tri','triadic'),('mono','monochromatic'),('anal','analogous')) + '.')
 + tagblock('🔵 Warm, cool &amp; contrast','Pick the right idea.',
   'Reds, oranges and yellows are ' + sel('warm',('warm','warm colours'),('cool','cool colours'))
   + '. Blues, greens and purples are ' + sel('cool',('cool','cool colours'),('warm','warm colours'))
   + '. The scheme with the BOLDEST contrast is ' + sel('comp',('comp','complementary'),('mono','monochromatic'))
   + '. The calmest, most harmonious scheme is ' + sel('anal',('anal','analogous'),('comp','complementary')) + '.')
 + mquiz('a11',[
   ('Which are real colour schemes?',[('mono','Monochromatic',1),('anal','Analogous',1),('comp','Complementary',1),('loud','Loudographic',0)],'Monochromatic, analogous and complementary are real schemes; “loudographic” is made up.'),
   ('Which pairs are COMPLEMENTARY (opposite) colours?',[('bo','Blue & orange',1),('rg','Red & green',1),('yp','Yellow & purple',1),('bg','Blue & blue-green',0)],'Opposites are complementary; blue & blue-green are analogous neighbours.'),
   ('Which describe an ANALOGOUS scheme?',[('next','Colours next to each other',1),('calm','Calm and harmonious',1),('one','Blue, blue-green, green',1),('opp','Two opposites',0)],'Analogous = neighbours, calm; two opposites is complementary.')])
 + mquiz('a11b',[
   ('Which belong to a MONOCHROMATIC scheme of blue?',[('navy','Navy (dark blue shade)',1),('sky','Sky (light blue tint)',1),('blue','Plain blue',1),('orange','Bright orange',0)],'Monochromatic = one hue’s tints and shades; orange is a different hue.'),
   ('Which are WARM colours?',[('red','Red',1),('orange','Orange',1),('yellow','Yellow',1),('blue','Blue',0)],'Reds, oranges and yellows are warm; blue is cool.')])
 + art_studio
 + quiz('a11',[
   ('One colour plus its tints and shades is a…',[('mono','Monochromatic scheme',1),('tri','Triadic scheme',0),('warm','Warm scheme',0)],'One hue, many values = monochromatic.'),
   ('Colours next to each other on the wheel are…',[('anal','Analogous',1),('comp','Complementary',0),('mono','Monochromatic',0)],'Neighbours = analogous.'),
   ('Two opposite colours (blue & orange) are…',[('comp','Complementary',1),('anal','Analogous',0),('tri','Triadic',0)],'Opposites = complementary.'),
   ('Three evenly-spaced colours are a…',[('tri','Triadic scheme',1),('mono','Monochromatic scheme',0),('anal','Analogous scheme',0)],'Three evenly spaced = triadic.'),
   ('Reds, oranges and yellows are…',[('warm','Warm colours',1),('cool','Cool colours',0),('none','No colours',0)],'They are warm.'),
   ('Which scheme has the boldest contrast?',[('comp','Complementary',1),('anal','Analogous',0),('mono','Monochromatic',0)],'Opposites create the strongest contrast.'),
   ('Which scheme feels calmest and most harmonious?',[('anal','Analogous',1),('comp','Complementary',0),('tri','Triadic',0)],'Neighbouring colours feel calm.'),
   ('Blues, greens and purples are…',[('cool','Cool colours',1),('warm','Warm colours',0),('grey','Always grey',0)],'They are cool.')])
 + writebox('a11w1',55,'In at least 55 words, choose a colour scheme (monochromatic, analogous, complementary, or triadic) for a bedroom you would design. Name the exact colours you would use and explain why that scheme fits the mood you want.','✍️ Write 1 · Design with a scheme')
 + writebox('a11w2',50,'In at least 50 words, explain the difference between an ANALOGOUS scheme and a COMPLEMENTARY scheme, and describe how each one makes a picture feel.','✍️ Write 2 · Analogous vs. complementary'))
art_pool=[
 ('One colour with tints and shades is', sel('mono',('mono','monochromatic'),('tri','triadic'))),
 ('Colours next to each other are', sel('anal',('anal','analogous'),('comp','complementary'))),
 ('Two opposite colours are', sel('comp',('comp','complementary'),('anal','analogous'))),
 ('Three evenly-spaced colours are', sel('tri',('tri','triadic'),('mono','monochromatic'))),
 ('Reds and oranges are', sel('warm',('warm','warm'),('cool','cool'))),
 ('Blues and greens are', sel('cool',('cool','cool'),('warm','warm'))),
 ('The boldest-contrast scheme is', sel('comp2',('comp2','complementary'),('mono2','monochromatic'))),
 ('The calmest scheme is', sel('anal2',('anal2','analogous'),('comp2','complementary'))),
 ('Blue and orange are', sel('comp3',('comp3','complementary'),('anal3','analogous'))),
 ('A planned set of colours is a colour', sel('scheme',('scheme','scheme'),('shadow','shadow'))),
 ('Adding white to a colour makes a', sel('tint',('tint','tint'),('shade','shade'))),
 ('Adding black to a colour makes a', sel('shade',('shade','shade'),('tint','tint'))),
 ('Red, yellow and blue together are a', sel('tri2',('tri2','triadic scheme'),('mono3','monochromatic scheme'))),
 ('Blue, blue-green and green make an', sel('anal4',('anal4','analogous scheme'),('comp4','complementary scheme'))),
 ('Warm colours tend to feel', sel('energetic',('energetic','energetic'),('sleepy','freezing'))),
 ('Cool colours tend to feel', sel('calm',('calm','calm'),('loud','loud'))),
 ('Colours opposite on the wheel are', sel('comp5',('comp5','complementary'),('same5','identical'))),
 ('A monochromatic picture uses one', sel('hue',('hue','hue/colour'),('shape','shape'))),
 ('Complementary pairs make each other look', sel('brighter',('brighter','brighter'),('duller','invisible'))),
 ('Choosing a scheme first makes a picture look more', sel('planned',('planned','planned/unified'),('messy','messy'))),
]
art_body=assemble('art','head-art','Art · Lesson 11 · ★ Your favorite',
   'Colour Harmony: Schemes That Work Together 🎨',
   'Great artists don’t grab random colours — they choose a plan. Today you learn the main colour schemes and use your blending studio to build one of your own.',
   ['Schemes','Name it','Warm/cool','Studio','Write'], art_mid, art_pool,
   "showLesson('math')",'Next: Math →','Art · Rapid Review')
h=add(h,'art',art_body)

# ===================== MATH L11: Percents in Real Life =====================
math_mid=(panel('％ What is a percent?',
   '<p>A <strong>percent</strong> just means “out of 100.” So <strong>50%</strong> = half, <strong>25%</strong> = a quarter, and <strong>10%</strong> = one tenth. Calculator welcome — but these three are easy by hand:</p>'
   '<div class="callout"><span class="ico">🎯</span><div><strong>10%</strong> → divide by 10 &nbsp;•&nbsp; <strong>50%</strong> → halve it (÷2) &nbsp;•&nbsp; <strong>25%</strong> → quarter it (÷4)</div></div>'
   +example('Find 10% of 80: divide 80 by 10 = <strong>8</strong>. &nbsp; Find 50% of 60: half of 60 = <strong>30</strong>. &nbsp; Find 25% of 40: 40 ÷ 4 = <strong>10</strong>. &nbsp; A $50 jacket with 10% off: 10% of 50 = $5 off, so you pay <strong>$45</strong>.'))
 + pset('🟦 Find 10% (just divide by 10)','Type the number.',[
   prob(1,'10% of 50 =','5'),
   prob(2,'10% of 80 =','8'),
   prob(3,'10% of 120 =','12'),
   prob(4,'10% of 200 =','20')])
 + pset('🟨 Find 50% (halve it) and 25% (quarter it)','Type the number.',[
   prob(1,'50% of 60 =','30'),
   prob(2,'50% of 18 =','9'),
   prob(3,'50% of 150 =','75'),
   prob(4,'25% of 40 =','10'),
   prob(5,'25% of 80 =','20'),
   prob(6,'25% of 200 =','50')])
 + tagblock('🟢 Percent sense','Pick the word.',
   '“Percent” means out of ' + sel('100',('100','100'),('10','10'),('50','50'))
   + '. 50% is the same as ' + sel('half',('half','one half'),('quarter','one quarter'),('tenth','one tenth'))
   + '. To find 10% of a number you ' + sel('div10',('div10','divide by 10'),('times10','multiply by 10'),('div2','divide by 2'))
   + '. A bigger percent of the same number gives a ' + sel('bigger',('bigger','bigger amount'),('smaller','smaller amount')) + '.')
 + mquiz('m11',[
   ('Which are ways to find 50% of a number?',[('half','Take half of it',1),('div2','Divide it by 2',1),('times','Multiply it by 2',0)],'50% = a half = divide by 2; multiplying by 2 doubles it.'),
   ('Which statements are TRUE?',[('p100','Percent means out of 100',1),('q25','25% is a quarter',1),('t10','10% of 90 is 9',1),('h10','10% is the same as a half',0)],'10% is one tenth, not a half.')])
 + quiz('m11',[
   ('“Percent” means out of…',[('100','100',1),('10','10',0),('50','50',0)],'Percent = per hundred.'),
   ('50% of a number is the same as…',[('half','Half of it',1),('double','Double it',0),('quarter','A quarter of it',0)],'50% = one half.'),
   ('To find 10% of a number you…',[('div10','Divide by 10',1),('times10','Multiply by 10',0),('div5','Divide by 5',0)],'10% = divide by 10.'),
   ('25% of 40 is…',[('10','10',1),('20','20',0),('4','4',0)],'40 ÷ 4 = 10.'),
   ('A $30 shirt with 10% off costs…',[('27','$27',1),('20','$20',0),('3','$3',0)],'10% of 30 = 3 off, so $27.'),
   ('Which is the biggest share?',[('50','50%',1),('25','25%',0),('10','10%',0)],'50% is the largest of these.')])
 + writebox('m11w1',55,'In at least 55 words, explain in your own words what a percent is, and show how you would find 10%, 50%, and 25% of $200. Give the answer for each.','✍️ Write 1 · Explain percents')
 + writebox('m11w2',50,'In at least 50 words, describe a real shopping example: pick a price and a discount (like 10% or 50% off), and work out how much you would save and how much you would pay.','✍️ Write 2 · A real discount'))
math_pool=[
 ('Percent means out of', sel('100',('100','100'),('10','10'))),
 ('50% is the same as one', sel('half',('half','half'),('tenth','tenth'))),
 ('25% is the same as one', sel('quarter',('quarter','quarter'),('half','half'))),
 ('To find 10% you divide by', sel('10',('10','10'),('2','2'))),
 ('To find 50% you divide by', sel('2',('2','2'),('10','10'))),
 ('To find 25% you divide by', sel('4',('4','4'),('2','2'))),
 ('10% of 100 is', sel('10a',('10a','10'),('1a','1'))),
 ('50% of 100 is', sel('50a',('50a','50'),('5a','5'))),
 ('25% of 100 is', sel('25a',('25a','25'),('4a','4'))),
 ('10% of 60 is', sel('6a',('6a','6'),('16a','16'))),
 ('50% of 20 is', sel('10b',('10b','10'),('2b','2'))),
 ('25% of 8 is', sel('2c',('2c','2'),('4c','4'))),
 ('A bigger percent gives a', sel('bigger',('bigger','bigger amount'),('smaller','smaller amount'))),
 ('100% of a number is the', sel('whole',('whole','whole thing'),('half2','half'))),
 ('10% off means you keep', sel('90',('90','90%'),('10p','10%'))),
 ('Half of 50 is', sel('25b',('25b','25'),('100b','100'))),
]
math_body=assemble('math','head-math','Math · Lesson 11',
   'Percents in Real Life: Sales, Tips &amp; Shares ％',
   'Percents are everywhere — sales, tips, phone batteries. Good news: 10%, 50% and 25% are easy tricks, not scary maths. We go one small step at a time, calculator welcome.',
   ['What it is','Find 10%','Find 50%/25%','Percent sense','Write'], math_mid, math_pool,
   "showLesson('english')",'Next: English →','Math · Rapid Review')
h=add(h,'math',math_body)

# ===================== ENGLISH L11: Figurative Language =====================
eng_mid=(panel('🗣️ Figurative language — saying more than the plain words',
   '<p><strong>Figurative language</strong> means words used in a colourful, not-literal way to paint pictures and feelings.</p>'
   '<table class="tidy"><tr><th>Tool</th><th>What it is</th></tr>'
   '<tr><td><strong>Simile</strong></td><td>Compares two things using “like” or “as” — <em>brave as a lion</em></td></tr>'
   '<tr><td><strong>Metaphor</strong></td><td>Says one thing IS another — <em>the classroom was a zoo</em></td></tr>'
   '<tr><td><strong>Personification</strong></td><td>Gives human actions to non-human things — <em>the wind whispered</em></td></tr>'
   '<tr><td><strong>Hyperbole</strong></td><td>A huge exaggeration — <em>I’ve told you a million times</em></td></tr>'
   '<tr><td><strong>Onomatopoeia</strong></td><td>A word that sounds like its noise — <em>buzz, splash, bang</em></td></tr>'
   '<tr><td><strong>Idiom</strong></td><td>A saying that doesn’t mean it literally — <em>it’s raining cats and dogs</em></td></tr></table>'
   +example('“The stars danced in the sky” is PERSONIFICATION (stars can’t really dance). “Her bag weighed a ton” is HYPERBOLE (a big exaggeration). “The bees buzzed” uses ONOMATOPOEIA (buzz sounds like the noise).'))
 + tagblock('🟢 Name the tool','Read each example and choose.',
   '“As quiet as a mouse” is a ' + sel('sim',('sim','simile'),('met','metaphor'),('hyp','hyperbole'))
   + '. “Time is a thief” is a ' + sel('met',('met','metaphor'),('sim','simile'),('idi','idiom'))
   + '. “The flowers nodded their heads” is ' + sel('per',('per','personification'),('ono','onomatopoeia'),('sim','simile'))
   + '. “I could eat a horse” is ' + sel('hyp',('hyp','hyperbole'),('idi','idiom'),('met','metaphor')) + '.')
 + tagblock('🔵 Sounds &amp; sayings','Fill the blanks.',
   'Words like buzz, splash and bang are ' + sel('ono',('ono','onomatopoeia'),('idi','idiom'),('sim','simile'))
   + '. “It’s raining cats and dogs” is an ' + sel('idi',('idi','idiom'),('ono','onomatopoeia'),('per','personification'))
   + '. A comparison using the word “like” or “as” is a ' + sel('sim2',('sim2','simile'),('met2','metaphor'))
   + '. Giving human actions to an object is ' + sel('per2',('per2','personification'),('hyp2','hyperbole')) + '.')
 + mquiz('e11',[
   ('Which are SIMILES?',[('brave','“Brave as a lion”',1),('cool','“Cool as a cucumber”',1),('like','“Runs like the wind”',1),('is','“The world is a stage”',0)],'Similes use “like” or “as”; “the world is a stage” is a metaphor.'),
   ('Which are examples of PERSONIFICATION?',[('wind','“The wind whispered”',1),('sun','“The sun smiled down”',1),('leaves','“The leaves danced”',1),('loud','“As loud as thunder”',0)],'Personification gives human traits to non-humans; “as loud as thunder” is a simile.'),
   ('Which are HYPERBOLE (exaggeration)?',[('million','“I’ve said it a million times”',1),('ton','“This bag weighs a ton”',1),('forever','“It took forever”',1),('blue','“The sky is blue”',0)],'Hyperbole is a big exaggeration; “the sky is blue” is literal.')])
 + mquiz('e11b',[
   ('Which words are ONOMATOPOEIA?',[('buzz','buzz',1),('splash','splash',1),('bang','bang',1),('happy','happy',0)],'Buzz, splash and bang imitate sounds; “happy” does not.'),
   ('Which are TRUE about figurative language?',[('picture','It paints pictures & feelings',1),('notlit','It is not meant literally',1),('poems','It is common in poems & stories',1),('math','It is a type of maths',0)],'Figurative language is non-literal and vivid — not maths.')])
 + quiz('e11',[
   ('A comparison using “like” or “as” is a…',[('sim','Simile',1),('met','Metaphor',0),('idi','Idiom',0)],'“like/as” = simile.'),
   ('Saying one thing IS another is a…',[('met','Metaphor',1),('sim','Simile',0),('ono','Onomatopoeia',0)],'X is Y = metaphor.'),
   ('Giving human traits to an object is…',[('per','Personification',1),('hyp','Hyperbole',0),('sim','Simile',0)],'Human traits on non-humans = personification.'),
   ('A giant exaggeration is…',[('hyp','Hyperbole',1),('idi','Idiom',0),('met','Metaphor',0)],'Exaggeration = hyperbole.'),
   ('“Buzz” and “splash” are examples of…',[('ono','Onomatopoeia',1),('sim','Simile',0),('per','Personification',0)],'Sound words = onomatopoeia.'),
   ('“It’s raining cats and dogs” is an…',[('idi','Idiom',1),('met','Metaphor',0),('hyp','Hyperbole',0)],'A non-literal saying = idiom.')])
 + writebox('e11w1',55,'In at least 55 words, write a short description of a stormy day. Include at least one simile, one example of personification, and one piece of onomatopoeia. Then label which is which.','✍️ Write 1 · Storm description')
 + writebox('e11w2',50,'In at least 50 words, explain the difference between a simile, a metaphor, and personification. Make up one fresh example of each.','✍️ Write 2 · Tell them apart'))
eng_pool=[
 ('A comparison using like/as is a', sel('sim',('sim','simile'),('met','metaphor'))),
 ('Saying one thing IS another is a', sel('met',('met','metaphor'),('sim','simile'))),
 ('Human actions on an object is', sel('per',('per','personification'),('hyp','hyperbole'))),
 ('A huge exaggeration is', sel('hyp',('hyp','hyperbole'),('idi','idiom'))),
 ('Words like buzz and bang are', sel('ono',('ono','onomatopoeia'),('sim','simile'))),
 ('A non-literal saying is an', sel('idi',('idi','idiom'),('met','metaphor'))),
 ('“Brave as a lion” is a', sel('sim2',('sim2','simile'),('met2','metaphor'))),
 ('“The wind whispered” is', sel('per2',('per2','personification'),('ono2','onomatopoeia'))),
 ('“I told you a million times” is', sel('hyp2',('hyp2','hyperbole'),('idi2','idiom'))),
 ('“Time is a thief” is a', sel('met3',('met3','metaphor'),('sim3','simile'))),
 ('“Splash” imitates a', sel('sound',('sound','sound'),('colour','colour'))),
 ('Figurative language is not meant to be', sel('literal',('literal','literal'),('read','read'))),
 ('“Raining cats and dogs” is an', sel('idi3',('idi3','idiom'),('ono3','onomatopoeia'))),
 ('A simile always uses like or', sel('as',('as','as'),('is','is'))),
 ('Giving a cloud a face and smile is', sel('per3',('per3','personification'),('hyp3','hyperbole'))),
 ('“Cool as a cucumber” is a', sel('sim4',('sim4','simile'),('met4','metaphor'))),
 ('Exaggerating for effect is', sel('hyp4',('hyp4','hyperbole'),('idi4','idiom'))),
 ('Sound-words make writing more', sel('vivid',('vivid','vivid/lively'),('boring','dull'))),
 ('“The sun smiled” is', sel('per4',('per4','personification'),('sim5','simile'))),
 ('Poets and authors use figurative language to', sel('paint',('paint','paint pictures'),('bore','confuse'))),
]
eng_body=assemble('english','head-english','English · Lesson 11',
   'Figurative Language: Similes, Metaphors &amp; More 📖',
   'Writers make words come alive by NOT saying exactly what they mean. Today you master the six big tools of figurative language — and use them yourself.',
   ['The tools','Name it','Sounds & sayings','Select-all','Write'], eng_mid, eng_pool,
   "showLesson('science')",'Next: Science →','English · Rapid Review')
h=add(h,'english',eng_body)

# ===================== SCIENCE L11: Ecosystems & Food Webs =====================
sci_mid=(panel('🌿 Living things and their homes',
   '<p>An <strong>ecosystem</strong> is all the living things in an area plus their environment, working together. Energy flows through it from the Sun, along a <strong>food chain</strong>.</p>'
   '<table class="tidy"><tr><th>Word</th><th>What it means</th></tr>'
   '<tr><td><strong>Producer</strong></td><td>Makes its own food from sunlight — plants</td></tr>'
   '<tr><td><strong>Consumer</strong></td><td>Eats other living things for energy — animals</td></tr>'
   '<tr><td><strong>Decomposer</strong></td><td>Breaks down dead things — fungi, bacteria, worms</td></tr>'
   '<tr><td><strong>Herbivore</strong></td><td>Eats only plants</td></tr>'
   '<tr><td><strong>Carnivore</strong></td><td>Eats only animals (meat)</td></tr>'
   '<tr><td><strong>Omnivore</strong></td><td>Eats both plants and animals</td></tr></table>'
   +example('A food chain shows who eats whom: grass (producer) → rabbit (herbivore) → fox (carnivore). The arrows point the way ENERGY flows — from the eaten to the eater. When things die, decomposers recycle them back into the soil.'))
 + tagblock('🟢 Who’s who','Fill the blanks.',
   'A plant that makes food from sunlight is a ' + sel('prod',('prod','producer'),('cons','consumer'),('dec','decomposer'))
   + '. An animal that eats other living things is a ' + sel('cons',('cons','consumer'),('prod','producer'),('dec','decomposer'))
   + '. A mushroom that breaks down dead leaves is a ' + sel('dec',('dec','decomposer'),('prod','producer'),('cons','consumer'))
   + '. An animal that eats only plants is a ' + sel('herb',('herb','herbivore'),('carn','carnivore'),('omni','omnivore')) + '.')
 + tagblock('🔵 Energy &amp; eating','Pick the right word.',
   'The original source of energy for almost every ecosystem is the ' + sel('sun',('sun','Sun'),('soil','soil'),('moon','Moon'))
   + '. In a food chain, the arrows show the flow of ' + sel('energy',('energy','energy'),('water','water'),('air','air'))
   + '. An animal that eats both plants and meat is an ' + sel('omni',('omni','omnivore'),('herb','herbivore'),('carn','carnivore'))
   + '. An animal that eats only meat is a ' + sel('carn',('carn','carnivore'),('herb','herbivore'),('prod','producer')) + '.')
 + mquiz('s11',[
   ('Which are PRODUCERS?',[('grass','Grass',1),('tree','A tree',1),('algae','Algae',1),('lion','A lion',0)],'Producers make their own food (plants, algae); a lion is a consumer.'),
   ('Which are DECOMPOSERS?',[('fungi','Fungi/mushrooms',1),('bact','Bacteria',1),('worm','Earthworms',1),('deer','A deer',0)],'Decomposers break down dead matter; a deer is a consumer.')])
 + mquiz('s11b',[
   ('Which are TRUE about food chains?',[('sun','Energy starts with the Sun',1),('arrow','Arrows point to the eater',1),('prod','Producers come first',1),('top','Plants eat animals',0)],'Plants are producers — they don’t eat animals.'),
   ('Which is an example of an OMNIVORE?',[('human','A human',1),('bear','A bear',1),('pig','A pig',1),('cow','A cow (plants only)',0)],'Humans, bears and pigs eat both; a cow is a herbivore.')])
 + quiz('s11',[
   ('A plant that makes its own food is a…',[('prod','Producer',1),('cons','Consumer',0),('dec','Decomposer',0)],'Plants are producers.'),
   ('An animal that eats other living things is a…',[('cons','Consumer',1),('prod','Producer',0),('dec','Decomposer',0)],'Animals are consumers.'),
   ('An animal that eats ONLY plants is a…',[('herb','Herbivore',1),('carn','Carnivore',0),('omni','Omnivore',0)],'Plant-only = herbivore.'),
   ('An animal that eats ONLY meat is a…',[('carn','Carnivore',1),('herb','Herbivore',0),('prod','Producer',0)],'Meat-only = carnivore.'),
   ('Fungi and bacteria that break down dead things are…',[('dec','Decomposers',1),('prod','Producers',0),('herb','Herbivores',0)],'They are decomposers.'),
   ('The energy in almost every food chain starts with the…',[('sun','Sun',1),('soil','Soil',0),('rain','Rain',0)],'Sunlight is the original energy source.')])
 + writebox('s11w1',55,'In at least 55 words, build and explain your own food chain with at least three living things. Say which is the producer, which is the consumer, and how energy flows through it.','✍️ Write 1 · Build a food chain')
 + writebox('s11w2',50,'In at least 50 words, explain why decomposers are important to an ecosystem. What would happen without them?','✍️ Write 2 · Why decomposers matter'))
sci_pool=[
 ('A plant that makes its own food is a', sel('prod',('prod','producer'),('cons','consumer'))),
 ('An animal that eats others is a', sel('cons',('cons','consumer'),('prod','producer'))),
 ('A mushroom breaking down dead leaves is a', sel('dec',('dec','decomposer'),('prod','producer'))),
 ('An animal that eats only plants is a', sel('herb',('herb','herbivore'),('carn','carnivore'))),
 ('An animal that eats only meat is a', sel('carn',('carn','carnivore'),('herb','herbivore'))),
 ('An animal that eats both is an', sel('omni',('omni','omnivore'),('prod','producer'))),
 ('Energy for most ecosystems comes from the', sel('sun',('sun','Sun'),('soil','soil'))),
 ('Food-chain arrows show the flow of', sel('energy',('energy','energy'),('water','water'))),
 ('All living + non-living things in an area make an', sel('eco',('eco','ecosystem'),('atom','atom'))),
 ('Producers are usually', sel('plants',('plants','plants'),('rocks','rocks'))),
 ('The first link in a food chain is a', sel('prod2',('prod2','producer'),('carn2','carnivore'))),
 ('Decomposers recycle nutrients back into the', sel('soil',('soil','soil'),('sky','sky'))),
 ('A rabbit that eats grass is a', sel('herb2',('herb2','herbivore'),('carn3','carnivore'))),
 ('A fox that eats rabbits is a', sel('carn2',('carn2','carnivore'),('prod3','producer'))),
 ('A human that eats plants and meat is an', sel('omni2',('omni2','omnivore'),('herb3','herbivore'))),
 ('Grass → rabbit → fox is a food', sel('chain',('chain','chain'),('ball','ball'))),
 ('Green plants trap sunlight to make', sel('food',('food','food/energy'),('rock','rock'))),
 ('Bacteria and fungi are', sel('dec2',('dec2','decomposers'),('prod4','producers'))),
 ('Many food chains linked together make a food', sel('web',('web','web'),('box','box'))),
 ('Without producers a food chain would have no', sel('start',('start','starting energy'),('colour','colour'))),
]
sci_body=assemble('science','head-science','Science · Lesson 11',
   'Ecosystems &amp; Food Webs: Who Eats Whom 🌿',
   'Every living thing is connected to others through what it eats. Today you follow energy from the Sun, through plants and animals, all the way to the decomposers that recycle it.',
   ['Living things','Who’s who','Energy flow','Select-all','Write'], sci_mid, sci_pool,
   "showLesson('anatomy')",'Next: Anatomy →','Science · Rapid Review')
h=add(h,'science',sci_body)

# ===================== ANATOMY L11: The Immune System =====================
ana_mid=(panel('🛡️ Your body’s defence force',
   '<p>Germs that can make you sick are called <strong>pathogens</strong> (bad bacteria and viruses). Your <strong>immune system</strong> is the army that finds and destroys them.</p>'
   '<table class="tidy"><tr><th>Word</th><th>Job</th></tr>'
   '<tr><td><strong>Pathogen</strong></td><td>A germ that causes disease — a virus or harmful bacteria</td></tr>'
   '<tr><td><strong>White blood cells</strong></td><td>The soldiers that hunt and destroy pathogens</td></tr>'
   '<tr><td><strong>Antibodies</strong></td><td>Special proteins that lock onto and tag germs</td></tr>'
   '<tr><td><strong>Vaccine</strong></td><td>A tiny safe dose that trains your body to fight a germ</td></tr>'
   '<tr><td><strong>Fever</strong></td><td>A higher temperature that helps fight infection</td></tr>'
   '<tr><td><strong>Skin</strong></td><td>Your first barrier — keeps most germs out</td></tr></table>'
   +example('When a virus (pathogen) gets in, your white blood cells attack it and make antibodies that lock onto it. Afterwards your body REMEMBERS that germ, so next time it fights it off faster. A vaccine gives that memory safely, without making you sick.'))
 + tagblock('🟢 Match the defender','Fill the blanks.',
   'A germ that makes you ill is a ' + sel('path',('path','pathogen'),('anti','antibody'),('vac','vaccine'))
   + '. The cells that hunt and destroy germs are ' + sel('wbc',('wbc','white blood cells'),('rbc','red blood cells'),('bone','bone cells'))
   + '. Proteins that lock onto germs are ' + sel('anti',('anti','antibodies'),('sugar','sugars'),('fats','fats'))
   + '. Your first physical barrier against germs is your ' + sel('skin',('skin','skin'),('hair','hair'),('nail','nails')) + '.')
 + tagblock('🔵 Fighting infection','Pick the right idea.',
   'A safe dose that trains your immune system is a ' + sel('vac',('vac','vaccine'),('path','pathogen'),('fever','fever'))
   + '. A higher body temperature that helps fight germs is a ' + sel('fever',('fever','fever'),('chill','shiver'),('bruise','bruise'))
   + '. After beating a germ, your body can ' + sel('remember',('remember','remember it'),('forget','forget it'))
   + ' it. Viruses and harmful bacteria are both types of ' + sel('path2',('path2','pathogen'),('vitamin','vitamin')) + '.')
 + mquiz('an11',[
   ('Which are pathogens (germs that cause disease)?',[('virus','Viruses',1),('bact','Harmful bacteria',1),('flu','The flu germ',1),('wbc','White blood cells',0)],'Viruses and harmful bacteria are pathogens; white blood cells defend you.'),
   ('Which help DEFEND your body?',[('wbc','White blood cells',1),('anti','Antibodies',1),('skin','Your skin',1),('virus','A virus',0)],'White blood cells, antibodies and skin defend; a virus attacks.')])
 + mquiz('an11b',[
   ('Which are TRUE about vaccines?',[('train','They train the immune system',1),('safe','They use a safe dose',1),('mem','They build memory against a germ',1),('sick','They are meant to make you very sick',0)],'Vaccines train immunity safely — not to make you ill.'),
   ('Which can help your body fight infection?',[('fever','A fever',1),('wbc','White blood cells',1),('rest','Rest and fluids',1),('none','Nothing at all',0)],'Fever, white blood cells and rest all help you recover.')])
 + quiz('an11',[
   ('A germ that causes disease is a…',[('path','Pathogen',1),('anti','Antibody',0),('vac','Vaccine',0)],'Disease-causing germ = pathogen.'),
   ('The cells that hunt and destroy germs are…',[('wbc','White blood cells',1),('rbc','Red blood cells',0),('nerve','Nerve cells',0)],'White blood cells fight germs.'),
   ('Proteins that lock onto and tag germs are…',[('anti','Antibodies',1),('sugars','Sugars',0),('bones','Bones',0)],'Tagging proteins = antibodies.'),
   ('A safe dose that trains your immunity is a…',[('vac','Vaccine',1),('fever','Fever',0),('germ','Germ',0)],'That is a vaccine.'),
   ('Your body’s first physical barrier to germs is your…',[('skin','Skin',1),('heart','Heart',0),('brain','Brain',0)],'Skin blocks most germs.'),
   ('A higher temperature that helps fight infection is a…',[('fever','Fever',1),('chill','Shiver',0),('cut','Cut',0)],'That is a fever.')])
 + writebox('an11w1',55,'In at least 55 words, explain how your immune system fights off a germ. Use the words pathogen, white blood cells, and antibodies in your answer.','✍️ Write 1 · How you fight germs')
 + writebox('an11w2',50,'In at least 50 words, explain what a vaccine is and how it helps protect you WITHOUT making you seriously ill.','✍️ Write 2 · How vaccines help'))
ana_pool=[
 ('A germ that causes disease is a', sel('path',('path','pathogen'),('anti','antibody'))),
 ('The cells that destroy germs are', sel('wbc',('wbc','white blood cells'),('rbc','red blood cells'))),
 ('Proteins that lock onto germs are', sel('anti',('anti','antibodies'),('sugars','sugars'))),
 ('A safe dose that trains immunity is a', sel('vac',('vac','vaccine'),('fever','fever'))),
 ('Your first barrier against germs is your', sel('skin',('skin','skin'),('hair','hair'))),
 ('A helpful higher body temperature is a', sel('fever',('fever','fever'),('bruise','bruise'))),
 ('Viruses and harmful bacteria are', sel('path2',('path2','pathogens'),('vitamins','vitamins'))),
 ('The whole defence system is the', sel('immune',('immune','immune system'),('skeletal','skeleton'))),
 ('After beating a germ, the body can', sel('remember',('remember','remember it'),('forget','forget it'))),
 ('White blood cells travel in your', sel('blood',('blood','blood'),('bones','bones'))),
 ('A vaccine builds immune', sel('memory',('memory','memory'),('sugar','sugar'))),
 ('Antibodies are made by the', sel('immune2',('immune2','immune system'),('stomach','stomach'))),
 ('Washing hands removes', sel('germs',('germs','germs'),('bones','bones'))),
 ('The flu is caused by a', sel('virus',('virus','virus'),('vitamin','vitamin'))),
 ('Rest and fluids help you', sel('recover',('recover','recover'),('worsen','get worse'))),
 ('Skin, white cells and antibodies all', sel('defend',('defend','defend you'),('attack','attack you'))),
 ('A vaccine does NOT try to make you', sel('sick',('sick','seriously sick'),('safe','safe'))),
 ('Pathogens are also called', sel('germs2',('germs2','germs'),('cells2','muscles'))),
 ('The immune system is like the body’s', sel('army',('army','army'),('kitchen','kitchen'))),
 ('Once trained, the body fights that germ', sel('faster',('faster','faster next time'),('slower','slower next time'))),
]
ana_body=assemble('anatomy','head-anatomy','Anatomy · Lesson 11',
   'The Immune System: Your Body’s Defence Force 🛡️',
   'Every day your body fights off invisible invaders. Today you meet the germ-fighting army inside you — white blood cells, antibodies, and how vaccines give them a head start.',
   ['Defenders','Match','Fighting infection','Select-all','Write'], ana_mid, ana_pool,
   "showLesson('social')",'Next: Social Studies →','Anatomy · Rapid Review')
h=add(h,'anatomy',ana_body)

# ===================== SOCIAL L11: The Cold War =====================
soc_pass=('<div class="callout" style="display:block"><p style="margin:.2rem 0"><strong>Read this:</strong></p>'
 '<p style="margin:.5rem 0">After World War II, the world’s two strongest countries — the <strong>United States</strong> and the <strong>Soviet Union (USSR)</strong> — became rivals. This long standoff (about <strong>1947–1991</strong>) was called the <strong>Cold War</strong> because the two sides never fought each other directly in a big “hot” war. Instead they competed in other ways. The U.S. believed in <strong>capitalism</strong> and democracy; the Soviet Union believed in <strong>communism</strong>. They raced to build weapons (the <strong>arms race</strong>) and to reach space (the <strong>Space Race</strong>). A divided city, <strong>Berlin</strong>, was split by a wall; when the <strong>Berlin Wall fell in 1989</strong>, the Cold War was ending. The USSR broke apart in <strong>1991</strong>.</p></div>')
soc_mid=(panel('🌍 A war without direct fighting',
   '<table class="tidy"><tr><th>Term</th><th>What it was</th></tr>'
   '<tr><td><strong>Cold War</strong></td><td>A tense rivalry with no direct “hot” fighting between the two sides</td></tr>'
   '<tr><td><strong>United States</strong></td><td>Led the capitalist, democratic side</td></tr>'
   '<tr><td><strong>Soviet Union (USSR)</strong></td><td>Led the communist side</td></tr>'
   '<tr><td><strong>Arms race</strong></td><td>Competing to build more powerful weapons</td></tr>'
   '<tr><td><strong>Space Race</strong></td><td>Competing to reach space and the Moon</td></tr>'
   '<tr><td><strong>Berlin Wall</strong></td><td>A wall dividing Berlin; its fall (1989) signalled the war’s end</td></tr></table>'
   +example('Remember: the Cold War was “cold” because the U.S. and USSR never fought each other head-on. They competed instead — building weapons (arms race) and racing to space. It ended around 1989–1991.'))
 + soc_pass
 + tagblock('🟢 Key facts','Answer from the passage.',
   'The two rivals in the Cold War were the U.S. and the ' + sel('ussr',('ussr','Soviet Union'),('uk','United Kingdom'),('japan','Japan'))
   + '. It was called “cold” because the two sides never fought each other ' + sel('directly',('directly','directly'),('ever','at sea'),('once','in space'))
   + '. The competition to build weapons was the ' + sel('arms',('arms','arms race'),('space','space race'),('gold','gold rush'))
   + '. The wall that divided a famous city was the ' + sel('berlin',('berlin','Berlin Wall'),('great','Great Wall'),('hadrian','Hadrian’s Wall')) + '.')
 + tagblock('🔵 Which belief?','Match the side to its idea.',
   'The United States believed in ' + sel('cap',('cap','capitalism'),('com','communism'))
   + ' and democracy. The Soviet Union believed in ' + sel('com',('com','communism'),('cap','capitalism'))
   + '. The race to reach the Moon was the ' + sel('space',('space','Space Race'),('arms','arms race'))
   + '. The Soviet Union finally broke apart in ' + sel('91',('91','1991'),('45','1945'),('76','1776')) + '.')
 + mquiz('so11',[
   ('Which are TRUE about the Cold War?',[('rivals','The U.S. and USSR were rivals',1),('nodirect','They avoided direct war with each other',1),('space','They competed in a Space Race',1),('same','They shared the same government',0)],'They were rival superpowers with different systems who avoided direct war.'),
   ('Which were ways the two sides COMPETED?',[('arms','Building more weapons',1),('space','Racing to space',1),('allies','Gaining allies around the world',1),('team','Teaming up as one country',0)],'They competed for weapons, space and allies — they did not unite.')])
 + mquiz('so11b',[
   ('Which describe the UNITED STATES’ side?',[('cap','Capitalism',1),('dem','Democracy',1),('west','The “Western” bloc',1),('com','Communism',0)],'The U.S. led the capitalist, democratic West; communism was the Soviet side.'),
   ('Which events signalled the Cold War’s END?',[('wall','The Berlin Wall fell (1989)',1),('ussr','The USSR broke apart (1991)',1),('thaw','Tensions eased',1),('start','A brand-new world war began',0)],'The wall’s fall and the USSR’s breakup ended it — no new world war.')])
 + quiz('so11',[
   ('The Cold War was mainly between the U.S. and the…',[('ussr','Soviet Union',1),('uk','United Kingdom',0),('china','Ancient Rome',0)],'The two superpowers were the U.S. and USSR.'),
   ('It was called “cold” because the two sides…',[('nofight','Never fought each other directly',1),('cold','Fought only in winter',0),('ice','Fought on ice',0)],'No direct “hot” war between them.'),
   ('The United States believed in…',[('cap','Capitalism & democracy',1),('com','Communism',0),('mon','Absolute monarchy',0)],'The U.S. side was capitalist and democratic.'),
   ('The Soviet Union believed in…',[('com','Communism',1),('cap','Capitalism',0),('feud','Feudalism',0)],'The USSR was communist.'),
   ('Competing to build weapons was the…',[('arms','Arms race',1),('space','Space Race',0),('gold','Gold Rush',0)],'That was the arms race.'),
   ('The fall of the Berlin Wall in 1989 signalled the war was…',[('ending','Ending',1),('starting','Just starting',0),('paused','Paused for a day',0)],'Its fall marked the Cold War’s end.')])
 + writebox('so11w1',55,'In at least 55 words, explain what the Cold War was, who the two main sides were, and why it was called “cold” instead of “hot”.','✍️ Write 1 · What was the Cold War?')
 + writebox('so11w2',50,'In at least 50 words, describe TWO ways the United States and the Soviet Union competed without fighting each other directly (for example, the arms race or the Space Race).','✍️ Write 2 · Competing without war'))
soc_pool=[
 ('The Cold War’s two rivals were the U.S. and the', sel('ussr',('ussr','Soviet Union'),('uk','United Kingdom'))),
 ('It was “cold” because they never fought each other', sel('directly',('directly','directly'),('slowly','slowly'))),
 ('The U.S. believed in', sel('cap',('cap','capitalism'),('com','communism'))),
 ('The Soviet Union believed in', sel('com',('com','communism'),('cap','capitalism'))),
 ('Building more weapons was the', sel('arms',('arms','arms race'),('space','space race'))),
 ('Racing to the Moon was the', sel('space',('space','Space Race'),('arms','arms race'))),
 ('The wall dividing a city was the', sel('berlin',('berlin','Berlin Wall'),('great','Great Wall'))),
 ('The Berlin Wall fell in', sel('89',('89','1989'),('45','1945'))),
 ('The USSR broke apart in', sel('91',('91','1991'),('76','1776'))),
 ('The Cold War lasted about', sel('4791',('4791','1947–1991'),('1600','the 1600s'))),
 ('The U.S. side was called the', sel('west',('west','West'),('east','East'))),
 ('Two superpowers means two very', sel('strong',('strong','strong countries'),('tiny','tiny towns'))),
 ('They competed for', sel('allies',('allies','allies & influence'),('nothing','nothing'))),
 ('The Cold War followed which war?', sel('ww2',('ww2','World War II'),('civil','the Civil War'))),
 ('A tense rivalry without direct battle is a', sel('cold',('cold','“cold” war'),('hot','“hot” war'))),
 ('Democracy means people help choose their', sel('leaders',('leaders','leaders'),('weather','weather'))),
 ('The Soviet Union is also called the', sel('ussr2',('ussr2','USSR'),('usa2','USA'))),
 ('The fall of the wall meant the war was', sel('ending',('ending','ending'),('starting','starting'))),
 ('The Space Race sent people toward the', sel('moon',('moon','Moon'),('sun','Sun'))),
 ('Capitalism and communism are two kinds of economic', sel('system',('system','system'),('animal','animal'))),
]
soc_body=assemble('social','head-social','Social Studies · Lesson 11',
   'The Cold War 🌍',
   'After World War II, two giant countries stared each other down for over forty years — without ever fighting directly. Today you learn what the Cold War was, and how the world competed instead of clashing.',
   ['The rivalry','Read','Which side','Select-all','Write'], soc_mid, soc_pool,
   "showLesson('home')",'Back to start →','Social Studies · Rapid Review')
h=add(h,'social',soc_body)

# home text (cosmetic; soft update if present)
for a,b in [('six subjects with <strong>ten lessons</strong> each','six subjects with <strong>eleven lessons</strong> each'),
            ('each with <strong>four lessons</strong>','each with <strong>eleven lessons</strong>')]:
    if a in h: h=h.replace(a,b,1)

open(OUT,"w",encoding="utf-8").write(h)
def get(s):
    a=h.find('id="%s-%d">'%(s,N)); e=h.find('</div><!-- /%s-%d -->'%(s,N)); return h[a:e]
print("Lesson %d step counts:"%N)
for s in ['art','math','english','science','anatomy','social']:
    print(" ", s, steps(get(s)))
print("wrote", OUT)
