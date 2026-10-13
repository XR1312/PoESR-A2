"""Annotate a raster drawing with a labelled coordinate grid + detected segments."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from detect import detect, merge_collinear

path = sys.argv[1]
name = sys.argv[2]
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.6
step = int(sys.argv[4]) if len(sys.argv) > 4 else 50

segs, sk = detect(path)
segs = merge_collinear(segs)
im = Image.open(path).convert('RGB')
W, H = im.size
im = im.point(lambda v: 255 - (255 - v) // 3)  # lighten original artwork
im = im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 14)
except Exception:
    font = ImageFont.load_default()

for gx in range(0, W, step):
    d.line([(gx * scale, 0), (gx * scale, H * scale)], fill=(200, 220, 255), width=1)
for gy in range(0, H, step):
    d.line([(0, gy * scale), (W * scale, gy * scale)], fill=(200, 220, 255), width=1)
for gx in range(0, W, step):
    for gy in range(0, H, step):
        if (gx // step) % 2 == 0 and (gy // step) % 2 == 0:
            d.text((gx * scale + 2, gy * scale + 2), f'{gx},{gy}', fill=(255, 120, 120), font=font)

for i, ((x0, y0), (x1, y1)) in enumerate(segs):
    d.line([(x0 * scale, y0 * scale), (x1 * scale, y1 * scale)], fill=(0, 150, 0), width=2)
    d.ellipse([x0 * scale - 3, y0 * scale - 3, x0 * scale + 3, y0 * scale + 3], fill=(255, 0, 0))
    d.ellipse([x1 * scale - 3, y1 * scale - 3, x1 * scale + 3, y1 * scale + 3], fill=(0, 0, 255))
    mx, my = (x0 + x1) / 2 * scale, (y0 + y1) / 2 * scale
    d.text((mx + 4, my + 4), str(i), fill=(180, 0, 180), font=font)

im.save(f'ann-{name}.png')
print(f'ann-{name}.png', im.size, len(segs), 'segments')
for i, ((x0, y0), (x1, y1)) in enumerate(segs):
    print(f'  [{i:2d}] ({x0:7.1f},{y0:7.1f}) -> ({x1:7.1f},{y1:7.1f})   len={np.hypot(x1-x0,y1-y0):7.1f}')
