# Two Circles keynote, 26 Nov 2026. Beats from Leaders in Sport FINAL v9X, in its order.
# Live numbers: Supabase hard-as-nails, queried 26 Nov 2026 (dash.v_funnel_now; baseline item means by profession).

def S(html, notes='', **kw):
    d = dict(html=html, notes=notes); d.update(kw); return d

FOOT = 'HARD AS NAILS × TWO CIRCLES · AVIATION HOUSE · 26 NOVEMBER 2026'

# ---------- league table ----------
COLS = [('Feels brave', 'out of 10'), ('Workplace courage', 'out of 7'),
        ('Contest culture', 'out of 5 · lower is better'), ('Acts for others', 'out of 3'),
        ('Rejects the Man Box', 'out of 5'), ('Men', 'n')]
# composite rank (each scale 0-1, contest reversed, averaged)
ROWS = [
    ('Health, care & education', 5.8, 5.7, 2.4, 1.7, 4.6, 68),
    ('Retail & hospitality', 5.7, 5.6, 2.4, 1.4, 4.7, 30),
    ('Public & emergency services', 6.2, 5.5, 2.5, 1.5, 4.5, 24),
    ('Creative & media', 5.2, 5.4, 2.4, 1.6, 4.7, 73),
    ('Transport & logistics', 4.2, 5.6, 2.1, 1.8, 4.3, 11),
    ('Office & finance', 5.2, 5.3, 2.6, 1.6, 4.6, 91),
    ('Tech & engineering', 5.1, 5.4, 2.5, 1.6, 4.5, 81),
    ('Construction & trades', 5.0, 5.3, 2.6, 1.5, 4.5, 59),
]
SPORT_PRED = ('Sport · predicted', 5.4, 5.4, 2.5, 1.6, 4.6, None)  # average of all 704 men


def league(rows, extra=None, extra_at=None, extra_cls='hl'):
    th = '<tr><th></th><th></th>' + ''.join(f'<th>{a}<small>{b}</small></th>' for a, b in COLS) + '</tr>'
    out, pos = [], 1
    items = list(rows)
    if extra is not None:
        items.insert(extra_at, ('__X__',) + extra)
    for r in items:
        if r[0] == '__X__':
            r = r[1:]
            if r[1] is None:
                out.append(f'<tr class="{extra_cls}"><td class="pos">?</td><td class="ind">{r[0]}</td>'
                           '<td>?</td><td>?</td><td>?</td><td>?</td><td>?</td><td class="n">you?</td></tr>')
                continue
            cls = extra_cls
        else:
            cls = ''
        n = f'{r[6]}' if r[6] else 'all 704'
        out.append(f'<tr class="{cls}"><td class="pos">{pos}</td><td class="ind">{r[0]}</td>'
                   + ''.join(f'<td>{v:.1f}</td>' for v in r[1:6]) + f'<td class="n">{n}</td></tr>')
        pos += 1
    return ('<p class="lab">The league table · starting positions · autumn 2026</p>'
            '<h2 class="m">Who’s brave enough?</h2>'
            f'<table class="lg">{th}{"".join(out)}</table>'
            '<p class="src">Hard As Nails database, 26 Nov 2026 · 704 men with a baseline · average starting scores by the industry men say they work in · a signal, not a result</p>')


def weird(k):
    items = [('2024', 'An Olympic champion.'), ('2025', 'An NBA player. A polish deal.'),
             ('Jan 2026', 'A club. Its president. Its fans.'), ('June 2026', 'The cover of Madden.'),
             ('Next?', 'A sport. On purpose.')]
    cells = ''.join(f'<div class="{"next" if i == 4 else ""}{" off" if i >= k else ""}"><b>{a}</b><p>{b}</p></div>'
                    for i, (a, b) in enumerate(items))
    return f'<p class="lab">What’s weird?</p><h2 class="l">Making the<br><em>weird normal.</em></h2><div class="tl">{cells}</div>'


SLIDES = [
# 1 TITLE
S('<img class="logo" src="tc-logo.png" style="position:absolute;top:60px;left:150px;height:110px">'
  '<h1 class="xl" style="margin-top:80px">Hard as<br><em>nails.</em></h1>'
  '<p class="body" style="max-width:38ch;font-size:42px">Building workplace courage, adaptive mindsets, empathy and <b style="color:var(--acid)">performance</b>… through nail polish.</p>'
  f'<p class="src">Sam Conniff + Daniele Fiandaca · {FOOT}</p>', tape=True,
  notes="SAM · walk-on. Up as the room fills. Nail techs and their kit already set up at the side, in full view. Daniele at his chair, not introduced yet.\n\n'Building workplace courage. Increasing adaptive and adoptive mindsets. Improving empathy and performance.' Say that 'performance' used to say 'engagement'. Pause. '...through nail polish.'\n\nQR top right on every slide goes to the Two Circles sign-up (hard-as-nails.com/two-circles)."),

# 2
S('<h2 class="m" style="max-width:20ch">There isn’t a challenge facing sport, society, business (or the world)</h2>'
  '<h2 class="m dim" style="max-width:22ch;margin-top:40px;color:var(--dim)">where negative stereotypes of masculinity <em>aren’t a contributing force.</em></h2>',
  notes="SAM · 0:00–0:01. Starts serious. 'This is a serious topic. Then we're going to have some fun. Bear with me on both.'"),
# 3
S('<h1 class="xl">Not men.<br><em>The construct.</em></h1>', tape=True,
  notes="SAM · 0:01–0:02. That box is what we're here to talk about. Not men. The construct around them."),
# 4
S('<h2 class="l" style="max-width:16ch">What if a technology could update the <em>performance model</em> of masculinity?</h2>',
  notes="SAM · 0:02–0:03. 'Think about the good men you know.' No names. The defining story of masculinity right now isn't the one we'd want, and that's why it's such a strategic point of intervention."),
# 5
S('<p class="lab">Technology for healthy masculinity</p>'
  '<ul class="list" style="max-width:1300px"><li><b>Under 20p</b> token cost per user.</li><li><b>No</b> data centre.</li>'
  '<li><b>No</b> hallucinations.</li><li><b>Time-honoured</b> over centuries.</li></ul>'
  '<p class="body dim" style="margin-top:40px">(It’s a bottle of nail varnish.)</p>',
  notes="SAM · 0:03–0:04. Pro-AI room: no AI jokes. Read the four lines, then 'So what is it?' Hold up the bottle. Let it sit."),
# 6 CRISIS
S('<p class="lab">The crisis</p>'
  '<div class="cols" style="grid-template-columns:1fr 1fr 1fr">'
  '<div class="rule"><p class="stat" style="font-size:150px">13</p><p>men a day take their own lives.</p></div>'
  '<div class="rule"><p class="stat" style="font-size:150px">~600</p><p>women killed since Sarah Everard.</p></div>'
  '<div class="rule"><p class="stat" style="font-size:110px">+26%<br>+38%</p><p>domestic abuse when England win, and when they lose.</p></div></div>'
  '<p class="body" style="max-width:40ch;margin-top:60px"><b>In sport:</b> not calling it out. Not admitting mistakes. Winning at all costs. Losing badly.</p>'
  '<p class="src">ONS · CALM · Femicide Census · Lancaster University, domestic abuse and England fixtures</p>',
  notes="SAM · 0:04–0:05. 'That might all sound a bit ridiculous. We know the risk. We take it very seriously.' Read the lines. Slowly.\n\n[CHECK, as in Leaders in Sport: these four are external stats, not on the Definitive Stats Card. Source line stays on the slide.]"),
# 7 DARE
S('<h1 class="l" style="max-width:13ch">Come and have a go if you’re <em>hard enough.</em></h1>', tape=True,
  notes="SAM · 0:06–0:08. 'Come and have a go if you think you're hard enough.' The chair comes out. Volunteer sits. Applause. Daniele and the nail techs start painting.\n\nIf Leo Thompson is live for the launch (Daisy, 10 Nov), offer him the chair first."),
# 8 SIGN UP
S('<p class="lab">Sign up</p><h2 class="l" style="max-width:1000px">Academic-grade<br><em>research.</em></h2>'
  '<p class="body" style="max-width:24ch">Leeds Beckett University. Overseen by Professor Brendan Gough, adviser to the World Health Organization.</p>'
  '<div style="position:absolute;right:150px;top:270px;text-align:center"><img src="qr.png" style="width:440px;height:440px;display:block">'
  '<p style="font-family:JetBrains Mono;font-size:24px;letter-spacing:.14em;margin-top:18px">HARD-AS-NAILS.COM/TWO-CIRCLES</p></div>',
  noqr=True,
  notes="SAM · 0:08–0:09. As he sits down: 'This is real science. He's going to be measured.' Leeds Beckett, Professor Brendan Gough, before-and-after measures, a comparison group. QR stays up while he gets painted.\n\nQR verified 26 Nov: decodes to hard-as-nails.com/two-circles, which lands on /signup/two-circles (the Two Circles cohort)."),
# 9 MEASURES
S('<p class="lab">2026 · What are we measuring?</p>'
  '<ul class="list" style="max-width:1450px;columns:2;column-gap:80px">'
  '<li><b>Empathy</b><span>Can he feel what someone else is feeling?</span></li>'
  '<li><b>The Man Box</b><span>How tightly do the old rules hold him?</span></li>'
  '<li><b>Mental health</b><span>Suppression. Anxiety. Asking for help.</span></li>'
  '<li><b>Bystander behaviour</b><span>Does he step in, or look away?</span></li>'
  '<li><b>Workplace courage</b><span>Speaking up. Owning a mistake. The dumb question.</span></li>'
  '<li><b>Contest culture</b><span>Does showing weakness cost you here?</span></li></ul>',
  notes="SAM. Empathy, the first thing we ever measured. The Man Box scale, the most widely validated measure of harmful masculinity norms. Mental health markers. Bystander behaviour. New this year: workplace courage. And masculinity contest culture. 'Not bad men. Rigid ones.'"),
# 10-12 COUNTER
S('<p class="lab">The experiment · 2024</p><p class="stat" style="font-size:420px">20</p><h2 class="sm" style="margin-top:20px">men. Mates, mostly.</h2>',
  notes="SAM. 2024: twenty men. Mostly people who owed me a favour."),
S('<p class="lab">The experiment · 2025</p><p class="stat" style="font-size:420px">429</p><h2 class="sm" style="margin-top:20px">409 more. A control group. Nine months.</h2>',
  notes="SAM. 2025: 409 more. Leeds Beckett. Proper science. The paper is in peer review."),
S('<p class="lab">The experiment · this afternoon</p><p class="stat" style="font-size:420px">1,453</p>'
  '<h2 class="sm" style="margin-top:20px">men signed up. <em>1,024 this year.</em></h2>',
  notes="SAM. 'At Leaders in Sport a fortnight ago we were eleven short of a thousand across three pilots. This afternoon: 1,024 men have signed up this year alone.' LBC on Wednesday did a lot of that.\n\nSay 'signed up', never 'painted'. 1,024 = dash.v_funnel_now, 26 Nov (real participants, 2026; includes the comparison group). 1,453 = 1,024 + 409 (2025) + 20 (2024); can't de-duplicate returners across years. 449 have logged nails on this year. If the live count has moved, say the new number."),
# 13-15 LEAGUE
S(league([r for r in ROWS if r[0] == 'Construction & trades']),
  notes="THE LEAGUE TABLE. 'First aboard: construction. Their starting positions. Five scores. It's a signal, not a result.'\n\nNumbers refreshed 26 Nov from the live database: average baseline score per man, by the industry he says he works in. Feels brave = BRAVE item (1-10). Workplace courage = Workplace Social Courage Scale item mean (1-7). Contest culture = Masculinity Contest Culture item mean (1-5, lower better). Acts for others = bystander vignettes, 0-3 (0 stay quiet, 3 step in directly). Rejects the Man Box = Man in a Box item mean (1-5, higher rejects more). Order = all five scales put on 0-1 (contest reversed) and averaged."),
S(league(ROWS),
  notes="'And then everyone else. Eight industries, 704 men. Health, care and education on top. Construction bottom, and they know it: Wates are the ones doing something about it. Transport is only 11 men, so don't lean on it.' Let them read it. Point at contest culture: lower is better."),
S(league(ROWS, extra=('Sport', None, None, None, None, None), extra_at=len(ROWS)),
  notes="'There's a row missing.' Beat. 'No sport category exists in our data yet. Not one man has told us he works in sport.' (True: one man wrote 'Sports Administrator' in free text; n = 1, never show it.) 'Two Circles: you work with the best teams and athletes in the world. Every team that gets in touch gets its own row, and its read against all of these. I'd love to know where sport sits.'"),
# 16-19 ORIGIN
S('<p class="lab">How the hell did we get here</p><h1 class="xl">WTF?</h1>',
  notes="SAM · 'So where did this come from?'"),
S('<h2 class="l" style="max-width:15ch">I got tickets for my <em>daughter’s birthday.</em></h2>',
  notes="She wanted to get her nails done. I joined in. We went. We glittered. We screamed. It was amazing."),
S('<h2 class="l" style="max-width:15ch">“You batting for the <em>other side</em> now, Sam?”</h2>',
  notes="And became convinced it would lead to conversations men don't have. Getting men talking is notoriously hard. Connection between men is one of the best antidotes to the loneliness and depression they face."),
S('<h2 class="l">So I did it.<br><em>Then Daniele did it.</em></h2>',
  notes="'And then Daniele did it. He's the man painting [volunteer]'s nails right now.' The letters started coming in. The press came: BBC, Spectator, radio, the Japanese press."),
# 20-22 METHOD/RESULTS 2025
S('<p class="lab">2025 study · Leeds Beckett</p><div class="cols" style="grid-template-columns:1fr 1fr 1fr">'
  '<div class="rule"><p class="stat">422</p><p>men signed up to have their nails painted.</p></div>'
  '<div class="rule"><p class="stat">155</p><p>completed the baseline and got them done.</p></div>'
  '<div class="rule"><p class="stat">9 mo</p><p>Pre, post, follow-up, nine months. 195 diaries. A 50-man control group.</p></div></div>',
  notes="That was last year's study. Canter. [422 is the manuscript total incl. the 20 first-wave men; the public site uses 409 enrolled.]"),
S('<p class="lab">2025 results · nine months · n = 51</p><div class="cols" style="grid-template-columns:1fr 1fr">'
  '<div class="rule"><p class="stat">+10%</p><p>rejecting the Man Box (4.23 → 4.66).</p></div>'
  '<div class="rule"><p class="stat">−22%</p><p>on the empathy deficit scale (1.78 → 1.38, lower is better).</p></div></div>'
  '<p class="body" style="margin-top:50px">Control group, 50 men: <b style="color:var(--acid)">no movement at any stage.</b></p>',
  notes="Baseline, then straight to nine months. Moved immediately, held at follow-up, strongest at nine months. The control group: flat.\n\n[CMNI −22% from the Leaders deck is left off: the card says CMNI was unchanged post and at follow-up. Confirm with Brendan before using it on stage.]"),
S('<p class="stat" style="font-size:420px">83%</p><h2 class="sm" style="margin-top:20px;max-width:24ch">began conversations they wouldn’t otherwise have had.</h2>',
  notes="Did painting your nails lead to conversations you wouldn't normally have had? 83% yes (101 of 122)."),
# 23-24 BYSTANDER
S('<p class="lab">Workplace allyship · 2025</p><h2 class="sm" style="max-width:26ch">A man is touching a woman in a way that’s making her visibly uncomfortable. What do you do?</h2>'
  '<div class="cols" style="grid-template-columns:1fr 1fr"><div class="rule"><p class="stat">17.3%</p><p>would intervene. Before.</p></div>'
  '<div class="rule"><p class="stat">37.3%</p><p>would intervene. Six weeks later (n = 66).</p></div></div>',
  notes="A behavioural scenario with a photo. Before: 17.3% would intervene directly. After: 37.3%. More than doubled. Doing nothing fell from 17.3% to 5.9%. The control group didn't shift.\n\n[As in the Leaders deck: after-figure is the manuscript's six-week follow-up, n = 66.]"),
S('<p class="lab">The finding we didn’t expect</p><h1 class="l">The most rigid men<br><em>moved most.</em></h1>'
  '<p class="src">Empathy gain by baseline rigidity · top third vs bottom, d = 0.40, p = 0.034 · lowest-empathy subgroup d = 1.23 (n = 25)</p>',
  notes="The one I'd have bet against. The blokes you'd write off as uncoachable made the biggest gains. That's a performance conversation."),
# 25-26 GAP
S('<p class="lab">The gap · we asked Britain</p><h2 class="sm" style="max-width:26ch">“I’m comfortable talking about the things that worry me.”</h2>'
  '<div class="cols" style="grid-template-columns:1fr 1fr"><div class="rule"><p class="stat">49%</p><p>me.</p></div>'
  '<div class="rule"><p class="stat">16%</p><p>most other men.</p></div></div>'
  '<p class="src">YouGov · GB men · n = 970 · August 2026</p>',
  notes="We asked a thousand British men, through YouGov. Half said yes. Then: and most other men? One in six. 'Half of men can. They think one in six can.'"),
S('<p class="lab">The gap · our men, before a single nail</p><h2 class="sm" style="max-width:26ch">“The strongest men can be honest about their feelings in front of others.”</h2>'
  '<div class="cols" style="grid-template-columns:1fr 1fr"><div class="rule"><p class="stat">86%</p><p>me.</p></div>'
  '<div class="rule"><p class="stat">28%</p><p>most other men.</p></div></div>'
  '<p class="body">Most men already agree. <em>They just think they’re alone.</em></p>'
  '<p class="src">Hard As Nails 2026 baseline · n = 314 · early data</p>',
  notes="'Most men already agree. They just think they're alone. That gap is the whole game.' In a dressing room, that's the whole game too."),
# 27-29 MAN BOX + hands up
S('<img src="man-box.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">', cls='photo',
  notes="THE MAN BOX. Four rules. Feelings = weakness. Aggression = strength. Women = objects. Success = solo hero. The best known, most widely validated measure of harmful masculinity norms."),
S('<p class="lab">Workplace courage · hands up</p><h2 class="m" style="max-width:22ch">If I thought a question was dumb, I would still ask it.</h2>'
  '<p class="body dim">1 strongly disagree · 4 neutral · 7 strongly agree</p><p class="body">You? Your team? The man next to you?</p>',
  notes="Hands up where you'd put yourself. Then your team. Quick."),
S('<p class="lab">Contest culture · in my work environment…</p><h2 class="m" style="max-width:22ch">Admitting you don’t know the answer <em>looks weak.</em></h2>'
  '<p class="body dim">1 strongly disagree · 4 neutral · 7 strongly agree</p><p class="body">Your dressing room? Your boardroom?</p>',
  notes="Hands up. [Item wording from the Masculinity Contest Culture scale (Glick et al.).] In sport this is the head coach and the analyst."),
# 30-32 EXPECTATION GAP
S('<p class="lab">So why does it work?</p><h2 class="l">The expectation gap.</h2>'
  '<p class="body" style="max-width:34ch">He expects judgement. He gets a shrug. <em>The gap is where the change happens.</em></p>',
  notes="'The expectation gap: the distance between what a man expects to happen and what actually does. He braces for judgement. He gets a shrug. And that gap is where the change happens.'"),
S('<p class="lab">195 research diaries</p><p class="stat" style="font-size:380px">68%</p><h2 class="sm" style="margin-top:20px">braced for confrontation. <em>Found conversation.</em></h2>',
  notes="68% of the diaries say the same thing: nobody reacted the way I expected. 'I expected backlash. I got nothing. That threw me more than insults would've.'"),
S('<p class="lab">How it works</p><div class="cols" style="grid-template-columns:1fr 1fr 1fr">'
  '<div class="rule"><h2 class="sm">Surprise</h2><p class="stat" style="font-size:110px;margin-top:20px">68%</p><p>surprised by how others reacted.</p></div>'
  '<div class="rule"><h2 class="sm">Introspection</h2><p class="stat" style="font-size:110px;margin-top:20px">35→62%</p><p>reflecting on themselves.</p></div>'
  '<div class="rule"><h2 class="sm">Realisation</h2><p class="stat" style="font-size:110px;margin-top:20px">98%</p><p>took at least one new action, nine months on.</p></div></div>'
  '<p class="src">Conniff, Fiandaca & Gough · Leeds Beckett University · in peer review</p>',
  notes="Surprise: the world doesn't push back. Introspection: if nobody else was judging me, who was? Realisation: and then they do something. We never ask a man if he's changed. We measure what he expected, what he noticed, and what he did."),
# 33 MAX
S('<h2 class="l" style="max-width:15ch">Max went to the pub to watch the football.</h2><h2 class="l" style="margin-top:40px"><em>He didn’t watch the football.</em></h2>',
  notes="MAX. Your words. He went to the pub to watch the match. Nobody mentioned the nails for ages. Then somebody did. That's the breakthrough."),

# 34 WHAT'S HAPPENED SINCE LEADERS IN SPORT
S('<p class="lab">Since Leaders in Sport · 12 November</p><h2 class="m">What happened next.</h2>'
  '<ul class="list" style="max-width:1450px">'
  '<li><b>The Lionesses</b><span>The FA asked us into camp. A call is booked for after World Cup qualifying.</span></li>'
  '<li><b>British Cycling</b><span>Head of coaching wore purple nails for a week and put us forward to UK Sport.</span></li>'
  '<li><b>English cricket</b><span>The ECB has invited us to ECB Live, 28 January.</span></li>'
  '<li><b>Cricket Scotland</b><span>The men’s head coach took the chair. On stage.</span></li></ul>',
  notes="'A fortnight ago I did this for Leaders in Sport. Here's what's happened since.'\n\nLIONESSES: Dr Kate Hays, The FA, 12 Nov: 'I loved your session this morning - it was the highlight of the conference for me!' She wants us to 'come into camp'; they're in final World Cup qualifying, in camp until 5 Dec. Call booked w/c 7 Dec. NO commitment yet: say 'asked', not 'signed'.\n\nBRITISH CYCLING: Jon Norfolk, 18 Nov: 'I've really enjoyed my week in nails… could be a tool we use moving forward.' Recommended us to UK Sport for PLX (1 Dec). UK Sport 'interested in something longer term'. No formal British Cycling commitment.\n\nECB: Jaime Newell, Talent Pathway Inclusion Officer: invited to ECB Live kick-off, Thu 28 Jan; she's taken it to their People Director. No fee agreed, no reply since 16 Nov.\n\nCRICKET SCOTLAND: Owen Dawkins, men's head coach, was the man in the chair. No correspondence with Cricket Scotland itself.\n\nLottie Wright, Leaders in Sport, 20 Nov: 'The likes of The FA, British Cycling, Team GB and others have been sharing how personally (and on LinkedIn!) the session resonated.'\n\nPrivate emails: quote them out loud only if you're comfortable. Nothing here is on the slide verbatim."),
S('<p class="q">“I don’t believe you can ask anyone else to do something and you’re not prepared to.”</p>'
  '<p class="who">Owen Dawkins · head coach, Cricket Scotland men · Leaders in Sport, 12 Nov 2026</p>', tape=True,
  notes="From the Leaders in Sport film (HAN_x_LeadersInSport_1_Owen_Dawkins_HERO_v4.mp4). If you can, play the clip here instead.\n\n[CHECK: the approval log shows sign-offs from Jaime Newell and Jon Norfolk, not from Owen himself. Fine to say in the room; don't put the slide on social without his OK.]"),

# 36 WOMEN
S('<p class="lab">How women get involved</p><h2 class="l" style="max-width:16ch">The Lionesses have rather <em>outperformed</em> the Lions.</h2>'
  '<p class="body" style="max-width:36ch">As usual, women lead, outperform, and get the men to rise to the challenge.</p>',
  notes="FOR EVERYONE IN THE ROOM. 'This isn't a men-only job. In this country's most popular sport, the Lionesses have rather outperformed the Lions.' Laugh. 'So, as usual, the opportunity is for women to lead, outperform, and get the men to rise to the challenge.'\n\nSam to Kate Hays, 13 Nov: the ask is for the Lionesses and the team around them, Sarina included, each to nominate a man."),
S('<p class="lab">Three ways in · hard-as-nails.com/women</p>'
  '<ul class="list" style="max-width:1400px">'
  '<li><b>Nominate him.</b><span>About eleven seconds for you, five minutes for him.</span></li>'
  '<li><b>Paint them.</b><span>Partners, daughters, mates. Get the kit out.</span></li>'
  '<li><b>Watch what changes.</b><span>You’ll see it before he says it.</span></li></ul>',
  notes="'You already know which man.' Three ways in, from the /women page.\n\nNOMINATOR: nominate-a-man is the most successful thing we've done to get men involved (Sam to Kate Hays, 13 Nov). Don't quote the 20% conversion or the 57 LBC nominators: neither is on the stats card yet."),
# 38 NOMINATOR
S('<p class="lab">The Nominator</p><h1 class="l" style="max-width:14ch">Nominate a man.<br><em>He’ll thank you. Eventually.</em></h1>'
  '<div style="position:absolute;right:150px;bottom:150px;text-align:center"><img src="qr-nom.png" style="width:300px;height:300px;display:block">'
  '<p style="font-family:JetBrains Mono;font-size:20px;letter-spacing:.14em;margin-top:14px">HARD-AS-NAILS.COM/TWO-CIRCLES-NOMINATE</p></div>',
  notes="THE NOMINATOR MAN. [Sam: I couldn't find 'the Nominator Man' anywhere in Drive, Gmail or the site, so this slide is the nominate ask. Tell the story your way.]\n\nTwo Circles has its own nominate link: hard-as-nails.com/two-circles-nominate. Staff nominate a man; his link sends him to the Two Circles sign-up. The big QR on this slide is the nominate link (verified 26 Nov); the small one top right is the sign-up."),
# 39 RESPECT
S('<p class="lab">Respect</p><h2 class="l" style="max-width:16ch">We didn’t invent this. <em>We’re standing on it.</em></h2>'
  '<p class="body" style="max-width:42ch">Queer communities. Black women, who built modern nail culture. Vietnamese nail technicians, who built the salon trade. Black men in public life. Trans and non-binary people.</p>'
  '<p class="src">Credit you wait to be asked for isn’t really credit · hard-as-nails.com/respect</p>',
  notes="RESPECT AND CREDIT. 'Our men get a week. Optional. With a research study to hide behind and a date it ended. Other people have been living this for decades without any of those three things.'\n\n'Credit you wait to be asked for isn't really credit.' Then turn to the nail techs in the room: credit them by name."),

# 40 MISSION CONTROL
S('<p class="lab">Mission Control · who they’re doing it for</p>'
  '<ul class="list" style="max-width:1500px;font-size:34px">'
  '<li>“My daughter, who frequently wants to paint my nails anyway!”</li>'
  '<li>“My two sons, who I hope I can teach to be emotionally intelligent men.”</li>'
  '<li>“For my son, who I lost, because he didn’t feel able to be whatever he wants to be.”</li>'
  '<li>“Me, my younger self who spent so much emotional energy trying to fit in.”</li>'
  '<li>“My four year old, who’ll grow up in a world where being yourself means everything.”</li></ul>'
  '<p class="src">Hard As Nails database · 2026 cohort, real participants · approved dedications, no names</p>',
  notes="Read them slowly. Slow down from the two sons. (Approved dedications, as used at Leaders in Sport.)"),

# 41-45 WEIRD NORMAL
S(weird(0), notes="THE MOMENT. 'How does a norm tip?' Let it sit."),
S(weird(2), notes="2024: Tom Daley, Olympic champion, Union Jack nails. 2025: Jared McCain, NBA. Sally Hansen signs him: their first male athlete."),
S(weird(3), notes="JAN 2026: Celta Vigo. A player gets homophobic abuse. A week later the fans, the players and the club president turn up with painted nails. 'That was one club, by accident, in a week. Imagine a sport doing it on purpose.'\n\n[Sam: this is Celta Vigo, not Celtic. I found no Celtic story anywhere. Say 'Celta Vigo'.]"),
S(weird(4), notes="JUNE 2026: Caleb Williams, Chicago Bears quarterback, on the cover of Madden. Nails front and centre."),
S(weird(5), notes="'Not weird. Not yet a bandwagon. You all know the feeling of being a year late to something. The foundations are laid. It needs a sport brave enough to push it into the mainstream. And since Leaders in Sport: the Lionesses, British Cycling, the ECB and Cricket Scotland have all leant in.'"),
# 46 NORMAL WEIRD
S('<p class="lab">What’s normal?</p><h2 class="m">And the normal <em>weird.</em></h2><div class="cols" style="grid-template-columns:1fr 1fr 1fr">'
  '<div class="rule"><p class="stat">58%</p><p>of women have experienced sexual harassment, bullying or verbal abuse at work.</p></div>'
  '<div class="rule"><p class="stat">77%</p><p>of men have had mental health concerns.</p></div>'
  '<div class="rule"><p class="stat">24%</p><p>of them ask for help.</p></div></div>'
  '<p class="src">TUC / Opinium, 1,010 working women, 2023 · men’s figures as used in the Wates keynote</p>',
  notes="'That's what's weird. Here's what's normal.' Read the three. Slowly. 'That's the normal we'd like to make weird.'"),
# 47-48 ROAD
S('<p class="lab">The road to 500,000</p><p class="stat" style="font-size:300px">500,000</p><h2 class="sm" style="margin-top:20px">men by 2032.</h2>'
  '<p class="body dim" style="font-family:JetBrains Mono;font-size:30px;letter-spacing:.06em">5K → 15K → 30K → 60K → 120K → 240K → 500K</p>',
  notes="'This year we're going for 5,000. Roughly doubling every year gets us to half a million men by 2032.' Imagine those benefits, fear of judgement down, men stepping in, at that scale.\n\n[ESTIMATE, not a forecast.] 1,024 signed up so far this year against the 5,000."),
S('<p class="lab">Sport. Or culture.</p><h2 class="l" style="max-width:15ch">500,000 men isn’t a big number with <em>sport</em> behind it.</h2>'
  '<p class="body">A sport. A team of teams. <b style="color:var(--acid)">Two Circles.</b></p>', tape=True,
  notes="THE HERO MOMENT. Slowly.\n\n'Sport is partisan. If one team does this, their rivals won't. So it isn't one team. It's a sport. Or a team of teams. You work with the best athletes and teams in the world. If a sport got behind this, with its clubs and its fans, we wouldn't be talking about half a million men. Job done.'\n\n'I've no idea what this does inside a performance environment. Nobody does, because nobody's measured it. If that sounds daft, tell me at the nail table. If it doesn't, same table.'"),
# 49 FINAL LEAGUE
S(league(ROWS, extra=SPORT_PRED, extra_at=4),
  notes="THE END. 'And here's where sport would sit. That's a prediction: the average of every man so far. Mid-table. Prove us wrong.' Ask Hannah for the live count."),
# 50 CLOSE
S('<img src="tc-logo.png" style="height:110px;width:auto;align-self:flex-start">'
  '<h1 class="l" style="margin-top:50px">Two Circles:<br><em>join up.</em></h1>'
  '<p class="body" style="font-family:JetBrains Mono;font-size:34px">hard-as-nails.com/two-circles<br>hello@hard-as-nails.com</p>'
  '<div style="position:absolute;right:150px;top:220px"><img src="qr.png" style="width:560px;height:560px;display:block"></div>',
  noqr=True, tape=True,
  notes="BOTH · end, then the nail bar. Thank you. The nail techs are open."),
]
