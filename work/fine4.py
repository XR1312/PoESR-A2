import numpy as np
from PIL import Image
a = np.array(Image.open('img-119.jpg').convert('L')).astype(int)
ink = a < 160
def grp(idx, gap=2, minlen=1):
    if len(idx)==0: return []
    g=[];s=idx[0];p=idx[0]
    for v in idx[1:]:
        if v<=p+gap: p=v
        else: g.append((s,p)); s=v; p=v
    g.append((s,p))
    return [(int(s),int(e)) for s,e in g if e-s+1>=minlen]
def rr(y,x0,x1,gap=2,ml=1):
    return grp(np.nonzero(ink[y,x0:x1])[0]+x0,gap,ml)
for y in list(range(20,36))+list(range(106,118))+list(range(213,222))+list(range(266,276)):
    print(y, rr(y,0,340))
