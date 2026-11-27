"""Figures for class 7 maths Ch 7, A Tale of Three Intersecting Lines.
Every triangle is built from its given measurements (1 cm = CM units), and every angle label is
asserted against the drawn geometry by geo.Fig.angle."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "7")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

CM = 30
RED, YEL = "#c62828", "#ef8f00"

# ---------------------------------------------------------------- helpers
def sss(ab, ac, bc, A=P(0, 0), rot=0):
    """Triangle with AB, AC, BC in cm: A at A, B along direction rot, C on the left (A, B, C anticlockwise)."""
    B = along(A, rot, ab * CM)
    x = (ab ** 2 + ac ** 2 - bc ** 2) / (2 * ab)
    C = along(A, rot + math.degrees(math.acos(x / ac)), ac * CM)
    return A, B, C

def sas(ab, angA, ac, A=P(0, 0)):
    return A, along(A, 0, ab * CM), along(A, angA, ac * CM)

def asa(angA, ab, angB, A=P(0, 0)):
    B = along(A, 0, ab * CM)
    return A, B, meet(A, angA, B, 180 - angB)

def centroid(*ps): return (sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps))

def tri(f, pts, names="ABC", dots=True, color=INK, fill=None):
    if fill: f.poly(list(pts), fill=fill, color=color)
    else:
        for i in range(3): f.seg(pts[i], pts[(i + 1) % 3], color=color)
    g = centroid(*pts)
    for p, n in zip(pts, names):
        if dots: f.dot(p, color=color)
        if n: f.label(along(p, dirto(g, p), 15), n)

def side(f, p, q, s, pts, color=GIVEN, off=13, size=13):
    """Length label at the middle of pq, pushed away from the triangle's centre."""
    g = centroid(*pts); m = mul(add(p, q), 0.5)
    a = dirto(p, q); n = a + 90
    if dist(along(m, n, 1), g) < dist(along(m, n + 180, 1), g): n += 180
    w = len(s) * size * 0.56          # keep the whole word clear of the side, not just its centre
    f.label(along(m, n, off + w / 2 * abs(math.cos(d2r(n)))), s, color=color, size=size)

def iang(f, pts, i, label, expect=None, r=20, color=GIVEN, lr=None):
    """Interior angle at vertex i of an anticlockwise triangle."""
    V, Pn, Pp = pts[i], pts[(i + 1) % 3], pts[(i - 1) % 3]
    f.angle(V, dirto(V, Pn), dirto(V, Pp), label, expect, r=r, color=color, lr=lr)

def interior(pts, i):
    V, Pn, Pp = pts[i], pts[(i + 1) % 3], pts[(i - 1) % 3]
    return (dirto(V, Pp) - dirto(V, Pn)) % 360

def caption(f, x, y, s, size=13, color=INK, bold=False):
    f.label(P(x, y), s, size=size, color=color, bold=bold)

# ---------------------------------------------------------------- 7.1 naming
@fig
def triangles_named():
    f = Fig("triangles_named")
    t1 = sss(3, 2.5, 2.2); tri(f, t1, "ABC"); caption(f, 45, -30, "∆ABC")
    t2 = sss(3.2, 3.6, 2.4, A=P(140, 10), rot=12); tri(f, t2, "YZX"); caption(f, 195, -30, "∆YZX")
    t3 = sss(2.6, 2.0, 3.4, A=P(290, 0), rot=-8); tri(f, t3, "WUV"); caption(f, 330, -30, "∆WUV")
    return f

@fig
def collinear():
    f = Fig("collinear")
    A, B, C = P(0, 0), P(110, 0), P(200, 0)
    f.seg(A, C)
    for p, n in ((A, "A"), (B, "B"), (C, "C")): f.dot(p); f.label(add(p, (0, -16)), n)
    caption(f, 100, 26, "A, B and C on one line: no corner, no triangle", size=12)
    return f

# ---------------------------------------------------------------- 7.1-7.2 constructions with a compass
@fig
def equi_steps():
    f = Fig("equi_steps"); s = 4 * CM
    for k in range(3):
        A = P(k * 175, 0); B = along(A, 0, s); C = along(A, 60, s)
        f.seg(A, B); f.dot(A); f.dot(B)
        f.label(add(A, (-6, -14)), "A"); f.label(add(B, (6, -14)), "B"); side(f, A, B, "4 cm", (A, B, C))
        f.carc(A, s, 35, 85, color=GIVEN)
        if k >= 1: f.carc(B, s, 95, 145, color=ASK)
        if k == 2:
            f.seg(A, C); f.seg(B, C); f.dot(C); f.label(add(C, (0, 15)), "C")
        caption(f, A[0] + s / 2, -40, ["Step 1: arc 4 cm from A", "Step 2: arc 4 cm from B", "Step 3: join AC and BC"][k], size=12)
    return f

@fig
def sss_456():
    f = Fig("sss_456")
    A, B, C = sss(4, 5, 6)
    f.circle(A, 5 * CM, color=GIVEN, dash="5,4"); f.carc(B, 6 * CM, 95, 140, color=ASK)
    tri(f, (A, B, C)); side(f, A, B, "4 cm", (A, B, C)); side(f, A, C, "5 cm", (A, B, C)); side(f, B, C, "6 cm", (A, B, C))
    caption(f, A[0], -5.6 * CM, "circle: every point 5 cm from A   ·   arc: every point 6 cm from B", size=12)
    return f

@fig
def construct_answers():
    f = Fig("construct_answers"); x, y = 0, 0
    sets = [("(a) 4, 4, 6", (6, 4, 4), "isosceles"), ("(b) 3, 4, 5", (5, 3, 4), "scalene"),
            ("(c) 1, 5, 5", (1, 5, 5), "isosceles"), ("(d) 4, 6, 8", (8, 4, 6), "scalene"),
            ("(e) 3.5, 3.5, 3.5", (3.5, 3.5, 3.5), "equilateral")]
    for i, (name, (ab, ac, bc), kind) in enumerate(sets):
        if i == 3: x, y = 0, -230
        t = sss(ab, ac, bc, A=P(x, y))
        a1, a2 = dirto(t[0], t[2]), dirto(t[1], t[2])
        f.carc(t[0], ac * CM, a1 - 12, a1 + 12, color=HELP); f.carc(t[1], bc * CM, a2 - 12, a2 + 12, color=HELP)
        tri(f, t, ("", "", ""))
        for p, q, L in ((t[0], t[1], ab), (t[0], t[2], ac), (t[1], t[2], bc)): side(f, p, q, f"{L:g}", t, size=12)
        cx = x + ab * CM / 2
        caption(f, cx, y - 36, name, bold=True); caption(f, cx, y - 54, kind, color=ANS)
        x += ab * CM + 90
    return f

@fig
def circle_iso_q():
    f = Fig("circle_iso_q"); O = P(0, 0); r = 80
    f.circle(O, r, color=INK, w=2); f.dot(O); f.label(add(O, (12, -10)), "O")
    for i, a in enumerate((20, 75, 140, 200, 250, 320)):
        p = along(O, a, r); f.dot(p); f.label(along(O, a, r + 14), "PQRSTU"[i])
    return f

@fig
def circle_iso_a():
    f = Fig("circle_iso_a"); O = P(0, 0); r = 80
    f.circle(O, r, color=INK, w=2)
    pts = {n: along(O, a, r) for n, a in zip("PQRSTU", (20, 75, 140, 200, 250, 320))}
    f.poly([O, pts["P"], pts["Q"]], fill="#c8e6c9", color=ANS)
    f.poly([O, pts["S"], pts["T"]], fill="#ffe0b2", color=INK)
    f.ticks(O, pts["P"], 1, color=ANS); f.ticks(O, pts["Q"], 1, color=ANS)
    f.ticks(O, pts["S"], 2); f.ticks(O, pts["T"], 2)
    f.dot(O); f.label(add(O, (-4, 14)), "O")
    for n, p in pts.items(): f.dot(p); f.label(along(O, dirto(O, p), r + 14), n)
    return f

def two_circles(f, r=70, centres=2):
    A, B = P(0, 0), P(r, 0)
    f.circle(A, r, color=INK, w=1.8); f.circle(B, r, color=INK, w=1.8)
    C = along(A, -60, r)
    if centres == 3: f.circle(C, r, color=INK, w=1.8)
    for p, n, o in ((A, "A", (-10, 8)), (B, "B", (10, 8))) + (((C, "C", (0, -15)),) if centres == 3 else ()):
        f.dot(p); f.label(add(p, o), n)
    return A, B, C

@fig
def two_circles_q():
    f = Fig("two_circles_q"); two_circles(f); return f

@fig
def two_circles_a():
    f = Fig("two_circles_a"); r = 70; A, B, _ = two_circles(f, r)
    C, D = along(A, 60, r), along(A, -60, r); E = along(B, 25, r)
    f.poly([A, B, C], fill="#c8e6c9", color=ANS); f.poly([A, B, D], fill="#c8e6c9", color=ANS)
    f.seg(A, E, color=GIVEN, w=2); f.seg(B, E, color=GIVEN, w=2)
    for p, n, o in ((C, "C", (0, 14)), (D, "D", (0, -15)), (E, "E", (12, 4))): f.dot(p); f.label(add(p, o), n)
    f.dot(A); f.dot(B)
    return f

@fig
def three_circles_q():
    f = Fig("three_circles_q"); two_circles(f, centres=3); return f

@fig
def three_circles_a():
    f = Fig("three_circles_a"); r = 70; A, B, C = two_circles(f, r, centres=3)
    f.poly([A, B, C], fill="#c8e6c9", color=ANS)
    G = along(C, -120, r)        # another point on circle C: CA = CG (radii)
    f.seg(C, G, color=GIVEN, w=2); f.seg(A, G, color=GIVEN, w=2); f.dot(G); f.label(add(G, (-10, -10)), "G")
    for p in (A, B, C): f.dot(p)
    return f

# ---------------------------------------------------------------- triangle inequality
@fig
def no_meet_348():
    f = Fig("no_meet_348")
    A, B = P(0, 0), P(8 * CM, 0)
    f.seg(A, B); f.dot(A); f.dot(B); f.label(add(A, (-8, -14)), "A"); f.label(add(B, (8, -14)), "B")
    f.label(P(4 * CM, -16), "8 cm", color=GIVEN, size=13)
    f.carc(A, 3 * CM, 0, 100, color=GIVEN); f.carc(B, 4 * CM, 80, 180, color=ASK)
    f.label(along(A, 60, 3 * CM + 14), "3 cm", color=GIVEN, size=13); f.label(along(B, 120, 4 * CM + 14), "4 cm", color=ASK, size=13)
    caption(f, 4 * CM, -38, "3 + 4 = 7, less than 8: the arcs never meet", size=12)
    return f

@fig
def tent_tree():
    f = Fig("tent_tree")
    T, R, Pl = P(0, 0), P(240, 30), P(120, 120)
    f.seg(T, R, color=RED, w=3); f.seg(T, Pl, color=YEL, w=3, dash="8,5"); f.seg(Pl, R, color=YEL, w=3, dash="8,5")
    f.poly([add(T, (-16, -8)), add(T, (16, -8)), add(T, (0, 18))], fill="#bbdefb")
    f.poly([add(R, (-14, 4)), add(R, (14, 4)), add(R, (0, 34))], fill="#a5d6a7"); f.seg(R, add(R, (0, 4)), w=4)
    f.seg(add(Pl, (0, -8)), add(Pl, (0, 26)), w=4)
    f.label(add(T, (0, -22)), "tent"); f.label(add(R, (16, -12)), "tree"); f.label(add(Pl, (0, 38)), "pole")
    f.label(P(120, -2), "direct path", color=RED, size=12); f.label(P(40, 80), "via the pole", color=YEL, size=12)
    return f

@fig
def rough_10_15_30():
    f = Fig("rough_10_15_30")
    A, C, B = P(0, 0), P(170, 0), P(110, 100)     # drawn as if it existed
    t = (A, C, B); tri(f, t, "ACB")
    side(f, A, C, "30 cm", t); side(f, A, B, "15 cm", t); side(f, C, B, "10 cm", t)
    caption(f, 85, -34, "a rough sketch: not drawn to size", size=12, color=HELP)
    return f

def two_circle_case(f, x, r1, r2, ab=8, title="", y=0):
    A, B = P(x, y), P(x + ab * CM, y)
    f.circle(A, r1 * CM, color=GIVEN); f.circle(B, r2 * CM, color=ASK)
    f.seg(A, B); f.dot(A); f.dot(B); f.label(add(A, (-8, -13)), "A"); f.label(add(B, (8, -13)), "B")
    if title: caption(f, x + ab * CM / 2, -max(r1, r2) * CM - 22, title, size=12, bold=True)
    return A, B

@fig
def circles_458():
    f = Fig("circles_458")
    A, B = two_circle_case(f, 0, 4, 5)
    X = P(4 * CM, 0); f.dot(X, color=GIVEN); f.label(add(X, (8, 12)), "X", color=GIVEN)
    x = (64 + 16 - 25) / 16; C = along(A, math.degrees(math.acos(x / 4)), 4 * CM); D = (C[0], -C[1])
    for p, n, o in ((C, "C", (-14, 12)), (D, "C′", (-14, -12))): f.dot(p, color=ANS); f.label(add(p, o), n, color=ANS)
    f.seg(A, C, color=ANS); f.seg(B, C, color=ANS)
    f.label(P(2 * CM, -14), "AX = 4", color=GIVEN, size=12); f.label(P(6 * CM, -14), "XB = 4", size=12)
    return f

@fig
def three_cases():
    f = Fig("three_cases")
    rows = ((3, 5, "Case 1: 3 + 5 = 8, the circles just touch"), (3, 4, "Case 2: 3 + 4 is less than 8, they don't meet"),
            (4, 5, "Case 3: 4 + 5 is more than 8, they cross"))
    for k, (r1, r2, t) in enumerate(rows):
        y = -k * 360
        two_circle_case(f, 0, r1, r2, y=y)
        caption(f, 4 * CM, y + 5.6 * CM, t, size=15, bold=True)
        if k == 0: f.dot(P(3 * CM, y), color=ANS)
        if k == 2:
            x = (64 + 16 - 25) / 16; C = along(P(0, y), math.degrees(math.acos(x / 4)), 4 * CM)
            f.dot(C, color=ANS); f.dot((C[0], 2 * y - C[1]), color=ANS)
    return f

# ---------------------------------------------------------------- SAS and ASA
@fig
def sas_steps():
    f = Fig("sas_steps")
    A, B, C = sas(5, 45, 4)
    f.line(A, 45, 0, 5.2 * CM, color=HELP, dash="6,4")
    tri(f, (A, B, C)); iang(f, (A, B, C), 0, "45°", 45, r=26, lr=42)
    side(f, A, B, "5 cm", (A, B, C)); side(f, A, C, "4 cm", (A, B, C))
    return f

def sas_answer(name, s1, ang, s2):
    f = Fig(name)
    t = sas(s1, ang, s2); tri(f, t, "ABC")
    iang(f, t, 0, f"{ang}°", ang, r=20, lr=36)
    side(f, t[0], t[1], f"{s1} cm", t); side(f, t[0], t[2], f"{s2} cm", t)
    side(f, t[1], t[2], f"BC ≈ {dist(t[1], t[2]) / CM:.1f} cm", t, color=ANS)
    return f

@fig
def sas_a(): return sas_answer("sas_a", 7, 75, 3)
@fig
def sas_b(): return sas_answer("sas_b", 6, 25, 3)
@fig
def sas_c(): return sas_answer("sas_c", 8, 120, 3)

@fig
def asa_steps():
    f = Fig("asa_steps")
    A, B, C = asa(45, 5, 80)
    f.line(A, 45, 0, dist(A, C) + 30, color=HELP, dash="6,4"); f.line(B, 100, 0, dist(B, C) + 30, color=HELP, dash="6,4")
    tri(f, (A, B, C)); iang(f, (A, B, C), 0, "45°", 45, r=26, lr=42); iang(f, (A, B, C), 1, "80°", 80, r=22, lr=38)
    side(f, A, B, "5 cm", (A, B, C))
    return f

def asa_answer(name, a1, s, a2, k=1):
    """k > 1 draws a small triangle k times bigger (the labels still give the true sizes)."""
    f = Fig(name)
    t = asa(a1, s * k, a2); tri(f, t, "ABC")
    iang(f, t, 0, f"{a1}°", a1, r=20, lr=36); iang(f, t, 1, f"{a2}°", a2, r=20, lr=36)
    iang(f, t, 2, f"{180 - a1 - a2}°", 180 - a1 - a2, r=18, lr=34, color=ANS)
    side(f, t[0], t[1], f"{s} cm", t)
    return f

@fig
def asa_a(): return asa_answer("asa_a", 75, 5, 75)
@fig
def asa_b(): return asa_answer("asa_b", 25, 3, 60, k=2)
@fig
def asa_c(): return asa_answer("asa_c", 120, 6, 30)

@fig
def asa_limit():
    f = Fig("asa_limit"); A, B = P(0, 0), P(140, 0)
    f.seg(add(A, (-30, 0)), add(B, (40, 0))); f.dot(A); f.dot(B)
    f.label(add(A, (-4, -15)), "A"); f.label(add(B, (4, -15)), "B")
    f.line(A, 40, 0, 300); f.label(along(A, 40, 312), "l"); f.arrows(along(A, 40, 200), 40)
    C = meet(A, 40, B, 80); f.seg(B, C, color=ANS, w=2.2); f.dot(C, color=ANS); f.label(add(C, (-12, 4)), "C", color=ANS)
    f.line(B, 40, 0, 300, color=GIVEN); f.arrows(along(B, 40, 200), 40, color=GIVEN); f.label(along(B, 40, 312), "m", color=GIVEN)
    f.line(B, 25, 0, 230, color=ASK, dash="6,4")
    f.angle(A, 0, 40, "40°", 40, r=30, lr=46)
    f.angle(B, 40, 180, "140°", 140, r=22, lr=36, color=GIVEN)
    f.angle(B, 80, 180, "100°", 100, r=50, lr=64, color=ANS)
    return f

# ---------------------------------------------------------------- angle sum
def angle_sum_fig(name, labels):
    f = Fig(name)
    t = asa(50, 6, 70); B, C, A = t[0], t[1], t[2]      # base BC, apex A
    tri(f, (B, C, A), "BCA")
    f.line(A, 0, -120, 120, color=GIVEN); f.label(along(A, 180, 132), "X"); f.label(along(A, 0, 132), "Y")
    f.arrows(along(A, 0, 90), 0, color=GIVEN); f.arrows(along(B, 0, 140), 0)
    b, c, a = labels
    f.angle(B, 0, 50, b, 50, r=26, lr=42); f.angle(C, 110, 180, c, 70, r=24, lr=40)
    f.angle(A, 180, 230, b, 50, r=26, lr=44); f.angle(A, 290, 360, c, 70, r=26, lr=44)
    f.angle(A, 230, 290, a, 60, r=20, lr=36, color=ASK)
    return f

@fig
def angle_sum_50_70():
    return angle_sum_fig("angle_sum_50_70", ("50°", "70°", "?"))

@fig
def angle_sum_proof():
    return angle_sum_fig("angle_sum_proof", ("b", "c", "a"))

@fig
def fold_triangle():
    f = Fig("fold_triangle")
    B, C, A = asa(55, 8, 65)
    D = P(A[0], 0); M1, M2 = mul(add(A, B), 0.5), mul(add(A, C), 0.5)
    f.poly([B, C, A], fill="#fff3e0")
    f.seg(M1, M2, color=HELP, dash="6,4"); f.seg(M1, P(M1[0], 0), color=HELP, dash="6,4"); f.seg(M2, P(M2[0], 0), color=HELP, dash="6,4")
    f.dot(D, color=ASK)
    for p, n, o in ((A, "A", (0, 14)), (B, "B", (-10, -10)), (C, "C", (10, -10)), (D, "D", (0, -15))): f.label(add(p, o), n)
    f.angle(D, 0, 65, "C", 65, r=18, lr=32, color=ASK); f.angle(D, 65, 125, "A", 60, r=18, lr=32, color=ANS); f.angle(D, 125, 180, "B", 55, r=18, lr=32, color=GIVEN)
    caption(f, A[0], -38, "fold along the dashed lines: A, B and C all land on D", size=12)
    return f

@fig
def iso_50():
    f = Fig("iso_50")
    B, C, A = asa(65, 5, 65)
    tri(f, (B, C, A), "BCA")
    f.angle(A, 245, 295, "50°", 50, r=24, lr=40)
    f.angle(B, 0, 65, "?", 65, r=22, lr=38, color=ASK); f.angle(C, 115, 180, "?", 65, r=22, lr=38, color=ASK)
    f.ticks(B, A, 1); f.ticks(C, A, 1)
    return f

@fig
def exterior():
    f = Fig("exterior")
    B, C, A = asa(60, 5, 70)
    D = along(C, 0, 90)
    tri(f, (B, C, A), "BCA"); f.seg(C, D, dash="7,4"); f.dot(D); f.label(add(D, (6, -14)), "D")
    f.angle(A, 240, 290, "50°", 50, r=22, lr=38); f.angle(B, 0, 60, "60°", 60, r=24, lr=40)
    f.angle(C, 110, 180, "70°", 70, r=20, lr=34, color=ANS); f.angle(C, 0, 110, "110°", 110, r=28, lr=46, color=ASK)
    return f

# ---------------------------------------------------------------- altitudes
def foot(A, B, C):
    """Foot of the perpendicular from A to line BC."""
    return meet(A, dirto(B, C) + 90, B, dirto(B, C))

@fig
def altitudes():
    f = Fig("altitudes")
    B, C, A = asa(65, 7, 55)
    tri(f, (B, C, A), "BCA")
    for v, p, q, n in ((A, B, C, "D"), (B, C, A, "E"), (C, A, B, "F")):
        d = foot(v, p, q); f.seg(v, d, color=GIVEN, dash="6,4"); f.right(d, dirto(d, v) - 90, s=9, color=GIVEN)
        f.dot(d, color=GIVEN); f.label(along(d, dirto(v, d), 14), n, color=GIVEN)
    return f

@fig
def altitude_obtuse():
    f = Fig("altitude_obtuse")
    B, C = P(0, 0), P(150, 0); A = along(B, 125, 120)
    D = P(A[0], 0)
    tri(f, (B, C, A), "BCA"); f.seg(D, B, dash="7,4"); f.seg(A, D, color=GIVEN, w=2.4); f.right(D, 0, color=GIVEN)
    f.dot(D, color=GIVEN); f.label(add(D, (0, -15)), "D", color=GIVEN)
    f.angle(B, 0, 125, "125°", 125, r=18, lr=32)
    return f

@fig
def set_square():
    f = Fig("set_square")
    B, C = P(0, 0), P(240, 0); A = P(160, 120)
    f.poly([P(-20, -6), P(280, -6), P(280, -34), P(-20, -34)], fill="#fff9c4")      # the ruler
    for i in range(16): f.seg(P(-10 + 18 * i, -6), P(-10 + 18 * i, -14 if i % 5 else -20), w=1.2)
    f.poly([P(A[0], -6), P(A[0] + 60, -6), P(A[0], 170)], fill="#bbdefb")             # set square, upright edge through A
    tri(f, (B, C, A), "BCA")
    f.seg(A, P(A[0], 0), color=ASK, w=2.6); f.right(P(A[0], 0), 0, color=ASK)
    f.label(P(A[0] + 50, 70), "set square", size=12, anchor="start"); f.label(P(60, -21), "ruler", size=12)
    return f

@fig
def right_altitude():
    f = Fig("right_altitude")
    B, C, A = P(0, 0), P(170, 0), P(0, 110)
    tri(f, (B, C, A), "BCA"); f.right(B, 0, s=13)
    f.seg(A, B, color=ASK, w=3.2); f.seg(B, C, color=GIVEN, w=3.2)
    f.label(P(-30, 55), "AB ⊥ BC", color=ASK, size=12)
    return f

@fig
def types():
    f = Fig("types"); x = 0
    rows = [("equilateral", sss(2.6, 2.6, 2.6), ("1", "1", "1")), ("isosceles", sss(3, 2.6, 2.6), ("", "1", "1")),
            ("scalene", sss(3.4, 2, 2.8), ("", "", "")), ("acute-angled", asa(70, 3, 60), None),
            ("right-angled", asa(90, 2.4, 50), None), ("obtuse-angled", asa(115, 2.2, 35), None)]
    for i, (name, t, tk) in enumerate(rows):
        dx = P(x, 0 if i < 3 else -150); t = tuple(add(p, dx) for p in t)
        tri(f, t, ("", "", ""), dots=False)
        if tk:
            for j, n in enumerate(tk):
                if n: f.ticks(t[j], t[(j + 1) % 3], 1)
        else:
            for j in range(3):
                a = interior(t, j)
                if abs(a - 90) < 0.05: f.right(t[j], dirto(t[j], t[(j + 1) % 3]), s=10, color=ASK)
                else: iang(f, t, j, "", None, r=12, color=ASK if a > 90 else GIVEN)
        caption(f, centroid(*t)[0], dx[1] - 22, name, bold=True)
        x = 0 if i == 2 else x + 150
    return f

# ---------------------------------------------------------------- exercises
@fig
def ex1():
    f = Fig("ex1")
    B, C, A = sss(5, 6, 5)             # BC = 5, BA = 6, CA = 5
    tri(f, (B, C, A), "BCA")
    side(f, B, C, "5 cm", (B, C, A)); side(f, B, A, "6 cm", (B, C, A)); side(f, C, A, "5 cm", (B, C, A))
    D = foot(A, B, C); assert abs(dist(A, D) / CM - 4.8) < 1e-9
    f.seg(A, D, color=ANS, w=2.4); f.right(D, 0, color=ANS); f.dot(D, color=ANS); f.label(add(D, (0, -15)), "D", color=ANS)
    f.label(add(mul(add(A, D), 0.5), (-26, 0)), "4.8 cm", color=ANS, size=12)
    return f

@fig
def ex2():
    f = Fig("ex2")
    R, Y = P(0, 0), P(4 * CM, 0); T = along(R, 140, 7 * CM)
    D = P(T[0], 0)
    tri(f, (R, Y, T), "RYT"); f.angle(R, 0, 140, "140°", 140, r=18, lr=32)
    side(f, R, Y, "4 cm", (R, Y, T)); side(f, R, T, "7 cm", (R, Y, T))
    f.seg(D, R, dash="7,4"); f.seg(T, D, color=ANS, w=2.4); f.right(D, 0, color=ANS)
    f.dot(D, color=ANS); f.label(add(D, (0, -15)), "D", color=ANS)
    f.label(add(mul(add(T, D), 0.5), (-30, 0)), f"≈ {dist(T, D) / CM:.1f} cm", color=ANS, size=12)
    return f

@fig
def ex3():
    f = Fig("ex3"); A, C = P(0, 0), P(5 * CM, 0); r = 2.5 * CM; O = P(r, 0)
    f.carc(O, r, 0, 180, color=HELP, dash="5,4")
    f.seg(A, C, w=2.6); f.dot(A); f.dot(C); f.label(add(A, (-10, -10)), "A"); f.label(add(C, (10, -10)), "C")
    f.label(P(r, -16), "AC = 5 cm", color=GIVEN, size=13)
    for k, angA in enumerate((25, 45, 65)):
        B = meet(A, angA, C, 180 - (90 - angA))
        col = (GIVEN, ANS, ASK, "#6a1b9a")[k]
        f.seg(A, B, color=col, w=1.8); f.seg(C, B, color=col, w=1.8); f.dot(B, color=col)
        f.right(B, dirto(B, A), s=8, color=col)
        f.label(along(O, dirto(O, B), r + 14), f"B{k + 1}", color=col, size=12)
    return f

@fig
def ex4():
    f = Fig("ex4")
    t1 = asa(45, 4, 45); tri(f, t1, "ABC")
    f.right(t1[2], dirto(t1[2], t1[0]), s=10)
    assert abs(interior(t1, 2) - 90) < 1e-6
    iang(f, t1, 0, "45°", 45, r=22, lr=38); iang(f, t1, 1, "45°", 45, r=22, lr=38)
    f.ticks(t1[0], t1[2], 1); f.ticks(t1[1], t1[2], 1); caption(f, 2 * CM, -36, "right-angled isosceles", bold=True)
    t2 = asa(30, 5, 30, A=P(190, 0)); tri(f, t2, "PQR")
    iang(f, t2, 0, "30°", 30, r=30, lr=48); iang(f, t2, 1, "30°", 30, r=30, lr=48); iang(f, t2, 2, "120°", 120, r=14, lr=28, color=ANS)
    f.ticks(t2[0], t2[2], 1); f.ticks(t2[1], t2[2], 1); caption(f, 190 + 2.5 * CM, -36, "obtuse-angled isosceles", bold=True)
    return f

@fig
def spider_net():
    f = Fig("spider_net"); u = 40          # box 4 long, 2 wide, 1 high (units)
    S = P(0, 0)
    f.poly([S, P(4 * u, 0), P(4 * u, 1 * u), P(0, 1 * u)], fill="#ffe0b2")             # front face (height 1)
    f.poly([P(0, u), P(4 * u, u), P(4 * u, 3 * u), P(0, 3 * u)], fill="#fff3e0")        # top face (width 2), unfolded
    E = P(4 * u, 3 * u)
    f.seg(S, E, color=ASK, w=3); f.dot(S, color=ASK); f.dot(E, color=ASK)
    f.seg(S, P(4 * u, 0), color=GIVEN, w=2.4, dash="6,4"); f.seg(P(4 * u, 0), E, color=GIVEN, w=2.4, dash="6,4")
    f.label(add(S, (-26, -4)), "spider"); f.label(add(E, (24, 6)), "target")
    f.label(P(2 * u, -14), "4", size=12); f.label(P(4 * u + 12, u / 2), "1", size=12); f.label(P(4 * u + 12, 2 * u), "2", size=12)
    f.label(P(1.2 * u, 1.75 * u), "5", color=ASK, bold=True)
    f.label(P(2 * u, 0.5 * u), "front face", size=11, color=HELP); f.label(P(2 * u, 2.5 * u), "top face", size=11, color=HELP)
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
