"""Compose "21 Geezers to Go": treated clips + clone grid + captions + end card -> MP4.

Usage: python3 compose.py <treated_dir> <track.mp3> <out.mp4> [--still t1,t2,...]
The number of places is one constant (PLACES) so a recount is a one-line change.
"""
import sys, os, subprocess, functools
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
import treat
from treat import W, H, BLACK, PINK, PINK_DEEP, ACID, PAPER

HERE = os.path.dirname(os.path.abspath(__file__))
TR, TRACK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FPS, DUR = 30, 60.03
PLACES = 21
NUM_WORD = "TWENTY-ONE"
URL = "hard-as-nails.com/control-group"

def font(size, weight=900, family="intertight"):
    f = ImageFont.truetype(f"{HERE}/{family}-latin.ttf", size)
    f.set_variation_by_axes([weight])
    return f

rgb = lambda a: tuple(int(v) for v in a)

# ---------------------------------------------------------------- clips
@functools.lru_cache(maxsize=64)
def _load(path):
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    return im[..., ::-1].copy() if im.ndim == 3 else im

def nframes(name):
    return len([f for f in os.listdir(f"{TR}/{name}") if f.startswith("f")])

def clip(name, ct):
    i = int(np.clip(round(ct * 24), 0, nframes(name) - 1))
    return _load(f"{TR}/{name}/f{i:04d}.jpg")

def zoom(img, z, cx=0.5, cy=0.4):
    if z <= 1.001: return img
    w, h = int(W / z), int(H / z)
    x0 = int(np.clip(cx * W - w / 2, 0, W - w)); y0 = int(np.clip(cy * H - h / 2, 0, H - h))
    return cv2.resize(img[y0:y0 + h, x0:x0 + w], (W, H), interpolation=cv2.INTER_LINEAR)

BEAT = 60 / 132.0
def punch(t, t0, steps=(1.0, 1.18, 1.38, 1.18)):
    return steps[int((t - t0) / BEAT) % len(steps)]

# ---------------------------------------------------------------- clone grid
# A crew photo, not a spreadsheet: six staggered rows of 4,3,4,3,4,3, each row standing in front of the last.
CW, CH = 290, 268                     # one clone
CROP = (0, 90, 1080, 1090)            # region of the nod frame that holds hat-to-hands
MW = CW
ROW_STEP, GY = 212, 215
def _slots():
    out = []
    for r in range(6):
        n = 4 if r % 2 == 0 else 3
        x0 = 8 if n == 4 else 140
        out += [(x0 + c * 258, GY + r * ROW_STEP) for c in range(n)]
    return out
SLOTS = _slots()
NOD_N = None
HUES = [0, 95, 210, 40, 260, 150, 320, 70, 180, 15, 235, 120, 290, 55, 195, 340, 105, 250, 30, 165, 275]

def _cellsrc(i):
    src = _load(f"{TR}/nod/src{i:04d}.jpg")[CROP[1]:CROP[3], CROP[0]:CROP[2]]
    pm = _load(f"{TR}/nod/pm{i:04d}.png")[CROP[1]:CROP[3], CROP[0]:CROP[2]]
    return (cv2.resize(src, (MW, CH), interpolation=cv2.INTER_AREA),
            cv2.resize(pm, (MW, CH), interpolation=cv2.INTER_AREA).astype(np.float32) / 255)
_cellsrc = functools.lru_cache(maxsize=140)(_cellsrc)

def _nail_small(src):
    f = src.astype(np.float32); mx, mn = f.max(2), f.min(2)
    m = (((mx - mn) > 45) & ((mx - mn) / (mx + 1) > 0.28)).astype(np.float32)
    return cv2.GaussianBlur(cv2.dilate(m, np.ones((4, 4), np.uint8)), (0, 0), 0.7)

def clone(k, t):
    """One clone, nodding out of phase with his neighbours, with his own nail colour."""
    global NOD_N
    if NOD_N is None: NOD_N = nframes("nod")
    p = int(t * 24 + k * 9) % (2 * NOD_N - 2)
    i = p if p < NOD_N else 2 * NOD_N - 2 - p          # ping-pong so the loop has no jump
    src, pm = _cellsrc(i)
    g = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    g = np.clip((g - 0.06) / 0.86, 0, 1); g = g * g * (3 - 2 * g) * 0.65 + g * 0.35
    man = BLACK + (PAPER - BLACK) * g[..., None]
    nm = _nail_small(src)[..., None]
    nails = treat.shift_hue(src, HUES[k % len(HUES)]).astype(np.float32)
    grey = nails.mean(2, keepdims=True); nails = np.clip(grey + (nails - grey) * 1.9 + 12, 0, 255)
    man = man * (1 - nm) + nails * nm
    return man, np.maximum(pm, nm[..., 0])

@functools.lru_cache(maxsize=1)
def outline():
    _, pm = _cellsrc(0)
    b = (pm > 0.5).astype(np.uint8)
    edge = cv2.dilate(b, np.ones((5, 5), np.uint8)) - cv2.erode(b, np.ones((3, 3), np.uint8))
    return b.astype(np.float32), edge.astype(np.float32)

@functools.lru_cache(maxsize=1)
def grid_ground():
    return treat.ground(np.full((H, W), 0.13, np.float32), 22)

def grid(t, present, popped=None):
    """present[k] in {0: nothing, 1: clone, 2: empty outline}; popped[k] = seconds since pop-in."""
    out = grid_ground().copy()
    for k in range(PLACES):
        x, y = SLOTS[k]
        x1 = min(x + MW, W); w = x1 - x
        if present[k] == 1:
            man, a = clone(k, t)
            if popped is not None and popped[k] < 0.1:   # two-frame overshoot on entry
                s = 1.18
                man = cv2.resize(man, None, fx=s, fy=s)[int(CH * (s - 1)):, int(MW * (s - 1) / 2):][:CH, :MW]
                a = cv2.resize(a, None, fx=s, fy=s)[int(CH * (s - 1)):, int(MW * (s - 1) / 2):][:CH, :MW]
            a = a[:, :w, None]
            out[y:y + CH, x:x1] = out[y:y + CH, x:x1] * (1 - a) + man[:, :w] * a
        elif present[k] == 2:
            fill, e = outline()
            fill = fill[:, :w, None]; e = e[:, :w, None]
            out[y:y + CH, x:x1] = (out[y:y + CH, x:x1] * (1 - fill) + BLACK * fill) * (1 - e) + PAPER * e
    return np.clip(out, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------- type
def blocks(d, lines, x, bottom, size, fill=PAPER, bg=BLACK, pad=(20, 8), gap=0, acid_words=(), weight=900):
    """Each line of type on its own hard ink block, stacked upward from `bottom`."""
    f = font(size, weight)
    asc, desc = f.getmetrics(); lh = int(size * 0.98) + 2 * pad[1]
    y = bottom - len(lines) * lh - (len(lines) - 1) * gap
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.rectangle([x, y, x + w + 2 * pad[0], y + lh], fill=rgb(bg))
        cx = x + pad[0]
        for word in ln.split(" "):
            col = ACID if word.strip(",.?!") in acid_words else fill
            d.text((cx, y + pad[1] - int(size * 0.13)), word, font=f, fill=rgb(col))
            cx += d.textlength(word + " ", font=f)
        y += lh + gap

def wrap(d, text, f, maxw):
    """Greedy wrap to find the line count, then the narrowest width that keeps that count (no orphans)."""
    def greedy(mw):
        lines, cur = [], ""
        for w_ in text.split(" "):
            tryl = (cur + " " + w_).strip()
            if d.textlength(tryl, font=f) <= mw or not cur: cur = tryl
            else: lines.append(cur); cur = w_
        return lines + [cur]
    base = greedy(maxw); best = base
    for mw in range(int(maxw), 200, -20):
        g = greedy(mw)
        if len(g) != len(base) or max(d.textlength(l, font=f) for l in g) > maxw: break
        best = g
    return best

N = NUM_WORD
CAPS = [  # start, end, text, kind
    (0.00, 1.60, f"I got {N} places, you know", "l"), (1.62, 4.12, f"I got {N} places to go", "l"),
    (7.26, 8.90, f"I got {N} places, you know", "l"), (8.92, 11.25, f"I got {N} places to go", "l"),
    (11.28, 12.56, "If you're a man, let me know", "l"), (12.60, 14.28, "Come and join the control group, yo", "l"),
    (14.30, 16.52, f"I got {N} places to make the science robust", "l"),
    (16.58, 18.70, "Did you see me with my nails done?", "l"), (18.70, 18.98, "(oh no)", "a"),
    (18.98, 20.04, "Did you see me with my nails done?", "l"), (20.06, 21.60, "(oh no, not again)", "a"),
    (22.28, 23.52, "Sammy C's never fading", "l"), (23.56, 25.40, "Painted nails, and the men started changing", "l"),
    (25.44, 27.00, "Less scared of what the lads would be saying", "l"),
    (27.04, 29.40, "More likely to step in when a stranger needs saving", "l"),
    (29.52, 30.96, "The pilot was amazing", "l"), (31.02, 32.50, "But one study ain't worth celebrating", "l"),
    (32.54, 34.60, "Was it the nails, or the times that are changing?", "l"),
    (34.64, 36.20, "Randomise it, that's real science we're making", "l"),
    (36.22, 38.06, "The algorithm allocates, no faking", "l"), (38.10, 39.86, "Chance picks your half, there's no trading", "l"),
    (39.90, 41.50, f"{N} places still waiting", "l"), (41.54, 43.64, "For the science of masculinity, just take it", "l"),
    (43.68, 46.95, "Man of the control group, who could it be?", "l"),
    (47.18, 50.60, "Control group geezer, could be you or me", "l"),
    (51.08, 54.25, "Man of the control group, who could it be?", "l"),
    (54.64, 57.18, "Control group geezer, could be you or me", "l"),
]
CAP_BOTTOM, CAP_X, CAP_W = 1640, 60, 860

def overlay(img, t):
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    if t < END0:
        blocks(d, ["AI-GENERATED SAM. REAL TRIAL."], 60, 190, 27, pad=(14, 9), weight=700)
    for a, b, text, kind in CAPS:
        if a <= t < b:
            size = 74; f = font(size)
            lines = wrap(d, text.upper(), f, CAP_W)
            blocks(d, lines, CAP_X, CAP_BOTTOM, size, fill=PINK if kind == "a" else PAPER, acid_words=(N,))
    return im

# ---------------------------------------------------------------- shots
C0, C1 = 4.15, 7.20                    # the count
D0, D1, YS = 51.0, 55.3, 55.4          # drop-out to outlines, then YOUR SPACE
END0 = 57.25
POP = [C0 + 0.05 + k * (C1 - C0 - 0.45) / (PLACES - 1) for k in range(PLACES)]
DROP_ORDER = [10, 3, 17, 0, 13, 7, 20, 5, 15, 1, 11, 18, 8, 4, 14, 19, 2, 9, 16, 6, 12]
DROP = {k: D0 + n * (D1 - D0) / (PLACES - 1) for n, k in enumerate(DROP_ORDER)}

@functools.lru_cache(maxsize=1)
def still_s1():
    return np.asarray(Image.open(f"{TR}/still_s1.jpg").convert("RGB"))

def end_card():
    im = Image.new("RGB", (W, H), rgb(BLACK)); d = ImageDraw.Draw(im)
    d.text((54, 250), str(PLACES), font=font(560), fill=rgb(ACID))
    y = 860
    for ln in ["PLACES LEFT IN A", "RANDOMISED TRIAL", "OF MEN'S COURAGE."]:
        d.text((60, y), ln, font=font(96), fill=rgb(PAPER)); y += 100
    blocks(d, ["JOIN OR NOMINATE A MAN."], 60, 1330, 66, fill=PAPER, bg=PINK_DEEP, pad=(24, 16))
    d.rectangle([60, 1400, 1020, 1402], fill=rgb(PAPER))
    d.text((60, 1424), URL, font=font(51, 700, "inter"), fill=rgb(PAPER))
    d.text((60, 1510), "PART AI SAM. REAL TRIAL.", font=font(27, 700, "inter"), fill=rgb(PAPER))
    return im

def frame(t):
    if t < C0: img = clip("lipA", t)
    elif t < C1:
        present = [1 if t >= POP[k] else 0 for k in range(PLACES)]
        img = grid(t, present, [t - POP[k] for k in range(PLACES)])
    elif t < 14.30: img = zoom(clip("lipB", t - 7.1), 1.22 if 11.28 <= t < 12.60 else 1.0, 0.5, 0.33)
    elif t < 16.55: img = grid(t, [1] * PLACES)
    elif t < 21.45: img = zoom(clip("lipC", t - 14.3), 1.25 if 18.98 <= t < 20.06 else 1.0, 0.5, 0.36)
    elif t < 22.28: img = clip("hands", (t - 21.45) + 0.4)
    elif t < 25.42: img = clip("fish", (t - 22.28) * 1.55)
    elif t < 29.50: img = zoom(clip("arms", t - 25.42), 1.0 if t < 27.04 else 1.4, 0.55, 0.25)
    elif t < 32.52: img = zoom(clip("run", (t - 29.50) * 1.0), 1.0 if t < 31.02 else 1.35, 0.5, 0.22)
    elif t < 34.62: img = clip("hands", (t - 32.52) + 2.2)
    elif t < 39.90: img = zoom(clip("coin", (t - 34.62) * 0.95), 1.0 if t < 38.10 else 1.3, 0.5, 0.42)
    elif t < 43.68: img = grid(t, [1] * PLACES)
    elif t < 47.15: img = zoom(clip("nod", (t - 43.68) % 5.0), punch(t, 43.68, (1.0, 1.0, 1.3, 1.3)), 0.5, 0.2)
    elif t < D0: img = grid(t, [1] * PLACES)
    elif t < END0: img = grid(t, [2 if t >= DROP[k] else 1 for k in range(PLACES)])
    else: return end_card()
    im = overlay(img, t); d = ImageDraw.Draw(im)
    if C0 <= t < C1:                                    # the count: acid numeral, one place at a time
        n = sum(1 for k in range(PLACES) if t >= POP[k])
        d.rectangle([60, 1560, 60 + 560, 1730], fill=rgb(BLACK))
        d.text((78, 1540), f"{n:02d}", font=font(170), fill=rgb(ACID))
        d.text((300, 1600), "PLACES", font=font(74), fill=rgb(PAPER))
    if YS <= t < END0:
        f = font(150); tw = d.textlength("YOUR SPACE", font=f)
        x = (W - tw) / 2
        d.rectangle([x - 40, 760, x + tw + 40, 960], fill=rgb(PINK_DEEP))
        d.text((x, 770), "YOUR SPACE", font=f, fill=rgb(PAPER))
    return im

if __name__ == "__main__":
    if "--still" in sys.argv:
        for ts in sys.argv[sys.argv.index("--still") + 1].split(","):
            frame(float(ts)).save(f"{OUT}_{float(ts):05.2f}.jpg", quality=88)
        sys.exit()
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", TRACK, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR),
                           "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    n = int(DUR * FPS); card = None
    for i in range(n):
        t = i / FPS
        fr = frame(t)
        ff.stdin.write(np.asarray(fr.convert("RGB")).tobytes())
        if i % 150 == 0: print(f"{t:5.1f}s", flush=True)
    ff.stdin.close(); ff.wait(); print("done", OUT)
