import numpy as np
from PIL import Image
import sys

def render(path, cols=120, crop=None, thresh=140, aspect=2.0):
    im = Image.open(path).convert('L')
    if crop:
        im = im.crop(crop)
    a = np.array(im) < thresh
    H, W = a.shape
    cw = max(1.0, W / cols)
    ch = cw * aspect
    rows = max(1, int(H / ch))
    lines = []
    for r in range(rows):
        y0, y1 = int(r * ch), max(int(r * ch) + 1, int((r + 1) * ch))
        line = []
        for c in range(cols):
            x0, x1 = int(c * cw), max(int(c * cw) + 1, int((c + 1) * cw))
            blk = a[y0:y1, x0:x1]
            line.append('#' if blk.any() else '.')
        lines.append(''.join(line))
    # header with pixel coordinates: mark every 10th column
    hdr = [' '] * cols
    for c in range(0, cols, 10):
        lab = str(int(c * cw))
        for i, chx in enumerate(lab):
            if c + i < cols:
                hdr[c + i] = chx
    out = [''.join(hdr)]
    for r, ln in enumerate(lines):
        out.append('%4d %s' % (int(r * ch), ln))
    return '\n'.join(out)

if __name__ == '__main__':
    path = sys.argv[1]
    cols = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    crop = None
    if len(sys.argv) > 6:
        crop = tuple(int(v) for v in sys.argv[3:7])
    elif len(sys.argv) > 3:
        crop = tuple(int(v) for v in sys.argv[3:7]) if len(sys.argv) >= 7 else None
    print(render(path, cols, crop))
