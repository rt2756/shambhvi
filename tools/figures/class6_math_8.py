"""Figures for class 6 maths Ch 8, Playing with Constructions. Drawn at 1 cm = 20 units. Every
construction is done the way the notes describe (compass arcs meet at exact intersection points),
and each result is asserted: right angles are 90°, constructed lengths and diagonals match, squares
on the dot grid have equal sides and right angles, and the diagonal angles add up as stated."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class6", "math", "8")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

CM = 20
BLUE, YELLOW, GREEN, GREY, ORANGE, PINK = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0"

def cm(x, y): return P(x * CM, y * CM)

def disc(f, c, r, fill, color=INK, n=20):
    f.poly([P(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)], fill=fill, color=color)

def pt(f, p, name, dx=0, dy=12, color=INK, dot=True):
    if dot: f.dot(p, color=color)
    if name: f.label(P(p[0] + dx, p[1] + dy - 5), name, size=13, bold=True, color=color)

def poly(f, ps, fill="#ffffff", color=INK):
    f.poly(ps, fill=fill, color=color)

def inter(c1, r1, c2, r2):
    """The two meeting points of two circles."""
    d = dist(c1, c2)
    assert abs(r1 - r2) < d < r1 + r2, "circles don't meet"
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d); h = math.sqrt(r1 * r1 - a * a)
    m = add(c1, mul((c2[0] - c1[0], c2[1] - c1[1]), a / d))
    off = mul((-(c2[1] - c1[1]), c2[0] - c1[0]), h / d)
    return add(m, off), add(m, mul(off, -1))

def tick_arc(f, c, p, span=14):
    """A short compass mark through p, drawn with centre c."""
    r = dist(c, p); a = dirto(c, p)
    f.carc(c, r, a - span, a + span, color=HELP, w=1.4)

def dim(f, p, q, text, off=14, color=GIVEN):
    a = dirto(p, q); n = a + 90
    p2, q2 = along(p, n, off), along(q, n, off)
    f.seg(p2, q2, color=color, w=1.2)
    for e, d in ((p2, a + 180), (q2, a)):
        f.seg(e, along(e, d + 155, 7), color=color, w=1.2); f.seg(e, along(e, d - 155, 7), color=color, w=1.2)
    m = mul(add(p2, q2), 0.5); t = along(m, n, 10)
    f.label(P(t[0], t[1] - 5), text, size=12, color=color)

def angle_at(v, p, q):
    s = (dirto(v, q) - dirto(v, p)) % 360
    return min(s, 360 - s)

def is_rect(ps, tol=1e-6):
    for i in range(4):
        if abs(angle_at(ps[i], ps[i - 1], ps[(i + 1) % 4]) - 90) > tol: return False
    return abs(dist(ps[0], ps[1]) - dist(ps[2], ps[3])) < tol and abs(dist(ps[1], ps[2]) - dist(ps[3], ps[0])) < tol

# ---------------------------------------------------------------- 8.1 artwork and the circle
@fig
def artwork():
    f = Fig("artwork")
    R = 1.6 * CM
    f.circle(cm(0, 0), R, color=INK, w=2); f.circle(cm(3.2, 0), R, color=INK, w=2)       # two touching circles
    assert abs(dist(cm(0, 0), cm(3.2, 0)) - 2 * R) < 1e-9
    for r in (1.6, 0.9, 0.5): f.circle(cm(7.5, 0), r * CM, color=INK, w=2)              # circles with one centre
    for k in range(3): f.circle(cm(k * 2.6 - 0.5, -5), 1.8 * CM, color=INK, w=2)       # three overlapping
    c = cm(7.5, -5.3); f.circle(c, 1.9 * CM, color=INK, w=2)                            # a face with ears
    for s in (-1, 1):
        f.circle(cm(7.5 + s * 1.7, -3.4), 0.8 * CM, color=INK, w=2)
        f.circle(cm(7.5 + s * 0.65, -4.9), 0.3 * CM, color=INK, w=1.6); disc(f, cm(7.5 + s * 0.65, -4.9), 2.5, INK, n=10)
    disc(f, cm(7.5, -5.5), 2.5, INK, n=10); f.seg(cm(7.0, -6.3), cm(8.0, -6.3), w=1.6)
    return f

@fig
def points_4cm():
    f = Fig("points_4cm")
    Pc = cm(0, 0); R = 4 * CM
    f.circle(Pc, R, color=HELP, w=1.2, dash="4 4")
    for k in range(12):
        q = along(Pc, 30 * k + 10, R); disc(f, q, 3.2, ASK, color=ASK, n=12)
        assert abs(dist(Pc, q) - R) < 1e-9
    f.seg(Pc, along(Pc, 10, R), color=GIVEN, w=1.4, dash="5 3")
    t = along(Pc, 10, R / 2); f.label(P(t[0], t[1] + 4), "4 cm", size=12, color=GIVEN)
    pt(f, Pc, "P", dx=-10, dy=-20)
    f.label(P(0, -R - 26), "every point 4 cm from P lies on a circle with centre P", size=11, color=HELP)
    return f

def person(f, x0=0, show_centre=False):
    head_c, head_r = cm(x0, 7), 1.2 * CM
    f.circle(head_c, head_r, color=INK, w=2)
    neck_top, neck_bot = cm(x0, 7 - 1.2), cm(x0, 5)
    f.seg(neck_top, neck_bot, w=2)
    # body: a rectangle 3 cm wide whose top is a downward-curving arc through (-1.5, 5.4) and (1.5, 5.4)
    L, Rt = cm(x0 - 1.5, 5.4), cm(x0 + 1.5, 5.4)
    centre = cm(x0, 8.2); r = dist(centre, L)
    a1, a2 = dirto(centre, L), dirto(centre, Rt)
    assert (a2 - a1) % 360 < 180                         # the short arc, dipping in the middle
    f.carc(centre, r, a1, a2, color=INK, w=2)
    low = along(centre, 270, r)
    f.seg(L, cm(x0 - 1.5, 1.5), w=2); f.seg(Rt, cm(x0 + 1.5, 1.5), w=2); f.seg(cm(x0 - 1.5, 1.5), cm(x0 + 1.5, 1.5), w=2)
    assert abs(dist(centre, Rt) - r) < 1e-9 and low[1] < L[1]
    if show_centre:
        f.seg(centre, L, color=HELP, w=1.2, dash="4 3"); f.seg(centre, Rt, color=HELP, w=1.2, dash="4 3")
        disc(f, centre, 3, ASK, color=ASK, n=12)
        f.label(P(centre[0] + 12, centre[1] + 2), "compass point", size=11, color=ASK, anchor="start")
    return centre, r

@fig
def person_fig():
    f = Fig("person_fig"); person(f); return f

@fig
def person_answer():
    f = Fig("person_answer"); person(f, show_centre=True); return f

@fig
def wave():
    f = Fig("wave")
    A, X, B = cm(0, 0), cm(4, 0), cm(8, 0)
    f.seg(A, B, w=1.6)
    f.carc(cm(2, 0), 2 * CM, 0, 180, color=INK, w=2.4)
    f.carc(cm(6, 0), 2 * CM, 180, 360, color=INK, w=2.4)
    for xx in range(1, 40):
        x = xx / 10
        h = math.sqrt(max(0, 4 - (x - 2) ** 2)) * CM
        if xx % 2 == 0: f.seg(cm(x, 0), P(x * CM, h), color=HELP, w=0.8); f.seg(cm(x + 4, 0), P((x + 4) * CM, -h), color=HELP, w=0.8)
    pt(f, A, "A", dx=-12, dy=-4); pt(f, X, "X", dy=-22); pt(f, B, "B", dx=12, dy=-4)
    dim(f, A, B, "AB = 8 cm", off=-62)
    return f

@fig
def wave_answer():
    f = Fig("wave_answer")
    A, X, B = cm(0, 0), cm(4, 0), cm(8, 0)
    f.seg(A, B, w=1.6)
    f.carc(cm(2, 0), 2 * CM, 0, 180, color=INK, w=2.4)
    f.seg(cm(2, 0), along(cm(2, 0), 60, 2 * CM), color=ASK, w=1.6)
    t = along(cm(2, 0), 60, CM); f.label(P(t[0] + 22, t[1] - 4), "2 cm", size=12, color=ASK)
    disc(f, cm(2, 0), 3, ASK, color=ASK, n=12)
    pt(f, A, "A", dx=-12, dy=-4); pt(f, X, "X", dy=-22); pt(f, B, "B", dx=12, dy=-4)
    dim(f, A, X, "AX = 4 cm", off=-30)
    assert dist(A, X) == 2 * (2 * CM)
    return f

@fig
def wave_small():
    """Waves smaller than a half circle: both arcs have radius 3 cm on 4 cm halves, centres 2.24 cm away from AB."""
    f = Fig("wave_small")
    A, X, B = cm(0, 0), cm(4, 0), cm(8, 0); r = 3
    h = math.sqrt(r * r - 4)
    c1, c2 = cm(2, -h), cm(6, h)
    for c in (c1, c2):
        assert abs(dist(c, A if c is c1 else B) - r * CM) < 1e-9 and abs(dist(c, X) - r * CM) < 1e-9
    a = math.degrees(math.asin(2 / r))
    f.carc(c1, r * CM, 90 - a, 90 + a, color=INK, w=2.4); f.carc(c2, r * CM, 270 - a, 270 + a, color=INK, w=2.4)
    f.seg(A, B, w=1.6)
    for c in (c1, c2): disc(f, c, 3, ASK, color=ASK, n=12)
    f.seg(c1, A, color=HELP, w=1, dash="4 3"); f.seg(c1, X, color=HELP, w=1, dash="4 3")
    f.seg(c2, X, color=HELP, w=1, dash="4 3"); f.seg(c2, B, color=HELP, w=1, dash="4 3")
    pt(f, A, "A", dx=-12, dy=-4); pt(f, X, "X", dy=6); pt(f, B, "B", dx=12, dy=-4)
    f.label(P(c1[0], c1[1] - 20), "centre 1", size=11, color=ASK); f.label(P(c2[0], c2[1] + 8), "centre 2", size=11, color=ASK)
    return f

def eye(f, cx, show=False):
    L, R = cm(cx - 2, 0), cm(cx + 2, 0)
    r = 2.9
    h = math.sqrt(r * r - 4)
    up, lo = cm(cx, -h), cm(cx, h)          # centre for the upper curve is below, for the lower curve above
    a = math.degrees(math.asin(2 / r))
    f.carc(up, r * CM, 90 - a, 90 + a, color=INK, w=2.4); f.carc(lo, r * CM, 270 - a, 270 + a, color=INK, w=2.4)
    disc(f, cm(cx, 0), 0.55 * CM, INK, n=24)
    if show:
        f.seg(cm(cx - 2.4, 0), cm(cx + 2.4, 0), color=HELP, w=1, dash="4 3")
        for c, n in ((up, "A"), (lo, "B")):
            disc(f, c, 3, ASK, color=ASK, n=12); f.label(P(c[0] + 12, c[1] - 5), n, size=12, bold=True, color=ASK, anchor="start")
        f.seg(cm(cx, -h), cm(cx, h), color=HELP, w=1, dash="4 3")
    assert abs(dist(up, L) - r * CM) < 1e-9 and abs(dist(lo, R) - r * CM) < 1e-9

@fig
def eyes():
    f = Fig("eyes"); eye(f, 0); eye(f, 4.4); return f

@fig
def eyes_hint():
    f = Fig("eyes_hint"); eye(f, 0, show=True); return f

# ---------------------------------------------------------------- 8.2 squares and rectangles
@fig
def rect_four_squares():
    f = Fig("rect_four_squares")
    for i in range(-1, 13):
        for j in range(-1, 10): disc(f, P(i * 16, j * 16), 1.6, HELP, color=HELP, n=8)
    u = 16
    poly(f, [P(3 * u, 3 * u), P(9 * u, 3 * u), P(9 * u, 6 * u), P(3 * u, 6 * u)], fill=BLUE)
    for (x, y) in [(0, 0), (10, 0), (0, 7), (10, 7)]:
        poly(f, [P(x * u, y * u), P((x + 2) * u, y * u), P((x + 2) * u, (y + 2) * u), P(x * u, (y + 2) * u)], fill=YELLOW)
    return f

@fig
def names_rect_square():
    f = Fig("names_rect_square")
    A, B, C, D = cm(0, 3), cm(6, 3), cm(6, 0), cm(0, 0)
    poly(f, [A, B, C, D]); f.seg(A, B, color=GIVEN, w=2.6); f.seg(D, C, color=GIVEN, w=2.6)
    for n, p, d in [("A", A, (-10, 4)), ("B", B, (10, 4)), ("C", C, (10, -20)), ("D", D, (-10, -20))]: pt(f, p, n, *d)
    assert is_rect([A, B, C, D])
    S, Pp, Q, R = cm(9, 3), cm(12, 3), cm(12, 0), cm(9, 0)
    poly(f, [S, Pp, Q, R])
    for n, p, d in [("S", S, (-10, 4)), ("P", Pp, (10, 4)), ("Q", Q, (10, -20)), ("R", R, (-10, -20))]: pt(f, p, n, *d)
    return f

GRID_SHAPES = {"A": ((2, 1), (3, 2), (-2, 3)), "B": ((8, 1), (3, 1), (1, 3)), "C": ((17, 1), (3, 3), (-3, 2)), "D": ((23, 2), (2, 1), (-1, 2))}

def square_test(u, v):
    return u[0] * v[0] + u[1] * v[1] == 0 and u[0] ** 2 + u[1] ** 2 == v[0] ** 2 + v[1] ** 2

@fig
def grid_squares():
    f = Fig("grid_squares")
    g = 15
    for i in range(0, 26):
        for j in range(0, 8): disc(f, P(i * g, j * g), 1.6, HELP, color=HELP, n=8)
    for name, (o, u, v) in GRID_SHAPES.items():
        ps = [o, (o[0] + u[0], o[1] + u[1]), (o[0] + u[0] + v[0], o[1] + u[1] + v[1]), (o[0] + v[0], o[1] + v[1])]
        f.poly([P(x * g, y * g) for x, y in ps], fill="none" if False else "#ffffff00", color=INK)
        cx = sum(x for x, _ in ps) / 4 * g
        f.label(P(cx, -22), name, size=14, bold=True)
    assert [n for n, (o, u, v) in GRID_SHAPES.items() if square_test(u, v)] == ["A", "D"]
    return f

def perp_steps(f, Pp, Q, side, label="S"):
    """Square on PQ: right angle at P with a protractor mark, S marked by a compass arc."""
    S = along(Pp, dirto(Pp, Q) + 90, side)
    return S

@fig
def square_construction():
    f = Fig("square_construction")
    Pp, Q = cm(0, 0), cm(6, 0)
    S = along(Pp, 90, 6 * CM); R = along(Q, 90, 6 * CM)
    f.seg(Pp, Q, w=2.4)
    f.seg(Pp, along(Pp, 90, 7 * CM), w=1.4, color=HELP); f.seg(Q, along(Q, 90, 7 * CM), w=1.4, color=HELP)
    f.right(Pp, 0, s=12); f.right(Q, 90, s=12)
    f.carc(Pp, 6 * CM, 80, 100, color=ASK, w=1.6); f.carc(S, 6 * CM, -10, 10, color=ASK, w=1.6)
    f.seg(S, R, w=2.4); f.seg(Pp, S, w=2.4); f.seg(Q, R, w=2.4)
    for n, p, d in [("P", Pp, (-10, -20)), ("Q", Q, (10, -20)), ("R", R, (12, 2)), ("S", S, (-12, 2))]: pt(f, p, n, *d)
    dim(f, Pp, Q, "6 cm", off=-26); dim(f, Q, R, "6 cm", off=-30)
    assert is_rect([Pp, Q, R, S]) and abs(dist(S, R) - 6 * CM) < 1e-9
    f.label(P(3 * CM, -60), "red arcs: the compass, opened to 6 cm, marks S above P and then R", size=11, color=HELP)
    return f

# ---------------------------------------------------------------- 8.4 an exploration in rectangles
RA, RB, RC, RD = cm(0, 4), cm(7, 4), cm(7, 0), cm(0, 0)
def X_at(a): return cm(0, 4 - a)
def Y_at(b): return cm(7, 4 - b)
def XY(a, b): return dist(X_at(a), Y_at(b)) / CM

@fig
def xy_rect():
    f = Fig("xy_rect")
    cases = [(0.5, 3), (1, 2), (0, 0), (4, 0)]
    for k, (a, b) in enumerate(cases):
        o = P((k % 2) * 220, -(k // 2) * 140)
        ps = [add(p, o) for p in (RA, RB, RC, RD)]
        poly(f, ps)
        X, Y = add(X_at(a), o), add(Y_at(b), o)
        f.seg(X, Y, color=ASK, w=2, dash="6 4")
        for n, p, d in [("A", ps[0], (-10, 4)), ("B", ps[1], (10, 4)), ("C", ps[2], (10, -20)), ("D", ps[3], (-10, -20))]: pt(f, p, n, *d)
        pt(f, X, "X", dx=-14 if a not in (0, 4) else 14, dy=-6, color=ASK); pt(f, Y, "Y", dx=14 if b not in (0, 4) else -14, dy=-6, color=ASK)
        f.label(P(o[0] + 70, o[1] - 36), f"XY = {XY(a, b):.1f} cm", size=12, bold=True)
    return f

def xy_table():
    return [(a, b, XY(a, b)) for a, b in [(0.5, 3), (1, 1), (2, 4), (0.5, 0.5), (1.5, 1.5), (0, 4), (4, 0)]]

XY_VALUES = xy_table()
assert abs(XY(1, 1) - 7) < 1e-9 and abs(XY(0, 4) - math.sqrt(65)) < 1e-9

@fig
def two_squares():
    f = Fig("two_squares")
    A, B, C, D, E, F = cm(0, 4), cm(4, 4), cm(8, 4), cm(8, 0), cm(4, 0), cm(0, 0)
    poly(f, [A, C, D, F]); f.seg(B, E)
    for p, q in [(A, B), (B, C), (F, E), (E, D), (A, F), (B, E), (C, D)]: f.ticks(p, q)
    for n, p, d in [("A", A, (-10, 4)), ("B", B, (0, 8)), ("C", C, (10, 4)), ("D", D, (10, -20)), ("E", E, (0, -22)), ("F", F, (-10, -20))]: pt(f, p, n, *d)
    assert is_rect([A, B, E, F]) and is_rect([B, C, D, E]) and dist(A, B) == dist(A, F)
    return f

@fig
def three_squares():
    f = Fig("three_squares")
    s = 3
    A, F = cm(0, s), cm(0, 0)
    pts_top = [cm(k * s, s) for k in range(4)]; pts_bot = [cm(k * s, 0) for k in range(4)]
    f.seg(A, F, w=2.2)
    for k in range(3):
        f.seg(pts_top[k], pts_top[k + 1], w=2.2); f.seg(pts_bot[k], pts_bot[k + 1], w=2.2)
        f.seg(pts_top[k + 1], pts_bot[k + 1], w=2.2 if k == 2 else 1.6)
    for k in range(1, 4):
        f.carc(pts_top[k - 1], s * CM, -14, 14, color=ASK, w=1.4)
    f.carc(F, s * CM, 76, 104, color=ASK, w=1.4)
    assert dist(pts_top[0], pts_top[3]) == 3 * dist(A, F)
    f.label(P(1.5 * s * CM, -28), "compass kept at AF: step it along the top three times", size=11, color=HELP)
    return f

@fig
def square_in_rect():
    f = Fig("square_in_rect")
    R = [cm(0, 4), cm(8, 4), cm(8, 0), cm(0, 0)]
    poly(f, R); Sq = [cm(2, 4), cm(6, 4), cm(6, 0), cm(2, 0)]
    poly(f, Sq, fill=YELLOW)
    f.seg(R[0], R[2], color=HELP, w=1, dash="4 3"); f.seg(R[1], R[3], color=HELP, w=1, dash="4 3")
    disc(f, cm(4, 2), 3, ASK, color=ASK, n=12)
    dim(f, R[3], R[2], "8 cm", off=-28); dim(f, cm(0, 4), cm(2, 4), "2 cm", off=14); dim(f, cm(6, 4), cm(8, 4), "2 cm", off=14)
    assert mul(add(Sq[0], Sq[2]), 0.5) == mul(add(R[0], R[2]), 0.5) and is_rect(Sq) and dist(Sq[0], Sq[1]) == dist(Sq[1], Sq[2])
    return f

def falling(f, sizes, x0=0):
    x = y = 0
    for s in sizes:
        poly(f, [cm(x0 + x, y), cm(x0 + x + s, y), cm(x0 + x + s, y + s), cm(x0 + x, y + s)], fill=ORANGE)
        t = cm(x0 + x + s / 2, y + s / 2); f.label(P(t[0], t[1] - 5), f"{s} cm", size=12)
        x, y = x + s, y + s

@fig
def falling_squares():
    f = Fig("falling_squares")
    falling(f, [4, 4, 4]); falling(f, [7, 5, 3], x0=15)
    return f

@fig
def shadings():
    f = Fig("shadings")
    s = 8
    poly(f, [cm(0, 0), cm(s, 0), cm(s, s), cm(0, s)])
    f.seg(cm(s / 2, 0), cm(s / 2, s)); f.seg(cm(0, s / 2), cm(s, s / 2))
    for (qx, qy) in [(0, s / 2), (s / 2, s / 2), (s / 2, 0)]:
        h = s / 4
        f.seg(cm(qx + h, qy), cm(qx + h, qy + 2 * h), w=1.6); f.seg(cm(qx, qy + h), cm(qx + 2 * h, qy + h), w=1.6)
        for i in range(2):
            for j in range(2):
                x, y = qx + i * h, qy + j * h
                for t in range(1, 6):
                    d = t * h / 6
                    f.seg(cm(x, y + h - d), cm(x + h - d, y + h), color=GIVEN, w=1)
                f.seg(cm(x, y), cm(x + h, y + h), w=1.4)
    return f

@fig
def square_hole():
    f = Fig("square_hole")
    poly(f, [cm(0, 0), cm(6, 0), cm(6, 6), cm(0, 6)])
    f.seg(cm(0, 0), cm(6, 6), color=HELP, w=1, dash="4 3"); f.seg(cm(6, 0), cm(0, 6), color=HELP, w=1, dash="4 3")
    f.circle(cm(3, 3), 2 * CM, color=INK, w=2); disc(f, cm(3, 3), 3, ASK, color=ASK, n=12)
    return f

@fig
def square_holes():
    f = Fig("square_holes")
    poly(f, [cm(0, 0), cm(8, 0), cm(8, 8), cm(0, 8)]); f.seg(cm(4, 0), cm(4, 8)); f.seg(cm(0, 4), cm(8, 4))
    for cx in (2, 6):
        for cy in (2, 6):
            f.circle(cm(cx, cy), 1.5 * CM, color=INK, w=2)
            f.seg(cm(cx - 2, cy - 2), cm(cx + 2, cy + 2), color=HELP, w=0.8, dash="3 3"); f.seg(cm(cx + 2, cy - 2), cm(cx - 2, cy + 2), color=HELP, w=0.8, dash="3 3")
    return f

@fig
def square_curves():
    f = Fig("square_curves")
    s, r = 8, 8
    corners = [cm(0, 0), cm(s, 0), cm(s, s), cm(0, s)]
    poly(f, corners, fill="#ffffff", color=HELP)
    off = math.sqrt(r * r - (s / 2) ** 2)
    for k in range(4):
        p, q = corners[k], corners[(k + 1) % 4]
        m = mul(add(p, q), 0.5); a = dirto(p, q) - 90                # outward direction for this side
        c = along(m, a, off * CM)
        assert abs(dist(c, p) - r * CM) < 1e-9 and abs(dist(c, q) - r * CM) < 1e-9
        a1, a2 = dirto(c, q), dirto(c, p)
        if (a2 - a1) % 360 > 180: a1, a2 = a2, a1
        assert abs((a2 - a1) % 360 - 60) < 1e-6           # the short arc between the two corners
        f.carc(c, r * CM, a1, a2, color=INK, w=2.4)
        if k == 0:                                         # show one compass point and its radii
            disc(f, c, 3, ASK, color=ASK, n=12)
            f.seg(c, p, color=HELP, w=1, dash="4 3"); f.seg(c, q, color=HELP, w=1, dash="4 3")
    f.label(P(4 * CM, -off * CM - 24), "each arc: radius 8 cm, centre outside the square on the line through the middle of its side", size=10, color=HELP)
    return f

# ---------------------------------------------------------------- 8.5 diagonals
@fig
def rect_diagonals():
    f = Fig("rect_diagonals")
    Pp, Q, R, S = cm(0, 4), cm(6, 4), cm(6, 0), cm(0, 0)
    poly(f, [Pp, Q, R, S]); f.seg(Pp, R, w=1.8); f.seg(Q, S, w=1.8)
    assert abs(dist(Pp, R) - dist(Q, S)) < 1e-9
    labels = [(Pp, S, R, "c"), (Pp, R, Q, "d"), (Q, Pp, S, "e"), (Q, S, R, "f"), (R, Q, Pp, "g"), (R, Pp, S, "h"), (S, R, Q, "a"), (S, Q, Pp, "b")]
    for v, p, q, n in labels:
        a1, a2 = dirto(v, p), dirto(v, q)
        if (a2 - a1) % 360 > 180: a1, a2 = a2, a1
        f.angle(v, a1, a2, n, r=22, lr=34)
    for n, p, d in [("P", Pp, (-10, 6)), ("Q", Q, (10, 6)), ("R", R, (10, -22)), ("S", S, (-10, -22))]: pt(f, p, n, *d)
    return f

def rect_by_angle(f, ang, base=5, o=(0, 0), names="ABCD"):
    """Rectangle ABCD where the diagonal AC makes `ang` with AB: AB drawn, perpendicular at B,
    ray from A at ang meets it at C, then D by a compass (AD = BC)."""
    A = add(cm(0, 0), o); B = add(cm(base, 0), o)
    C = meet(A, ang, B, 90)
    D = inter(A, dist(B, C), C, dist(A, B))
    D = D[0] if D[0][0] < D[1][0] else D[1]
    poly(f, [A, B, C, D]); f.seg(A, C, w=1.8)
    f.right(B, 90, s=10)
    f.angle(A, 0, ang, f"{ang}°", expect=ang, r=24, lr=40)
    f.angle(A, ang, 90, f"{90 - ang}°", expect=90 - ang, r=34, lr=50)
    tick_arc(f, A, D); tick_arc(f, C, D)
    for n, p, d in zip(names, [A, B, C, D], [(-10, -20), (10, -20), (10, 4), (-10, 4)]): pt(f, p, n, *d)
    assert is_rect([A, B, C, D])
    return A, B, C, D

@fig
def rect_60_30():
    f = Fig("rect_60_30"); rect_by_angle(f, 60, base=3); return f

@fig
def rect_50_40():
    f = Fig("rect_50_40"); rect_by_angle(f, 50, base=4); return f

@fig
def rect_45():
    f = Fig("rect_45")
    A, B, C, D = rect_by_angle(f, 45, base=4)
    assert abs(dist(A, B) - dist(B, C)) < 1e-9
    return f

def rect_side_diag(f, side, diag, o=(0, 0)):
    """Rectangle with DC = side and diagonal DB = diag: perpendicular l at C, circle arc of radius diag
    about D cuts l at B; then A from perpendiculars (checked)."""
    D, C = add(cm(0, 0), o), add(cm(side, 0), o)
    f.seg(D, C, w=2.4)
    f.seg(C, add(C, cm(0, diag + 0.5)), color=HELP, w=1.4)
    h = math.sqrt(diag * diag - side * side)
    B = add(C, cm(0, h))
    assert abs(dist(D, B) - diag * CM) < 1e-9
    a = dirto(D, B); f.carc(D, diag * CM, a - 6, a + 6, color=ASK, w=1.8)
    A = add(D, cm(0, h))
    f.seg(D, A, w=2.4); f.seg(A, B, w=2.4); f.seg(C, B, w=2.4); f.seg(D, B, color=ASK, w=1.6, dash="6 4")
    f.right(C, 90, s=10); f.right(D, 0, s=10)
    for n, p, d in [("D", D, (-10, -20)), ("C", C, (10, -20)), ("B", B, (12, 4)), ("A", A, (-12, 4))]: pt(f, p, n, *d)
    dim(f, D, C, f"{side:g} cm", off=-26)
    t = mul(add(D, B), 0.5); f.label(P(t[0] - 16, t[1] + 4), f"{diag:g} cm", size=12, color=ASK)
    assert is_rect([A, B, C, D])
    return h

@fig
def rect_5_7():
    f = Fig("rect_5_7")
    D = cm(0, 0); f.circle(D, 7 * CM, color=HELP, w=1, dash="4 4")
    h = rect_side_diag(f, 5, 7)
    assert abs(h - math.sqrt(24)) < 1e-9
    return f

@fig
def rect_4_8():
    f = Fig("rect_4_8"); h = rect_side_diag(f, 4, 8); assert abs(h - math.sqrt(48)) < 1e-9; return f

@fig
def rect_3_7():
    f = Fig("rect_3_7"); h = rect_side_diag(f, 3, 7); assert abs(h - math.sqrt(40)) < 1e-9; return f

# ---------------------------------------------------------------- 8.6 the house
def house(f, s, show_circles=False, o=(0, 0)):
    D, E = add(cm(0, 0), o), add(cm(s, 0), o)
    B, C = add(D, cm(0, s)), add(E, cm(0, s))
    A = inter(B, s * CM, C, s * CM); A = A[0] if A[0][1] > A[1][1] else A[1]
    assert abs(dist(A, B) - s * CM) < 1e-9 and abs(dist(A, C) - s * CM) < 1e-9
    if show_circles:
        f.circle(B, s * CM, color=HELP, w=1, dash="4 4"); f.circle(C, s * CM, color=HELP, w=1, dash="4 4")
    for p, q in [(D, E), (D, B), (E, C), (A, B), (A, C)]: f.seg(p, q, w=2.4)
    a1, a2 = dirto(A, B), dirto(A, C)
    assert abs((a2 - a1) % 360 - 60) < 1e-6            # the short arc from B to C, below A
    f.carc(A, s * CM, a1, a2, color=INK, w=2.4)
    door = [add(D, cm(s / 2 - 0.5, 0)), add(D, cm(s / 2 + 0.5, 0)), add(D, cm(s / 2 + 0.5, 2)), add(D, cm(s / 2 - 0.5, 2))]
    poly(f, door)
    for n, p, d in [("A", A, (0, 8)), ("B", B, (-12, 0)), ("C", C, (12, 0)), ("D", D, (-10, -20)), ("E", E, (10, -20))]: pt(f, p, n, *d)
    dim(f, D, E, f"{s} cm", off=-26)
    return A

@fig
def house_fig():
    f = Fig("house_fig"); house(f, 5); return f

@fig
def house_circles():
    f = Fig("house_circles"); house(f, 5, show_circles=True); return f

@fig
def house_7():
    f = Fig("house_7"); house(f, 7); return f

@fig
def rhombus():
    f = Fig("rhombus")
    s = 5
    A, C = cm(0, 0), cm(s, 0)
    B = inter(A, s * CM, C, s * CM); B = B[0] if B[0][1] > B[1][1] else B[1]
    D = inter(B, s * CM, C, s * CM); D = D[0] if D[0][0] > D[1][0] else D[1]
    for p, q in [(A, C), (A, B), (B, D), (D, C)]: f.seg(p, q, w=2.4)
    f.seg(B, C, color=HELP, w=1.2, dash="5 4")
    for c, p in [(A, B), (C, B), (B, D), (C, D)]: tick_arc(f, c, p)
    for p, q in [(A, C), (A, B), (B, D), (D, C)]:
        assert abs(dist(p, q) - s * CM) < 1e-9; f.ticks(p, q)
    assert abs(angle_at(A, C, B) - 60) < 1e-9          # equal sides but a 60° corner: not a square
    f.angle(A, 0, 60, "60°", expect=60, r=24, lr=40)
    for n, p, d in [("A", A, (-10, -20)), ("C", C, (10, -20)), ("B", B, (-10, 6)), ("D", D, (10, 6))]: pt(f, p, n, *d)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
