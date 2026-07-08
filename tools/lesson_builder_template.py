# -*- coding: utf-8 -*-
"""
lesson_builder_template.py — reference builder for adding a lesson to ALL six
subjects. This is the Lesson 12 build, kept as the current working template.

TO ADD LESSON N (the file is already locked + has parent-checking + gates):
  1. Copy this file. Set N and PREV (= N-1). SRC/OUT already point at the
     deliverable, so add() appends the new lesson in place.
  2. Replace the six subject bodies with new topics. Keep the SAME structure so
     each lesson lands on TARGET (38) graded steps (assemble() asserts it). Do
     NOT add writebox() calls — writing is inserted as a mid-lesson gate later.
     Builders emit PLAINTEXT data-answer/answers/why; that is expected.
  3. Run:  python3 your_lesson_N.py
  4. Hash + shuffle the new answers:  python3 tools/postprocess.py <deliverable>
  5. Insert the writing gate for the new lessons:
        python3 tools/add_gate.py <deliverable>
     (add_gate skips any lesson-part that already has a gate.)
  6. Verify:  NODE_PATH=<jsdom> node tools/verify.js <deliverable>   (see README)
  7. Commit, push, deliver.

Keep math gentle. Keep other subjects normal, not dumbed down.
"""
import re
F = "/home/user/7th-into-8th-Refresher/8th-grade-refresher-ONE-FILE.html"
h = open(F, encoding="utf-8").read()
N = 12; PREV = 11; TARGET = 38

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
def panel(title,html): return '<section class="panel"><h2>%s</h2>%s</section>'%(title,html)
def plan(items): return '<ul class="plan-strip">%s</ul>'%"".join('<li><b>%d.</b> %s</li>'%(i+1,t) for i,t in enumerate(items))
def goals(items): return '<ul class="goal-list">%s</ul>'%"".join('<li>%s</li>'%t for t in items)
def howto():
    return panel('🧭 How this lesson works — read this first',
      goals(['Read each <strong>coloured box</strong> first — it teaches and shows you how.',
             'Drop-downs (▾): pick the <strong>one</strong> correct word.',
             '<strong>☑ Select-all boxes:</strong> tick <em>every</em> correct one, leave the wrong ones empty.',
             'Type-in boxes: work it out and type the answer.',
             '<strong>Writing checkpoint:</strong> partway through you must write 60 words to unlock the rest.'])
      +'<div class="callout"><span class="ico">📊</span><div>The bar at the top shows how much you have answered. A parent checks the answers.</div></div>')
def head(s,klass,kicker,title,intro):
    return ('<div class="lesson-part" id="%s-%d">\n    <header class="lesson-head %s"><div class="kicker">%s</div>'
            '<h1>%s</h1><p>%s</p></header>\n')%(s,N,klass,kicker,title,intro)
def review(title,pairs):
    out=""
    for ci in range(0,len(pairs),8):
        chunk=pairs[ci:ci+8]
        items="".join("%s %s. "%(c,s) for c,s in chunk)
        t=title if ci==0 else title+" (cont.)"
        out+=('<section class="panel"><h2>⚡ %s</h2><p>Quick-fire review — fill every blank.</p>'
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
    cur=steps(main); pad=TARGET-cur
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

# ===================== ART L12: Texture & Pattern =====================
art_studio=('<section class="panel"><h2>🖌️ Studio · Fill shapes with texture</h2>'
 '<p><strong>What to do:</strong> Draw 3 or 4 simple shapes and fill each with a DIFFERENT texture. <strong>How:</strong> use tight parallel lines (hatching), crossed lines (cross-hatching) for darker/rougher, and lots of dots (stippling) — more marks = darker and rougher. Try a repeating <strong>pattern</strong> in one shape.</p>'
 '<div class="studio"><div class="tools"><div class="swatches">'
 +"".join('<span class="swatch" data-color="%s" title="c"></span>'%c for c in ['#1f1300','#5b3a29','#2d6cdf','#1fae8b','#f0883e','#e5484d','#8b5cf6','#ffffff'])
 +'</div><div class="wheel-wrap"><div class="color-wheel" title="Tap to blend a colour"></div><div class="wheel-side"><span class="color-current"></span><input type="range" class="shade-slider" min="8" max="92" value="50" /></div></div>'
 '<div class="brush-size"><label for="brushSize13">Brush</label><input type="range" id="brushSize13" min="2" max="60" value="8" /><span data-brushval>8px</span></div></div>'
 '<div class="canvas-wrap"><canvas id="artCanvas13" aria-label="Texture studio"></canvas></div>'
 '<div class="btn-row"><button class="btn" data-save>💾 Save</button><button class="btn ghost" data-clear>🧽 Clear</button></div></div></section>')
art_mid=(panel('🖐️ Texture &amp; pattern',
   '<p><strong>Texture</strong> is how a surface looks or feels — rough, smooth, furry, bumpy. Artists can’t always make you FEEL it, so they make you SEE it with marks.</p>'
   '<table class="tidy"><tr><th>Word</th><th>What it is</th></tr>'
   '<tr><td><strong>Visual texture</strong></td><td>Texture you can SEE but not feel (a drawing of bricks)</td></tr>'
   '<tr><td><strong>Actual texture</strong></td><td>Texture you can really FEEL (real sandpaper, thick paint)</td></tr>'
   '<tr><td><strong>Hatching</strong></td><td>Parallel lines that shade and give texture</td></tr>'
   '<tr><td><strong>Cross-hatching</strong></td><td>Crossed lines — darker and rougher</td></tr>'
   '<tr><td><strong>Stippling</strong></td><td>Dots — more dots = darker/rougher</td></tr>'
   '<tr><td><strong>Pattern</strong></td><td>A design that repeats</td></tr></table>'
   +example('To make an area look rough and dark, add MORE marks — pile up cross-hatching or lots of dots. For a light, smooth look, use just a few soft lines.'))
 + tagblock('🟢 Name the technique','Fill the blanks.',
   'Shading with tight parallel lines is ' + sel('hatch',('hatch','hatching'),('stip','stippling'),('pat','pattern'))
   + '. Making texture with lots of dots is ' + sel('stip',('stip','stippling'),('hatch','hatching'),('cross','cross-hatching'))
   + '. Crossed lines for a darker, rougher look are ' + sel('cross',('cross','cross-hatching'),('stip','stippling'),('hatch','hatching'))
   + '. A design that repeats is a ' + sel('pat',('pat','pattern'),('hatch','hatch'),('blur','blur')) + '.')
 + tagblock('🔵 See or feel?','Pick the right idea.',
   'A pencil drawing of fur has ' + sel('vis',('vis','visual texture'),('act','actual texture'))
   + '. Real, bumpy sandpaper has ' + sel('act',('act','actual texture'),('vis','visual texture'))
   + '. Adding MORE dots or lines makes an area look ' + sel('dark',('dark','darker and rougher'),('light','lighter and smoother'))
   + '. A few soft, spaced lines look ' + sel('smooth',('smooth','smooth and light'),('rough','rough and dark')) + '.')
 + mquiz('a12',[
   ('Which are ways to CREATE texture with a pencil?',[('hatch','Hatching (parallel lines)',1),('cross','Cross-hatching',1),('stip','Stippling (dots)',1),('erase','Erasing the whole page',0)],'Hatching, cross-hatching and stippling build texture; erasing removes it.'),
   ('Which are examples of VISUAL texture (see, not feel)?',[('brick','A drawing of bricks',1),('furpic','A photo of fur',1),('bark','A painting of rough bark',1),('sand','Real sandpaper you can touch',0)],'Visual texture is seen only; real sandpaper is actual texture.'),
   ('Which make an area look DARKER and rougher?',[('more','More cross-hatch lines',1),('dots','More dots',1),('press','Pressing a bit harder',1),('fewer','Using fewer marks',0)],'More/heavier marks = darker and rougher; fewer marks = lighter.')])
 + mquiz('a12b',[
   ('Which are TRUE about a PATTERN?',[('rep','It repeats',1),('parts','It can use shapes, lines or colours',1),('nature','It is found in nature and in art',1),('never','It never repeats',0)],'A pattern is a repeating design; “never repeats” is the opposite.'),
   ('Which marks show texture?',[('dot','Dots (stippling)',1),('crossed','Crossed lines',1),('short','Short strokes',1),('blank','A blank, empty space',0)],'Marks make texture; a blank space shows none.')])
 + art_studio
 + quiz('a12',[
   ('Texture is how a surface looks or…',[('feel','Feels',1),('sounds','Sounds',0),('smells','Smells',0)],'Texture = how it looks or feels.'),
   ('Texture you can SEE but not feel is…',[('vis','Visual texture',1),('act','Actual texture',0),('none','No texture',0)],'Seen-only = visual texture.'),
   ('Texture you can really FEEL is…',[('act','Actual texture',1),('vis','Visual texture',0),('flat','Flat colour',0)],'Felt = actual texture.'),
   ('Crossed lines that build dark texture are…',[('cross','Cross-hatching',1),('stip','Stippling',0),('pat','Pattern',0)],'Crossed lines = cross-hatching.'),
   ('Making texture with dots is…',[('stip','Stippling',1),('hatch','Hatching',0),('blend','Blending',0)],'Dots = stippling.'),
   ('A design that repeats is a…',[('pat','Pattern',1),('shade','Shade',0),('hue','Hue',0)],'Repeating design = pattern.'),
   ('More dots or lines make an area look…',[('dark','Darker',1),('light','Lighter',0),('gone','Invisible',0)],'More marks = darker.'),
   ('Parallel lines used to shade are…',[('hatch','Hatching',1),('cross','Cross-hatching',0),('stip','Stippling',0)],'Parallel lines = hatching.')])
 )
art_pool=[
 ('Shading with parallel lines is', sel('hatch',('hatch','hatching'),('stip','stippling'))),
 ('Making texture with dots is', sel('stip',('stip','stippling'),('hatch','hatching'))),
 ('Crossed lines for rough dark texture are', sel('cross',('cross','cross-hatching'),('pat','pattern'))),
 ('A repeating design is a', sel('pat',('pat','pattern'),('blur','blur'))),
 ('Texture you can see but not feel is', sel('vis',('vis','visual'),('act','actual'))),
 ('Texture you can really feel is', sel('act',('act','actual'),('vis','visual'))),
 ('More marks make an area look', sel('dark',('dark','darker'),('light','lighter'))),
 ('Fewer, softer marks look', sel('smooth',('smooth','smooth'),('rough','rough'))),
 ('Texture is how a surface looks or', sel('feel',('feel','feels'),('sings','sings'))),
 ('A drawing of bricks shows ___ texture', sel('vis2',('vis2','visual'),('act2','actual'))),
 ('Real sandpaper has ___ texture', sel('act2',('act2','actual'),('vis2','visual'))),
 ('Patterns can be made of shapes, lines or', sel('colour',('colour','colours'),('sounds','sounds'))),
 ('Piling up cross-hatching makes it', sel('darker',('darker','darker'),('lighter','lighter'))),
 ('Stippling uses lots of', sel('dots',('dots','dots'),('circles','big circles'))),
 ('Patterns appear in art and in', sel('nature',('nature','nature'),('nowhere','nowhere'))),
 ('Rough bark in a painting is ___ texture', sel('vis3',('vis3','visual'),('act3','actual'))),
 ('Short repeated strokes can suggest', sel('tex',('tex','texture'),('silence','silence'))),
 ('To show something smooth, use ___ marks', sel('few',('few','few, soft'),('many','many heavy'))),
]
art_body=assemble('art','head-art','Art · Lesson 12 · ★ Your favorite',
   'Texture &amp; Pattern: Making a Surface You Can Almost Feel 🎨',
   'A flat pencil can make paper look furry, rough, or bumpy. Today you learn hatching, cross-hatching, stippling and pattern — and fill your own shapes with texture.',
   ['Texture words','Name it','See/feel','Studio'], art_mid, art_pool,
   "showLesson('math')",'Next: Math →','Art · Rapid Review')
h=add(h,'art',art_body)

# ===================== MATH L12: Area & Perimeter =====================
math_mid=(panel('📐 Area &amp; perimeter',
   '<p>Two easy ideas about shapes:</p>'
   '<div class="callout"><span class="ico">🎯</span><div><strong>Perimeter</strong> = the distance ALL THE WAY AROUND (add up every side). &nbsp; <strong>Area</strong> = the space INSIDE (for a rectangle: length × width), measured in <strong>square units</strong>.</div></div>'
   +example('A rectangle 5 across and 3 up: <strong>perimeter</strong> = 5 + 3 + 5 + 3 = <strong>16</strong>. <strong>Area</strong> = 5 × 3 = <strong>15</strong> square units. Tip: a square has 4 equal sides, so perimeter = side × 4.'))
 + pset('🟦 Perimeter — add up all the sides','Type the number.',[
   prob(1,'Rectangle 4 by 2: 4 + 2 + 4 + 2 =','12'),
   prob(2,'Square with side 5 (5 × 4) =','20'),
   prob(3,'Rectangle 6 by 3: perimeter =','18'),
   prob(4,'Rectangle 10 by 5: perimeter =','30')])
 + pset('🟨 Area — length × width','Type the number (square units).',[
   prob(1,'Rectangle 4 by 2: area =','8'),
   prob(2,'Rectangle 5 by 3: area =','15'),
   prob(3,'Square side 5: area =','25'),
   prob(4,'Rectangle 6 by 3: area =','18'),
   prob(5,'Rectangle 10 by 2: area =','20'),
   prob(6,'Square side 4: area =','16')])
 + tagblock('🟢 Which is which?','Pick the word.',
   'The distance around a shape is its ' + sel('per',('per','perimeter'),('area','area'),('angle','angle'))
   + '. The space inside a shape is its ' + sel('area',('area','area'),('per','perimeter'),('side','side'))
   + '. Area is measured in ' + sel('sq',('sq','square units'),('deg','degrees'),('sides','sides'))
   + '. To find a rectangle’s area you ' + sel('mult',('mult','multiply length × width'),('add','add the two sides')) + '.')
 + mquiz('m12',[
   ('Which statements are TRUE?',[('padd','Perimeter = add up all sides',1),('amul','Area = length × width',1),('asq','Area uses square units',1),('pmul','Perimeter = length × width',0)],'Perimeter adds the sides; area multiplies length × width.'),
   ('Which give the AREA of a 3 by 4 rectangle?',[('mul','3 × 4',1),('twelve','12 square units',1),('add','3 + 4',0)],'Area = 3 × 4 = 12 square units; 3 + 4 is not the area.')])
 + quiz('m12',[
   ('The distance all the way around a shape is the…',[('per','Perimeter',1),('area','Area',0),('angle','Angle',0)],'Around = perimeter.'),
   ('The amount of space inside a shape is the…',[('area','Area',1),('per','Perimeter',0),('side','Side',0)],'Inside = area.'),
   ('To find the perimeter you…',[('add','Add up all the sides',1),('mult','Multiply the sides',0),('sub','Subtract the sides',0)],'Perimeter = add the sides.'),
   ('To find a rectangle’s area you…',[('mult','Multiply length by width',1),('add','Add length and width',0),('half','Halve one side',0)],'Area = length × width.'),
   ('Area is measured in…',[('sq','Square units',1),('deg','Degrees',0),('litres','Litres',0)],'Area uses square units.'),
   ('A square with sides of 5 has an area of…',[('25','25',1),('20','20',0),('10','10',0)],'5 × 5 = 25.')])
 )
math_pool=[
 ('The distance around a shape is the', sel('per',('per','perimeter'),('area','area'))),
 ('The space inside a shape is the', sel('area',('area','area'),('per','perimeter'))),
 ('Perimeter means you ___ the sides', sel('add',('add','add up'),('mult','multiply'))),
 ('Rectangle area = length ×', sel('width',('width','width'),('two','two'))),
 ('Area is measured in ___ units', sel('sq',('sq','square'),('round','round'))),
 ('A square has ___ equal sides', sel('4',('4','4'),('3','3'))),
 ('Perimeter of a square = side ×', sel('4b',('4b','4'),('2b','2'))),
 ('Area of a 2 by 3 rectangle is', sel('6a',('6a','6'),('5a','5'))),
 ('Perimeter of a 2 by 3 rectangle is', sel('10a',('10a','10'),('6a','6'))),
 ('Area of a square side 3 is', sel('9a',('9a','9'),('6b','6'))),
 ('Area of a 4 by 5 rectangle is', sel('20a',('20a','20'),('9b','9'))),
 ('Distance around is perimeter; inside is', sel('area2',('area2','area'),('side2','side'))),
 ('You measure a fence by finding the', sel('per2',('per2','perimeter'),('area2','area'))),
 ('You measure carpet for a floor by finding the', sel('area3',('area3','area'),('per3','perimeter'))),
 ('Length × width gives the', sel('area4',('area4','area'),('per4','perimeter'))),
 ('Adding all four sides gives the', sel('per5',('per5','perimeter'),('area5','area'))),
]
math_body=assemble('math','head-math','Math · Lesson 12',
   'Area &amp; Perimeter: Around It and Inside It 📐',
   'Two tidy ideas: the distance around a shape (perimeter) and the space inside it (area). We stick to whole numbers and simple rectangles — calculator welcome.',
   ['The two ideas','Perimeter','Area','Which is which'], math_mid, math_pool,
   "showLesson('english')",'Next: English →','Math · Rapid Review')
h=add(h,'math',math_body)

# ===================== ENGLISH L12: Main Idea & Inference =====================
eng_pass=('<div class="callout" style="display:block"><p style="margin:.2rem 0"><strong>Read this:</strong></p>'
 '<p style="margin:.5rem 0">Diego forgot his umbrella, and by the time he reached the bus stop his jacket was soaked through. '
 'Puddles covered the sidewalk, and passing cars threw up sheets of water. He shivered and wished he had checked the sky before leaving home.</p></div>')
eng_mid=(panel('🔎 Main idea &amp; reading between the lines',
   '<table class="tidy"><tr><th>Word</th><th>What it means</th></tr>'
   '<tr><td><strong>Main idea</strong></td><td>What the text is MOSTLY about</td></tr>'
   '<tr><td><strong>Supporting detail</strong></td><td>A fact or example that backs up the main idea</td></tr>'
   '<tr><td><strong>Inference</strong></td><td>A smart conclusion from clues + what you already know (“reading between the lines”)</td></tr>'
   '<tr><td><strong>Summary</strong></td><td>The main idea and key details said in a few words</td></tr>'
   '<tr><td><strong>Context clue</strong></td><td>A hint about a tricky word from the words around it</td></tr></table>'
   +example('The passage never says “it is raining,” but soaked jacket + puddles + sheets of water are clues. Using them you can INFER that it’s raining. The MAIN IDEA: Diego got caught in the rain without an umbrella.'))
 + eng_pass
 + tagblock('🟢 From the passage','Answer using the text above.',
   'The main idea is that Diego got caught in the ' + sel('rain',('rain','rain'),('snow','snow'),('sun','sun'))
   + '. “Puddles covered the sidewalk” is a ' + sel('detail',('detail','supporting detail'),('idea','main idea'),('title','title'))
   + '. Deciding it is raining (though it is never stated) is an ' + sel('inf',('inf','inference'),('fact','stated fact'),('opinion','opinion'))
   + '. Saying the whole thing in one short sentence is a ' + sel('sum',('sum','summary'),('detail','detail'),('quote','quote')) + '.')
 + tagblock('🔵 Reading skills','Fill the blanks.',
   'What a text is MOSTLY about is the ' + sel('main',('main','main idea'),('detail','one detail'))
   + '. A conclusion from clues plus what you know is an ' + sel('inf',('inf','inference'),('title','title'))
   + '. A hint about a hard word from nearby words is a ' + sel('ctx',('ctx','context clue'),('rhyme','rhyme'))
   + '. Retelling the key points briefly is a ' + sel('sum',('sum','summary'),('essay','long essay')) + '.')
 + mquiz('e12',[
   ('Which are good clues that it is RAINING in the passage?',[('soak','His jacket was soaked',1),('pud','Puddles on the sidewalk',1),('water','Cars threw up sheets of water',1),('bus','He went to a bus stop',0)],'Soaked, puddles and sheets of water point to rain; a bus stop alone does not.'),
   ('Which are SUPPORTING DETAILS (not the main idea)?',[('pud','Puddles covered the sidewalk',1),('shiver','He shivered',1),('umb','He forgot his umbrella',1),('caught','Diego got caught in the rain',0)],'The details back up the main idea; “got caught in the rain” IS the main idea.'),
   ('Which describe an INFERENCE?',[('clue','It uses clues in the text',1),('know','It uses what you already know',1),('between','It is “reading between the lines”',1),('stated','It is copied word-for-word',0)],'An inference is a smart guess from clues, not a copied line.')])
 + mquiz('e12b',[
   ('Which would belong in a good SUMMARY of the passage?',[('rain','Diego was caught in the rain',1),('umb','He had no umbrella',1),('wish','He wished he had checked the sky',1),('name','A list of every word he said',0)],'A summary keeps the key points briefly, not every detail.'),
   ('Which are TRUE about the MAIN IDEA?',[('most','It is what the text is mostly about',1),('one','A text usually has one main idea',1),('details','Details support it',1),('tiny','It is the smallest detail',0)],'The main idea is the big point details support — not a tiny detail.')])
 + quiz('e12',[
   ('What a text is mostly about is the…',[('main','Main idea',1),('detail','One detail',0),('title','Author',0)],'Mostly about = main idea.'),
   ('A fact or example that backs up the main idea is a…',[('detail','Supporting detail',1),('idea','Main idea',0),('sum','Summary',0)],'It is a supporting detail.'),
   ('A conclusion from clues plus what you know is an…',[('inf','Inference',1),('fact','Stated fact',0),('rhyme','Rhyme',0)],'That is an inference.'),
   ('Saying the key points in a few words is a…',[('sum','Summary',1),('quote','Quote',0),('list','Full copy',0)],'That is a summary.'),
   ('A hint about a hard word from nearby words is a…',[('ctx','Context clue',1),('inf','Inference',0),('title','Title',0)],'That is a context clue.'),
   ('“Reading between the lines” means you…',[('inf','Infer from clues',1),('copy','Copy the text',0),('skip','Skip the text',0)],'It means to infer.')])
 )
eng_pool=[
 ('What a text is mostly about is the', sel('main',('main','main idea'),('detail','a detail'))),
 ('A fact that backs up the main idea is a', sel('detail',('detail','supporting detail'),('idea','main idea'))),
 ('A conclusion from clues is an', sel('inf',('inf','inference'),('fact','stated fact'))),
 ('The key points in a few words is a', sel('sum',('sum','summary'),('quote','quote'))),
 ('A hint about a hard word nearby is a', sel('ctx',('ctx','context clue'),('rhyme','rhyme'))),
 ('“Reading between the lines” means to', sel('infer',('infer','infer'),('copy','copy'))),
 ('Soaked jacket + puddles is a clue it is', sel('rain',('rain','raining'),('sunny','sunny'))),
 ('Most texts have ___ main idea', sel('one',('one','one'),('no','no'))),
 ('Details ___ the main idea', sel('support',('support','support'),('hide','hide'))),
 ('An inference uses clues plus what you', sel('know',('know','already know'),('forget','forget'))),
 ('A short retelling of key points is a', sel('sum2',('sum2','summary'),('essay','long essay'))),
 ('The biggest point of a paragraph is the', sel('main2',('main2','main idea'),('title2','last word'))),
 ('Context clues help you figure out a', sel('word',('word','hard word'),('colour','colour'))),
 ('A summary is ___ than the whole text', sel('short',('short','shorter'),('long','longer'))),
 ('“It is raining” from clues is an', sel('inf2',('inf2','inference'),('quote2','quote'))),
 ('A stated fact is written', sel('directly',('directly','directly'),('nowhere','nowhere'))),
 ('Good readers use clues to', sel('infer2',('infer2','infer'),('ignore','ignore'))),
 ('The main idea plus key details makes a good', sel('sum3',('sum3','summary'),('rhyme3','rhyme'))),
 ('Puddles and sheets of water are', sel('clues',('clues','clues'),('titles','titles'))),
 ('Details that back the main idea are', sel('support2',('support2','supporting'),('random','unrelated'))),
]
eng_body=assemble('english','head-english','English · Lesson 12',
   'Main Idea &amp; Inference: Reading Between the Lines 📖',
   'Good readers do two things: spot what a text is mostly about, and pick up on clues the writer doesn’t say out loud. Today you practise both.',
   ['Reading tools','Read','From the text','Skills'], eng_mid, eng_pool,
   "showLesson('science')",'Next: Science →','English · Rapid Review')
h=add(h,'english',eng_body)

# ===================== SCIENCE L12: The Water Cycle =====================
sci_mid=(panel('💧 The water cycle',
   '<p>Earth’s water is used over and over in a loop powered by the <strong>Sun</strong>. The same water can be in a cloud today and in your glass next week.</p>'
   '<table class="tidy"><tr><th>Step</th><th>What happens</th></tr>'
   '<tr><td><strong>Evaporation</strong></td><td>The Sun heats water so it turns into invisible water vapour (gas) and rises</td></tr>'
   '<tr><td><strong>Condensation</strong></td><td>Vapour cools high up and turns back into tiny droplets, forming clouds</td></tr>'
   '<tr><td><strong>Precipitation</strong></td><td>Droplets join, get heavy and fall as rain, snow, sleet or hail</td></tr>'
   '<tr><td><strong>Collection</strong></td><td>Water gathers in oceans, lakes and rivers — and the loop starts again</td></tr></table>'
   +example('Order of the loop: EVAPORATION (up as vapour) → CONDENSATION (clouds form) → PRECIPITATION (rain falls) → COLLECTION (water gathers) → and back to evaporation. The Sun’s heat drives the whole thing.'))
 + tagblock('🟢 Name the step','Use the table.',
   'The Sun heating water into vapour is ' + sel('evap',('evap','evaporation'),('cond','condensation'),('prec','precipitation'))
   + '. Vapour cooling into cloud droplets is ' + sel('cond',('cond','condensation'),('evap','evaporation'),('coll','collection'))
   + '. Rain or snow falling is ' + sel('prec',('prec','precipitation'),('evap','evaporation'),('cond','condensation'))
   + '. Water gathering in oceans and lakes is ' + sel('coll',('coll','collection'),('prec','precipitation'),('evap','evaporation')) + '.')
 + tagblock('🔵 How it works','Fill the blanks.',
   'The energy that powers the water cycle comes from the ' + sel('sun',('sun','Sun'),('moon','Moon'),('wind','wind'))
   + '. Water as an invisible gas is called water ' + sel('vap',('vap','vapour'),('ice','ice'),('mud','mud'))
   + '. Clouds are made of tiny ' + sel('drop',('drop','water droplets'),('rocks','rocks'),('dust','sand'))
   + '. Snow, sleet and hail are all types of ' + sel('prec',('prec','precipitation'),('evap','evaporation'),('cond','condensation')) + '.')
 + mquiz('s12',[
   ('Which are STEPS of the water cycle?',[('evap','Evaporation',1),('cond','Condensation',1),('prec','Precipitation',1),('photo','Photosynthesis',0)],'Evaporation, condensation and precipitation are steps; photosynthesis is a plant process.'),
   ('Which are types of PRECIPITATION?',[('rain','Rain',1),('snow','Snow',1),('hail','Hail',1),('cloud','A cloud',0)],'Rain, snow and hail fall as precipitation; a cloud is condensation.')])
 + mquiz('s12b',[
   ('Which are TRUE about the water cycle?',[('sun','The Sun powers it',1),('loop','It repeats in a loop',1),('same','The same water is reused',1),('new','New water is made each time',0)],'The cycle reuses the same water in a Sun-driven loop; no new water is made.'),
   ('Which happen during EVAPORATION?',[('heat','The Sun heats the water',1),('gas','Water becomes vapour (gas)',1),('rise','The vapour rises',1),('fall','Rain falls to the ground',0)],'Evaporation is water rising as vapour; falling rain is precipitation.')])
 + quiz('s12',[
   ('The Sun heating water into vapour is…',[('evap','Evaporation',1),('cond','Condensation',0),('coll','Collection',0)],'Water → vapour = evaporation.'),
   ('Vapour cooling into cloud droplets is…',[('cond','Condensation',1),('evap','Evaporation',0),('prec','Precipitation',0)],'Vapour → droplets = condensation.'),
   ('Rain, snow or hail falling is…',[('prec','Precipitation',1),('evap','Evaporation',0),('coll','Collection',0)],'Falling water = precipitation.'),
   ('Water gathering in oceans and lakes is…',[('coll','Collection',1),('cond','Condensation',0),('evap','Evaporation',0)],'Gathering = collection.'),
   ('What powers the whole water cycle?',[('sun','The Sun',1),('moon','The Moon',0),('soil','The soil',0)],'The Sun drives it.'),
   ('Clouds are made of tiny…',[('drop','Water droplets',1),('rock','Rocks',0),('sand','Sand',0)],'Clouds = water droplets.')])
 )
sci_pool=[
 ('The Sun turning water to vapour is', sel('evap',('evap','evaporation'),('cond','condensation'))),
 ('Vapour cooling into droplets is', sel('cond',('cond','condensation'),('evap','evaporation'))),
 ('Rain or snow falling is', sel('prec',('prec','precipitation'),('coll','collection'))),
 ('Water gathering in oceans is', sel('coll',('coll','collection'),('prec','precipitation'))),
 ('The water cycle is powered by the', sel('sun',('sun','Sun'),('moon','Moon'))),
 ('Water as a gas is called water', sel('vap',('vap','vapour'),('ice','ice'))),
 ('Clouds are made of tiny water', sel('drop',('drop','droplets'),('rocks','rocks'))),
 ('Snow and hail are types of', sel('prec2',('prec2','precipitation'),('evap2','evaporation'))),
 ('The water cycle repeats in a', sel('loop',('loop','loop'),('line','straight line'))),
 ('The cycle reuses the ___ water', sel('same',('same','same'),('new','brand-new'))),
 ('Evaporation makes water', sel('rise',('rise','rise up'),('freeze','freeze'))),
 ('Condensation forms', sel('clouds',('clouds','clouds'),('rocks','rocks'))),
 ('After collection the cycle starts', sel('again',('again','again'),('stops','and stops'))),
 ('Heat is needed for', sel('evap3',('evap3','evaporation'),('coll3','collection'))),
 ('Water vapour is', sel('invis',('invis','invisible'),('solid','solid'))),
 ('Rivers carry collected water to the', sel('ocean',('ocean','ocean'),('sky','sky'))),
 ('The three main steps are evaporation, condensation and', sel('prec3',('prec3','precipitation'),('erosion','erosion'))),
 ('Cooling causes', sel('cond2',('cond2','condensation'),('evap4','evaporation'))),
 ('Heating causes', sel('evap5',('evap5','evaporation'),('cond3','condensation'))),
 ('The water cycle never truly', sel('ends',('ends','ends'),('starts','starts'))),
]
sci_body=assemble('science','head-science','Science · Lesson 12',
   'The Water Cycle: Earth’s Endless Loop 💧',
   'The water in your glass may once have been a cloud, a river, or the sea. Today you follow water on its endless Sun-powered journey around the planet.',
   ['The loop','Name the step','How it works','Select-all'], sci_mid, sci_pool,
   "showLesson('anatomy')",'Next: Anatomy →','Science · Rapid Review')
h=add(h,'science',sci_body)

# ===================== ANATOMY L12: The Skin =====================
ana_mid=(panel('🧑 Your skin — the body’s biggest organ',
   '<p>Your <strong>skin</strong> is your largest organ. It is your body’s waterproof coat — it keeps germs out, holds water in, and lets you feel the world.</p>'
   '<table class="tidy"><tr><th>Word</th><th>What it is / does</th></tr>'
   '<tr><td><strong>Epidermis</strong></td><td>The thin OUTER layer you can see and touch</td></tr>'
   '<tr><td><strong>Dermis</strong></td><td>The thicker INNER layer with nerves, sweat glands and hair roots</td></tr>'
   '<tr><td><strong>Protection</strong></td><td>Skin is a barrier that keeps out germs and dirt</td></tr>'
   '<tr><td><strong>Temperature control</strong></td><td>Sweating cools you down when you are hot</td></tr>'
   '<tr><td><strong>Sensation</strong></td><td>Nerves in the skin let you feel touch, heat and pain</td></tr></table>'
   +example('When you get hot, tiny glands in the DERMIS make SWEAT. As the sweat dries it cools your skin — that’s your body’s built-in air-conditioning. Nerves in the same layer let you feel a gentle touch or a hot stove.'))
 + tagblock('🟢 Match the part','Use the table.',
   'The thin outer layer of skin is the ' + sel('epi',('epi','epidermis'),('derm','dermis'),('bone','bone'))
   + '. The thicker inner layer with nerves and sweat glands is the ' + sel('derm',('derm','dermis'),('epi','epidermis'),('skull','skull'))
   + '. The largest organ of the body is the ' + sel('skin',('skin','skin'),('heart','heart'),('liver','liver'))
   + '. Feeling a soft touch happens through ' + sel('nerves',('nerves','nerves in the skin'),('bones','bones'),('hair','hair only')) + '.')
 + tagblock('🔵 What skin does','Fill the blanks.',
   'Keeping germs and dirt out is skin’s job of ' + sel('prot',('prot','protection'),('sens','sensation'),('growth','growth'))
   + '. Sweating to cool you down is ' + sel('temp',('temp','temperature control'),('prot','protection'),('sens','sensation'))
   + '. Letting you feel heat, touch and pain is ' + sel('sens',('sens','sensation'),('temp','temperature control'),('prot','protection'))
   + '. Sweat is made by glands in the ' + sel('derm',('derm','dermis'),('epi','epidermis'),('brain','brain')) + '.')
 + mquiz('an12',[
   ('Which are JOBS of your skin?',[('prot','Protecting against germs',1),('temp','Helping control temperature',1),('sens','Letting you feel touch',1),('think','Doing your maths homework',0)],'Skin protects, cools and senses; it does not do homework.'),
   ('Which are TRUE about skin?',[('big','It is the largest organ',1),('layers','It has layers (epidermis & dermis)',1),('water','It helps keep water in',1),('bone','It is made of bone',0)],'Skin is a layered organ, not bone.')])
 + mquiz('an12b',[
   ('Which happen when you get HOT?',[('sweat','Sweat glands make sweat',1),('cool','The drying sweat cools you',1),('skin','It happens through the skin',1),('shiver','You shiver to warm up',0)],'Sweating cools you when hot; shivering warms you when cold.'),
   ('Which are found in the DERMIS (inner layer)?',[('nerve','Nerves',1),('sweat','Sweat glands',1),('root','Hair roots',1),('nail','Fingernails',0)],'The dermis holds nerves, sweat glands and hair roots.')])
 + quiz('an12',[
   ('The body’s largest organ is the…',[('skin','Skin',1),('heart','Heart',0),('brain','Brain',0)],'Skin is the largest organ.'),
   ('The thin outer layer of skin is the…',[('epi','Epidermis',1),('derm','Dermis',0),('bone','Bone',0)],'Outer layer = epidermis.'),
   ('The thicker inner layer is the…',[('derm','Dermis',1),('epi','Epidermis',0),('skull','Skull',0)],'Inner layer = dermis.'),
   ('Sweating helps with…',[('temp','Cooling you down',1),('see','Seeing',0),('hear','Hearing',0)],'Sweat cools you.'),
   ('You feel touch and pain through skin…',[('nerve','Nerves',1),('bones','Bones',0),('hair','Hair only',0)],'Skin nerves sense touch.'),
   ('One big job of skin is to…',[('prot','Keep germs out (protection)',1),('pump','Pump blood',0),('think','Think',0)],'Skin protects the body.')])
 )
ana_pool=[
 ('The largest organ is the', sel('skin',('skin','skin'),('heart','heart'))),
 ('The outer layer of skin is the', sel('epi',('epi','epidermis'),('derm','dermis'))),
 ('The inner layer of skin is the', sel('derm',('derm','dermis'),('epi','epidermis'))),
 ('Sweat glands sit in the', sel('derm2',('derm2','dermis'),('epi2','epidermis'))),
 ('Skin keeps germs out — that is', sel('prot',('prot','protection'),('sens','sensation'))),
 ('Sweating to cool down is', sel('temp',('temp','temperature control'),('prot','protection'))),
 ('Feeling touch and pain is', sel('sens',('sens','sensation'),('temp','temperature control'))),
 ('Nerves in the skin let you', sel('feel',('feel','feel things'),('see','see'))),
 ('Skin helps keep water', sel('in',('in','inside the body'),('out','out of the body'))),
 ('When hot, your body makes', sel('sweat',('sweat','sweat'),('bone','bone'))),
 ('When cold, you may', sel('shiver',('shiver','shiver'),('sweat','sweat'))),
 ('Skin is your waterproof', sel('coat',('coat','coat/barrier'),('bone','bone'))),
 ('Hair roots are found in the', sel('derm3',('derm3','dermis'),('nail','nail'))),
 ('The skin, hair and nails are the ___ system', sel('integ',('integ','integumentary'),('skel','skeletal'))),
 ('The part you can see and touch is the', sel('epi3',('epi3','epidermis'),('derm4','dermis'))),
 ('Sweat cools you as it', sel('dries',('dries','dries'),('freezes','freezes'))),
 ('Skin is a barrier against', sel('germs',('germs','germs and dirt'),('nothing','nothing'))),
 ('Touch, heat and pain are', sel('senses',('senses','sensations'),('bones','bones'))),
 ('The dermis is ___ than the epidermis', sel('thick',('thick','thicker'),('thin','thinner'))),
 ('Your skin works every day without you', sel('trying',('trying','even trying'),('breathing','breathing'))),
]
ana_body=assemble('anatomy','head-anatomy','Anatomy · Lesson 12',
   'The Skin: Your Body’s Largest Organ 🧑',
   'It is waterproof, it keeps germs out, it cools you down, and it lets you feel a feather or a flame. Today you meet your skin — the biggest organ you have.',
   ['Your skin','Match the part','What it does','Select-all'], ana_mid, ana_pool,
   "showLesson('social')",'Next: Social Studies →','Anatomy · Rapid Review')
h=add(h,'anatomy',ana_body)

# ===================== SOCIAL L12: Three Branches of Government =====================
soc_pass=('<div class="callout" style="display:block"><p style="margin:.2rem 0"><strong>Read this:</strong></p>'
 '<p style="margin:.5rem 0">The U.S. government is split into <strong>three branches</strong> so that no one part becomes too powerful. '
 'The <strong>Legislative</strong> branch (Congress) <strong>makes</strong> the laws. The <strong>Executive</strong> branch (the President) '
 '<strong>carries out</strong> and enforces the laws. The <strong>Judicial</strong> branch (the courts, led by the Supreme Court) '
 '<strong>interprets</strong> the laws and decides whether they follow the <strong>Constitution</strong>. Each branch can limit the others — '
 'a system called <strong>checks and balances</strong>.</p></div>')
soc_mid=(panel('🏛️ Three branches of government',
   '<table class="tidy"><tr><th>Branch</th><th>Who &amp; what it does</th></tr>'
   '<tr><td><strong>Legislative</strong></td><td>Congress — <strong>makes</strong> the laws</td></tr>'
   '<tr><td><strong>Executive</strong></td><td>The President — <strong>carries out / enforces</strong> the laws</td></tr>'
   '<tr><td><strong>Judicial</strong></td><td>The courts (Supreme Court) — <strong>interprets</strong> the laws</td></tr>'
   '<tr><td><strong>Checks and balances</strong></td><td>Each branch can limit the others so none gets too powerful</td></tr>'
   '<tr><td><strong>Constitution</strong></td><td>The highest law — the rulebook the whole government follows</td></tr></table>'
   +example('An easy way to remember: Legislative = Laws (makes them), Executive = Enforces them, Judicial = Judges them. Splitting power three ways, with checks and balances, stops any one branch from taking over.'))
 + soc_pass
 + tagblock('🟢 Which branch?','Answer from the passage.',
   'The branch that MAKES laws is the ' + sel('leg',('leg','Legislative'),('exe','Executive'),('jud','Judicial'))
   + '. The branch that CARRIES OUT laws is the ' + sel('exe',('exe','Executive'),('leg','Legislative'),('jud','Judicial'))
   + '. The branch that INTERPRETS laws is the ' + sel('jud',('jud','Judicial'),('leg','Legislative'),('exe','Executive'))
   + '. The highest law of the land is the ' + sel('con',('con','Constitution'),('king','king'),('mayor','mayor')) + '.')
 + tagblock('🔵 Who does it','Match the leader/body.',
   'Congress is part of the ' + sel('leg',('leg','Legislative branch'),('exe','Executive branch'))
   + '. The President leads the ' + sel('exe',('exe','Executive branch'),('jud','Judicial branch'))
   + '. The Supreme Court is part of the ' + sel('jud',('jud','Judicial branch'),('leg','Legislative branch'))
   + '. Keeping any branch from getting too powerful is called ' + sel('cb',('cb','checks and balances'),('vote','a monarchy')) + '.')
 + mquiz('so12',[
   ('Which are the three BRANCHES of government?',[('leg','Legislative',1),('exe','Executive',1),('jud','Judicial',1),('mil','Military',0)],'The three branches are Legislative, Executive and Judicial.'),
   ('Which match the LEGISLATIVE branch?',[('cong','Congress',1),('make','Makes the laws',1),('law','Legislative = laws',1),('pres','The President',0)],'Congress makes the laws; the President is the Executive.')])
 + mquiz('so12b',[
   ('Which are TRUE about the government?',[('three','It has three branches',1),('cb','Checks and balances limit each branch',1),('con','The Constitution is the highest law',1),('one','One branch controls everything',0)],'Power is split three ways with checks and balances — not held by one branch.'),
   ('Which does the JUDICIAL branch do?',[('interp','Interprets the laws',1),('court','Includes the Supreme Court',1),('const','Decides if laws follow the Constitution',1),('makes','Writes brand-new laws',0)],'Courts interpret laws; Congress writes them.')])
 + quiz('so12',[
   ('The branch that MAKES laws is the…',[('leg','Legislative',1),('exe','Executive',0),('jud','Judicial',0)],'Legislative makes laws.'),
   ('The branch that CARRIES OUT laws is the…',[('exe','Executive',1),('leg','Legislative',0),('jud','Judicial',0)],'Executive enforces laws.'),
   ('The branch that INTERPRETS laws is the…',[('jud','Judicial',1),('leg','Legislative',0),('exe','Executive',0)],'Judicial interprets laws.'),
   ('Congress belongs to the…',[('leg','Legislative branch',1),('exe','Executive branch',0),('jud','Judicial branch',0)],'Congress = Legislative.'),
   ('The President leads the…',[('exe','Executive branch',1),('leg','Legislative branch',0),('jud','Judicial branch',0)],'President = Executive.'),
   ('The system that stops one branch getting too powerful is…',[('cb','Checks and balances',1),('mon','Monarchy',0),('none','Nothing',0)],'That is checks and balances.')])
 )
soc_pool=[
 ('The branch that makes laws is the', sel('leg',('leg','Legislative'),('exe','Executive'))),
 ('The branch that carries out laws is the', sel('exe',('exe','Executive'),('jud','Judicial'))),
 ('The branch that interprets laws is the', sel('jud',('jud','Judicial'),('leg','Legislative'))),
 ('The highest law of the land is the', sel('con',('con','Constitution'),('king','king'))),
 ('Congress is the ___ branch', sel('leg2',('leg2','Legislative'),('jud2','Judicial'))),
 ('The President leads the ___ branch', sel('exe2',('exe2','Executive'),('leg3','Legislative'))),
 ('The Supreme Court is the ___ branch', sel('jud3',('jud3','Judicial'),('exe3','Executive'))),
 ('Limiting each branch is called checks and', sel('bal',('bal','balances'),('coins','coins'))),
 ('There are ___ branches of government', sel('three',('three','three'),('five','five'))),
 ('Legislative = makes the', sel('laws',('laws','laws'),('money','money'))),
 ('Executive = ___ the laws', sel('enforce',('enforce','enforces'),('writes','writes'))),
 ('Judicial = ___ the laws', sel('interp',('interp','interprets'),('deletes','deletes'))),
 ('Splitting power stops one branch getting too', sel('powerful',('powerful','powerful'),('friendly','friendly'))),
 ('The Constitution is the government’s', sel('rules',('rules','rulebook'),('map','map'))),
 ('The three branches are Legislative, Executive and', sel('jud4',('jud4','Judicial'),('royal','Royal'))),
 ('Congress ___ laws', sel('makes',('makes','makes'),('judges','judges'))),
 ('Courts decide if laws follow the', sel('con2',('con2','Constitution'),('weather','weather'))),
 ('Checks and balances keep power', sel('shared',('shared','shared/limited'),('hidden','hidden'))),
 ('A president enforcing a law is the ___ branch', sel('exe4',('exe4','Executive'),('jud5','Judicial'))),
 ('The rulebook every branch follows is the', sel('con3',('con3','Constitution'),('menu','menu'))),
]
soc_body=assemble('social','head-social','Social Studies · Lesson 12',
   'The Three Branches of Government 🏛️',
   'Who makes the rules — and who stops anyone from grabbing all the power? Today you learn how the U.S. government splits its job into three branches that keep each other in check.',
   ['The branches','Read','Which branch','Select-all'], soc_mid, soc_pool,
   "showLesson('home')",'Back to start →','Social Studies · Rapid Review')
h=add(h,'social',soc_body)

# home text (cosmetic; soft)
for a,b in [('six subjects with <strong>eleven lessons</strong> each','six subjects with <strong>twelve lessons</strong> each'),
            ('<strong>eleven lessons</strong>','<strong>twelve lessons</strong>')]:
    if a in h: h=h.replace(a,b,1)

open(F,"w",encoding="utf-8").write(h)
def get(s):
    a=h.find('id="%s-%d">'%(s,N)); e=h.find('</div><!-- /%s-%d -->'%(s,N)); return h[a:e]
print("Lesson %d graded step counts:"%N)
for s in ['art','math','english','science','anatomy','social']:
    print(" ", s, steps(get(s)))
