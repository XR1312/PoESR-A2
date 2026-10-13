from ans import *

sh=Sheet(1)
T=lambda u,v: m59(u,v)
W='white'
# ---------- 作图过程: 投影连线 (thin blue) ----------
sh.seg(T(193,79.45),T(193,298.1),color=BLUE,w=1.1)        # m' -> m
sh.seg(T(348.85,138.1),T(348.85,323.8),color=BLUE,w=1.1)  # n' -> n
# ---------- 不可见部分 (dashed red) ----------
for a,b in [((193,298.1),(193,393.0)), ((193,246.0),(348.85,323.8)), ((403,350.7),(403,393.0))]:
    sh.seg(T(*a),T(*b),color=W,w=2.6)                     # erase black ink underneath
    sh.seg(T(*a),T(*b),color=RED,w=2.0,dash=(5,3))
# ---------- 补全被题图抹掉的可见线段 (solid black) ----------
for a,b in [((193,285.0),(193,298.1)), ((193,283.0),(267.1,283.0)),
            ((348.85,323.8),(403.0,350.7)), ((193.0,393.0),(403.0,393.0))]:
    sh.seg(T(*a),T(*b),color=BLACK,w=2.4)
# ---------- 所求交线 MN (thick red) ----------
sh.seg(T(193,79.45),T(348.85,138.1),color=RED,w=2.3)      # m'n'  (位于四边形正面投影 d'e'f'g' 上)
sh.seg(T(193,298.1),T(348.85,323.8),color=RED,w=2.3)      # mn
for p in [(193,298.1),(348.85,323.8),(193,79.45),(348.85,138.1)]:
    sh.dot(T(*p))
sh.text(T(170,289),'m',size=19); sh.text(T(374,318),'n',size=19)
sh.text(T(170,70),"m'",size=19);  sh.text(T(322,129),"n'",size=19)
sh.save('ans_p2.png')
print('ok')
