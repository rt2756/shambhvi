"""Figures for class 7 maths Ch 9, Geometric Twins (congruence).
Triangles are built from their given measurements (1 cm = CM units); every labelled angle is
asserted against the drawn geometry by geo.Fig.angle, and equal sides marked with ticks are
asserted equal."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "9")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

CM = 30
FILL1, FILL2 = "#c8e6c9", "#ffe0b2"

# ---------------------------------------------------------------- helpers
def sss(ab, ac, bc, A=P(0, 0), rot=0):
    B = along(A, rot, ab * CM)
    x = (ab ** 2 + ac ** 2 - bc ** 2) / (2 * ab)
    return A, B, along(A, rot + math.degrees(math.acos(x / ac)), ac * CM)

def asa(angA, ab, angB, A=P(0, 0)):
    B = along(A, 0, ab * CM)
    return A, B, meet(A, angA, B, 180 - angB)

def centroid(*ps): return (sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps))

def tri(f, pts, names="ABC", fill=None, color=INK, dots=True):
    if fill: f.poly(list(pts), fill=fill, color=color)
    else:
        for i in range(3): f.seg(pts[i], pts[(i + 1) % 3], color=color)
    g = centroid(*pts)
    for p, n in zip(pts, names):
        if dots: f.dot(p, color=color)
        if n: f.label(along(p, dirto(g, p), 15), n)

def side(f, p, q, s, pts, color=GIVEN, off=13, size=13):
    g = centroid(*pts); m = mul(add(p, q), 0.5); n = dirto(p, q) + 90
    if dist(along(m, n, 1), g) < dist(along(m, n + 180, 1), g): n += 180
    w = len(s) * size * 0.56
    f.label(along(m, n, off + w / 2 * abs(math.cos(d2r(n)))), s, color=color, size=size)

def iang(f, pts, i, label, expect=None, r=20, color=GIVEN, lr=None):
    V, Pn, Pp = pts[i], pts[(i + 1) % 3], pts[(i - 1) % 3]
    f.angle(V, dirto(V, Pn), dirto(V, Pp), label, expect, r=r, color=color, lr=lr)

def interior(pts, i):
    V, Pn, Pp = pts[i], pts[(i + 1) % 3], pts[(i - 1) % 3]
    return (dirto(V, Pp) - dirto(V, Pn)) % 360

def eq_ticks(f, pairs, n, color=INK):
    """Tick n marks on each segment, after checking they really are equal."""
    L = [dist(p, q) for p, q in pairs]
    assert max(L) - min(L) < 1e-6, f"{f.name}: ticked sides differ {L}"
    for p, q in pairs: f.ticks(p, q, n, color=color)

def arcs(f, V, a1, a2, n=1, r=16, color=INK):
    """Unlabelled equal-angle marks: n arcs at V for the (smaller) angle between rays a1 and a2."""
    if (a2 - a1) % 360 > 180: a1, a2 = a2, a1
    for k in range(n): f.angle(V, a1, a2, "", r=r + 5 * k, color=color)

def name(f, p, s, o=(0, 14), color=INK):
    f.dot(p, color=color); f.label(add(p, o), s, color=color)

def caption(f, x, y, s, size=13, color=INK, bold=False):
    f.label(P(x, y), s, size=size, color=color, bold=bold)

def moved(pts, ang=0, flip=False, shift=(0, 0)):
    """Turn a shape about the origin, optionally flip it (mirror in the y-axis), then slide it."""
    out = []
    for x, y in pts:
        if flip: x = -x
        c, s = math.cos(d2r(ang)), math.sin(d2r(ang))
        out.append((x * c - y * s + shift[0], x * s + y * c + shift[1]))
    return out

# ---------------------------------------------------------------- 1.1 congruent figures
def bent(f, B, a, ang, l1=4, l2=8, labels=True, k=CM, names=True, color=INK):
    """The bent-arm symbol: BC along direction a, BA turned ang anticlockwise from it."""
    C, A = along(B, a, l2 * k), along(B, a + ang, l1 * k)
    f.seg(B, A, color=color, w=3); f.seg(B, C, color=color, w=3)
    if names:
        for p, s in ((A, "A"), (B, "B"), (C, "C")): f.dot(p); f.label(along(p, dirto(centroid(A, B, C), p), 14), s)
    if labels:
        f.angle(B, a, a + ang, f"{ang}°", ang, r=18, lr=34)
    return A, B, C

@fig
def symbol_arms():
    f = Fig("symbol_arms"); k = 20
    for i, ang in enumerate((40, 80, 130)):
        B = P(i * 270, 0)
        A, _, C = bent(f, B, 10, ang, k=k)
        f.label(along(mul(add(A, B), 0.5), 10 + ang + 90, 14), "4 cm", color=GIVEN, size=12)
        f.label(along(mul(add(B, C), 0.5), 10 - 90, 14), "8 cm", color=GIVEN, size=12)
    return f

@fig
def moves():
    f = Fig("moves")
    L = [(0, 0), (60, 0), (60, 20), (20, 20), (20, 80), (0, 80)]
    for i, (ang, flip, cap) in enumerate(((0, False, "original"), (0, False, "slid"), (90, False, "turned"), (0, True, "flipped"))):
        sh = (i * 130 + (60 if ang == 90 else 0) + (60 if flip else 0), 0)
        f.poly(moved(L, ang, flip, sh), fill=FILL1 if i else FILL2)
        caption(f, i * 130 + 30, -22, cap, bold=True)
    return f

@fig
def cy_bent():
    f = Fig("cy_bent")
    A, B, C = bent(f, P(0, 0), 0, 110, l1=3, l2=5, names=False)
    f.label(add(mul(add(A, B), 0.5), (-22, 0)), "3 cm", color=GIVEN, size=12); f.label(P(2.5 * CM, -14), "5 cm", color=GIVEN, size=12)
    B2 = P(330, 40); C2, A2 = along(B2, 200, 5 * CM), along(B2, 200 - 110, 3 * CM)   # turned and flipped
    f.seg(B2, A2, w=3); f.seg(B2, C2, w=3); f.angle(B2, 90, 200, "110°", 110, r=18, lr=34)
    f.label(add(mul(add(A2, B2), 0.5), (20, 0)), "3 cm", color=GIVEN, size=12)
    f.label(add(mul(add(B2, C2), 0.5), (4, -16)), "5 cm", color=GIVEN, size=12)
    return f

@fig
def cy_pairs():
    f = Fig("cy_pairs")
    tri_ = [(0, 0), (70, 0), (20, 50)]
    arrow = [(0, 10), (40, 10), (40, 25), (70, 0), (40, -25), (40, -10), (0, -10)]
    def star(R, r, n=6): return [along((0, 0), 90 + 180 * i / n, R if i % 2 == 0 else r) for i in range(2 * n)]
    house = lambda h: [(0, 0), (60, 0), (60, 40), (30, 40 + h), (0, 40)]
    rows = [("(a)", tri_, moved(tri_, 30, True)), ("(b)", arrow, moved(arrow, 90)),
            ("(c)", star(36, 16), star(46, 20)), ("(d)", house(25), house(40))]
    for i, (lab, s1, s2) in enumerate(rows):
        x, y = (i % 2) * 300, -(i // 2) * 160
        def place(s, dx):
            cx, cy = centroid(*s); return [(p[0] - cx + dx, p[1] - cy + y) for p in s]
        f.poly(place(s1, x + 60), fill=FILL2); f.poly(place(s2, x + 180), fill=FILL1)
        f.label(P(x, y + 45), lab, bold=True)
    return f

def branch(f, O, a, pr=2, rq=3, rs=2.5, ang=60, flip=False, k=26, show=True):
    """Segment PQ with a branch RS: PR, RQ along direction a, RS at ang to RQ."""
    s = -1 if flip else 1
    Pp = O; R = along(Pp, a, pr * k); Q = along(R, a, rq * k); S = along(R, a + s * ang, rs * k)
    f.seg(Pp, Q, w=3); f.seg(R, S, w=3)
    for p in (Pp, Q, R, S): f.dot(p)
    return Pp, R, Q, S

@fig
def cy_branch():
    f = Fig("cy_branch")
    Pp, R, Q, S = branch(f, P(0, 0), 0)
    for p, n, o in ((Pp, "P", (-10, -10)), (R, "R", (0, -15)), (Q, "Q", (10, -10)), (S, "S", (8, 10))): f.label(add(p, o), n)
    f.angle(R, 0, 60, "60°", 60, r=16, lr=30)
    f.label(P(26, -14), "2 cm", color=GIVEN, size=12); f.label(P(110, -30), "3 cm", color=GIVEN, size=12)
    f.label(add(mul(add(R, S), 0.5), (-22, 6)), "2.5 cm", color=GIVEN, size=12)
    # pair (a): the same figure turned and flipped; pair (b): branch at a different place
    caption(f, 360, 60, "(a)", bold=True)
    branch(f, P(330, -30), 30); branch(f, P(560, 40), -40, flip=True)
    caption(f, 360, -110, "(b)", bold=True)
    branch(f, P(330, -200), 30); branch(f, P(520, -200), 0, ang=95)
    return f

# ---------------------------------------------------------------- 1.2 SSS
@fig
def sss_two():
    f = Fig("sss_two")
    A, B, E = sss(6, 4, 8); F = (E[0], -E[1])
    for p in (E, F):
        a, b = dirto(A, p), dirto(B, p)
        f.carc(A, 4 * CM, a - 20, a + 20, color=GIVEN); f.carc(B, 8 * CM, b - 10, b + 10, color="#c62828")
    f.poly([A, B, E], fill=FILL1); f.poly([A, B, F], fill=FILL2)
    for p, n, o in ((A, "A", (-12, 8)), (B, "B", (12, 8)), (E, "E", (0, 14)), (F, "F", (0, -15))): name(f, p, n, o)
    f.label(P(3 * CM, 12), "6 cm", color=GIVEN, size=12)
    return f

@fig
def correspond():
    f = Fig("correspond")
    t = sss(5, 3, 4)
    tri(f, t, "ABC", fill=FILL1)
    u = tuple(add(p, (260, 140)) for p in moved(t, 150))
    tri(f, u, "XYZ", fill=FILL2)
    eq_ticks(f, [(t[0], t[1]), (u[0], u[1])], 1); eq_ticks(f, [(t[1], t[2]), (u[1], u[2])], 2); eq_ticks(f, [(t[0], t[2]), (u[0], u[2])], 3)
    return f

@fig
def rectangle_bd():
    f = Fig("rectangle_bd")
    A, B, C, D = P(0, 100), P(200, 100), P(200, 0), P(0, 0)
    f.poly([A, B, C, D], fill="#ffffff"); f.seg(B, D, color=GIVEN, w=2.4)
    for p, n, o in ((A, "A", (-10, 10)), (B, "B", (10, 10)), (C, "C", (10, -10)), (D, "D", (-10, -10))): name(f, p, n, o)
    for v, a in ((A, 270), (B, 180), (C, 90), (D, 0)): f.right(v, a)
    eq_ticks(f, [(A, B), (D, C)], 1); eq_ticks(f, [(A, D), (B, C)], 2)
    return f

@fig
def red_jam():
    f = Fig("red_jam")
    E, D, R = sss(5, 3.5, 6)                        # ED = 5, ER = 3.5, DR = 6
    tri(f, (E, D, R), "EDR")
    side(f, E, D, "5 cm", (E, D, R)); side(f, E, R, "3.5 cm", (E, D, R)); side(f, D, R, "6 cm", (E, D, R))
    J = P(270, 60)
    A = along(J, -50, 3.5 * CM)
    x = (3.5 ** 2 + 6 ** 2 - 5 ** 2) / (2 * 3.5)       # M from J: JM = 6, AM = 5
    M = along(J, -50 + math.degrees(math.acos(x / 6)), 6 * CM)
    t = (J, A, M); tri(f, t, "JAM")
    assert abs(dist(A, M) / CM - 5) < 1e-9
    side(f, J, A, "3.5 cm", t); side(f, A, M, "5 cm", t); side(f, J, M, "6 cm", t)
    return f

def reflect(p, a, b):
    """Mirror image of p in the line through a and b."""
    d = unit(dirto(a, b)); v = (p[0] - a[0], p[1] - a[1]); t = v[0] * d[0] + v[1] * d[1]
    foot = add(a, mul(d, t)); return add(foot, (foot[0] - p[0], foot[1] - p[1]))

@fig
def kite():
    f = Fig("kite")
    A, C = P(0, 0), P(70, -190); B = P(10, -150); D = reflect(B, A, C)
    f.seg(A, B); f.seg(B, C); f.seg(C, D); f.seg(D, A); f.seg(A, C, color=HELP, dash="6,4")
    for p, n, o in ((A, "A", (-8, 10)), (B, "B", (-12, 0)), (C, "C", (0, -15)), (D, "D", (12, 0))): name(f, p, n, o)
    eq_ticks(f, [(A, B), (A, D)], 1); eq_ticks(f, [(C, B), (C, D)], 2)
    return f

@fig
def kite_ans():
    f = kite(); f.name = "kite_ans"
    A, C = P(0, 0), P(70, -190); B = P(10, -150); D = reflect(B, A, C)
    a = dirto(A, C)
    arcs(f, A, dirto(A, B), a, 1, r=26, color=ANS); arcs(f, A, a, dirto(A, D), 1, r=30, color=ANS)
    arcs(f, C, a + 180, dirto(C, B), 2, r=18, color=ASK); arcs(f, C, a + 180, dirto(C, D), 2, r=22, color=ASK)
    return f

@fig
def dfe_ged():
    f = Fig("dfe_ged")
    D, E, F, G = P(0, 160), P(0, 40), P(-80, 0), P(80, 0)
    f.seg(D, F); f.seg(D, G); f.seg(F, E); f.seg(G, E); f.seg(D, E)
    for p, n, o in ((D, "D", (0, 14)), (E, "E", (0, -15)), (F, "F", (-10, -10)), (G, "G", (10, -10))): name(f, p, n, o)
    eq_ticks(f, [(D, F), (D, G)], 1); eq_ticks(f, [(F, E), (G, E)], 2)
    return f

# ---------------------------------------------------------------- AAA, SAS, SSA, ASA
@fig
def aaa():
    f = Fig("aaa"); x = 0
    for base in (3.5, 5, 6.5):
        t = asa(30, base, 70, A=P(x, 0)); tri(f, t, "BCA", dots=False)
        iang(f, t, 0, "30°", 30, r=18, lr=32); iang(f, t, 1, "70°", 70, r=16, lr=30); iang(f, t, 2, "80°", 80, r=14, lr=28)
        x += base * CM + 50
    return f

@fig
def ssa():
    f = Fig("ssa")
    Pp, Q = P(0, 0), P(6 * CM, 0)
    c = 6 * math.cos(d2r(30)); h = math.sqrt(c * c - 20)
    R, S = along(Pp, 30, (c - h) * CM), along(Pp, 30, (c + h) * CM)
    assert abs(dist(Q, R) - 4 * CM) < 1e-6 and abs(dist(Q, S) - 4 * CM) < 1e-6
    f.line(Pp, 30, 0, (c + h) * CM + 40, color=HELP); f.label(along(Pp, 30, (c + h) * CM + 52), "l")
    f.carc(Q, 4 * CM, 70, 160, color="#c62828", dash="5,4")
    f.poly([Pp, Q, R], fill=FILL2); f.seg(Q, S, color=GIVEN, w=2.4)
    f.seg(Pp, Q)
    for p, n, o in ((Pp, "P", (-10, -10)), (Q, "Q", (10, -10)), (R, "R", (-6, 14)), (S, "S", (0, 14))): name(f, p, n, o)
    f.angle(Pp, 0, 30, "30°", 30, r=40, lr=56)
    f.label(P(3 * CM, -15), "6 cm", color=GIVEN, size=12)
    f.label(add(mul(add(Q, R), 0.5), (4, 16)), "4 cm", color=GIVEN, size=12); f.label(add(mul(add(Q, S), 0.5), (16, 0)), "4 cm", color=GIVEN, size=12)
    return f

@fig
def midpoint_o():
    f = Fig("midpoint_o")
    O = P(0, 0); A, D = along(O, 145, 100), along(O, 325, 100); B, C = along(O, 210, 90), along(O, 30, 90)
    f.seg(A, D); f.seg(B, C); f.seg(A, B); f.seg(C, D)
    for p, n, o in ((A, "A", (-8, 10)), (B, "B", (-10, -8)), (C, "C", (10, 8)), (D, "D", (8, -10)), (O, "O", (0, -16))): name(f, p, n, o)
    eq_ticks(f, [(A, O), (O, D)], 1); eq_ticks(f, [(B, O), (O, C)], 2)
    f.angle(O, 145, 210, "", r=16, color=ASK); f.angle(O, 325, 390, "", r=16, color=ASK)
    return f

@fig
def sas_47():
    f = Fig("sas_47")
    B = P(0, 0); C = along(B, -8, 5 * CM); A = along(B, -8 + 47, 7 * CM)
    t = (B, C, A); tri(f, t, "BCA"); iang(f, t, 0, "47°", 47, r=20, lr=36)
    side(f, B, C, "5 cm", t); side(f, B, A, "7 cm", t)
    Z = P(390, 0); Y = along(Z, 188, 5 * CM); X = along(Z, 188 - 47, 7 * CM)
    u = (Z, X, Y); tri(f, u, "ZXY"); iang(f, u, 0, "47°", 47, r=20, lr=36)
    side(f, Z, Y, "5 cm", u); side(f, Z, X, "7 cm", u)
    return f

@fig
def par_cd_ab():
    f = Fig("par_cd_ab")
    A, B = P(0, 0), P(150, -14); D = P(20, 150); C = add(D, (B[0] - A[0], B[1] - A[1]))
    f.seg(A, B); f.seg(D, C); f.seg(D, B); f.seg(C, A)
    O = meet(D, dirto(D, B), A, dirto(A, C))
    for p, n, o in ((A, "A", (-10, -6)), (B, "B", (10, -8)), (C, "C", (10, 8)), (D, "D", (-10, 8)), (O, "O", (14, 0))): name(f, p, n, o)
    f.arrows(mul(add(A, B), 0.5), dirto(A, B)); f.arrows(mul(add(D, C), 0.5), dirto(D, C))
    eq_ticks(f, [(A, B), (D, C)], 1)
    return f

@fig
def par_cd_ab_ans():
    f = par_cd_ab(); f.name = "par_cd_ab_ans"
    A, B = P(0, 0), P(150, -14); D = P(20, 150); C = add(D, (B[0] - A[0], B[1] - A[1]))
    arcs(f, A, dirto(A, B), dirto(A, C), 1, r=22, color=ANS); arcs(f, C, dirto(C, D), dirto(C, A), 1, r=22, color=ANS)
    arcs(f, B, dirto(B, D), dirto(B, A), 2, r=20, color=ASK); arcs(f, D, dirto(D, B), dirto(D, C), 2, r=20, color=ASK)
    return f

@fig
def two_angle_pairs():
    f = Fig("two_angle_pairs")
    B, C, A = P(0, 0), P(200, 0), P(80, 90); D = reflect(A, B, C)
    f.seg(A, B); f.seg(A, C); f.seg(D, B); f.seg(D, C); f.seg(B, C)
    for p, n, o in ((A, "A", (0, 14)), (B, "B", (-12, 0)), (C, "C", (12, 0)), (D, "D", (0, -15))): name(f, p, n, o)
    arcs(f, B, 0, dirto(B, A), 1, r=22); arcs(f, B, dirto(B, D), 360, 1, r=22)
    arcs(f, C, dirto(C, A), 180, 2, r=18); arcs(f, C, 180, dirto(C, D), 2, r=18)
    return f

@fig
def cross_abdc():
    f = Fig("cross_abdc")
    B, C, A, D = P(0, 0), P(180, 0), P(-30, 150), P(210, 150)
    f.seg(A, B); f.seg(D, C); f.seg(B, C); f.seg(A, C); f.seg(B, D)
    for p, n, o in ((A, "A", (-8, 10)), (B, "B", (-8, -12)), (C, "C", (8, -12)), (D, "D", (8, 10))): name(f, p, n, o)
    arcs(f, B, dirto(B, D), dirto(B, A), 1, r=22); arcs(f, C, dirto(C, D), dirto(C, A), 1, r=22)
    arcs(f, B, 0, dirto(B, D), 2, r=30); arcs(f, C, dirto(C, A), 180, 2, r=30)
    mag = lambda V, p, q: min((dirto(V, p) - dirto(V, q)) % 360, (dirto(V, q) - dirto(V, p)) % 360)
    assert abs(mag(B, A, D) - mag(C, D, A)) < 1e-9 and abs(mag(C, A, B) - mag(B, D, C)) < 1e-9
    return f

@fig
def aas():
    f = Fig("aas")
    for x, (n1, n2, n3) in ((0, "BCA"), (230, "YZX")):
        t = asa(70, 4, 75, A=P(x, 0)); tri(f, t, (n1, n2, n3))
        iang(f, t, 2, "35°", 35, r=22, lr=38); iang(f, t, 1, "75°", 75, r=18, lr=34)
        iang(f, t, 0, "70°", 70, r=18, lr=34, color=ANS)
        side(f, t[0], t[1], "4 cm", t)
    return f

@fig
def rhs():
    f = Fig("rhs")
    Q, R = P(0, 0), P(4 * CM, 0); Pt, Pb = P(0, 3 * CM), P(0, -3 * CM)
    assert abs(dist(R, Pt) - 5 * CM) < 1e-9
    f.line(Q, 90, -4 * CM, 4 * CM, color=HELP); f.label(P(0, 4 * CM + 12), "l")
    f.carc(R, 5 * CM, 120, 240, color="#c62828", dash="5,4")
    f.poly([Q, R, Pt], fill=FILL1); f.poly([Q, R, Pb], fill=FILL2)
    f.right(Q, 0); f.right(Q, 270)
    for p, n, o in ((Q, "Q", (-12, 0)), (R, "R", (12, 0)), (Pt, "P", (-12, 4)), (Pb, "P′", (-14, -4))): name(f, p, n, o)
    f.label(P(2 * CM, -14), "4 cm", color=GIVEN, size=12)
    f.label(add(mul(add(Pt, R), 0.5), (14, 10)), "5 cm", color=GIVEN, size=12); f.label(add(mul(add(Pb, R), 0.5), (14, -10)), "5 cm", color=GIVEN, size=12)
    return f

@fig
def iso_altitude():
    f = Fig("iso_altitude")
    B, C, A = asa(50, 6, 50); D = P(A[0], 0)
    t = (B, C, A); tri(f, t, "BCA"); f.seg(A, D, color=GIVEN, dash="6,4"); f.right(D, 0, color=GIVEN)
    name(f, D, "D", (0, -15), color=GIVEN)
    iang(f, t, 2, "80°", 80, r=20, lr=36)
    eq_ticks(f, [(A, B), (A, C)], 1)
    return f

# ---------------------------------------------------------------- exercises
@fig
def ex_ob_oc():
    f = Fig("ex_ob_oc")
    O = P(0, 0); A, D = along(O, 115, 110), along(O, 295, 110); B, C = along(O, 205, 90), along(O, 25, 90)
    f.seg(A, D); f.seg(B, C); f.seg(A, B); f.seg(C, D)
    for p, n, o in ((A, "A", (-8, 10)), (B, "B", (-12, -4)), (C, "C", (10, 8)), (D, "D", (8, -12)), (O, "O", (14, 4))): name(f, p, n, o)
    eq_ticks(f, [(O, A), (O, D)], 1); eq_ticks(f, [(O, B), (O, C)], 2)
    return f

@fig
def ex_ob_oc_ans():
    f = ex_ob_oc(); f.name = "ex_ob_oc_ans"
    O = P(0, 0); A, D = along(O, 115, 110), along(O, 295, 110); B, C = along(O, 205, 90), along(O, 25, 90)
    arcs(f, A, dirto(A, B), dirto(A, D), 1, r=20, color=ANS); arcs(f, D, dirto(D, C), dirto(D, A), 1, r=20, color=ANS)
    f.arrows(mul(add(A, B), 0.5), dirto(B, A), color=ANS); f.arrows(mul(add(D, C), 0.5), dirto(D, C), color=ANS)
    return f

@fig
def ex_square():
    f = Fig("ex_square")
    A, B, C, D = P(0, 140), P(140, 140), P(140, 0), P(0, 0)
    f.poly([A, B, C, D], fill="#ffffff"); f.seg(A, C, color=GIVEN, w=2.4)
    for p, n, o in ((A, "A", (-10, 10)), (B, "B", (10, 10)), (C, "C", (10, -10)), (D, "D", (-10, -10))): name(f, p, n, o)
    for v, a in ((A, 270), (B, 180), (C, 90), (D, 0)): f.right(v, a)
    eq_ticks(f, [(A, B), (B, C), (C, D), (D, A)], 1)
    return f

@fig
def ex_circle():
    f = Fig("ex_circle")
    A = P(0, 0); r = 100; B, C = along(A, 210, r), along(A, 330, r)
    f.circle(A, r, color=INK, w=2); f.seg(A, B); f.seg(A, C); f.seg(B, C)
    for p, n, o in ((A, "A", (0, 14)), (B, "B", (-12, -6)), (C, "C", (12, -6))): name(f, p, n, o)
    f.angle(A, 210, 330, "120°", 120, r=16, lr=30)
    f.angle(B, 0, 30, "?", 30, r=36, lr=50, color=ASK); f.angle(C, 150, 180, "?", 30, r=36, lr=50, color=ASK)
    return f

def iso_part(f, x, apex, labels, ticks_all=False, right=False):
    """Isosceles triangle on a 4 cm base at x, with the given apex angle."""
    base = (180 - apex) / 2
    t = asa(base, 4, base, A=P(x, 0)); tri(f, t, ("", "", ""), dots=False)
    la, lb, lc = labels
    if right: f.right(t[2], dirto(t[2], t[0]))
    else: iang(f, t, 2, la, apex, r=16, lr=30, color=GIVEN if la not in ("?", "x") else ASK)
    iang(f, t, 0, lb, base, r=18, lr=32, color=GIVEN if lb not in ("?", "x") else ASK)
    iang(f, t, 1, lc, base, r=18, lr=32, color=GIVEN if lc not in ("?", "x") else ASK)
    eq_ticks(f, [(t[0], t[2]), (t[1], t[2])], 1)
    if ticks_all: eq_ticks(f, [(t[0], t[1]), (t[0], t[2])], 1)
    return t

@fig
def ex6a():
    f = Fig("ex6a"); iso_part(f, 0, 68, ("68°", "?", "?")); return f
@fig
def ex6b():
    f = Fig("ex6b"); iso_part(f, 0, 34, ("34°", "?", "?")); return f
@fig
def ex6c():
    f = Fig("ex6c"); iso_part(f, 0, 90, ("", "?", "?"), right=True); return f
@fig
def ex6d():
    f = Fig("ex6d")
    t = asa(60, 4, 60); tri(f, t, ("", "", ""), dots=False)
    for i in range(3): iang(f, t, i, "?", 60, r=16, lr=30, color=ASK)
    eq_ticks(f, [(t[0], t[1]), (t[1], t[2]), (t[2], t[0])], 1)
    return f
@fig
def ex6e():
    f = Fig("ex6e")
    t = asa(44, 4, 44); tri(f, t, ("", "", ""), dots=False)
    iang(f, t, 0, "44°", 44, r=20, lr=36); iang(f, t, 1, "?", 44, r=20, lr=36, color=ASK); iang(f, t, 2, "?", 92, r=14, lr=28, color=ASK)
    eq_ticks(f, [(t[0], t[2]), (t[1], t[2])], 1)
    return f
@fig
def ex6f():
    f = Fig("ex6f")
    B, C, A = asa(56, 5, 56); D = P(A[0], 0)
    t = (B, C, A); tri(f, t, "BCA"); f.seg(A, D); f.right(D, 0); name(f, D, "D", (0, -15))
    f.angle(A, 270 - 34, 270, "34°", 34, r=34, lr=50); f.angle(A, 270, 270 + 34, "?", 34, r=34, lr=50, color=ASK)
    iang(f, t, 0, "?", 56, r=18, lr=32, color=ASK); iang(f, t, 1, "?", 56, r=18, lr=32, color=ASK)
    eq_ticks(f, [(A, B), (A, C)], 1)
    return f

GRID_SOL = ["aaabb", "ccadb", "ec#db", "ecddf", "eefff"]      # found by trying every tetromino shape
COLS = {"a": "#c8e6c9", "b": "#ffe0b2", "c": "#bbdefb", "d": "#f8bbd0", "e": "#fff59d", "f": "#d1c4e9"}

def grid(f, sol=None, s=40):
    for r in range(5):
        for c in range(5):
            x, y = c * s, (4 - r) * s
            ch = GRID_SOL[r][c]
            fill = "#4caf50" if ch == "#" else (COLS[ch] if sol else "#ffffff")
            f.poly([P(x, y), P(x + s, y), P(x + s, y + s), P(x, y + s)], fill=fill, color=HELP)
    if sol:      # thick lines between different regions
        for r in range(5):
            for c in range(5):
                x, y = c * s, (4 - r) * s
                if c < 4 and GRID_SOL[r][c] != GRID_SOL[r][c + 1]: f.seg(P(x + s, y), P(x + s, y + s), w=4)
                if r < 4 and GRID_SOL[r][c] != GRID_SOL[r + 1][c]: f.seg(P(x, y), P(x + s, y), w=4)
        f.seg(P(0, 0), P(5 * s, 0), w=4); f.seg(P(5 * s, 0), P(5 * s, 5 * s), w=4); f.seg(P(5 * s, 5 * s), P(0, 5 * s), w=4); f.seg(P(0, 5 * s), P(0, 0), w=4)

@fig
def puzzle_q():
    f = Fig("puzzle_q"); grid(f); return f

@fig
def puzzle_a():
    f = Fig("puzzle_a")
    from collections import Counter
    cnt = Counter("".join(GRID_SOL).replace("#", "")); assert set(cnt.values()) == {4} and len(cnt) == 6
    grid(f, sol=True); return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
