"""Brand treatment: B&W man, rhodamine halftone ground, nails keep their own colour."""
import numpy as np, cv2
from rembg import new_session, remove
from PIL import Image

W, H = 1080, 1920
BLACK = np.array([10, 7, 9], np.float32)
PINK = np.array([230, 0, 126], np.float32)
PINK_DEEP = np.array([200, 0, 109], np.float32)
ACID = np.array([228, 255, 61], np.float32)
PAPER = np.array([243, 236, 239], np.float32)
_sess = None
SEG_MODEL = "isnet-general-use"

def screen(w, h, pitch, angle=45.0):
    """Distance (0..~0.71) from each pixel to the nearest dot centre of a rotated screen."""
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    a = np.deg2rad(angle)
    u = (x * np.cos(a) + y * np.sin(a)) / pitch
    v = (-x * np.sin(a) + y * np.cos(a)) / pitch
    return np.hypot(u - np.round(u), v - np.round(v))

_SCR = {}
def dots(lum, pitch, w, h, angle=45.0):
    """lum 0..1 -> coverage map 0..1 of dots whose area tracks lum."""
    k = (w, h, pitch, angle)
    if k not in _SCR: _SCR[k] = screen(w, h, pitch, angle)
    r = 0.72 * np.sqrt(np.clip(lum, 0, 1))
    return np.clip((r - _SCR[k]) * pitch / 1.5 + 0.5, 0, 1)

def cover(img, w=W, h=H):
    ih, iw = img.shape[:2]
    s = max(w / iw, h / ih)
    r = cv2.resize(img, (int(round(iw * s)), int(round(ih * s))), interpolation=cv2.INTER_CUBIC)
    y0 = (r.shape[0] - h) // 2; x0 = (r.shape[1] - w) // 2
    return r[y0:y0 + h, x0:x0 + w]

def person_mask(rgb):
    """Union of a general and a human matting model, with enclosed holes filled."""
    global _sess
    if _sess is None: _sess = [new_session("isnet-general-use"), new_session("u2net_human_seg")]
    small = Image.fromarray(cv2.resize(rgb, (576, 1024), interpolation=cv2.INTER_AREA))
    m = np.zeros((1024, 576), np.float32)
    for s_ in _sess:
        m = np.maximum(m, np.asarray(remove(small, session=s_, only_mask=True)).astype(np.float32) / 255)
    b = (m > 0.5).astype(np.uint8)
    b = cv2.morphologyEx(b, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    ff = np.pad(b, 1).copy(); cv2.floodFill(ff, None, (0, 0), 2)
    b = (ff[1:-1, 1:-1] != 2).astype(np.float32)          # anything not reachable from the border is the man
    m = cv2.resize(b, (rgb.shape[1], rgb.shape[0]), interpolation=cv2.INTER_CUBIC)
    return np.clip((cv2.GaussianBlur(m, (0, 0), 2) - 0.5) * 6 + 0.5, 0, 1)

def nail_mask(rgb):
    f = rgb.astype(np.float32)
    mx, mn = f.max(2), f.min(2)
    chroma = mx - mn
    m = ((chroma > 55) & (chroma / (mx + 1) > 0.33)).astype(np.float32)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.dilate(m, np.ones((3, 3), np.uint8))
    return cv2.GaussianBlur(m, (0, 0), 1.2)

def shift_hue(rgb, deg):
    if deg == 0: return rgb
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV_FULL).astype(np.int16)
    hsv[..., 0] = (hsv[..., 0] + int(deg / 360 * 255)) % 256
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB_FULL)

def man_plate(rgb):
    """High-contrast black plate with a light visible screen in the mid-tones."""
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    g = np.clip((g - 0.06) / 0.86, 0, 1)
    g = g * g * (3 - 2 * g) * 0.65 + g * 0.35
    h, w = g.shape
    d = dots(1 - g, 9, w, h, 15)          # black dots, bigger in shadow
    ht = 1 - d
    out = 0.72 * g + 0.28 * ht * (0.35 + 0.65 * g)
    return np.clip(out, 0, 1)

def ground(lum, pitch=26):
    """Black ground with rhodamine dots sized by lum."""
    h, w = lum.shape
    d = dots(lum, pitch, w, h)[..., None]
    return BLACK * (1 - d) + PINK * d

def treat(rgb, use_seg=True, hue=0, bg_gain=1.0, pitch=26, return_parts=False):
    rgb = cover(rgb)
    nm = nail_mask(rgb)[..., None]
    plate = man_plate(rgb)[..., None]
    man = BLACK + (PAPER - BLACK) * plate
    f = rgb.astype(np.float32)
    # nails: the real pixels, hue optionally rotated per clone, saturation lifted
    nails = shift_hue(rgb, hue).astype(np.float32)
    grey = nails.mean(2, keepdims=True)
    nails = np.clip(grey + (nails - grey) * 1.25, 0, 255)
    man = man * (1 - nm) + nails * nm
    if use_seg:
        pm = person_mask(rgb)
        pm = np.maximum(pm, nm[..., 0])[..., None]
        lum = cv2.GaussianBlur(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY), (0, 0), 14).astype(np.float32) / 255
        lum = np.clip((lum - 0.12) * 1.3 * bg_gain, 0, 0.6)
        out = ground(lum, pitch) * (1 - pm) + man * pm
    else:
        pm = np.ones(rgb.shape[:2] + (1,), np.float32); out = man
    out = np.clip(out, 0, 255).astype(np.uint8)
    if return_parts: return out, pm[..., 0], nm[..., 0]
    return out

if __name__ == "__main__":
    import sys
    for p in sys.argv[2:]:
        im = np.asarray(Image.open(p).convert("RGB"))
        Image.fromarray(treat(im)).save(f"{sys.argv[1]}/t_{p.split('/')[-1].split('.')[0]}.jpg", quality=90)
