import numpy as np
from PIL import Image
a = np.array(Image.open('img-119.jpg').convert('L')).astype(int)
ink = a < 160

def grp(idx, gap=2, minlen=3):
    if len(idx)==0: return []
    g=[];s=idx[0];p=idx[0]
    for v in idx[1:]:
        if v<=p+gap: p=v
        else: g.append((s,p)); s=v; p=v
    g.append((s,p))
    return [(int(s),int(e)) for s,e in g if e-s+1>=minlen]

def rr(y,x0,x1,gap=2,ml=3):
    xs=np.nonzero(ink[y,x0:x1])[0]+x0
    return grp(xs,gap,ml)
def cr(x,y0,y1,gap=2,ml=3):
    ys=np.nonzero(ink[y0:y1,x])[0]+y0
    return grp(ys,gap,ml)

print("== ROWS (front view x0..340) ==")
for y in range(10,300,4):
    r=rr(y,0,340)
    if r: print(y,r)
print("== COLS (front view y0..300) ==")
for x in range(16,344,4):
    c=cr(x,0,300)
    if c: print(x,c)
