import numpy as np
from PIL import Image
im = Image.open('/Users/XR1312/Desktop/工表-2/work/img-059.jpg').convert('L')
g = np.array(im).astype(float); H,W=g.shape
ink = g<150
SEG=[  # (x0,y0,x1,y1,halfwidth)
 (100,46,100,206,1.2),      # V-a thin
 (100,44,403,159,2.4),      # V-b thick
 (196,1,488,149,2.4),       # V-c
 (196,122,488,152,2.4),     # V-d
 (193,2,193,126,2.4),       # V-e upper thick
 (193,126,193,206,1.2),     # V-e lower thin
 (401.5,156,401.5,206,1.2), # V-f
 (486,149,486,206,1.2),     # V-g
 (100,206,100,283,1.2),     # h1 thin
 (100,283,100,441,2.4),     # h1 thick
 (193,206,193,246,1.2),     # h2 thin
 (193,246,193,285,2.4),     # h2 thick
 (401.5,206,401.5,283,1.2), # h3 upper thin
 (401.5,283,401.5,346,2.4), # h3 mid thick
 (401.5,391,401.5,441,2.4), # h3 lower thick
 (486,206,486,394,1.2),     # h4
 (100,283,196,283,2.4),     # h5 left
 (256,283,403,283,2.4),     # h5 right
 (100,439.5,403,439.5,2.4), # h6
 (400,393,487,393,2.4),     # h7
 (194,246,486,393,2.4),     # h8
 (0,206.5,537,206.5,1.2),   # axis
]
yy,xx=np.mgrid[0:H,0:W]
expl=np.zeros((H,W),bool)
for (x0,y0,x1,y1,hw) in SEG:
    dx,dy=x1-x0,y1-y0; L2=dx*dx+dy*dy
    t=np.clip(((xx-x0)*dx+(yy-y0)*dy)/L2,0,1)
    d=np.hypot(xx-(x0+t*dx), yy-(y0+t*dy))
    expl |= (d<=hw+0.6)
# also explain the axis band
resid = ink & ~expl
print('total ink',ink.sum(),'unexplained',resid.sum())
seen=np.zeros_like(resid,bool); comps=[]
ys,xs=np.nonzero(resid)
pts=list(zip(xs.tolist(),ys.tolist()))
for x,y in pts:
    if seen[y,x]: continue
    st=[(x,y)]; seen[y,x]=True; comp=[]
    while st:
        cx,cy=st.pop(); comp.append((cx,cy))
        for ddx in(-1,0,1):
            for ddy in(-1,0,1):
                nx,ny=cx+ddx,cy+ddy
                if 0<=nx<W and 0<=ny<H and resid[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx]=True; st.append((nx,ny))
    if len(comp)>=12:
        a=np.array(comp)
        comps.append((len(comp),a[:,0].min(),a[:,0].max(),a[:,1].min(),a[:,1].max()))
comps.sort(reverse=True)
print('%-7s %-13s %-13s'%('px','xrange','yrange'))
for c in comps[:25]:
    print('%-7d %5d..%-6d %5d..%-6d'%(c[0],c[1],c[2],c[3],c[4]))
