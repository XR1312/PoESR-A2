import numpy as np
from PIL import Image
g=np.array(Image.open('/Users/XR1312/Desktop/工表-2/work/img-059.jpg').convert('L')).astype(float)
H,W=g.shape
def fit(x0,y0,x1,y1,band=7.0,it=4):
    dx,dy=x1-x0,y1-y0; L=np.hypot(dx,dy)
    for _ in range(it):
        yy,xx=np.mgrid[max(0,int(min(y0,y1)-band-2)):min(H,int(max(y0,y1)+band+3)),
                       max(0,int(min(x0,x1)-band-2)):min(W,int(max(x0,x1)+band+3))]
        m=(g[yy,xx]<150)
        X=xx[m].astype(float); Y=yy[m].astype(float)
        if len(X)<10: return None
        ux,uy=dx/L,dy/L; nx,ny=-uy,ux
        d=(X-x0)*nx+(Y-y0)*ny
        keep=np.abs(d)<band
        X,Y=X[keep],Y[keep]
        mx,my=X.mean(),Y.mean()
        A=np.c_[X-mx,Y-my]
        u,s,vt=np.linalg.svd(A,full_matrices=False)
        dirv=vt[0]; nrm=vt[1]
        t=(X-mx)*dirv[0]+(Y-my)*dirv[1]
        t0,t1=t.min(),t.max()
        x0,y0=mx+t0*dirv[0], my+t0*dirv[1]
        x1,y1=mx+t1*dirv[0], my+t1*dirv[1]
        resid=np.abs((X-mx)*nrm[0]+(Y-my)*nrm[1])
        rms=np.sqrt((resid**2).mean()); n=len(X); band=max(2.0,min(band,3.0*rms+0.8))
    ang=np.degrees(np.arctan2(y1-y0,x1-x0))
    # ink width
    ws=[]
    for tt in np.linspace(0.15,0.85,25):
        cx,cy=x0+tt*(x1-x0),y0+tt*(y1-y0)
        ks=np.arange(-5,5.001,0.2)
        def sm(px,py):
            if not(0<=px<W-1 and 0<=py<H-1): return 255.0
            i,j=int(px),int(py); fx,fy=px-i,py-j
            return (g[j,i]*(1-fx)*(1-fy)+g[j,i+1]*fx*(1-fy)+g[j+1,i]*(1-fx)*fy+g[j+1,i+1]*fx*fy)
        ws.append(sum((255.0-sm(cx+k*nx,cy+k*ny)) for k in ks)/255.0*0.2)
    return dict(p0=(x0,y0),p1=(x1,y1),n=n,ang=ang,rms=rms,w=np.mean(ws))
LINES={
 'V-a':(102,46,102,206),'V-b':(101,44,403,159),'V-c':(196,1,488,149),
 'V-d':(196,122,488,152),'V-e':(193,2,193,206),'V-f':(401.5,156,401.5,206),
 'V-g':(486,149,486,206),
 'h1':(101,206,101,441),'h2':(193,206,193,285),'h3':(401.5,206,401.5,441),
 'h4':(486,206,486,394),'h5':(101,283,403,283),'h6':(101,439.5,403,439.5),
 'h7':(400,393,487,393),'h8':(194,246,486,393),
}
for k,(a,b,c,d) in LINES.items():
    r=fit(a,b,c,d)
    if r is None: print(k,'FAIL'); continue
    (x0,y0),(x1,y1)=r['p0'],r['p1']
    def cvt(p):
        x,y=p
        if k[0]=='V' or k in ('h1','h2','h3','h4') and y<206: pass
        return x,y
    print('%-5s n=%4d ang=%7.2f rms=%4.2f w=%4.2f  (%7.1f,%7.1f)->(%7.1f,%7.1f)'%(k,r['n'],r['ang'],r['rms'],r['w'],x0,y0,x1,y1))
