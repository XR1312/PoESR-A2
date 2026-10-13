import numpy as np, itertools
L=353.0; D=231.3; H=243.0
ZP_a,ZP_b = 400.40,-0.7290        # Z = ZP_a + ZP_b*X
YQ_a,YQ_b = 52.19, 1.3755         # Y = YQ_a + YQ_b*X
k = H/(D/2.0)
hs=[ ((-1,0,0),0.0),                # X>=0
     ((1,0,0),L),                   # X<=L
     ((0,-1,0),0.0),                # Y>=0
     ((0,1,0),D),                   # Y<=D
     ((0,0,-1),0.0),                # Z>=0
     ((0,-k,1),0.0),                # Z<=kY   front slant
     ((0,k,1),k*D),                 # Z<=k(D-Y) back slant
     ((0.729,0,1),ZP_a),            # Z<=ZP
     ((-1.3755,1,0),YQ_a)]          # Y<=YQ
nm=['X>=0','X<=L','Y>=0','Y<=D','Z>=0','frontslant','backslant','P','Q']
V=[]
for tri in itertools.combinations(range(9),3):
    A=np.array([hs[i][0] for i in tri],float); bb=np.array([hs[i][1] for i in tri],float)
    if abs(np.linalg.det(A))<1e-9: continue
    x=np.linalg.solve(A,bb)
    if all(np.dot(n,x)-b<=1e-6 for n,b in hs):
        if not any(np.allclose(x,v,atol=1e-6) for v in V): V.append(x)
V=np.array(V)
print('vertices',len(V))
for i,v in enumerate(V): print('  V%d  X=%8.2f Y=%8.2f Z=%8.2f'%(i,*v))
# faces
print('faces:')
FACES=[]
for pi,(n,b) in enumerate(hs):
    pts=[i for i,v in enumerate(V) if abs(np.dot(n,v)-b)<1e-6]
    if len(pts)<3: continue
    # order by angle in the plane
    c=V[pts].mean(0); n_=np.array(n,float); n_/=np.linalg.norm(n_)
    e1=np.cross(n_,[0,0,1.0]);
    if np.linalg.norm(e1)<1e-6: e1=np.cross(n_,[1.0,0,0])
    e1/=np.linalg.norm(e1); e2=np.cross(n_,e1)
    ang=[(np.arctan2(np.dot(V[p]-c,e2),np.dot(V[p]-c,e1)),p) for p in pts]
    ang.sort(); order=[p for _,p in ang]
    FACES.append((nm[pi],n_,order))
    print('  %-11s n=(%6.3f,%6.3f,%6.3f) verts %s'%(nm[pi],*n_,order))
# edges
E={}
for fname,n_,order in FACES:
    for i in range(len(order)):
        a,b_=order[i],order[(i+1)%len(order)]
        key=(min(a,b_),max(a,b_))
        E.setdefault(key,[]).append(fname)
print('edges:',len(E))
for k_,f in E.items(): print('   V%d-V%d  faces %s'%(k_[0],k_[1],f))
np.save('V3.npy',V)
import json; json.dump({'FACES':[(f[0],list(f[1]),f[2]) for f in FACES],'E':{str(k_):v for k_,v in E.items()}},open('solid3.json','w'))
