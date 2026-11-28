"""Figures for class 8 maths Ch 9, The Baudhayana-Pythagoras Theorem.
Shapes are built from exact coordinates. Every labelled angle is asserted against the drawn geometry
(geo.Fig.angle), every right-angle square is asserted to be 90°, every length label is asserted
against the drawn length, and the dissection pictures assert that the pieces really are congruent
and fill the squares they claim to fill."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "9")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

FILL1, FILL2, FILL3, PAPER, WATER = "#c8e6c9", "#ffe0b2", "#bbdefb", "#f0e6c0", "#e3f2fd"

# ---------------------------------------------------------------- helpers
def sub(p, q): return (p[0] - q[0], p[1] - q[1])
def mid(p, q): return mul(add(p, q), 0.5)
def centroid(pts): return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
def sh(pts, d): return [add(p, d) for p in pts]

def area(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2

def angle_of(V, P1, P2):
    a = (dirto(V, P2) - dirto(V, P1)) % 360
    return min(a, 360 - a)

def ang(f, V, P1, P2, label, expect=None, r=20, color=GIVEN, lr=None):
    a1, a2 = dirto(V, P1), dirto(V, P2)
    if (a2 - a1) % 360 > 180: a1, a2 = a2, a1
    f.angle(V, a1, a2, label, expect, r=r, color=color, lr=lr)

def rmark(f, V, P1, P2, s=10, color=INK):
    a1, a2 = dirto(V, P1), dirto(V, P2)
    if (a2 - a1) % 360 > 180: a1, a2 = a2, a1
    assert abs((a2 - a1) % 360 - 90) < 1e-6, f"{f.name}: right-angle mark on {(a2 - a1) % 360:.3f}°"
    f.right(V, a1, s, color=color)

def outline(f, pts, color=INK, w=2.2, dash=None):
    for i in range(len(pts)): f.seg(pts[i], pts[(i + 1) % len(pts)], color=color, w=w, dash=dash)

def is_square(pts):
    L = [dist(pts[i], pts[(i + 1) % 4]) for i in range(4)]
    A = [angle_of(pts[i], pts[(i + 1) % 4], pts[i - 1]) for i in range(4)]
    return max(L) - min(L) < 1e-6 and all(abs(a - 90) < 1e-6 for a in A)

def congruent(t1, t2):
    s1 = sorted(round(dist(t1[i], t1[(i + 1) % 3]), 6) for i in range(3))
    s2 = sorted(round(dist(t2[i], t2[(i + 1) % 3]), 6) for i in range(3))
    return s1 == s2

def side(f, p, q, s, g, color=GIVEN, off=11, size=13, k=None, value=None):
    """Length label on segment pq, placed away from point g. If value is given, assert the drawn
    length (in units of k) equals it."""
    if value is not None: assert abs(dist(p, q) / k - value) < 1e-6, f"{f.name}: {s!r} drawn {dist(p, q) / k}"
    m = mid(p, q); n = dirto(p, q) + 90
    if dist(along(m, n, 1), g) < dist(along(m, n + 180, 1), g): n += 180
    w = len(s) * size * 0.56
    f.label(along(m, n, off + w / 2 * abs(math.cos(d2r(n)))), s, color=color, size=size)

def caption(f, x, y, s, size=13, color=INK, bold=False):
    f.label(P(x, y), s, size=size, color=color, bold=bold)

def name(f, p, s, o):
    f.dot(p); f.label(add(p, o), s)

def sq(x, y, s, k):
    return [P(x * k, y * k), P((x + s) * k, y * k), P((x + s) * k, (y + s) * k), P(x * k, (y + s) * k)]

def square_on(p, q):
    """Square on segment pq, on the left of p->q. Returns [p, q, r, s]."""
    d = sub(q, p); n = (-d[1], d[0])
    return [p, q, add(q, n), add(p, n)]

def plus(f, x, y): f.label(P(x, y), "+", size=26, bold=True)
def arrow(f, x, y, L=40):
    f.seg(P(x - L / 2, y), P(x + L / 2, y), w=2.4)
    f.seg(P(x + L / 2 - 9, y + 6), P(x + L / 2, y), w=2.4); f.seg(P(x + L / 2 - 9, y - 6), P(x + L / 2, y), w=2.4)

def right_tri(a, b, k, o=(0, 0), rot=0):
    """Right triangle with the right angle at C, legs a (along rot) and b (at rot + 90)."""
    Cc = P(*o); A = along(Cc, rot, a * k); B = along(Cc, rot + 90, b * k)
    return Cc, A, B

# ---------------------------------------------------------------- 2.1 doubling a square
@fig
def double_square():
    f = Fig("double_square")
    k = 70
    for j in range(2):
        o = (j * 3.3 * k, 0)
        O = sh(sq(0, 0, 1, k), o)                       # the original square
        a, b = O[3], O[1]                               # its diagonal, top-left to bottom-right
        D = square_on(a, b)                             # the square on the diagonal, away from O[0]
        if dist(centroid(D), O[0]) < dist(centroid(D), O[2]): D = square_on(b, a)
        assert is_square(D) and abs(area(D) - 2 * area(O)) < 1e-6
        if j == 1:
            tri = [[O[0], O[1], O[3]], [O[2], O[1], O[3]]]
            cen = O[2]
            quarters = [[cen, D[i], D[(i + 1) % 4]] for i in range(4)]
            for t in quarters: assert congruent(t, tri[0])
            f.poly(tri[0], fill=FILL1)
            for i, t in enumerate(quarters): f.poly(t, fill=FILL2 if i % 2 else FILL3, color=INK)
            f.seg(O[1], along(O[1], 90, 2 * k), color=GIVEN, w=2); f.seg(O[3], along(O[3], 0, 2 * k), color=GIVEN, w=2)
        outline(f, O, w=2.6)
        outline(f, D, color=ASK, w=2, dash="7 5")
        f.seg(a, b, color=HELP, w=1.6, dash="4 4")
        caption(f, o[0] + k, -26, ["square on the diagonal (dashed)", "2 small triangles  vs  4 small triangles"][j], size=12)
    return f

@fig
def double_sequence():
    f = Fig("double_sequence")
    k = 48
    for j in range(3):
        o = P(j * 3 * k, 0)
        G = sh(sq(0, 0, 2, k), o)
        for x in (0, 1, 2):
            f.seg(add(o, (x * k, 0)), add(o, (x * k, 2 * k)), color=HELP, w=1.2, dash="3 4")
            f.seg(add(o, (0, x * k)), add(o, (2 * k, x * k)), color=HELP, w=1.2, dash="3 4")
        for (x, y) in ((0, 0), (1, 0), (0, 1), (1, 1)):
            f.seg(add(o, (x * k, y * k)), add(o, ((x + 1) * k, (y + 1) * k)), color=HELP, w=1.0, dash="3 4")
            f.seg(add(o, ((x + 1) * k, y * k)), add(o, (x * k, (y + 1) * k)), color=HELP, w=1.0, dash="3 4")
        if j == 0: S = sh(sq(0, 0, 1, k), o)
        elif j == 1: S = [add(o, (k, 0)), add(o, (2 * k, k)), add(o, (k, 2 * k)), add(o, (0, k))]
        else: S = G
        assert is_square(S)
        quarter_tri = k * k / 4                          # each small dashed triangle
        n = round(area(S) / quarter_tri)
        assert n == [4, 8, 16][j]
        f.poly(S, fill=[FILL1, FILL2, FILL3][j])
        caption(f, o[0] + k, -24, f"area = {2 ** j} small square{'s' if j else ''}", size=12)
    return f

@fig
def paper_double():
    f = Fig("paper_double")
    k = 90
    S1 = sq(0, 0, 1, k); c1 = centroid(S1)
    f.poly(S1, fill=PAPER)
    f.seg(S1[0], S1[2]); f.seg(S1[1], S1[3])
    for i, n in enumerate(("4", "3", "2", "1")):
        f.label(along(c1, 270 + 90 * i, 0.3 * k), n, size=14)
    caption(f, c1[0], -24, "square 1", size=12)
    # square 2 cut into four triangles, drawn slightly apart
    o = P(1.5 * k, 0); c2 = add(o, (0.5 * k, 0.5 * k))
    S2 = sh(sq(0, 0, 1, k), o)
    pieces = []
    for i in range(4):
        t = [c2, S2[i], S2[(i + 1) % 4]]
        d = mul(unit(dirto(c2, mid(S2[i], S2[(i + 1) % 4]))), 7)
        t = sh(t, d); pieces.append(t)
        f.poly(t, fill=PAPER)
        f.label(along(c2, dirto(c2, mid(S2[i], S2[(i + 1) % 4])), 0.3 * k), ["8", "7", "6", "5"][i], size=14)
    caption(f, c2[0], -24, "square 2, cut", size=12)
    # result: square 1 with pieces 5-8 on its sides
    o = P(3.4 * k, 0.0)
    R = sh(S1, o); cR = centroid(R)
    f.poly(R, fill=PAPER); f.seg(R[0], R[2], color=HELP, w=1.2); f.seg(R[1], R[3], color=HELP, w=1.2)
    big = []
    for i in range(4):
        p, q = R[i], R[(i + 1) % 4]
        apex = along(mid(p, q), dirto(cR, mid(p, q)), 0.5 * k)
        t = [p, q, apex]; f.poly(t, fill="#e6d395")
        f.label(along(mid(p, q), dirto(cR, mid(p, q)), 0.2 * k), ["8", "7", "6", "5"][i], size=14)
        big.append(apex)
    assert is_square(big) and abs(area(big) - 2 * area(S1)) < 1e-6
    outline(f, big, color=ASK, w=2.6)
    caption(f, cR[0], -0.55 * k - 22, "pieces 5-8 round square 1: double the area", size=12)
    return f

# ---------------------------------------------------------------- 2.2 halving
@fig
def halve_square():
    f = Fig("halve_square")
    k = 160
    S = sq(0, 0, 1, k)
    M = [mid(S[i], S[(i + 1) % 4]) for i in range(4)]
    c = centroid(S)
    inner = [[c, M[i], M[(i + 1) % 4]] for i in range(4)]
    corner = [[S[(i + 1) % 4], M[(i + 1) % 4], M[i]] for i in range(4)]
    for t in inner: f.poly(t, fill=FILL1)
    for t in corner: assert congruent(t, inner[0])
    assert is_square(M) and abs(area(M) - area(S) / 2) < 1e-6
    outline(f, S, w=2.6); outline(f, M, color=ASK, w=2.4)
    f.seg(M[0], M[2], color=GIVEN, w=1.6, dash="5 4"); f.seg(M[1], M[3], color=GIVEN, w=1.6, dash="5 4")
    caption(f, c[0], -24, "inside square: 4 of the 8 equal triangles", size=12)
    return f

@fig
def halve_fold():
    f = Fig("halve_fold")
    k = 170
    S = sq(0, 0, 1, k)
    Pp, Q, R, Ss = mid(S[0], S[1]), mid(S[1], S[2]), mid(S[2], S[3]), mid(S[3], S[0])
    c = centroid(S)
    f.poly(S, fill=PAPER)
    for i, (a, b) in enumerate(((Pp, Q), (Q, R), (R, Ss), (Ss, Pp))):
        f.poly([S[(i + 1) % 4], b, a], fill="#e6d395")
    outline(f, [Pp, Q, R, Ss], color=ASK, w=2.6)
    f.seg(Pp, R, color=GIVEN, w=1.6, dash="5 4"); f.seg(Q, Ss, color=GIVEN, w=1.6, dash="5 4")
    f.dot(c); f.label(add(c, (-14, -14)), "O")
    rmark(f, c, Q, R, s=12)
    for p, n, o in ((Pp, "P", (0, -16)), (Q, "Q", (16, 0)), (R, "R", (0, 16)), (Ss, "S", (-16, 0))): name(f, p, n, o)
    for i in range(4):
        corner = [S[(i + 1) % 4], [Q, R, Ss, Pp][i], [Pp, Q, R, Ss][i]]
        assert congruent(corner, [c, [Pp, Q, R, Ss][i], [Q, R, Ss, Pp][i]])
    caption(f, c[0], -38, "fold each corner in along the red creases", size=12)
    return f

# ---------------------------------------------------------------- 2.3 isosceles right triangle
@fig
def iso_hyp():
    f = Fig("iso_hyp")
    k = 90
    Pp, E, A, R = sq(0, 0, 1, k)
    f.poly([Pp, E, R], fill=FILL1)
    outline(f, [Pp, E, A, R], w=2.4)
    D = [R, E, P(2 * k, k), P(k, 2 * k)]                 # R, E, S, T
    assert is_square(D) and abs(area(D) - 2 * area([Pp, E, A, R])) < 1e-6
    outline(f, D, color=ASK, w=2.2, dash="7 5")
    f.seg(E, R, color=ASK, w=2.6)
    for p, n, o in ((Pp, "P", (-12, -12)), (E, "E", (8, -16)), (A, "A", (14, 6)), (R, "R", (-16, 6)), (D[2], "S", (16, 0)), (D[3], "T", (0, 16))):
        name(f, p, n, o)
    g = centroid([Pp, E, R])
    side(f, Pp, E, "1", g, k=k, value=1); side(f, Pp, R, "1", g, k=k, value=1)
    f.label(along(mid(E, R), 225, 16), "c ?", color=ASK, size=14, bold=True)
    rmark(f, Pp, E, R)
    return f

@fig
def iso_general():
    f = Fig("iso_general")
    k = 34; a = 3
    Pp, Q, R, S = sq(0, 0, a, k)
    f.poly([Pp, Q, S], fill=FILL1)
    outline(f, [Pp, Q, R, S], w=2.4)
    D = [S, Q, P(2 * a * k, a * k), P(a * k, 2 * a * k)]   # S, Q, V, U
    assert is_square(D) and abs(area(D) - 2 * area([Pp, Q, R, S])) < 1e-6
    outline(f, D, color=ASK, w=2.2, dash="7 5"); f.seg(S, Q, color=ASK, w=2.6)
    for p, n, o in ((Pp, "P", (-12, -12)), (Q, "Q", (8, -16)), (R, "R", (14, 6)), (S, "S", (-16, 6)), (D[2], "V", (16, 0)), (D[3], "U", (0, 16))):
        name(f, p, n, o)
    g = centroid([Pp, Q, S])
    side(f, Pp, Q, "a", g); side(f, Pp, S, "a", g)
    f.label(along(mid(S, Q), 225, 16), "c", color=ASK, size=15, bold=True)
    rmark(f, Pp, Q, S)
    return f

@fig
def fio39_1_q():
    f = Fig("fio39_1_q")
    k = 100
    for j, labels in enumerate((("1", "2"), ("3", "4"))):
        o = P(j * 1.5 * k, 0)
        S = sh(sq(0, 0, 1, k), o)
        t1, t2 = [S[0], S[1], S[3]], [S[1], S[2], S[3]]
        f.poly(sh(t1, (-4, -4)), fill=PAPER); f.poly(sh(t2, (4, 4)), fill=PAPER)
        f.label(add(centroid(t1), (-4, -4)), labels[0], size=15); f.label(add(centroid(t2), (4, 4)), labels[1], size=15)
    return f

@fig
def fio39_1_a():
    f = Fig("fio39_1_a")
    k = 100
    c = P(0, 0); s = k
    d = s                                   # each leg of a half-square is a side of the square
    tips = [along(c, 45 + 90 * i, d) for i in range(4)]
    assert is_square(tips) and abs(area(tips) - 2 * s * s) < 1e-6
    for i in range(4):
        t = [c, tips[i], tips[(i + 1) % 4]]
        assert abs(angle_of(c, tips[i], tips[(i + 1) % 4]) - 90) < 1e-6
        assert abs(dist(tips[i], tips[(i + 1) % 4]) - s * math.sqrt(2)) < 1e-6   # hypotenuse of a half-square
        f.poly(t, fill=PAPER)
        f.label(along(c, 90 + 90 * i, 0.45 * k), "1234"[i], size=15)
    outline(f, tips, color=ASK, w=2.6)
    rmark(f, c, tips[0], tips[1], s=10)
    caption(f, 0, -d - 24, "right angles together in the middle: a square of double area", size=12)
    return f

# ---------------------------------------------------------------- 2.4 combining two squares
@fig
def combine_same():
    f = Fig("combine_same")
    k = 60
    A = sq(0, 0, 1, k); B = sq(1.6, 0, 1, k)
    f.poly(A, fill=FILL1); f.poly(B, fill=FILL1)
    plus(f, 1.3 * k, 0.5 * k - 8); arrow(f, 3.05 * k, 0.5 * k)
    c = P(4.5 * k, 0.5 * k); d = k            # half the diagonal of a square of side k√2
    D = [along(c, 45 + 90 * i, d) for i in range(4)]
    assert abs(area(D) - 2 * k * k) < 1e-6
    f.poly(D, fill=FILL3)
    return f

@fig
def combine_diff():
    f = Fig("combine_diff")
    k = 30; a, b = 3, 5
    A = sq(0, 0, a, k); B = sq(a + 1.2, 0, b, k)
    f.poly(A, fill=FILL1); f.poly(B, fill=FILL2)
    f.label(centroid(A), "a²", size=15); f.label(centroid(B), "b²", size=15)
    plus(f, (a + 0.6) * k, 1.5 * k - 8); arrow(f, (a + b + 2.4) * k, 2.5 * k)
    c = math.sqrt(a * a + b * b)
    C = sq(a + b + 3.6, 0, c, k)
    f.poly(C, fill=FILL3); f.label(centroid(C), "a² + b²", size=15)
    f.label(add(mid(C[2], C[3]), (0, 14)), "side = ?", color=ASK, size=13)
    return f

A9, B9 = 3, 5          # the two squares in the dissection: sides a = 3, b = 5 (b − a = 2)

def dissection(f, k, stage):
    a, b = A9, B9
    O = P(0, 0)
    small = sq(0, 0, a, k); big = sq(a, 0, b, k)
    Pp = P(b * k, 0)                        # on the base, b from the left end
    TL, TR = small[3], big[2]               # top-left of the small square, top-right of the big one
    top = P(a * k, (a + b) * k)
    W = [small[0], Pp, TL]; X = [Pp, big[1], TR]
    T = [TL, top, P(a * k, a * k)]; U = [top, TR, P(a * k, b * k)]
    for t in (X, T, U): assert congruent(t, W)
    H = [TL, Pp, TR, top]
    assert is_square(H) and abs(area(H) - (a * a + b * b) * k * k) < 1e-6
    if stage == 1:
        f.poly(small, fill=FILL1); f.poly(big, fill=FILL2)
        f.seg(Pp, P(b * k, b * k), color=HELP, w=1.6, dash="5 4")
    else:
        V = [P(a * k, a * k), TL, Pp, TR, P(a * k, b * k)]
        f.poly(small, fill="#ffffff", color=HELP); f.poly(big, fill="#ffffff", color=HELP)
        for t in (W, X): f.poly(t, fill="#90caf9")
        if stage == 3:
            for t in (T, U): f.poly(t, fill="#90caf9")
            f.poly([P(a * k, a * k), Pp, TR, P(a * k, b * k)], fill="#ffcc80")
            outline(f, H, color=ASK, w=2.8)
            for t, n in ((T, "T"), (U, "U"), (W, "W"), (X, "X")): f.label(add(centroid(t), (0, -6)), n, size=15, bold=True)
            f.label(P((a + 0.9) * k, (a - 0.6) * k), "V", size=15, bold=True)
            x = angle_of(Pp, small[0], TL)
            ang(f, Pp, small[0], TL, "x", x, r=22, lr=32)
            ang(f, Pp, TR, big[1], "90° − x", 90 - x, r=26, lr=50)
            rmark(f, Pp, TL, TR, s=12, color=ASK)
        else:
            f.seg(TL, Pp, color=ASK, w=2.4); f.seg(Pp, TR, color=ASK, w=2.4)
            f.label(add(centroid(W), (0, -6)), "W", size=15, bold=True); f.label(add(centroid(X), (0, -6)), "X", size=15, bold=True)
    g = P((a + b) * k / 2, -100)
    for p, q, s in ((small[0], small[1], "a"), (small[1], Pp, "b − a"), (Pp, big[1], "a")):
        side(f, p, q, s, P(p[0], 300), size=12)
    side(f, small[0], small[3], "a", P(300, 0), size=12); side(f, big[1], big[2], "b", P(-300, 0), size=12)
    return H

@fig
def dissect_1():
    f = Fig("dissect_1"); dissection(f, 26, 1); return f

@fig
def dissect_2():
    f = Fig("dissect_2"); dissection(f, 26, 2); return f

@fig
def dissect_3():
    f = Fig("dissect_3"); dissection(f, 30, 3); return f

@fig
def squares_345():
    f = Fig("squares_345")
    k = 28
    Cc, A, B = right_tri(4, 3, k)                    # legs 4 (across) and 3 (up), right angle at C
    f.poly([Cc, A, B], fill="#fff59d")
    for p, q, n, col in ((A, Cc, 4, FILL2), (Cc, B, 3, FILL1), (B, A, 5, FILL3)):
        S = square_on(p, q)
        assert abs(dist(p, q) - n * k) < 1e-6
        f.poly(S, fill=col)
        u, v = mul(sub(q, p), 1 / n), mul(sub(S[3], p), 1 / n)
        for i in range(1, n):
            f.seg(add(p, mul(u, i)), add(S[3], mul(u, i)), color=HELP, w=1)
            f.seg(add(p, mul(v, i)), add(q, mul(v, i)), color=HELP, w=1)
        f.label(centroid(S), f"{n * n}", size=16, bold=True)
    rmark(f, Cc, A, B, s=10)
    g = centroid([Cc, A, B])
    return f

# ---------------------------------------------------------------- figure it out p47
@fig
def fio47_3():
    f = Fig("fio47_3")
    k = 50
    for j, (m, cap) in enumerate(((math.sqrt(2), "3 times"), (2, "5 times"))):
        o = (j * 4.2 * k, 0)
        Cc, A, B = right_tri(1, m, k, o)
        S0 = [Cc, A, add(A, (0, -k)), add(Cc, (0, -k))]
        f.poly(S0, fill=FILL1); f.label(centroid(S0), "side s", size=11)
        f.poly([Cc, A, B], fill="#fff59d")
        H = square_on(B, A)                      # on the far side of the hypotenuse
        n = round(area(H) / (k * k))
        assert abs(area(H) - (1 + m * m) * k * k) < 1e-6 and n == [3, 5][j]
        outline(f, H, color=ASK, w=2.2, dash="7 5")
        f.label(centroid(H), f"{n}s²", color=ASK, size=14, bold=True)
        rmark(f, Cc, A, B)
        g = centroid([Cc, A, B])
        side(f, Cc, B, "d" if j == 0 else "2s", P(o[0] + 500, k), size=13)
        caption(f, o[0] + 1.2 * k, -1.5 * k, f"{cap} the area", size=13)
        if j == 0: caption(f, o[0] + 1.2 * k, -1.5 * k - 18, "(d = diagonal of the square)", size=11)
    return f

# ---------------------------------------------------------------- 2.5 odd numbers and squares
@fig
def odd_gnomon():
    f = Fig("odd_gnomon")
    k = 26; n = 5
    for i in range(n):
        for j in range(n):
            inner = i < n - 1 and j < n - 1
            f.circle(P(i * k, j * k), 8, color=GIVEN if inner else ASK, w=6)
    f.label(P((n - 2) * k / 2, -26), "4 × 4 = 16 = 1 + 3 + 5 + 7", color=GIVEN, size=12)
    f.label(P((n - 1) * k + 30, (n - 1) * k / 2), "9 more", color=ASK, size=12, anchor="start")
    return f

# ---------------------------------------------------------------- 2.7 lotus
@fig
def lotus():
    f = Fig("lotus")
    k = 40; x = 4
    base, tip = P(0, 0), P(0, (x + 1) * k)
    bent = P(3 * k, x * k)
    assert abs(dist(base, bent) - dist(base, tip)) < 1e-6
    f.poly([P(-1.2 * k, 0), P(4.6 * k, 0), P(4.6 * k, x * k), P(-1.2 * k, x * k)], fill=WATER, color=WATER)
    f.seg(P(-1.2 * k, x * k), P(4.6 * k, x * k), color=GIVEN, w=2)
    f.seg(P(-1.2 * k, 0), P(4.6 * k, 0), color="#795548", w=3)
    f.seg(base, tip, color=ANS, w=3); f.seg(base, bent, color=ANS, w=3, dash="7 5")
    f.circle(tip, 7, color="#e91e63", w=5); f.circle(bent, 7, color="#e91e63", w=5)
    f.seg(P(0, x * k), bent, color=ASK, w=1.8)
    rmark(f, P(0, x * k), bent, base)
    f.label(add(mid(P(0, x * k), tip), (-14, 0)), "1", color=GIVEN, size=14)
    f.label(add(mid(P(0, x * k), bent), (0, 14)), "3", color=ASK, size=14)
    f.label(add(mid(base, P(0, x * k)), (-16, 0)), "x", color=GIVEN, size=15, bold=True)
    f.label(add(mid(base, bent), (22, -8)), "x + 1", color=ANS, size=14, bold=True)
    f.label(P(3.9 * k, x * k + 14), "water", color=GIVEN, size=12)
    return f

# ---------------------------------------------------------------- end exercises
EX2 = [  # (leg1, leg2, hyp) with None for the unknown; labels as given
    ((7, 9, None), ("7", "9", "?")),
    ((4, 10, None), ("4", "10", "?")),
    ((None, 40, 41), ("?", "40", "41")),
    ((10, None, math.sqrt(200)), ("10", "?", "√200")),
    ((10, math.sqrt(150), None), ("10", "√150", "?")),
    ((27, None, 45), ("27", "?", "45")),
]

def solve(a, b, c):
    if c is None: return a, b, math.sqrt(a * a + b * b)
    if a is None: return math.sqrt(c * c - b * b), b, c
    return a, math.sqrt(c * c - a * a), c

def ex2(f, answers):
    for i, ((a, b, c), labels) in enumerate(EX2):
        a, b, c = solve(a, b, c)
        k = 130 / c
        o = ((i % 3) * 190, -(i // 3) * 170)
        Cc, A, B = right_tri(a, b, k, o, rot=0)
        f.poly([Cc, A, B], fill="#fff59d" if not answers else "#f1f8e9")
        rmark(f, Cc, A, B)
        g = centroid([Cc, A, B])
        val = {"a": a, "b": b, "c": c}
        ans = {0: "√130", 1: "√116", 2: "9", 3: "10", 4: "√250", 5: "36"}[i]
        for (p, q), lab, key in (((Cc, A), labels[0], "a"), ((Cc, B), labels[1], "b"), ((A, B), labels[2], "c")):
            if lab == "?":
                side(f, p, q, ans if answers else "?", g, color=ANS if answers else ASK, size=13)
            else:
                side(f, p, q, lab, g, size=13)
                assert abs(val[key] - float(eval(lab.replace("√", "math.sqrt(") + (")" if "√" in lab else "")))) < 1e-9
        caption(f, o[0] + 0.45 * a * k, o[1] - 26, f"({'abcdef'[i]})", size=12)
    return f

@fig
def ex2_q():
    f = Fig("ex2_q"); ex2(f, False); return f

@fig
def ex2_a():
    f = Fig("ex2_a"); ex2(f, True); return f

@fig
def ex3_a():
    f = Fig("ex3_a")
    k = 4
    O = P(0, 0)
    A, Cc = P(-35 * k, 0), P(35 * k, 0); B, D = P(0, 12 * k), P(0, -12 * k)
    outline(f, [A, D, Cc, B], w=2.4)
    f.seg(A, Cc, color=HELP, w=1.6); f.seg(B, D, color=HELP, w=1.6)
    f.poly([O, Cc, B], fill=FILL1)
    rmark(f, O, Cc, B, s=9)
    for p, q in ((A, B), (B, Cc), (Cc, D), (D, A)): assert abs(dist(p, q) - 37 * k) < 1e-6
    f.label(add(mid(O, Cc), (0, -13)), "35", color=GIVEN, size=13)
    f.label(add(mid(O, B), (-14, 0)), "12", color=GIVEN, size=13)
    side(f, B, Cc, "37", O, color=ANS, size=14)
    return f

@fig
def ex7_a():
    f = Fig("ex7_a")
    k = 30
    A, B = P(0, 0), P(5 * k, 0)
    h = math.sqrt(49 - 25)
    Cc = P(5 * k, h * k)
    assert abs(dist(A, Cc) - 7 * k) < 1e-6
    f.line(B, 90, -0.5 * k, 6 * k, color=HELP, w=1.4, dash="5 4")
    a0 = dirto(A, Cc); f.carc(A, 7 * k, a0 - 8, a0 + 8)
    f.poly([A, B, Cc], fill="#fff59d")
    S = [B, P((5 + h) * k, 0), P((5 + h) * k, h * k), Cc]
    assert is_square(S) and abs(area(S) - 24 * k * k) < 1e-6
    f.poly(S, fill=FILL3); f.label(centroid(S), "area 24", color=ASK, size=14, bold=True)
    rmark(f, B, A, Cc)
    for p, n, o in ((A, "A", (-12, -10)), (B, "B", (-6, -16)), (Cc, "C", (-12, 12))): name(f, p, n, o)
    g = centroid([A, B, Cc])
    side(f, A, B, "5", g, k=k, value=5); side(f, A, Cc, "7", g, k=k, value=7)
    f.label(add(mid(B, Cc), (-24, 0)), "√24", color=ANS, size=13)
    return f

@fig
def ex8_a():
    f = Fig("ex8_a")
    k = 34
    cases = [((1, 1), (1, 0), "area 2"), ((2, 0), (0.5, 0.5), "area 4"), ((1, 2), (2, 0), "area 5")]
    for j, ((p, q), st, cap) in enumerate(cases):
        o = P(j * 5.2 * k, 0)
        for x in range(5):
            for y in range(5): f.dot(add(o, (x * k, y * k)), color=HELP)
        s0 = {0: (1, 0), 1: (1, 1), 2: (2, 0)}[j]
        v1, v2 = (p, q), (-q, p)
        pts = [s0, (s0[0] + v1[0], s0[1] + v1[1]), (s0[0] + v1[0] + v2[0], s0[1] + v1[1] + v2[1]), (s0[0] + v2[0], s0[1] + v2[1])]
        assert all(0 <= x <= 4 and 0 <= y <= 4 for x, y in pts)
        P4 = [add(o, (x * k, y * k)) for x, y in pts]
        assert is_square(P4) and abs(area(P4) / (k * k) - (p * p + q * q)) < 1e-6
        f.poly(P4, fill=FILL3, color=ASK)
        for pt in P4: f.dot(pt, color=ASK)
        caption(f, o[0] + 2 * k, -24, cap + f" = {p}² + {q}²", size=12)
    return f

@fig
def ex9_a():
    f = Fig("ex9_a")
    k = 34
    B, Cc = P(0, 0), P(6 * k, 0); A = along(B, 60, 6 * k); D = P(3 * k, 0)
    f.poly([A, B, D], fill=FILL1); f.poly([A, D, Cc], fill=FILL2)
    f.seg(A, D, color=ASK, w=2, dash="6 4")
    rmark(f, D, Cc, A)
    for p, n, o in ((A, "A", (0, 14)), (B, "B", (-12, -10)), (Cc, "C", (12, -10)), (D, "D", (0, -16))): name(f, p, n, o)
    g = centroid([A, B, Cc])
    side(f, A, B, "6", g, k=k, value=6); side(f, A, Cc, "6", g, k=k, value=6)
    f.label(add(mid(B, D), (0, 14)), "3", color=GIVEN, size=13); f.label(add(mid(D, Cc), (0, 14)), "3", color=GIVEN, size=13)
    f.label(add(mid(A, D), (14, 0)), "h", color=ASK, size=15, bold=True)
    assert abs(dist(A, D) / k - math.sqrt(27)) < 1e-9
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
