import numpy as np
from PIL import Image

_cache = {}

def ink(path, thresh=140):
    key = (path, thresh)
    if key not in _cache:
        _cache[key] = np.array(Image.open(path).convert('L')) < thresh
    return _cache[key]

def fit_line(path, p0, p1, width=3.0, trim=6.0, thresh=140):
    """Fit a straight line to ink pixels near segment p0-p1.
    Returns (point, unit_direction, npts, rms)."""
    a = ink(path, thresh)
    x0, y0 = p0
    x1, y1 = p1
    L = np.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    ys, xs = np.nonzero(a)
    # keep pixels inside bounding box + margin
    m = 8
    sel = (xs >= min(x0, x1) - m) & (xs <= max(x0, x1) + m) & (ys >= min(y0, y1) - m) & (ys <= max(y0, y1) + m)
    xs, ys = xs[sel], ys[sel]
    dx, dy = xs - x0, ys - y0
    t = dx * ux + dy * uy
    d = dx * nx + dy * ny
    keep = (np.abs(d) <= width) & (t >= trim) & (t <= L - trim)
    xs, ys, t, d = xs[keep], ys[keep], t[keep], d[keep]
    if len(xs) < 5:
        return None
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    Q = P - c
    _, s, V = np.linalg.svd(Q, full_matrices=False)
    dirv = V[0]
    if dirv @ np.array([ux, uy]) < 0:
        dirv = -dirv
    resid = np.abs(Q @ V[1])
    return dict(p=c, d=dirv, n=len(xs), rms=float(np.sqrt((resid ** 2).mean())),
                tmin=float(t.min()), tmax=float(t.max()))

def isect(L1, L2):
    """Intersection of two fitted lines."""
    p1, d1 = L1['p'], L1['d']
    p2, d2 = L2['p'], L2['d']
    A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
    b = p2 - p1
    s, t = np.linalg.solve(A, b)
    return p1 + s * d1

def show(name, L):
    if L is None:
        print('  %-22s FAILED' % name)
        return
    print('  %-22s p=(%.2f,%.2f) d=(%.4f,%.4f) n=%4d rms=%.2f t=[%.1f,%.1f]'
          % (name, L['p'][0], L['p'][1], L['d'][0], L['d'][1], L['n'], L['rms'], L['tmin'], L['tmax']))
