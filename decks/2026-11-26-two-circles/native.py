#!/usr/bin/env python3
"""Native, editable PowerPoint of the Two Circles keynote, with Morph on every slide.
Same 50 beats and notes as slides.py (notes.json). Shapes that should morph share a "!!" name.
    python3 native.py  -> TwoCircles_editable.pptx
"""
import json, copy
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from lxml import etree

PX = 6350
def px(v): return Emu(int(v * PX))
W, P, A, PA, D, M, L = 'FFFFFF', 'E6007E', 'E4FF3D', 'F3ECEF', 'B9AAB1', '8B7C84', '3A2A33'
HEAD, BODY, MONO = 'Archivo Black', 'Archivo', 'JetBrains Mono'

prs = Presentation()
prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
BLANK = prs.slide_layouts[6]
NOTES = json.load(open('notes.json'))
cur = None

MORPH = ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
         '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
         '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
         'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" spd="slow" p14:dur="900">'
         '<p159:morph option="byObject"/></p:transition></mc:Choice><mc:Fallback>'
         '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow"><p:fade/></p:transition>'
         '</mc:Fallback></mc:AlternateContent>')


def new(qr=True, tape=False, pink=False):
    global cur
    s = prs.slides.add_slide(BLANK)
    if pink:
        bg = s.background.fill; bg.solid(); bg.fore_color.rgb = RGBColor.from_string('C8006D')
    else:
        pic = s.shapes.add_picture('bg.png', 0, 0, prs.slide_width, prs.slide_height); pic.name = '!!bg'
    if qr:
        q = s.shapes.add_picture('qr.png', px(1696), px(48), px(168), px(168)); q.name = '!!qr'
        t = text(1650, 222, 260, 40, 'TWO CIRCLES · SIGN UP', 14, MONO, PA, align='c', name='!!qrlab', s=s)
    if tape:
        t = s.shapes.add_picture('chev.png', 0, px(1080 - 34), prs.slide_width, px(34)); t.name = '!!tape'
    cur = s
    return s


def text(x, y, w, h, content, size, font=BODY, color=PA, name=None, align='l', s=None, anchor='t', spacing=None, bold=False):
    """content: str (\\n = new paragraph) or list of paragraphs, each a list of (text, color) runs."""
    s = s or cur
    tb = s.shapes.add_textbox(px(x), px(y), px(w), px(h))
    if name: tb.name = name
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    paras = content.split('\n') if isinstance(content, str) else content
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        if spacing: p.line_spacing = spacing
        runs = [(para, color)] if isinstance(para, str) else para
        for t, c in runs:
            r = p.add_run(); r.text = t
            f = r.font; f.size = Pt(size * 0.5); f.name = font; f.bold = bold
            f.color.rgb = RGBColor.from_string(c)
    return tb


def rule(x, y, w, color=P, h=3, name=None):
    sh = cur.shapes.add_shape(1, px(x), px(y), px(w), px(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor.from_string(color); sh.line.fill.background()
    if name: sh.name = name
    return sh


def lab(t, y=150, color=P): text(150, y, 1400, 40, t.upper(), 24, MONO, color, name='!!lab')
def src(t): text(150, 990, 1450, 60, t.upper(), 17, MONO, M, name='!!src')
def head(paras, size, y, w=1450, h=500, name='!!title', color=W):
    return text(150, y, w, h, paras, size, HEAD, color, name=name, spacing=0.92)
def body(t, y, w=1100, size=40, color=PA, name='!!body'):
    return text(150, y, w, 300, t, size, BODY, color, name=name, spacing=1.15)
def stat(t, x, y, size, w=1500, name='!!stat'):
    return text(x, y, w, size * 1.05, t, size, HEAD, A, name=name)
def H(*parts):
    """H('white *pink* white|next para') -> paragraphs of runs."""
    import re
    paras = []
    for para in ''.join(parts).split('|'):
        runs = []
        for i, seg in enumerate(re.split(r'\*', para)):
            if seg: runs.append((seg.upper(), P if i % 2 else W))
        paras.append(runs)
    return paras


def bigqr(x, y, size, img='qr.png', caption=None):
    q = cur.shapes.add_picture(img, px(x), px(y), px(size), px(size)); q.name = '!!bigqr'
    if caption: text(x - 100, y + size + 16, size + 200, 40, caption, 22, MONO, PA, align='c')


def cols(items, y=420, gap=70, statsize=150):
    n = len(items); w = (1620 - gap * (n - 1)) / n
    for i, (st, tx) in enumerate(items):
        x = 150 + i * (w + gap)
        rule(x, y, w, name=f'!!rule{i}')
        stat(st, x, y + 30, statsize, w=w, name=f'!!col{i}')
        text(x, y + 40 + statsize * (1.05 * st.count('\n') + 1.05), w, 220, tx, 36, BODY, PA, name=f'!!colt{i}', spacing=1.1)


def items(rows, y=330, size=40, sub=30, step=None, x=150, w=1400, cols_=1):
    step = step or (size + sub + 50)
    per = (len(rows) + cols_ - 1) // cols_
    for i, (b, sp) in enumerate(rows):
        cx = x + (i // per) * (w / cols_ + 40); cy = y + (i % per) * step
        rule(cx, cy, w / cols_ - 40, color=L, h=2)
        text(cx, cy + 16, w / cols_ - 40, step, [[(b.upper(), W)]] + ([[(sp, D)]] if sp else []), size if not sp else size,
             HEAD if sp is not None else BODY, W, name=f'!!item{i}')
        # sub-line smaller
        tb = cur.shapes[-1]
        if sp:
            r = tb.text_frame.paragraphs[1].runs[0]; r.font.name = BODY; r.font.size = Pt(sub * 0.5)


# ---------- league ----------
COLS = [('FEELS BRAVE', 'OUT OF 10'), ('WORKPLACE COURAGE', 'OUT OF 7'), ('CONTEST CULTURE', 'OUT OF 5 · LOWER BETTER'),
        ('ACTS FOR OTHERS', 'OUT OF 3'), ('REJECTS MAN BOX', 'OUT OF 5'), ('MEN', 'N')]
ROWS = [('Health, care & education', 5.8, 5.7, 2.4, 1.7, 4.6, 68), ('Retail & hospitality', 5.7, 5.6, 2.4, 1.4, 4.7, 30),
        ('Public & emergency services', 6.2, 5.5, 2.5, 1.5, 4.5, 24), ('Creative & media', 5.2, 5.4, 2.4, 1.6, 4.7, 73),
        ('Transport & logistics', 4.2, 5.6, 2.1, 1.8, 4.3, 11), ('Office & finance', 5.2, 5.3, 2.6, 1.6, 4.6, 91),
        ('Tech & engineering', 5.1, 5.4, 2.5, 1.6, 4.5, 81), ('Construction & trades', 5.0, 5.3, 2.6, 1.5, 4.5, 59)]
CX = [760, 960, 1170, 1370, 1570, 1700]  # right edges-ish start x for 6 columns (w 180)


def league(rows):
    """rows: list of (name, v1..v5, n, style) ; style '', 'hl', 'q'"""
    lab('The league table · starting positions · autumn 2026', y=120)
    head(H('Who’s brave enough?'), 88, 170, h=120)
    for i, (a, b) in enumerate(COLS):
        text(CX[i] - 40, 300, 200, 70, [[(a, D)], [(b, M)]], 17, MONO, D, align='r', name=f'!!lgh{i}')
    y0, step = 385, 66
    for i, r in enumerate(rows):
        nm, vals, n, style = r[0], r[1:6], r[6], r[7]
        y = y0 + i * step
        key = '!!row-' + ''.join(ch for ch in nm.lower() if ch.isalnum())[:20]
        c = A if style else W
        g = cur.shapes.add_group_shape(); g.name = key
        def gt(x, w, t, size, font, col, align='l'):
            tb = g.shapes.add_textbox(px(x), px(y), px(w), px(step))
            tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]; p.alignment = {'l': PP_ALIGN.LEFT, 'r': PP_ALIGN.RIGHT}[align]
            rr = p.add_run(); rr.text = t; rr.font.size = Pt(size * .5); rr.font.name = font
            rr.font.color.rgb = RGBColor.from_string(col)
        ln = g.shapes.add_shape(1, px(150), px(y), px(1620), px(2 if not style else 3))
        ln.fill.solid(); ln.fill.fore_color.rgb = RGBColor.from_string(A if style else L); ln.line.fill.background()
        gt(150, 60, '?' if style == 'q' else str(i + 1), 34, HEAD, A if style else P)
        gt(215, 560, nm.upper(), 28, HEAD, c)
        for j, v in enumerate(vals):
            gt(CX[j] - 40, 200, '?' if v is None else f'{v:.1f}', 36, BODY, c, 'r')
        gt(CX[5] - 40, 200, 'you?' if style == 'q' else (str(n) if n else 'all 704'), 20, MONO, A if style else M, 'r')
    src('Hard As Nails database, 26 Nov 2026 · 704 men with a baseline · average starting scores by the industry men say they work in · a signal, not a result')


def lr(rows, style=''): return [r + (style,) for r in rows]


# ---------- weird ----------
TL = [('2024', 'An Olympic champion.'), ('2025', 'An NBA player. A polish deal.'), ('JAN 2026', 'A club. Its president. Its fans.'),
      ('JUNE 2026', 'The cover of Madden.'), ('NEXT?', 'A sport. On purpose.')]
def weird(k):
    lab('What’s weird?', y=230)
    head(H('Making the|*weird normal.*'), 120, 290, h=260)
    w = (1620 - 4 * 34) / 5
    for i, (a, b) in enumerate(TL):
        x = 150 + i * (w + 34); on = i < k
        rule(x, 640, w, color=(A if i == 4 else P) if on else L, name=f'!!tlr{i}')
        text(x, 665, w, 50, a, 28, MONO, A if on else L, name=f'!!tla{i}')
        text(x, 715, w, 200, b, 42, BODY, W if on else L, name=f'!!tlb{i}', spacing=1.05)


# ================= SLIDES (same order as slides.py) =================
# 1
new(tape=True)
lg = cur.shapes.add_picture('tc-logo.png', px(150), px(60), height=px(110)); lg.name = '!!logo'
head(H('Hard as|*nails.*'), 190, 280, h=400)
body([[('Building workplace courage, adaptive mindsets, empathy and ', PA), ('performance', A), ('… through nail polish.', PA)]], 700, w=1000, size=42)
src('Sam Conniff + Daniele Fiandaca · Hard As Nails × Two Circles · Aviation House · 26 November 2026')
# 2
new(); head(H('There isn’t a challenge facing sport, society, business (or the world)'), 88, 200, w=1300, h=380)
text(150, 600, 1350, 360, [[('WHERE NEGATIVE STEREOTYPES OF MASCULINITY ', D), ('AREN’T A CONTRIBUTING FORCE.', P)]], 88, HEAD, D, name='!!title2', spacing=.92)
# 3
new(tape=True); head(H('Not men.|*The construct.*'), 190, 330, h=450)
# 4
new(); head(H('What if a technology could update the *performance model* of masculinity?'), 120, 250, w=1300, h=600)
# 5
new(); lab('Technology for healthy masculinity', y=230)
for i, (b, t) in enumerate([('UNDER 20P', ' token cost per user.'), ('NO', ' data centre.'), ('NO', ' hallucinations.'), ('TIME-HONOURED', ' over centuries.')]):
    rule(150, 310 + i * 100, 1300, color=L, h=2)
    text(150, 330 + i * 100, 1300, 80, [[(b, W), (t, PA)]], 44, BODY, W, name=f'!!item{i}', bold=False)
    cur.shapes[-1].text_frame.paragraphs[0].runs[0].font.name = HEAD
body('(It’s a bottle of nail varnish.)', 760, color=D)
# 6
new(); lab('The crisis', y=150)
cols([('13', 'men a day take their own lives.'), ('~600', 'women killed since Sarah Everard.'), ('+26%\n+38%', 'domestic abuse when England win, and when they lose.')], y=230, statsize=130)
body([[('In sport: ', W), ('not calling it out. Not admitting mistakes. Winning at all costs. Losing badly.', PA)]], 760, w=1400)
src('ONS · CALM · Femicide Census · Lancaster University, domestic abuse and England fixtures')
# 7
new(tape=True); head(H('Come and have a go if you’re *hard enough.*'), 120, 260, w=1200, h=600)
# 8
new(qr=False); lab('Sign up', y=250)
head(H('Academic-grade|*research.*'), 100, 310, w=1050, h=260)
body('Leeds Beckett University. Overseen by Professor Brendan Gough, adviser to the World Health Organization.', 560, w=900)
bigqr(1280, 250, 460, caption='HARD-AS-NAILS.COM/TWO-CIRCLES')
# 9
new(); lab('2026 · What are we measuring?', y=200)
items([('Empathy', 'Can he feel what someone else is feeling?'), ('The Man Box', 'How tightly do the old rules hold him?'),
       ('Mental health', 'Suppression. Anxiety. Asking for help.'), ('Bystander behaviour', 'Does he step in, or look away?'),
       ('Workplace courage', 'Speaking up. Owning a mistake. The dumb question.'), ('Contest culture', 'Does showing weakness cost you here?')],
      y=280, size=40, sub=30, step=150, w=1600, cols_=2)
# 10-12
for labt, st, under in [('The experiment · 2024', '20', H('Men. Mates, mostly.')),
                        ('The experiment · 2025', '429', H('409 more. A control group. Nine months.')),
                        ('The experiment · this afternoon', '1,453', H('Men signed up. *1,024 this year.*'))]:
    new(); lab(labt, y=180); stat(st, 150, 250, 420)
    head(under, 62, 760, h=200, name='!!under')
# 13-15 league
new(); league(lr([r for r in ROWS if r[0] == 'Construction & trades']))
new(); league(lr(ROWS))
new(); league(lr(ROWS) + [('Sport', None, None, None, None, None, None, 'q')])
# 16-19
new(); lab('How the hell did we get here', y=330); head(H('WTF?'), 190, 400, h=250)
new(); head(H('I got tickets for my *daughter’s birthday.*'), 120, 300, w=1200, h=600)
new(); head(H('“You batting for the *other side* now, Sam?”'), 120, 300, w=1250, h=600)
new(); head(H('So I did it.|*Then Daniele did it.*'), 120, 380, h=400)
# 20-22
new(); lab('2025 study · Leeds Beckett', y=200)
cols([('422', 'men signed up to have their nails painted.'), ('155', 'completed the baseline and got them done.'), ('9 MO', 'Pre, post, follow-up, nine months. 195 diaries. A 50-man control group.')], y=300)
new(); lab('2025 results · nine months · n = 51', y=200)
cols([('+10%', 'rejecting the Man Box (4.23 → 4.66).'), ('−22%', 'on the empathy deficit scale (1.78 → 1.38, lower is better).')], y=300)
body([[('Control group, 50 men: ', PA), ('no movement at any stage.', A)]], 760, w=1400)
new(); stat('83%', 150, 230, 420); head(H('began conversations they wouldn’t otherwise have had.'), 62, 700, w=1300, h=250, name='!!under')
# 23-24
new(); lab('Workplace allyship · 2025', y=140)
head(H('A man is touching a woman in a way that’s making her visibly uncomfortable. What do you do?'), 58, 200, w=1300, h=260)
cols([('17.3%', 'would intervene. Before.'), ('37.3%', 'would intervene. Six weeks later (n = 66).')], y=520)
new(); lab('The finding we didn’t expect', y=330); head(H('The most rigid men|*moved most.*'), 120, 400, h=300)
src('Empathy gain by baseline rigidity · top third vs bottom, d = 0.40, p = 0.034 · lowest-empathy subgroup d = 1.23 (n = 25)')
# 25-26
new(); lab('The gap · we asked Britain', y=160)
head(H('“I’m comfortable talking about the things that worry me.”'), 62, 220, w=1300, h=220)
cols([('49%', 'me.'), ('16%', 'most other men.')], y=480, statsize=170)
src('YouGov · GB men · n = 970 · August 2026')
new(); lab('The gap · our men, before a single nail', y=140)
head(H('“The strongest men can be honest about their feelings in front of others.”'), 58, 200, w=1300, h=220)
cols([('86%', 'me.'), ('28%', 'most other men.')], y=440, statsize=170)
body([[('Most men already agree. ', PA), ('They just think they’re alone.', P)]], 860, w=1400)
src('Hard As Nails 2026 baseline · n = 314 · early data')
# 27
new(); mb = cur.shapes.add_picture('man-box-s.jpg', 0, 0, prs.slide_width, prs.slide_height); mb.name = 'manbox'
# move QR on top
for sh in list(cur.shapes):
    if sh.name in ('!!qr', '!!qrlab'): cur.shapes._spTree.remove(sh._element); cur.shapes._spTree.append(sh._element)
# 28-29
new(); lab('Workplace courage · hands up', y=220)
head(H('If I thought a question was dumb, I would still ask it.'), 88, 280, w=1300, h=300)
body('1 strongly disagree · 4 neutral · 7 strongly agree', 620, color=D); body('You? Your team? The man next to you?', 700, name='!!body2')
new(); lab('Contest culture · in my work environment…', y=220)
head(H('Admitting you don’t know the answer *looks weak.*'), 88, 280, w=1300, h=300)
body('1 strongly disagree · 4 neutral · 7 strongly agree', 620, color=D); body('Your dressing room? Your boardroom?', 700, name='!!body2')
# 30-32
new(); lab('So why does it work?', y=330); head(H('The expectation gap.'), 120, 400, h=150)
body([[('He expects judgement. He gets a shrug. ', PA), ('The gap is where the change happens.', P)]], 580, w=1300)
new(); lab('195 research diaries', y=180); stat('68%', 150, 250, 380)
head(H('Braced for confrontation. *Found conversation.*'), 62, 700, w=1400, h=200, name='!!under')
new(); lab('How it works', y=200)
for i, (h1, st, t) in enumerate([('SURPRISE', '68%', 'surprised by how others reacted.'), ('INTROSPECTION', '35→62%', 'reflecting on themselves.'), ('REALISATION', '98%', 'took at least one new action, nine months on.')]):
    x = 150 + i * 560
    rule(x, 300, 500, name=f'!!rule{i}'); text(x, 330, 520, 80, h1, 50, HEAD, W, name=f'!!h{i}')
    stat(st, x, 430, 110, w=520, name=f'!!col{i}'); text(x, 580, 480, 200, t, 36, BODY, PA, name=f'!!colt{i}')
src('Conniff, Fiandaca & Gough · Leeds Beckett University · in peer review')
# 33
new(); head(H('Max went to the pub to watch the football.|*He didn’t watch the football.*'), 110, 200, w=1300, h=800)
# 34
new(); lab('Since Leaders in Sport · 12 November', y=140); head(H('What happened next.'), 88, 190, h=120)
items([('The Lionesses', 'The FA asked us into camp. A call is booked for after World Cup qualifying.'),
       ('British Cycling', 'Head of coaching wore purple nails for a week and put us forward to UK Sport.'),
       ('English cricket', 'The ECB has invited us to ECB Live, 28 January.'),
       ('Cricket Scotland', 'The men’s head coach took the chair. On stage.')], y=340, size=44, sub=32, step=155, w=1500)
# 35
new(tape=True)
text(150, 300, 1400, 400, '“I don’t believe you can ask anyone else to do something and you’re not prepared to.”', 72, BODY, W, name='!!quote', spacing=1.1, bold=True)
text(150, 720, 1400, 60, 'OWEN DAWKINS · HEAD COACH, CRICKET SCOTLAND MEN · LEADERS IN SPORT, 12 NOV 2026', 24, MONO, D, name='!!who')
# 36
new(); lab('How women get involved', y=220)
head(H('The Lionesses have rather *outperformed* the Lions.'), 104, 280, w=1400, h=500)
body('As usual, women lead, outperform, and get the men to rise to the challenge.', 830, w=1300)
# 37
new(); lab('Three ways in · hard-as-nails.com/women', y=220)
items([('Nominate him.', 'About eleven seconds for you, five minutes for him.'), ('Paint them.', 'Partners, daughters, mates. Get the kit out.'),
       ('Watch what changes.', 'You’ll see it before he says it.')], y=300, size=48, sub=34, step=170, w=1400)
# 38
new(); lab('The Nominator', y=200)
head(H('Nominate a man.|*He’ll thank you. Eventually.*'), 120, 260, w=1050, h=700)
bigqr(1360, 560, 320, img='qr-nom.png', caption='HARD-AS-NAILS.COM/TWO-CIRCLES-NOMINATE')
# 39
new(); lab('Respect', y=150)
head(H('We didn’t invent this. *We’re standing on it.*'), 110, 210, w=1350, h=360)
body('Queer communities. Black women, who built modern nail culture. Vietnamese nail technicians, who built the salon trade. Black men in public life. Trans and non-binary people.', 600, w=1400, size=38)
src('Credit you wait to be asked for isn’t really credit · hard-as-nails.com/respect')
# 40
new(); lab('Mission Control · who they’re doing it for', y=150)
for i, q in enumerate(['“My daughter, who frequently wants to paint my nails anyway!”', '“My two sons, who I hope I can teach to be emotionally intelligent men.”',
                       '“For my son, who I lost, because he didn’t feel able to be whatever he wants to be.”', '“Me, my younger self who spent so much emotional energy trying to fit in.”',
                       '“My four year old, who’ll grow up in a world where being yourself means everything.”']):
    rule(150, 230 + i * 140, 1500, color=L, h=2); text(150, 250 + i * 140, 1500, 120, q, 40, BODY, W, name=f'!!item{i}')
src('Hard As Nails database · 2026 cohort, real participants · approved dedications, no names')
# 41-45
for k in (0, 2, 3, 4, 5): new(); weird(k)
# 46
new(); lab('What’s normal?', y=150); head(H('And the normal *weird.*'), 88, 200, h=120)
cols([('58%', 'of women have experienced sexual harassment, bullying or verbal abuse at work.'), ('77%', 'of men have had mental health concerns.'), ('24%', 'of them ask for help.')], y=380)
src('TUC / Opinium, 1,010 working women, 2023 · men’s figures as used in the Wates keynote')
# 47
new(); lab('The road to 500,000', y=200); stat('500,000', 150, 270, 300)
head(H('Men by 2032.'), 62, 600, h=100, name='!!under')
text(150, 720, 1500, 60, '5K → 15K → 30K → 60K → 120K → 240K → 500K', 34, MONO, D, name='!!path')
# 48
new(tape=True); lab('Sport. Or culture.', y=200)
head(H('500,000 men isn’t a big number with *sport* behind it.'), 120, 260, w=1300, h=560)
body([[('A sport. A team of teams. ', PA), ('Two Circles.', A)]], 830)
# 49
new(); league(lr(ROWS[:4]) + [('Sport · predicted', 5.4, 5.4, 2.5, 1.6, 4.6, None, 'hl')] + lr(ROWS[4:]))
# 50
new(qr=False, tape=True)
lg = cur.shapes.add_picture('tc-logo.png', px(150), px(200), height=px(110)); lg.name = '!!logo'
head(H('Two Circles:|*join up.*'), 120, 360, w=1000, h=300)
text(150, 680, 1000, 120, 'hard-as-nails.com/two-circles\nhello@hard-as-nails.com', 34, MONO, PA, name='!!body')
bigqr(1220, 220, 560)

# ---------- notes + morph ----------
assert len(prs.slides) == len(NOTES), (len(prs.slides), len(NOTES))
for s, n in zip(prs.slides, NOTES):
    s.notes_slide.notes_text_frame.text = n
    el = s._element
    tr = etree.fromstring(MORPH)
    clr = el.find('{http://schemas.openxmlformats.org/presentationml/2006/main}clrMapOvr')
    (clr.addnext(tr) if clr is not None else el.insert(1, tr))
prs.save('TwoCircles_editable.pptx')
print('TwoCircles_editable.pptx', len(prs.slides), 'slides')
