import numpy as np,sys
from PIL import Image
f=sys.argv[1]; x0,x1,y0,y1=[int(t) for t in sys.argv[2:6]]
sx=int(sys.argv[6]); sy=int(sys.argv[7])
g=np.array(Image.open(f).convert('L')).astype(int)
for y in range(y0,y1,sy):
    print('%4d '%y+''.join('#' if g[y,x]<60 else ('*' if g[y,x]<140 else ('.' if g[y,x]<210 else ' ')) for x in range(x0,x1,sx)))
