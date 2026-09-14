"""Extract the blue logo tile from the Gemini image.
1) Find the tile via its distinctive blue, crop (+shave 1px fringe).
2) Flood-fill the rounded-corner background pockets from the crop corners
   (the cream 'M' is enclosed by blue, so the fill can never reach it).
3) Pad to a square on a transparent canvas."""
import numpy as np
from PIL import Image, ImageDraw

SENTINEL = (255, 0, 255)

src = Image.open("logo-src.jpg").convert("RGB")
arr = np.array(src).astype(int)
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

blue = (b > 120) & (b > r + 60) & (b > g + 40)
ys, xs = np.where(blue)
y0, y1, x0, x1 = ys.min() + 1, ys.max() - 1, xs.min() + 1, xs.max() - 1

tile = src.crop((x0, y0, x1 + 1, y1 + 1))
tw, th = tile.size
print("tile crop:", tile.size)

# Corner background pockets are connected to the crop corners — fill them.
# Seed ONLY from the corners: edge midpoints are blue tile and would eat it.
seeds = [(1, 1), (tw - 2, 1), (1, th - 2), (tw - 2, th - 2)]
for s in seeds:
    px = tile.getpixel(s)
    if px != SENTINEL:
        ImageDraw.floodfill(tile, s, SENTINEL, thresh=60)

arr2 = np.array(tile)
bg = np.all(arr2 == SENTINEL, axis=-1)
alpha = np.where(bg, 0, 255).astype(np.uint8)

out = tile.convert("RGBA")
out.putalpha(Image.fromarray(alpha))

side = max(tw, th) + 24
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(out, ((side - tw) // 2, (side - th) // 2), out)

canvas.save("logo.png")
canvas.resize((512, 512), Image.LANCZOS).save("logo-512-new.png")
print("saved logo.png", canvas.size, "and logo-512-new.png")
