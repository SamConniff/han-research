"""Sixth cut: Sam's untouched vocal, clear calls to action, a Running Man crew, no 'your space'.

Usage: python3 compose6.py <treated_dir> <audio> <out.mp4> <lines.json> [--cover a-b,c-d] [--still t1,t2,...]
--cover lists time ranges where the lip-sync slips; those ranges show a call-to-action card instead.
"""
import sys, json, subprocess, functools, numpy as np, cv2
from PIL import Image, ImageDraw
import treat
import compose as C
import compose3 as C3
from compose import W, H, BLACK, PINK, PINK_DEEP, ACID, PAPER, PLACES, font, rgb, clip, zoom, grid

TR = sys.argv[1]; N = C.NUM_WORD; TOTAL = 64.0
J = json.load(open(sys.argv[4])); L = {(l["section"], l["i"]): (l["start"], l["end"]) for l in J["lines"]}
S = lambda sec, i: L[(sec, i)][0]
E = lambda sec, i: L[(sec, i)][1]
COVER = []
if "--cover" in sys.argv:
    for r in sys.argv[sys.argv.index("--cover") + 1].split(","):
        if r: a, b = r.split("-"); COVER.append((float(a), float(b)))

TEXT = {
    ("hook", 0): ["I GOT", N, "PLACES", "TO GO"], ("hook", 1): ["I GOT", N, "PLACES,", "YOU KNOW"],
    ("hook", 2): ["IF YOU'RE", "A MAN,", "LET ME KNOW"], ("hook", 3): ["COME AND JOIN", "THE CONTROL", "GROUP, YO"],
    ("hook", 4): ["I GOT", N, "PLACES TO MAKE", "THE SCIENCE", "FLOW"],
    ("nails", 0): ["DID YOU SEE ME", "WITH MY", "NAILS DONE?"], ("nails", 1): ["(OH NO)"],
    ("nails", 2): ["DID YOU SEE ME", "WITH MY", "NAILS DONE?"], ("nails", 3): ["(OH NO,"], ("nails", 4): ["(OH NO,", "NOT AGAIN)"],
    ("verse", 0): ["SAMMY C'S", "NEVER FADING"], ("verse", 1): ["PAINTED NAILS,", "AND THE MEN", "STARTED", "CHANGING"],
    ("verse", 2): ["LESS SCARED", "OF WHAT THE LADS", "WOULD BE SAYING"], ("verse", 3): ["MORE LIKELY", "TO STEP IN", "WHEN A STRANGER", "NEEDS SAVING"],
    ("verse", 4): ["THE PILOT", "WAS AMAZING"], ("verse", 5): ["BUT ONE STUDY", "AIN'T WORTH", "CELEBRATING"],
    ("verse", 6): ["WAS IT THE NAILS,", "OR THE TIMES", "THAT ARE", "CHANGING?"], ("verse", 7): ["RANDOMISE IT,", "THAT'S THE", "SCIENCE", "WE'RE MAKING"],
    ("verse", 8): ["THE ALGORITHM", "ALLOCATES,", "NO FAKING"], ("verse", 9): ["CHANCE PICKS", "YOUR HALF,", "THERE'S NO", "TRADING"],
    ("verse", 10): [N, "PLACES", "STILL WAITING"], ("verse", 11): ["FOR THE SCIENCE", "OF MASCULINITY,", "JUST TAKE IT"],
    ("chant", 0): ["MAN OF THE", "CONTROL GROUP,", "WHO COULD", "IT BE?"], ("chant", 1): ["CONTROL GROUP", "GEEZER,", "COULD BE", "YOU OR ME"],
    ("chant", 2): ["MAN OF THE", "CONTROL GROUP,", "WHO COULD", "IT BE?"], ("chant", 3): ["CONTROL GROUP", "GEEZER,", "COULD BE", "YOU OR ME"],
    ("cert", 0): ["THINK IT", "LOOKS SOFT?", "NAH MATE,", "HERE'S THE PROOF"], ("cert", 1): ["ONE OF", "THE HUNDRED,", "AND THAT'S", "THE TRUTH"],
    ("cert", 2): ["PROVE THIS AIN'T", "PERFORMATIVE", "RUBBISH"], ("cert", 3): ["GET YOUR", "CERTIFICATE", "WHEN WE GET"],
}
PUB = S("cert", 3) + 1.62                                      # where "published" lands in his take
CTA0 = PUB + 0.95                                              # calls to action begin
END0 = 59.7
CAPS = []
for key, lines in TEXT.items():
    a, b = L[key]
    if key == ("cert", 3): b = PUB
    nxt = min([s for (s, e) in L.values() if s > a + 0.05] + [b + 0.6])
    step = (b - a) * 0.8 / len(lines)
    CAPS.append((a, min(max(b + 0.25, a + 0.5), nxt), lines, [a + k * step for k in range(len(lines))]))
C0, C1 = E("hook", 4) + 0.05, S("nails", 0) - 0.05
POP = [C0 + 0.03 + k * (C1 - C0 - 0.35) / (PLACES - 1) for k in range(PLACES)]
V = lambda i: S("verse", i)

# ---------------------------------------------------------------- chevron and calls to action
@functools.lru_cache(maxsize=4)
def chevron(h=120):
    y, x = np.mgrid[0:h, 0:W]; band = (((x + y) // 60) % 2).astype(np.float32)[..., None]
    return (ACID * band + BLACK * (1 - band)).astype(np.uint8)

def cta(lines, colours, url=False):
    """Full-frame call to action: one chevron band, type as large as the width allows."""
    im = C3.slam(lines, colours); a = np.asarray(im).copy()
    a[250:370] = chevron()
    im = Image.fromarray(a)
    if url:
        d = ImageDraw.Draw(im); d.rectangle([60, 1560, 1020, 1562], fill=rgb(PAPER))
        d.text((60, 1584), C.URL, font=font(51, 700, "inter"), fill=rgb(PAPER))
    return im
CTA_A = (["SIGN UP", "TO", "SCIENCE."], [PAPER, PAPER, PAPER])
CTA_B = (["JOIN THE", "CONTROL", "GROUP", "NOW."], [PAPER, PAPER, PAPER, PINK])
CTA_C = ([str(PLACES), "SPACES", "LEFT"], [ACID, PAPER, PAPER])
CARDS = [CTA_B, CTA_A, CTA_C]

# ---------------------------------------------------------------- Running Man crew: 21 small full-body Sams
RW, RH = 150, 392                       # each figure cropped close: x 18-82%, y 5-99% of his frame
RX0, RX1, RY0, RY1 = 194, 886, 96, 1901
@functools.lru_cache(maxsize=140)
def _run_src(i):
    src = cv2.imread(f"{TR}/runman/src{i:04d}.jpg")[RY0:RY1, RX0:RX1, ::-1]; pm = cv2.imread(f"{TR}/runman/pm{i:04d}.png", cv2.IMREAD_UNCHANGED)[RY0:RY1, RX0:RX1]
    return cv2.resize(src, (RW, RH), interpolation=cv2.INTER_AREA), cv2.resize(pm, (RW, RH), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
RUN_N = None
def runcrew(t):
    global RUN_N
    if RUN_N is None:
        import os; RUN_N = len([f for f in os.listdir(f"{TR}/runman") if f.startswith("src")])
    out = C.grid_ground().copy()
    for k in range(PLACES):
        r, c = divmod(k, 7); x = 15 + c * 150; y = 225 + r * 400 + (34 if c % 2 else 0)
        n = RUN_N - 30; p = int(t * 24 + k * 7) % (2 * n - 2); i = 30 + (p if p < n else 2 * n - 2 - p)   # skip the settle-in second
        src, pm = _run_src(i)
        g = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
        g = np.clip((g - 0.06) / 0.86, 0, 1); g = g * g * (3 - 2 * g) * 0.65 + g * 0.35
        man = BLACK + (PAPER - BLACK) * g[..., None]
        nm = C._nail_small(src)[..., None]
        nails = treat.shift_hue(src, C.HUES[k % len(C.HUES)]).astype(np.float32); grey = nails.mean(2, keepdims=True)
        man = man * (1 - nm) + np.clip(grey + (nails - grey) * 1.9 + 12, 0, 255) * nm
        a = np.maximum(pm, nm[..., 0])[..., None]
        out[y:y + RH, x:x + RW] = out[y:y + RH, x:x + RW] * (1 - a) + man * a
    return np.clip(out, 0, 255).astype(np.uint8)

def stamp(im, t):
    d = ImageDraw.Draw(im)
    if t < END0: C.blocks(d, [C3.LABEL], 60, 190, 27, pad=(14, 9), weight=700)
    return im

def frame(t):
    if PUB <= t < CTA0: return stamp(C3.slam(["PUB", "LISH", "ED"], [ACID, ACID, ACID]), t)
    if t >= END0: return stamp(C.end_card(), t)
    if t >= CTA0:                                               # three calls to action, a bar and a bit each
        k = min(int((t - CTA0) / ((END0 - CTA0) / 3)), 2); lines, cols = (CTA_A, CTA_B, CTA_C)[k]
        return stamp(cta(lines, cols, url=(k == 2)), t)
    for n, (a, b) in enumerate(COVER):                          # where the lip-sync slips, say it in type instead
        if a <= t < b:
            lines, cols = CARDS[n % len(CARDS)]; return stamp(cta(lines, cols), t)
    cap = 190
    if t < C0:
        z = 2.0
        for a, b, zz in ((S("hook", 1), S("hook", 2), 2.5), (S("hook", 3), S("hook", 4), 2.7)):
            if a <= t < b: z = zz
        img = zoom(clip("lipR", t), z, 0.5, 0.50); cap = 150
    elif t < C1:
        img = grid(t, [1 if t >= POP[k] else 0 for k in range(PLACES)], [t - POP[k] for k in range(PLACES)])
    elif t < E("nails", 4) + 0.15: img = zoom(clip("lipC", t - 9.80), 1.25 if t >= S("nails", 2) else 1.0, 0.5, 0.36)
    elif t < V(0): return stamp(cta(*CTA_B), t)                 # the gap before the verse: first clear ask
    elif t < V(2): img = clip("fish", (t - V(0)) * 1.5)
    elif t < V(4): img = zoom(clip("arms", t - V(2)), 1.0 if t < V(3) else 1.4, 0.55, 0.25)
    elif t < V(6): img = zoom(clip("run", t - V(4)), 1.0 if t < V(5) else 1.35, 0.5, 0.22)
    elif t < V(7): img = clip("hands", (t - V(6)) + 2.2)
    elif t < V(10): img = zoom(clip("coin", (t - V(7)) * 0.75), 1.0 if t < V(9) else 1.3, 0.5, 0.42)
    elif t < S("chant", 0): img = grid(t, [1] * PLACES)
    elif t < S("chant", 1): img = zoom(clip("nodsolo", (t - S("chant", 0)) % 5.0), C.punch(t, S("chant", 0), (1.0, 1.0, 1.3, 1.3)), 0.5, 0.2)
    elif t < S("chant", 2): img = zoom(clip("rave", (t - S("chant", 1)) * 1.3 + 0.3), 1.15, 0.5, 0.3)
    elif t < S("chant", 3): img = grid(t, [1] * PLACES)
    elif t < S("cert", 0): img = runcrew(t)
    else: img = zoom(clip("lipF", t - 47.02), 1.25, 0.45, 0.60); cap = 118
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    for a, b, lines, times in CAPS:
        if a <= t < b: C3.bigcap(d, lines, shown=sum(1 for x in times if t >= x), cap=cap)
    if C0 <= t < C1:
        n = sum(1 for k in range(PLACES) if t >= POP[k])
        d.rectangle([50, 1560, 50 + 640, 1760], fill=rgb(BLACK))
        d.text((70, 1530), f"{n:02d}", font=font(210), fill=rgb(ACID))
        d.text((350, 1610), "PLACES", font=font(84), fill=rgb(PAPER))
    return stamp(im, t)

if __name__ == "__main__":
    OUT = sys.argv[3]
    if "--still" in sys.argv:
        for ts in sys.argv[sys.argv.index("--still") + 1].split(","):
            frame(float(ts)).convert("RGB").save(f"{OUT}_{float(ts):05.2f}.jpg", quality=88)
        sys.exit()
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30",
                           "-i", "-", "-i", sys.argv[2], "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-maxrate", "9M",
                           "-bufsize", "18M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL),
                           "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * 30)):
        ff.stdin.write(np.asarray(frame(i / 30).convert("RGB")).tobytes())
        if i % 300 == 0: print(f"{i/30:5.1f}s", flush=True)
    ff.stdin.close(); ff.wait(); print("done", OUT)
