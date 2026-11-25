"""Fifth cut: Sam's own voice. Every cut and caption is driven by where his lines land (lines_v5.json).

Usage: python3 compose5.py <treated_dir> <audio> <out.mp4> <lines.json> [--still t1,t2,...]
"""
import sys, json, subprocess, numpy as np
from PIL import Image, ImageDraw
import compose as C
import compose3 as C3
from compose import W, H, BLACK, PINK, PINK_DEEP, ACID, PAPER, PLACES, font, rgb, clip, zoom, grid

N = C.NUM_WORD
L = {}
for l in json.load(open(sys.argv[4])): L[(l["section"], l["i"])] = (l["start"], l["end"])
def S(sec, i): return L[(sec, i)][0]
def E(sec, i): return L[(sec, i)][1]

# what he says, line by line (captions follow the recording, e.g. "flow" where the sheet had "robust")
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
    ("cert", 0): ["THINK IT", "LOOKS SOFT?", "NAH MATE,", "HERE'S THE PROOF"], ("cert", 1): ["ONE OF", "THE HUNDRED,", "AND THAT'S", "THE TRUTH"],
    ("cert", 2): ["PROVE THIS AIN'T", "PERFORMATIVE", "RUBBISH"], ("cert", 3): ["GET YOUR", "CERTIFICATE", "WHEN WE GET"],
}
PUB = S("cert", 3) + 1.58                 # where "published" lands
CAPS = []
for key, lines in TEXT.items():
    a, b = L[key]
    if key == ("cert", 3): b = PUB
    nxt = min([s for (s, e) in L.values() if s > a + 0.05] + [b + 0.6])
    step = (b - a) * 0.8 / len(lines)
    CAPS.append((a, min(max(b + 0.25, a + 0.5), nxt), lines, [a + k * step for k in range(len(lines))]))

C0, C1 = E("hook", 4) + 0.05, S("nails", 0) - 0.05           # the count sits in the gap after the hook
D0, D1, YS, END0 = PUB + 0.95, PUB + 3.4, PUB + 3.6, 57.3
POP = [C0 + 0.05 + k * (C1 - C0 - 0.5) / (PLACES - 1) for k in range(PLACES)]
DROP = {k: D0 + n * (D1 - D0) / (PLACES - 1) for n, k in enumerate(C.DROP_ORDER)}
V = lambda i: S("verse", i)

def stamp(im, t):
    d = ImageDraw.Draw(im)
    if t < END0: C.blocks(d, [C3.LABEL], 60, 190, 27, pad=(14, 9), weight=700)
    return im

def frame(t):
    if PUB <= t < D0: return stamp(C3.slam(["PUB", "LISH", "ED"], [ACID, ACID, ACID]), t)
    if t >= END0: return stamp(C.end_card(), t)
    cap = 190
    if t < C0:                                                  # the real Sam opens
        z = 2.0
        for a, b, zz in ((S("hook", 1), S("hook", 2), 2.5), (S("hook", 3), S("hook", 4), 2.7)):
            if a <= t < b: z = zz
        img = zoom(clip("lipR", t), z, 0.5, 0.50); cap = 150
    elif t < C1:
        img = grid(t, [1 if t >= POP[k] else 0 for k in range(PLACES)], [t - POP[k] for k in range(PLACES)])
    elif t < E("nails", 4) + 0.2: img = zoom(clip("lipC", t - 10.40), 1.25 if t >= S("nails", 2) else 1.0, 0.5, 0.36)
    elif t < V(0): img = grid(t, [1] * PLACES)
    elif t < V(2): img = clip("fish", (t - V(0)) * 1.6)
    elif t < V(4): img = zoom(clip("arms", t - V(2)), 1.0 if t < V(3) else 1.4, 0.55, 0.25)
    elif t < V(6): img = zoom(clip("run", t - V(4)), 1.0 if t < V(5) else 1.35, 0.5, 0.22)
    elif t < V(7): img = clip("hands", (t - V(6)) + 2.2)
    elif t < V(10): img = zoom(clip("coin", (t - V(7)) * 0.8), 1.0 if t < V(9) else 1.3, 0.5, 0.42)
    elif t < S("chant", 0): img = grid(t, [1] * PLACES)
    elif t < S("chant", 1): img = zoom(clip("nodsolo", (t - S("chant", 0)) % 5.0), C.punch(t, S("chant", 0), (1.0, 1.0, 1.3, 1.3)), 0.5, 0.2)
    elif t < S("cert", 0): img = zoom(clip("rave", (t - S("chant", 1)) * 1.1 + 0.3), 1.15, 0.5, 0.3)
    elif t < PUB: img = zoom(clip("lipF", t - 43.70), 1.25, 0.45, 0.60); cap = 118   # real Sam holds up the certificate
    else: img = grid(t, [2 if t >= DROP[k] else 1 for k in range(PLACES)])
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    for a, b, lines, times in CAPS:
        if a <= t < b: C3.bigcap(d, lines, shown=sum(1 for x in times if t >= x), cap=cap)
    if C0 <= t < C1:
        n = sum(1 for k in range(PLACES) if t >= POP[k])
        d.rectangle([50, 1560, 50 + 640, 1760], fill=rgb(BLACK))
        d.text((70, 1530), f"{n:02d}", font=font(210), fill=rgb(ACID))
        d.text((350, 1610), "PLACES", font=font(84), fill=rgb(PAPER))
    if YS <= t < END0:
        f = font(170); tw = d.textlength("YOUR SPACE", font=f); x = (W - tw) / 2
        d.rectangle([x - 40, 740, x + tw + 40, 960], fill=rgb(PINK_DEEP))
        d.text((x, 748), "YOUR SPACE", font=f, fill=rgb(PAPER))
    return stamp(im, t)

if __name__ == "__main__":
    OUT = sys.argv[3]
    if "--still" in sys.argv:
        for ts in sys.argv[sys.argv.index("--still") + 1].split(","):
            frame(float(ts)).convert("RGB").save(f"{OUT}_{float(ts):05.2f}.jpg", quality=88)
        sys.exit()
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30",
                           "-i", "-", "-i", sys.argv[2], "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-maxrate", "9M",
                           "-bufsize", "18M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", "60.03",
                           "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(int(60.03 * 30)):
        ff.stdin.write(np.asarray(frame(i / 30).convert("RGB")).tobytes())
        if i % 300 == 0: print(f"{i/30:5.1f}s", flush=True)
    ff.stdin.close(); ff.wait(); print("done", OUT)
