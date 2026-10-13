import numpy as np
from PIL import Image
g = np.array(Image.open('/Users/XR1312/Desktop/工表-2/work/img-059.jpg').convert('L')).astype(float)
H,W = g.shape
def samp(x,y):
    x=max(0.0,min(W-1.001,x)); y=max(0.0,min(H-1.001,y))
    x0,y0=int(x),int(y); fx,fy=x-x0,y-y0
    return (g[y0,x0]*(1-fx)*(1-fy)+g[y0,x0+1]*fx*(1-fy)
            +g[y0+1,x0]*(1-fx)*fy+g[y0+1,x0+1]*fx*fy)
def prof(p0,p1,n=60,half=6):
    (x0,y0),(x1,y1)=p0,p1
    L=np.hypot(x1-x0,y1-y0)
    if L<1e-6: return [],[]
    ux,uy=(x1-x0)/L,(y1-y0)/L; nx,ny=-uy,ux
    w=[];mn=[]
    for t in np.linspace(0.02,0.98,n):
        cx,cy=x0+t*(x1-x0), y0+t*(y1-y0)
        ks=np.arange(-half,half+0.001,0.2)
        vals=np.array([samp(cx+k*nx,cy+k*ny) for k in ks])
        w.append((255.0-vals).sum()/255.0*(0.2))
        mn.append(vals.min())
    return np.array(w),np.array(mn)
SEG={
 'V-a':((100,46),(100,204)),
 'V-b':((103,46),(400,157)),
 'V-c':((199,4),(485,147)),
 'V-d':((199,124),(485,150)),
 'V-e-up':((193,5),(193,124)),
 'V-e-lo':((193,128),(193,204)),
 'V-f':((401.5,158),(401.5,204)),
 'V-g':((486,151),(486,204)),
 'h1-up':((100,209),(100,281)),
 'h1-lo':((100,286),(100,437)),
 'h2-up':((193,209),(193,244)),
 'h2-lo':((193,249),(193,282)),
 'h3-up':((401.5,209),(401.5,281)),
 'h3-mid':((401.5,286),(401.5,344)),
 'h3-lo':((401.5,391),(401.5,437)),
 'h4':((486,209),(486,391)),
 'h5a':((103,283),(190,283)),
 'h5b':((268,283),(400,283)),
 'h6':((103,439),(400,439)),
 'h7':((403,393),(484,393)),
 'h8':((197,247),(483,391)),
 'axis':((20,206.5),(430,206.5)),
}
print('%-8s %6s %6s  %s'%('seg','width','minG','absorber'))
for k,(p0,p1) in SEG.items():
    w,m=prof(p0,p1)
    print('%-8s %6.2f %6.0f'%(k,w.mean(),m.mean()))
print()
# gray profile along gap regions
def scanline(p0,p1,n=50,half=4):
    (x0,y0),(x1,y1)=p0,p1
    L=np.hypot(x1-x0,y1-y0); ux,uy=(x1-x0)/L,(y1-y0)/L; nx,ny=-uy,ux
    print('  t     x      y    minG  ink')
    for t in np.linspace(0,1,n):
        cx,cy=x0+t*(x1-x0),y0+t*(y1-y0)
        vals=np.array([samp(cx+k*nx,cy+k*ny) for k in np.arange(-half,half+.001,0.2)])
        print('  %.2f %6.1f %6.1f %6.0f %5.1f'%(t,cx,cy,vals.min(),(255-vals).sum()/255*0.2))
print('--- h5 gap: Y=76.5 row283, x 185..275')
scanline((185,283),(275,283),30,4)
