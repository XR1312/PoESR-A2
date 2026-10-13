"""Line-segment detection for clean black-on-white engineering drawings.

Pipeline: binarize -> Zhang-Suen thinning -> graph trace -> polyline fit.
"""
import numpy as np
from PIL import Image


def binarize(path, thresh=128):
    im = Image.open(path).convert('L')
    a = np.array(im)
    return (a < thresh)


def thin(img):
    """Zhang-Suen thinning."""
    img = img.copy().astype(np.uint8)
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            P = np.pad(img, 1)
            p2 = P[0:-2, 1:-1]
            p3 = P[0:-2, 2:]
            p4 = P[1:-1, 2:]
            p5 = P[2:, 2:]
            p6 = P[2:, 1:-1]
            p7 = P[2:, 0:-2]
            p8 = P[1:-1, 0:-2]
            p9 = P[0:-2, 0:-2]
            B = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
            seq = [p2, p3, p4, p5, p6, p7, p8, p9, p2]
            A = sum(((seq[i] == 0) & (seq[i + 1] == 1)).astype(np.uint8) for i in range(8))
            if step == 0:
                cond = (img == 1) & (B >= 2) & (B <= 6) & (A == 1) & \
                       ((p2 * p4 * p6) == 0) & ((p4 * p6 * p8) == 0)
            else:
                cond = (img == 1) & (B >= 2) & (B <= 6) & (A == 1) & \
                       ((p2 * p4 * p8) == 0) & ((p2 * p6 * p8) == 0)
            if cond.any():
                img[cond] = 0
                changed = True
    return img.astype(bool)


NB = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def neighbors(sk, r, c):
    H, W = sk.shape
    out = []
    for dr, dc in NB:
        rr, cc = r + dr, c + dc
        if 0 <= rr < H and 0 <= cc < W and sk[rr, cc]:
            out.append((rr, cc))
    return out


def trace(sk, min_len=12):
    """Trace skeleton into polylines between endpoints/junctions."""
    H, W = sk.shape
    deg = np.zeros((H, W), dtype=int)
    pts = np.argwhere(sk)
    for r, c in pts:
        deg[r, c] = len(neighbors(sk, r, c))

    nodes = set(map(tuple, np.argwhere(sk & (deg != 2))))
    visited_edges = set()
    polylines = []

    def walk(start, nxt):
        path = [start, nxt]
        prev, cur = start, nxt
        while True:
            if cur in nodes:
                break
            nbs = [p for p in neighbors(sk, *cur) if p != prev]
            if len(nbs) != 1:
                break
            prev, cur = cur, nbs[0]
            path.append(cur)
            if len(path) > 20000:
                break
        return path

    for n in nodes:
        for nb in neighbors(sk, *n):
            ekey = (n, nb)
            if ekey in visited_edges:
                continue
            path = walk(n, nb)
            visited_edges.add((n, nb))
            visited_edges.add((path[-1], path[-2]))
            if len(path) >= min_len:
                polylines.append(path)

    # isolated loops (no nodes)
    if not nodes:
        for r, c in pts:
            if sk[r, c]:
                path = walk((r, c), neighbors(sk, r, c)[0])
                if len(path) >= min_len:
                    polylines.append(path)
                break
    return polylines


def rdp(points, eps=1.5):
    """Ramer-Douglas-Peucker simplification."""
    if len(points) < 3:
        return points
    p0, p1 = np.array(points[0], float), np.array(points[-1], float)
    d = p1 - p0
    L = np.hypot(*d)
    if L == 0:
        dists = [np.hypot(*(np.array(p, float) - p0)) for p in points]
    else:
        n = np.array([-d[1], d[0]]) / L
        dists = [abs(np.dot(np.array(p, float) - p0, n)) for p in points]
    i = int(np.argmax(dists))
    if dists[i] > eps:
        left = rdp(points[:i + 1], eps)
        right = rdp(points[i:], eps)
        return left[:-1] + right
    return [points[0], points[-1]]


def segments(path, eps=1.5):
    """Return list of straight segments as ((x0,y0),(x1,y1)) in (x=col, y=row)."""
    pl = rdp([(c, r) for r, c in path], eps)
    # merge nearly-collinear consecutive pieces
    out = []
    for i in range(len(pl) - 1):
        (x0, y0), (x1, y1) = pl[i], pl[i + 1]
        if np.hypot(x1 - x0, y1 - y0) >= 3:
            out.append(((x0, y0), (x1, y1)))
    return out


def detect(path, thresh=128, eps=1.5, min_len=12):
    b = binarize(path, thresh)
    sk = thin(b)
    pls = trace(sk, min_len)
    segs = []
    for p in pls:
        segs.extend(segments(p, eps))
    return segs, sk


def merge_collinear(segs, ang_tol=2.0, dist_tol=3.0):
    """Merge segments that are collinear and touching/overlapping."""
    import math
    segs = [list(s) for s in segs]
    changed = True
    while changed:
        changed = False
        for i in range(len(segs)):
            for j in range(i + 1, len(segs)):
                a, b = segs[i], segs[j]
                (x1, y1), (x2, y2) = a
                (x3, y3), (x4, y4) = b
                d1 = np.array([x2 - x1, y2 - y1], float)
                d2 = np.array([x4 - x3, y4 - y3], float)
                n1, n2 = np.linalg.norm(d1), np.linalg.norm(d2)
                if n1 < 1e-9 or n2 < 1e-9:
                    continue
                ang = math.degrees(math.acos(min(1, abs(np.dot(d1, d2) / (n1 * n2)))))
                if ang > ang_tol:
                    continue
                # distance from b's endpoints to line a
                nrm = np.array([-d1[1], d1[0]]) / n1
                dA = [abs(np.dot(np.array([x, y], float) - np.array([x1, y1]), nrm))
                      for (x, y) in [(x3, y3), (x4, y4)]]
                if max(dA) > dist_tol:
                    continue
                # project all 4 points on direction, take extremes
                t = lambda p: np.dot(np.array(p, float) - np.array([x1, y1]), d1) / n1
                cand = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                cand.sort(key=t)
                segs[i] = [cand[0], cand[-1]]
                segs.pop(j)
                changed = True
                break
            if changed:
                break
    return [tuple(s) for s in segs]


def dump(path, name, **kw):
    segs, sk = detect(path, **kw)
    segs = merge_collinear(segs)
    print(f'### {name}: {len(segs)} segments')
    for (x0, y0), (x1, y1) in sorted(segs, key=lambda s: (round(s[0][1] / 10), s[0][0])):
        print(f'  ({x0:7.1f},{y0:7.1f}) -> ({x1:7.1f},{y1:7.1f})   len={np.hypot(x1-x0,y1-y0):7.1f}')
    return segs


if __name__ == '__main__':
    import sys
    dump(sys.argv[1], sys.argv[1])
