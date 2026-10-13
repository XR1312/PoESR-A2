import numpy as np, sys
from PIL import Image
_cache = {}
def img(path):
    if path not in _cache: _cache[path] = np.array(Image.open(path).convert('L')).astype(float)
    return _cache[path]
def prof(path, p0, p1, band=2.0, thresh=150, minpix=1):
    """Sample along segment p0->p1; at each step take the min gray over a perpendicular band."""
    a = img(path); H, W = a.shape
    x0, y0 = p0; x1, y1 = p1
    L = int(np.hypot(x1-x0, y1-y0))
    ux, uy = (x1-x0)/max(L,1), (y1-y0)/max(L,1)
    nx, ny = -uy, ux
    vals = []
    for i in range(L+1):
        cx, cy = x0+ux*i, y0+uy*i
        best = 255
        for t in np.arange(-band, band+0.25, 0.5):
            xx, yy = cx+nx*t, cy+ny*t
            ix, iy = int(round(xx)), int(round(yy))
            if 0 <= ix < W and 0 <= iy < H: best = min(best, a[iy, ix])
        vals.append(best)
    return vals
def runs_from(vals, thresh=150):
    out = []; s = None
    for i, v in enumerate(vals):
        if v < thresh and s is None: s = i
        elif v >= thresh and s is not None: out.append((s, i-1)); s = None
    if s is not None: out.append((s, len(vals)-1))
    return out
def report(name, path, p0, p1, band=2.0, thresh=150):
    v = prof(path, p0, p1, band, thresh)
    r = runs_from(v, thresh)
    L = len(v)-1
    print('%s: len=%d ngaps=%d' % (name, L, len(r)-1))
    print('   runs:', ' '.join('%d-%d(%d)' % (a, b, b-a+1) for a, b in r))
