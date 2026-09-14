"""Render the Moor Builds logo to a high-res PNG (no external deps beyond PIL+numpy)."""
import numpy as np
from PIL import Image, ImageDraw

S = 1024
SCALE = S / 48.0

def sc(v):
    return v * SCALE

# Diagonal gradient tile colours
c0 = np.array([0x1F, 0x4B, 0xA8], dtype=float)
c1 = np.array([0x2E, 0x63, 0xD6], dtype=float)

yy, xx = np.mgrid[0:S, 0:S]
t = ((xx + yy) / (2.0 * S))[..., None]
grad = (c0 * (1 - t) + c1 * t).astype(np.uint8)
img = Image.fromarray(grad, "RGB")

# Rounded-corner mask
mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([sc(2), sc(2), sc(46), sc(46)], radius=sc(12), fill=255)
bg = Image.new("RGB", (S, S), (0, 0, 0))
img = Image.composite(img, bg, mask).convert("RGBA")
img.putalpha(mask)

d = ImageDraw.Draw(img)

# Cream "M" — same path as the SVG: M14 33 V16 L24 27 L34 16 V33
pts = [(sc(14), sc(33)), (sc(14), sc(16)), (sc(24), sc(27)), (sc(34), sc(16)), (sc(34), sc(33))]
cream = (0xFB, 0xFA, 0xF5, 255)
w = int(round(sc(4.4)))
d.line(pts, fill=cream, width=w, joint="curve")
r = w / 2
for (px, py) in pts:  # round caps + joints
    d.ellipse([px - r, py - r, px + r, py + r], fill=cream)

# Amber dot
cx, cy, dr = sc(34.5), sc(11), sc(3.2)
d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=(0xF5, 0xA6, 0x23, 255))

img.save("logo-1024.png")
img.resize((512, 512), Image.LANCZOS).save("logo-512.png")
print("saved logo-1024.png and logo-512.png")
