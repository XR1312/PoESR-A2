import numpy as np
from PIL import Image
import sys

def runs(path, thresh=140, crop=None):
    im = Image.open(path).convert('L')
    if crop:
        im = im.crop(crop)
    a = np.array(im) < thresh
    off = (crop[0], crop[1]) if crop else (0, 0)
    out = []
    for y in range(a.shape[0]):
        row = a[y]
        idx = np.nonzero(row)[0]
        if len(idx) == 0:
            continue
        # group consecutive
        groups = []
        s = idx[0]
        p = idx[0]
        for v in idx[1:]:
            if v == p + 1:
                p = v
            else:
                groups.append((s, p))
                s = v
                p = v
        groups.append((s, p))
        out.append((y + off[1], [(g[0] + off[0], g[1] + off[0]) for g in groups]))
    return out

if __name__ == '__main__':
    path = sys.argv[1]
    crop = tuple(int(v) for v in sys.argv[2:6]) if len(sys.argv) >= 6 else None
    step = int(sys.argv[6]) if len(sys.argv) >= 7 else 1
    for y, g in runs(path, crop=crop):
        if y % step:
            continue
        print(y, ' '.join('%d-%d' % t if t[0] != t[1] else '%d' % t[0] for t in g))
