import numpy as np
from PIL import Image

def segments(img, th=150, axis_rows=None, minlen=28, maxdist=1.6, angstep=1):
    g=np.array(Image.open(img).convert('L')).astype(int)
    a = g<th
    if axis_rows:
        y0,y1=axis_rows; a[y0:y1,:]=False
    ys,xs=np.nonzero(a)
    P=np.c_[xs,ys].astype(float)
    H,W=g.shape
    thetas=np.deg2rad(np.arange(0,180,angstep))
    ct,st=np.cos(thetas),np.sin(thetas)
    diag=int(np.hypot(H,W))+1
    acc=np.zeros((len(thetas),2*diag+1),int)
    rho=P[:,0:1]*ct[None,:]+P[:,1:2]*st[None,:]
    ri=np.round(rho).astype(int)+diag
    for j in range(len(thetas)):
        np.add.at(acc[j],ri[:,j],1)
    # peaks
    cand=[]
    for j in range(len(thetas)):
        for k in range(acc.shape[1]):
            v=acc[j,k]
            if v<minlen: continue
            nb=acc[max(0,j-2):j+3, max(0,k-3):k+4]
            if v>=nb.max(): cand.append((v,j,k))
    cand.sort(reverse=True)
    segs=[]
    used=np.zeros(len(P),bool)
    for v,j,k in cand:
        d=np.abs(P[:,0]*ct[j]+P[:,1]*st[j]-(k-diag))
        sel=(d<maxdist)&(~used)
        if sel.sum()<minlen: continue
        Q=P[sel]
        # sort along direction
        dirv=np.array([-st[j],ct[j]])
        t=Q@dirv
        o=np.argsort(t); Q=Q[o]; t=t[o]
        # split runs
        br=np.nonzero(np.diff(t)>8)[0]
        groups=np.split(np.arange(len(Q)), br+1)
        for gr in groups:
            if len(gr)<minlen: continue
            R=Q[gr]
            # TLS fit
            c=R.mean(0); U=Q[gr]-c
            _,_,Vt=np.linalg.svd(U,full_matrices=False)
            dd=Vt[0]
            tt=(R-c)@dd
            p0=c+dd*tt.min(); p1=c+dd*tt.max()
            ang=np.rad2deg(np.arctan2(dd[1],dd[0]))%180
            segs.append((tuple(np.round(p0,1)),tuple(np.round(p1,1)),len(gr),round(ang,1)))
            used[np.nonzero(sel)[0][gr]]=True
    segs.sort(key=lambda s:-s[2])
    return segs

if __name__=='__main__':
    import sys
    img=sys.argv[1]; ar=None
    if len(sys.argv)>2: ar=(int(sys.argv[2]),int(sys.argv[3]))
    for s in segments(img,axis_rows=ar): print('p0=%s p1=%s n=%d ang=%.1f'%s)
