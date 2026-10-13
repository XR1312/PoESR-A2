import numpy as np
from PIL import Image
a = np.array(Image.open('img-119.jpg').convert('L')).astype(int)
def dump(x0,x1,y0,y1,thresh=160):
    print(f"crop x[{x0},{x1}) y[{y0},{y1})  (cols: x0 + index)")
    hdr='    '+''.join(str((x0+i)//100%10) if (x0+i)%10==0 else ' ' for i in range(x1-x0))
    print(hdr)
    hdr2='    '+''.join(str((x0+i)//10%10) if (x0+i)%10==0 else ' ' for i in range(x1-x0))
    print(hdr2)
    for y in range(y0,y1):
        row=''.join('#' if a[y,x]<thresh else ('+' if a[y,x]<200 else '.') for x in range(x0,x1))
        print(f"{y:3d} {row}")
dump(130,262,104,124)
