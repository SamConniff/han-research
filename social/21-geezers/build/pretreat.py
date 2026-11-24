"""Run the brand treatment over a clip and store 1080x1920 JPEG frames (plus masks for the clone source)."""
import sys, os, numpy as np, cv2, treat
src, out = sys.argv[1], sys.argv[2]
seg = "--noseg" not in sys.argv; parts = "--parts" in sys.argv
os.makedirs(out, exist_ok=True)
cap = cv2.VideoCapture(src); i = 0
while True:
    ok, fr = cap.read()
    if not ok: break
    rgb = fr[..., ::-1].copy()
    if parts:
        o, pm, nm = treat.treat(rgb, return_parts=True)
        cv2.imwrite(f"{out}/src{i:04d}.jpg", treat.cover(rgb)[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95])
        cv2.imwrite(f"{out}/pm{i:04d}.png", (pm * 255).astype(np.uint8))
    else:
        o = treat.treat(rgb, use_seg=seg)
    cv2.imwrite(f"{out}/f{i:04d}.jpg", o[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 92]); i += 1
print(src, i, "frames", cap.get(cv2.CAP_PROP_FPS))
