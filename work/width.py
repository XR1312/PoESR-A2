import numpy as np
from PIL import Image
def load(path, thresh=160):
    return np.array(Image.open(path).convert('L')).astype(int) < thresh
def width(ink, x, y, d=(1,0)):
    """measure ink extent along direction d from (x,y)"""
    n = 0; i = 0
    while True:
        xx, yy = int(round(x+d[0]*i)), int(round(y+d[1]*i))
        if 0 <= yy < ink.shape[0] and 0 <= xx < ink.shape[1] and ink[yy, xx]: n += 1; i += 1
        else: break
    i = -1
    while True:
        xx, yy = int(round(x+d[0]*i)), int(round(y+d[1]*i))
        if 0 <= yy < ink.shape[0] and 0 <= xx < ink.shape[1] and ink[yy, xx]: n += 1; i -= 1
        else: break
    return n
if __name__ == '__main__':
    ink = load('img-118.jpg')
    tests = [
      ('top edge y31 @x60',   (60,31), (0,1)),
      ('y274 @x60',           (60,274), (0,1)),
      ('y274 @x700 (tri base)',(700,274), (0,1)),
      ('y395 @x60',           (60,395), (0,1)),
      ('y395 @x200',          (200,395), (0,1)),
      ('y510 @x60 (ridge?)',  (60,510), (0,1)),
      ('y510 @x200',          (200,510), (0,1)),
      ('y510 @x330',          (330,510), (0,1)),
      ('y626 @x200',          (200,626), (0,1)),
      ('y626 @x10',           (10,626), (0,1)),
      ('y626 @x700',          (700,626), (0,1)),
      ('x27 @y100',           (27,100), (1,0)),
      ('x27 @y250',           (27,250), (1,0)),
      ('x27 @y600',           (27,600), (1,0)),
      ('x379 @y100',          (379,100), (1,0)),
      ('x379 @y600',          (379,600), (1,0)),
      ('P diag @(250,40)',    (250,40), (0.55,0.83)),
      ('P diag @(310,85)',    (310,85), (0.55,0.83)),
      ('Q diag @(120,443)',   (120,443), (0.58,-0.81)),
      ('Q diag @(70,512)',    (70,512), (0.58,-0.81)),
      ('tri left side @(610,150)', (610,150), (0.66,0.75)),
    ]
    for name, (x,y), d in tests:
        print('%-28s width=%d' % (name, width(ink, x, y, d)))
