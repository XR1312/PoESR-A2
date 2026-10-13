from ans import *
sh=Sheet(1); T=lambda u,v: m58(u,v)

# ---- given geometry in img-058 px (axis row 273.5) ----
AV=(596.4,150.0); BV=(429.7,69.2); CV=(395.4,206.5); DV=(530.4,233.8)   # V of quad
AH=(596.5,392.5); BH=(429.7,646.9); CH=(395.4,456.4); DH=(530.4,310.6) # H of quad (答案)
axis=273.5
# 正平线 through A  (V: through a' ⊥ e'f')
L1s=0.4824                       # row/col slope
I=(454.4, AV[1]+L1s*(AV[0]-454.4))       # where it cuts c'd'
i=(454.4, AH[1])                          # its H projection is horizontal through a
# 水平线 through A  (H: through a ⊥ ef)
L3=0.7609
Kp=(409.5,150.0)                          # V: horizontal through a' cuts b'c'
K=(409.5, AH[1]+L3*(AH[0]-409.5))
# 水平线 through C and D (V horizontals through c', d' cut the 正平线)
Mp=(AV[0]-(CV[1]-AV[1])/L1s, CV[1]);  M=(Mp[0], AH[1])
M2p=(AV[0]-(DV[1]-AV[1])/L1s, DV[1]); M2=(M2p[0], AH[1])

# ---- 作图线 (thin red) ----
sh.seg(T(*AV),T(432,AV[1]+L1s*(AV[0]-432)),color=RED,w=1.05)          # 过a'作正平线⊥e'f'
sh.seg(T(420,AH[1]),T(*AH),color=RED,w=1.05)                          # 正平线的水平投影
sh.seg(T(*AH),T(395.4,AH[1]+L3*(AH[0]-395.4)),color=RED,w=1.05)       # 过a作水平线⊥ef
sh.seg(T(*Kp),T(AV[0],Kp[1]),color=RED,w=1.05)                        # 水平线(A)的正面投影
sh.seg(T(*CV),T(*Mp),color=RED,w=1.05)                                # 水平线(C)的正面投影
sh.seg(T(*DV),T(M2p[0],DV[1]),color=RED,w=1.05)                       # 水平线(D)的正面投影
sh.seg(T(*Mp),T(*M),color=BLUE,w=1.0)                                 # 投影连线
sh.seg(T(*M2p),T(*M2),color=BLUE,w=1.0)
sh.seg(T(*M),T(*CH),color=RED,w=1.05)                                 # 水平线(C)的水平投影
sh.seg(T(*M2),T(*DH),color=RED,w=1.05)                                # 水平线(D)的水平投影
sh.seg(T(*Kp),T(409.5,AH[1]+L3*(AH[0]-409.5)),color=BLUE,w=1.0)       # 投影连线 b'c'上K
sh.seg(T(*I),T(*i),color=BLUE,w=1.0)                                  # 投影连线
for p,h in ((BV,BH),(CV,CH),(DV,DH)):                                  # 投影连线 b',c',d'
    sh.seg(T(*p),T(*h),color=BLUE,w=1.0)
# ---- 答案:水平投影 abcd (thick red) ----
for p,q in ((AH,BH),(BH,CH),(CH,DH),(DH,AH)):
    sh.seg(T(*p),T(*q),color=RED,w=2.3)
for p in (AH,BH,CH,DH,I,i,Kp,K,Mp,M,M2p,M2): sh.dot(T(*p),r=1.5)
sh.text(T(403,660),'b',size=18); sh.text(T(358,472),'c',size=18); sh.text(T(552,322),'d',size=18)
sh.save('ans_p1.png')
print('ok')
