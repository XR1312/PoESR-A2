import subprocess, math
from PIL import Image, ImageDraw, ImageFont

PDF='/Users/XR1312/Desktop/工表-2/工程系统表达原理-工程图学作业.pdf'
WORK='/Users/XR1312/Desktop/工表-2/work/'
S=4            # supersample
DPI=96
FONT='/System/Library/Fonts/Hiragino Sans GB.ttc'
RED=(220,0,0); BLUE=(0,70,220); BLACK=(0,0,0)

def render(page):
    out=WORK+'pg%d'%page
    subprocess.run(['pdftocairo','-png','-r',str(DPI),'-singlefile','-f',str(page),'-l',str(page),PDF,out],check=True)
    return Image.open(out+'.png').convert('RGB')

class Sheet:
    def __init__(self,page):
        self.page=page
        self.base=render(page)
        self.img=self.base.resize((self.base.width*S,self.base.height*S),Image.LANCZOS)
        self.dr=ImageDraw.Draw(self.img)
    def font(self,size):
        return ImageFont.truetype(FONT,size)
    def seg(self,p0,p1,color=RED,w=1.0,dash=None,arrow=None):
        """p0,p1 in page-px (96dpi). w in page-px."""
        x0,y0=p0[0]*S,p0[1]*S; x1,y1=p1[0]*S,p1[1]*S
        W=max(1,w*S)
        if dash is None:
            self.dr.line([x0,y0,x1,y1],fill=color,width=int(round(W)))
            return
        L=math.hypot(x1-x0,y1-y0)
        on,off=dash[0]*S,dash[1]*S
        t=0.0
        while t<L:
            e=min(t+on,L)
            f0=t/L; f1=e/L
            self.dr.line([x0+(x1-x0)*f0,y0+(y1-y0)*f0,x0+(x1-x0)*f1,y0+(y1-y0)*f1],fill=color,width=int(round(W)))
            t=e+off
    def dot(self,p,color=RED,r=1.6):
        x,y=p[0]*S,p[1]*S; R=r*S
        self.dr.ellipse([x-R,y-R,x+R,y+R],fill=color)
    def text(self,p,s,color=RED,size=13,anchor='mm'):
        f=self.font(int(size*S))
        self.dr.text((p[0]*S,p[1]*S),s,font=f,fill=color,anchor=anchor)
    def save(self,name):
        out=self.img.resize((self.base.width,self.base.height),Image.LANCZOS)
        out.save(WORK+name)
        return out

# ---------- figure page mappings: img px -> page px (96 dpi) ----------
def m58(u,v): return (219.68+0.54973*u, 153.12+0.55011*v)   # 645x728
def m59(u,v): return (203.68+0.71855*u, 672.64+0.71855*v)   # 538x443
def m118(u,v): return (180.00+0.55025*u, 169.92+0.55021*v)  # 788x629
def m119(u,v): return (162.88+0.67049*u, 604.96+0.67033*v)  # 698x459
