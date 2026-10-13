from ans import *
import math
sh=Sheet(2)
def T(p): return m119(*p)

REDW=2.4; CON=(30,90,215); WHITE=(255,255,255)

# ---------- model ----------
XA=21.5            # 主视图: X=0 -> img x
YA=149.0           # 主视图: img y = YA - Z
CX=544.75; CY=148.2  # 左视图 centre
YC=420.0           # 俯视图 axis height

R1=68.75; R2=120.75
W57=math.sqrt(R1*R1-37.5*37.5)     # 57.62  half width at Z=-37.5
W114=math.sqrt(R2*R2-37.5*37.5)    # 114.78 half width at Z=+37.5
W66=math.sqrt(R1*R1-18.75*18.75)   # 66.14  half width at Z=-18.75

def F(X,Z): return (XA+X, YA-Z)     # 主视图
def H(X,Y): return (XA+X, YC+Y)     # 俯视图
def W(Y,Z): return (CX+Y, CY-Z)     # 左视图  (x = CX+Y  -> mitre through (CX,YC))
def Zcut(X): return 0.625*X-37.5
def Yell(X): return math.sqrt(max(R1*R1-Zcut(X)**2,0.0))

def seg(p0,p1,**kw): sh.seg(T(p0),T(p1),**kw)
def arcx(y,R,side): return CX+side*math.sqrt(max(R*R-(y-CY)**2,0.0))
def mitY(x): return YC+(x-CX)

# 1. erase the stray printed rule that crosses the answer area
sh.seg(T((0,456.6)),T((356,456.6)),color=WHITE,w=4.0)

# 2. construction lines (thin blue)
# 2a. 长对正 : verticals from the 主视图 down into the 俯视图
for X in (0,30,60,120,186,230,301):
    seg((XA+X,272.5),(XA+X,545.5),color=CON,w=0.9)
# 2b. 45° mitre (宽相等) : y = YC + (x-CX)
seg((CX-135,YC-135),(CX+135,YC+135),color=CON,w=0.9)
sh.text(T((CX+133,YC+140)),'45°',color=CON,size=12,anchor='lm')
# 2c. level lines in the 主视图 + transfer of the widths
lv=[(186.5,R1,1,21.5),          # Z=-37.5  -> 57.62
    (167.75,R1,1,51.5),         # Z=-18.75 -> 66.14 (intermediate point)
    (167.75,R1,-1,51.5),        #    and its mirror
    (111.5,R2,1,141.5)]         # Z=+37.5  -> 114.78
for y,R,sd,x0 in lv:
    xa=arcx(y,R,sd)
    seg((x0,y),(xa,y),color=CON,w=0.9)              # level line to the arc
    seg((xa,y),(xa,mitY(xa)),color=CON,w=0.9)       # arc -> mitre
    seg((xa,mitY(xa)),(x0,mitY(xa)),color=CON,w=0.9)  # mitre -> 俯视图
# 2d. widths taken straight off the two circles (radii)
for R in (R1,R2):
    xa=CX-R
    seg((xa,CY),(xa,mitY(xa)),color=CON,w=0.9)
    seg((xa,mitY(xa)),(XA+ (60 if R==R1 else 186),mitY(xa)),color=CON,w=0.9)

# 3. answer : the 俯视图 (heavy red)
# outline
seg(H(0,-W57),H(0,W57),color=RED,w=REDW)                     # left end face X=0
seg(H(60,-R1),H(186,-R1),color=RED,w=REDW)                   # |Y|=R1
seg(H(60, R1),H(186, R1),color=RED,w=REDW)
seg(H(186,-R2),H(186,-W57),color=RED,w=REDW)                 # step at X=186
seg(H(186, W57),H(186, R2),color=RED,w=REDW)
seg(H(186,-R2),H(301,-R2),color=RED,w=REDW)                  # |Y|=R2
seg(H(186, R2),H(301, R2),color=RED,w=REDW)
seg(H(301,-R2),H(301,R2),color=RED,w=REDW)                   # right end face
# ellipse : the oblique cut  Z=0.625X-37.5 , X in [0,120]
N=61; pu=[]; pd=[]
for i in range(N):
    X=120.0*i/(N-1); Y=Yell(X); pu.append(H(X,-Y)); pd.append(H(X,Y))
for i in range(N-1):
    seg(pu[i],pu[i+1],color=RED,w=REDW)
    seg(pd[i],pd[i+1],color=RED,w=REDW)
# internal visible edges
seg(H(120,-W57),H(120,W57),color=RED,w=REDW)                 # crease X=120
seg(H(120,-W57),H(186,-W57),color=RED,w=REDW)                # |Y|=W57
seg(H(120, W57),H(186, W57),color=RED,w=REDW)
seg(H(186,-W114),H(230,-W114),color=RED,w=REDW)              # |Y|=W114
seg(H(186, W114),H(230, W114),color=RED,w=REDW)
seg(H(230,-W114),H(230,W114),color=RED,w=REDW)               # crease X=230
# axis
sh.seg(T((2,YC)),T((348,YC)),color=RED,w=1.1,dash=(5.5,3.0))

# 4. key points
for p in [H(0,-W57),H(0,W57),H(120,-W57),H(120,W57),H(186,-W57),H(186,W57),
          H(186,-R2),H(186,R2),H(60,-R1),H(60,R1),H(230,-W114),H(230,W114),
          H(186,-W114),H(186,W114),H(301,-R2),H(301,R2),
          H(30,-W66),H(30,W66),F(120,37.5),F(0,-37.5),F(30,-18.75)]:
    sh.dot(T(p),color=RED,r=1.5)
sh.text(T((58,346)),'中间点',color=RED,size=11,anchor='lm')
sh.save('ans_p4.png')
print('ok  W57=%.2f W114=%.2f W66=%.2f'%(W57,W114,W66))
