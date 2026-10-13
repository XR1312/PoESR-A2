import numpy as np,sys
from PIL import Image
g=np.array(Image.open('/Users/XR1312/Desktop/工表-2/work/img-059.jpg').convert('L')).astype(int)
x0,x1,y0,y1=[int(t) for t in sys.argv[1:5]]
sx=int(sys.argv[5]) if len(sys.argv)>5 else 1
sy=int(sys.argv[6]) if len(sys.argv)>6 else 1
hdr='     '+''.join(str((x//10)%10) for x in range(x0,x1,sx))
print(hdr)
print('     '+''.join(str(x%10) for x in range(x0,x1,sx)))
for y in range(y0,y1,sy):
    row=''.join('#' if g[y,x]<60 else ('*' if g[y,x]<140 else ('.' if g[y,x]<210 else ' ')) for x in range(x0,x1,sx))
    print('%4d %s'%(y,row))
