import numpy as np
from PIL import Image
a = np.array(Image.open('img-119.jpg').convert('L')).astype(int)
ink = a < 160

def hline(y0,x0,x1,band=1):
    seg = ink[y0-band:y0+band+1, x0:x1].any(axis=0)
    out=[];cur=seg[0];start=0
    for i,v in enumerate(seg):
        if v!=cur:
            out.append(('#' if cur else '.', int(i-start))); cur=v; start=i
    out.append(('#' if cur else '.', int(len(seg)-start)))
    print(f"y={y0} x[{x0},{x1}]", ' '.join(f"{c}{n}" for c,n in out))

def vline(x0,y0,y1,band=1):
    seg = ink[y0:y1, x0-band:x0+band+1].any(axis=1)
    out=[];cur=seg[0];start=0
    for i,v in enumerate(seg):
        if v!=cur:
            out.append(('#' if cur else '.', int(i-start))); cur=v; start=i
    out.append(('#' if cur else '.', int(len(seg)-start)))
    print(f"x={x0} y[{y0},{y1}]", ' '.join(f"{c}{n}" for c,n in out))

print("--- FRONT VIEW ---")
hline(218,21,210); hline(270,206,325); hline(29,250,325); hline(112,139,254)
vline(22,183,220); vline(208,110,272); vline(252,27,114); vline(323,26,272)
print("--- LEFT VIEW circles: sample along angle ---")
cy,cx,R = 149.4,545.5,120.6
import math
for R,name in ((120.6,'outer'),(69.0,'inner')):
    vals=[]
    for k in range(720):
        th=k*math.pi/360
        x=cx+R*math.cos(th); y=cy+R*math.sin(th)
        xi,yi=int(round(x)),int(round(y))
        vals.append(1 if ink[max(0,yi-1):yi+2, max(0,xi-1):xi+2].any() else 0)
    out=[];cur=vals[0];start=0
    for i,v in enumerate(vals):
        if v!=cur:
            out.append(('#' if cur else '.', i-start)); cur=v; start=i
    out.append(('#' if cur else '.', len(vals)-start))
    print(name, 'deg-runs:', ' '.join(f"{c}{n}" for c,n in out))
