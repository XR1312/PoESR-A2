import numpy as np
from PIL import Image
g=np.array(Image.open('/Users/XR1312/Desktop/工表-2/work/img-059.jpg').convert('L')).astype(float)
H,W=g.shape
def col_runs(xc,half=3,y0=0,y1=None,th=200):
    y1=H if y1 is None else y1
    v=g[y0:y1,max(0,xc-half):xc+half+1].min(axis=1)
    ink=v<th; out=[];s=None
    for i,b in enumerate(ink):
        if b and s is None: s=i
        if not b and s is not None: out.append((s+y0,i-1+y0)); s=None
    if s is not None: out.append((s+y0,len(ink)-1+y0))
    return out
def row_runs(yc,half=3,x0=0,x1=None,th=200):
    x1=W if x1 is None else x1
    v=g[max(0,yc-half):yc+half+1,x0:x1].min(axis=0)
    ink=v<th; out=[];s=None
    for i,b in enumerate(ink):
        if b and s is None: s=i
        if not b and s is not None: out.append((s+x0,i-1+x0)); s=None
    if s is not None: out.append((s+x0,len(ink)-1+x0))
    return out
print('h5  row283  x100..405 :',row_runs(283,3,95,410))
print('h6  row439  x100..405 :',row_runs(439,3,95,410))
print('h7  row392  x395..490 :',row_runs(392,3,395,492))
print('h3  col401  y206..441 :',col_runs(401,3,205,443))
print('h1  col102  y206..441 :',col_runs(102,3,205,443))
print('h2  col193  y206..290 :',col_runs(193,3,205,292))
print('h4  col486  y206..400 :',col_runs(486,3,205,398))
print('V-e col193  y0..206   :',col_runs(193,3,0,206))
print('V-a col102  y0..206   :',col_runs(102,3,0,206))
print('V-f col401  y0..206   :',col_runs(401,3,0,206))
print('V-g col486  y0..206   :',col_runs(486,3,0,206))
print()
print('--- h5 gap min-gray detail (row 280..287) ---')
for x in range(186,275,4):
    col=g[280:288,x]
    print(' x=%3d min=%3d  '%(x,col.min()), ''.join('%3d '%t for t in col))
