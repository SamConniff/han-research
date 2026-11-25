"""Fourth cut (adds the approved-face nod and crew, the dance, and the framed logo verse). Was: third cut: real Sam opens, the hat arrives with the crew, type fills the frame.

Usage: python3 compose3.py <treated_dir> <audio> <out.mp4> [--still t1,t2,...] [--draft]
Reuses the clone crew and end card from compose.py. --draft burns in the internal watermark.
"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw
import compose as C
from compose import W, H, BLACK, PINK, PINK_DEEP, ACID, PAPER, PLACES, font, rgb, clip, zoom, grid

DRAFT = "--draft" in sys.argv
N = C.NUM_WORD
LABEL = "PART AI SAM. REAL TRIAL."

def fit(d, text, width, cap):
    lo, hi = 30, cap
    while hi - lo > 2:
        m = (lo + hi) // 2
        if d.textlength(text, font=font(m)) <= width: lo = m
        else: hi = m
    return lo

def bigcap(d, lines, bottom=1700, width=980, cap=190, x=50, shown=None):
    """Lines stacked on hard ink blocks, each set as large as the width allows."""
    sizes = [fit(d, ln, width - 40, cap) for ln in lines]
    hs = [int(s * 0.94) for s in sizes]
    y = bottom - sum(hs)
    for i, (ln, s, h) in enumerate(zip(lines, sizes, hs)):
        if shown is None or i < shown:
            w = d.textlength(ln, font=font(s))
            d.rectangle([x, y, x + w + 40, y + h], fill=rgb(BLACK))
            cx = x + 20
            for word in ln.split(" "):
                col = ACID if word.strip(",.?!") == N else (PINK if ln.startswith("(") else PAPER)
                d.text((cx, y - int(s * 0.14)), word, font=font(s), fill=rgb(col))
                cx += d.textlength(word + " ", font=font(s))
        y += h

def slam(lines, colours=None):
    """Full-frame type on black."""
    im = Image.new("RGB", (W, H), rgb(BLACK)); d = ImageDraw.Draw(im)
    sizes = [fit(d, ln, 1000, 420) for ln in lines]; hs = [int(s * 0.88) for s in sizes]
    y = (H - sum(hs)) // 2 - 40
    for i, (ln, s, h) in enumerate(zip(lines, sizes, hs)):
        col = (colours or [PAPER] * len(lines))[i]
        d.text((40, y - int(s * 0.16)), ln, font=font(s), fill=rgb(col)); y += h
    return im

# start, end, lines, [times at which each line lands]
CAPS = [
    (0.00, 1.75, ["I GOT", N, "PLACES,", "YOU KNOW"], [0.0, 0.4, 0.74, 1.1]),
    (1.80, 3.28, ["I GOT", N, "PLACES", "TO GO"], [1.8, 2.14, 2.52, 2.88]),
    (3.32, 5.05, ["IF YOU'RE", "A MAN,", "LET ME KNOW"], [3.32, 3.9, 4.54]),
    (5.10, 6.80, ["COME AND JOIN", "THE CONTROL", "GROUP, YO"], [5.1, 5.86, 6.26]),
    (6.84, 9.85, ["I GOT", N, "PLACES TO MAKE", "THE SCIENCE", "ROBUST"], [6.84, 7.4, 7.76, 9.08, 9.38]),
    (13.94, 15.60, ["DID YOU SEE ME", "WITH MY", "NAILS DONE?"], [13.94, 14.68, 14.88]),
    (17.44, 19.00, ["DID YOU SEE ME", "WITH MY", "NAILS DONE?"], [17.44, 18.16, 18.38]),
    (21.44, 22.60, ["SAMMY C'S", "NEVER FADING"], [21.44, 22.12]),
    (22.64, 24.42, ["PAINTED NAILS,", "AND THE MEN", "STARTED", "CHANGING"], [22.64, 23.42, 23.74, 23.98]),
    (24.48, 26.05, ["LESS SCARED", "OF WHAT THE LADS", "WOULD BE SAYING"], [24.48, 25.08, 25.56]),
    (26.10, 28.40, ["MORE LIKELY", "TO STEP IN", "WHEN A STRANGER", "NEEDS SAVING"], [26.1, 26.44, 26.94, 27.26]),
    (28.50, 29.55, ["THE PILOT", "WAS AMAZING"], [28.5, 29.06]),
    (29.60, 31.25, ["BUT ONE STUDY", "AIN'T WORTH", "CELEBRATING"], [29.6, 30.38, 30.8]),
    (31.30, 33.20, ["WAS IT THE NAILS,", "OR THE TIMES", "THAT ARE", "CHANGING?"], [31.3, 32.14, 32.58, 32.84]),
    (33.24, 34.88, ["RANDOMISE IT,", "THAT'S REAL", "SCIENCE", "WE'RE MAKING"], [33.24, 33.82, 34.08, 34.38]),
    (34.92, 36.70, ["THE ALGORITHM", "ALLOCATES,", "NO FAKING"], [34.92, 35.52, 36.1]),
    (36.74, 38.38, ["CHANCE PICKS", "YOUR HALF,", "THERE'S NO", "TRADING"], [36.74, 37.2, 37.6, 38.02]),
    (38.42, 39.94, [N, "PLACES", "STILL WAITING"], [38.42, 39.24, 39.52]),
    (39.98, 42.00, ["FOR THE SCIENCE", "OF MASCULINITY,", "JUST TAKE IT"], [39.98, 40.46, 41.04]),
    (42.44, 45.70, ["MAN OF THE", "CONTROL GROUP,", "WHO COULD", "IT BE?"], [42.44, 42.82, 43.88, 44.5]),
    (45.78, 48.90, ["CONTROL GROUP", "GEEZER,", "COULD BE", "YOU OR ME"], [45.78, 46.36, 47.58, 48.2]),
    (49.00, 50.55, ["THINK IT", "LOOKS SOFT?", "NAH MATE,", "HERE'S THE PROOF"], [49.0, 49.3, 49.8, 50.1]),
    (50.60, 52.10, ["ONE OF", "THE HUNDRED,", "AND THAT'S", "THE TRUTH"], [50.6, 50.9, 51.4, 51.7]),
    (52.15, 53.55, ["PROVE THIS AIN'T", "PERFORMATIVE", "RUBBISH"], [52.15, 52.6, 53.1]),
    (53.60, 54.55, ["GET YOUR", "CERTIFICATE", "WHEN WE GET"], [53.6, 53.9, 54.25]),
]
SLAMS = [  # start, end, lines, colours
    (16.40, 17.40, ["(OH", "NO)"], [PINK, PINK]),
    (19.66, 21.40, ["(OH NO,", "NOT", "AGAIN)"], [PINK, PINK, PINK]),
    (54.55, 55.45, ["PUB", "LISH", "ED"], [ACID, ACID, ACID]),
]
C0, C1 = 9.85, 13.90
D0, D1, YS, END0 = 46.6, 48.9, 55.45, 57.3
POP = [C0 + 0.05 + k * (C1 - C0 - 0.5) / (PLACES - 1) for k in range(PLACES)]
DROP = {k: D0 + n * (D1 - D0) / (PLACES - 1) for n, k in enumerate(C.DROP_ORDER)}

def stamp(im, t):
    d = ImageDraw.Draw(im)
    if t < END0: C.blocks(d, [LABEL], 60, 190, 27, pad=(14, 9), weight=700)
    if DRAFT:
        C.blocks(d, ["INTERNAL DRAFT. PLACEHOLDER MUSIC. DO NOT POST."], 60, 132, 27, fill=BLACK, bg=ACID, pad=(14, 9), weight=800)
    return im

def frame(t):
    for a, b, lines, cols in SLAMS:
        if a <= t < b: return stamp(slam(lines, cols), t)
    if t >= END0:
        C.PLACES_LABEL = None
        return stamp(C.end_card(), t)
    if t < C0:
        z = 2.0                                         # he stands small and low in his own footage: come right in
        for a, b, zz in ((1.8, 3.3, 2.5), (5.1, 6.82, 2.7), (8.2, C0, 2.35)):
            if a <= t < b: z = zz
        img = zoom(clip("lipR", t), z, 0.5, 0.50)
    elif t < C1:
        img = grid(t, [1 if t >= POP[k] else 0 for k in range(PLACES)], [t - POP[k] for k in range(PLACES)])
    elif t < 21.44: img = zoom(clip("lipC", t - 13.9), 1.25 if t >= 17.4 else 1.0, 0.5, 0.36)
    elif t < 24.46: img = clip("fish", (t - 21.44) * 1.6)
    elif t < 28.46: img = zoom(clip("arms", t - 24.46), 1.0 if t < 26.1 else 1.4, 0.55, 0.25)
    elif t < 31.28: img = zoom(clip("run", t - 28.46), 1.0 if t < 29.6 else 1.35, 0.5, 0.22)
    elif t < 33.22: img = clip("hands", (t - 31.28) + 2.2)
    elif t < 38.40: img = zoom(clip("coin", (t - 33.22) * 0.95), 1.0 if t < 36.74 else 1.3, 0.5, 0.42)
    elif t < 42.42: img = grid(t, [1] * PLACES)
    elif t < 44.10: img = zoom(clip("nodsolo", (t - 42.42) % 5.0), C.punch(t, 42.42, (1.0, 1.0, 1.3, 1.3)), 0.5, 0.2)
    elif t < 45.76: img = zoom(clip("rave", (t - 44.10) + 0.6), 1.15, 0.5, 0.3)        # his own arms-up dance, on the lab-coat Sam
    elif t < 49.00: img = grid(t, [2 if t >= DROP[k] else 1 for k in range(PLACES)])
    elif t < 55.45: img = zoom(clip("framed", (t - 49.0) * 0.92), 1.25, 0.45, 0.60)   # real Sam holds up the certificate
    else: img = grid(t, [2] * PLACES)
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    for a, b, lines, times in CAPS:
        if a <= t < b: bigcap(d, lines, shown=sum(1 for x in times if t >= x), cap=150 if t < C0 else (118 if 49.0 <= t < 55.45 else 190))
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
