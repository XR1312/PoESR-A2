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
print("FRONT x[0,345] rows 76..88")
for y in range(76,89): print(y, rr(y,0,345))
print("LEFT x[400,698] rows 108..116")
for y in range(108,117): print(y, rr(y,400,698))
print("LEFT x[400,698] rows 213..223")
for y in range(213,224): print(y, rr(y,400,698))
print("LEFT x[400,698] rows 26..34")
for y in range(26,35): print(y, rr(y,400,698))
