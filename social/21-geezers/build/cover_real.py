"""Cover from a real frame of Sam: he is black and white, the necklace bottles keep their colours.
Usage: python3 cover_real.py <necklace_photo.png> <out.jpg> [out.png]"""
import sys, cv2, numpy as np
import treat as T
from treat import W, H, BLACK, PINK, ACID, PAPER
from PIL import Image, ImageDraw, ImageFont
def font(size, w=900):
    f = ImageFont.truetype("intertight-latin.ttf", size); f.set_variation_by_axes([w]); return f
rgb = lambda a: tuple(int(v) for v in a)
src = np.asarray(Image.open(sys.argv[1]).convert("RGB"))
out, pm, _ = T.treat(src, return_parts=True, nails=False, flat_bg=0.42)       # the real Sam, fully black and white
c = T.cover(src).astype(np.float32)
mx, mn = c.max(2), c.min(2); ch = mx - mn                                      # bottles: strongly saturated, on his chest only
key = ((ch > 95) & (ch / (mx + 1) > 0.5)).astype(np.uint8)
box = np.zeros_like(key); box[int(0.60 * H):int(0.87 * H), int(0.18 * W):int(0.64 * W)] = 1; key &= box
key = cv2.dilate(cv2.morphologyEx(key, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)), np.ones((3, 3), np.uint8))
bm = cv2.GaussianBlur(key.astype(np.float32), (0, 0), 1.2)[..., None]
grey = c.mean(2, keepdims=True); man = out.astype(np.float32) * (1 - bm) + np.clip(grey + (c - grey) * 1.25, 0, 255) * bm
DY = 75; canvas = T.ground(np.full((H, W), 0.42, np.float32)); a = np.maximum(pm, bm[..., 0])[..., None]
canvas[DY:] = canvas[DY:] * (1 - a[:H - DY]) + man[:H - DY] * a[:H - DY]
im = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
def fit(text, width, cap):
    lo, hi = 30, cap
    while hi - lo > 2:
        m = (lo + hi) // 2
        if d.textlength(text, font=font(m)) <= width: lo = m
        else: hi = m
    return lo
top = "THE SO SOLID SCIENCE REMIX"; s = fit(top, 900, 70); w = d.textlength(top, font=font(s))
d.rectangle([60, 290, 60 + w + 48, 290 + int(s * 1.15)], fill=rgb(ACID)); d.text((84, 290), top, font=font(s), fill=rgb(BLACK))
rows = [[("I'VE GOT ", PAPER), ("21 SPACES", ACID)], [("TO MAKE THE", PAPER)], [("SCIENCE ", PAPER), ("FLOW", PINK)]]
sizes = [fit("".join(t for t, _ in r), 940, 126) for r in rows]; hs = [int(z * 0.96) for z in sizes]; y = 290 + int(s * 1.15) + 12
for r, z, h in zip(rows, sizes, hs):
    tw = d.textlength("".join(t for t, _ in r), font=font(z)); d.rectangle([50, y, 50 + tw + 40, y + h], fill=rgb(BLACK)); x = 70
    for t, colr in r: d.text((x, y - int(z * 0.13)), t, font=font(z), fill=rgb(colr)); x += d.textlength(t, font=font(z))
    y += h
print("type ends at y", y)
im.save(sys.argv[2], quality=93)
if len(sys.argv) > 3: im.save(sys.argv[3])
