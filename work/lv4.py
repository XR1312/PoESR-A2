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
print("== LEFT VIEW rows (x 400..698) ==")
for y in range(20,290,4):
    r=rr(y,400,698)
    if r: print(y,r)
