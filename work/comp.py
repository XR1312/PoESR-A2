import numpy as np, sys
from PIL import Image
from collections import deque

def comps(path, thresh=160, minpix=8, crop=None):
    im = Image.open(path).convert('L')
    if crop: im = im.crop(crop)
    a = np.array(im) < thresh
    H, W = a.shape
    lab = np.zeros((H, W), np.int32); cur = 0; out = []
    for y in range(H):
        for x in range(W):
            if a[y, x] and lab[y, x] == 0:
                cur += 1; q = deque([(y, x)]); lab[y, x] = cur
                pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy+dy, cx+dx
                            if 0 <= ny < H and 0 <= nx < W and a[ny, nx] and lab[ny, nx] == 0:
                                lab[ny, nx] = cur; q.append((ny, nx))
                if len(pts) >= minpix:
                    arr = np.array(pts); y0, x0 = arr.min(0); y1, x1 = arr.max(0)
                    out.append(dict(id=cur, n=len(pts), bbox=(x0, y0, x1, y1), m=lab == cur, arr=arr))
    return out, (W, H)

def thumb(c, cols=56, aspect=2.0):
    x0, y0, x1, y1 = c['bbox']; w = max(1, x1-x0+1); h = max(1, y1-y0+1)
    cw = max(1.0, w/cols); ch = cw*aspect; rows = max(1, int(h/ch))
    m = c['m']; lines = []
    for r in range(rows):
        yy0, yy1 = y0+int(r*ch), max(y0+int(r*ch)+1, y0+int((r+1)*ch))
        line = ''
        for cc in range(cols):
            xx0, xx1 = x0+int(cc*cw), max(x0+int(cc*cw)+1, x0+int((cc+1)*cw))
            line += '#' if m[yy0:yy1, xx0:xx1].any() else '.'
        lines.append(line)
    return lines

if __name__ == '__main__':
    path = sys.argv[1]; thresh = int(sys.argv[2]) if len(sys.argv) > 2 else 160
    cs, (W, H) = comps(path, thresh)
    cs.sort(key=lambda c: -c['n'])
    print('image', W, H, 'components', len(cs))
    for c in cs[:int(sys.argv[3]) if len(sys.argv) > 3 else 12]:
        x0, y0, x1, y1 = c['bbox']
        print('--- id%d npix=%d bbox x %d-%d y %d-%d (w%d h%d)' % (c['id'], c['n'], x0, x1, y0, y1, x1-x0+1, y1-y0+1))
        for ln in thumb(c): print('   ', ln)
