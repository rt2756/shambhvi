"""Figures for class 6 maths Ch 2, Lines and Angles. Every angle label is checked against the drawn
geometry (geo.Fig.angle asserts it), protractor readings are computed from where an arm crosses the
scale, grid answers are tested for the right angle, and acute angles in the triangle pattern are
counted from the drawn segments."""
import math, os, sys, itertools
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class6", "math", "2")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, PURPLE, RED = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0", "#ce93d8", "#ef9a9a"

def disc(f, c, r, fill, color=INK, n=20):
    f.poly([P(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)], fill=fill, color=color)

def head(f, tip, a, color=INK, s=9):
    for d in (+28, -28):
        f.seg(along(tip, a + 180 + d, s), tip, color=color, w=2)

def ray(f, p, a, L, color=INK, w=2.2, name=None, at=None, dot_at=None):
    """Ray from p at angle a, drawn length L with an arrowhead; optional point name near the end."""
    q = along(p, a, L)
    f.seg(p, q, color=color, w=w); head(f, q, a, color=color)
    if dot_at is not None:
        f.dot(along(p, a, dot_at))
    if name:
        t = along(p, a, at if at else L - 18)
        f.label(add(along(t, a + 90, 13), (0, -5)), name, size=13, bold=True, color=color if color != INK else INK)
    return q

def line2(f, p, q, ext=26, color=INK, w=2.2):
    """A line through p and q, with arrowheads beyond both."""
    a = dirto(p, q)
    s, e = along(p, a, -ext), along(q, a, ext)
    f.seg(s, e, color=color, w=w); head(f, e, a, color); head(f, s, a + 180, color)

def pt(f, p, name, dx=0, dy=12, color=INK):
    f.dot(p, color=color)
    if name: f.label(P(p[0] + dx, p[1] + dy - 5), name, size=13, bold=True, color=color)

# ---------------------------------------------------------------- 2.1–2.4 point, segment, line, ray
@fig
def basics():
    f = Fig("basics")
    pt(f, P(0, 0), "P", dy=14); f.label(P(0, -30), "a point", size=12, color=HELP)
    A, B = P(70, 0), P(180, 0)
    f.seg(A, B); pt(f, A, "A", dy=14); pt(f, B, "B", dy=14); f.label(P(125, -30), "segment AB", size=12, color=HELP)
    A, B = P(250, 0), P(330, 0)
    line2(f, A, B); pt(f, A, "A", dy=14); pt(f, B, "B", dy=14); f.label(P(290, -30), "line AB (no ends)", size=12, color=HELP)
    A = P(410, 0)
    ray(f, A, 0, 110, dot_at=70); pt(f, A, "A", dy=14); f.label(P(480, 14 - 5), "P", size=13, bold=True)
    f.label(P(465, -30), "ray AP (one end)", size=12, color=HELP)
    return f

@fig
def routes():
    f = Fig("routes")
    A, B = P(0, 0), P(200, 60)
    curves = [[A, P(40, 70), P(110, 95), B], [A, P(60, -30), P(150, 0), B], [A, P(30, 40), P(80, 10), P(130, 70), P(170, 40), B]]
    for c in curves:
        for p, q in zip(c, c[1:]): f.seg(p, q, color=HELP, w=1.6, dash="5 4")
    f.seg(A, B, color=ASK, w=2.6)
    pt(f, A, "A", dx=-12, dy=-4); pt(f, B, "B", dx=12, dy=-4)
    L = dist(A, B)
    for c in curves:
        assert sum(dist(p, q) for p, q in zip(c, c[1:])) > L      # every other route is longer
    f.label(P(100, -50), "the straight route (red) is the shortest", size=12, color=ASK)
    return f

SEG24 = [("L", P(0, 0)), ("M", P(40, 60)), ("P", P(100, 40)), ("Q", P(140, 95)), ("R", P(250, 65))]

@fig
def fig_segments():
    f = Fig("fig_segments")
    pts = [p for _, p in SEG24]
    for p, q in zip(pts, pts[1:]): f.seg(p, q)
    offs = {"L": (-10, -14), "M": (-8, 12), "P": (4, -20), "Q": (0, 12), "R": (10, 0)}
    for n, p in SEG24: pt(f, p, n, *offs[n])
    return f

@fig
def fig_rays():
    f = Fig("fig_rays")
    T = P(0, 0)
    ray(f, T, 40, 150); pt(f, T, "T", dx=-12, dy=-4)
    f.label(add(along(T, 40, 128), (-14, 0)), "A", size=13, bold=True); f.dot(along(T, 40, 128))
    ray(f, T, 0, 200)
    N, B = P(120, 0), P(160, 0)
    pt(f, N, "N", dy=-20); pt(f, B, "B", dy=-20)
    return f

@fig
def fig_points5():
    f = Fig("fig_points5")
    D, E, O, B = P(0, 0), P(60, 25), P(140, 58.3), P(210, 87.5)
    assert abs(dirto(D, E) - dirto(E, O)) < 0.1 and abs(dirto(O, B) - dirto(D, E)) < 0.1
    line2(f, D, B)
    ray(f, O, 0, 110); ray(f, O, 90, 95)
    C = P(220, 58.3)
    for n, p, d in [("D", D, (0, -22)), ("E", E, (0, -22)), ("O", O, (-6, -22)), ("B", B, (-12, 4)), ("C", C, (0, -22))]:
        pt(f, p, n, *d)
    return f

@fig
def fig_ray_oba():
    f = Fig("fig_ray_oba")
    O = P(0, 0)
    ray(f, O, 40, 190)
    pt(f, O, "O", dx=-10, dy=-4); pt(f, along(O, 40, 90), "B", dx=-10, dy=4); pt(f, along(O, 40, 160), "A", dx=-10, dy=4)
    return f

@fig
def q4_drawings():
    f = Fig("q4_drawings")
    # (a) lines OP and OQ meet at O
    O = P(0, 0)
    line2(f, along(O, 20, -60), along(O, 20, 60)); line2(f, along(O, 120, -55), along(O, 120, 55))
    pt(f, O, "O", dx=-4, dy=-26); pt(f, along(O, 20, 50), "P", dx=4, dy=-24); pt(f, along(O, 120, 48), "Q", dx=12)
    f.label(P(0, -95), "(a)", bold=True, size=13)
    # (b) lines XY and PQ cross at M
    M = P(190, 0)
    X, Y = along(M, 160, 60), along(M, 160, -60); Pp, Q = along(M, 60, -55), along(M, 60, 55)
    line2(f, X, Y); line2(f, Pp, Q)
    for n, p, d in [("M", M, (14, -8)), ("X", X, (0, 12)), ("Y", Y, (0, 12)), ("P", Pp, (12, 0)), ("Q", Q, (12, 0))]: pt(f, p, n, *d)
    f.label(P(190, -95), "(b)", bold=True, size=13)
    # (c) line l through E and F, D not on it
    E, F, D = P(300, -20), P(380, 20), P(320, 50)
    line2(f, E, F); pt(f, E, "E", dy=-22); pt(f, F, "F", dy=-22); pt(f, D, "D")
    f.label(P(418, 22), "l", size=15, bold=True)
    f.label(P(340, -95), "(c)", bold=True, size=13)
    # (d) P on segment AB
    A, B = P(470, 0), P(590, 0)
    f.seg(A, B); pt(f, A, "A", dy=14); pt(f, B, "B", dy=14); pt(f, P(515, 0), "P", dy=14)
    f.label(P(530, -95), "(d)", bold=True, size=13)
    return f

# ---------------------------------------------------------------- 2.5 angles
@fig
def angle_parts():
    f = Fig("angle_parts")
    B = P(0, 0)
    ray(f, B, 25, 170); ray(f, B, -25, 170)
    pt(f, B, "B", dx=-12, dy=-4)
    pt(f, along(B, 25, 140), "D", dy=12); pt(f, along(B, -25, 140), "E", dy=-22)
    f.angle(B, -25, 25, "", expect=50, r=26)
    f.label(add(along(B, 25, 75), (-14, 14)), "arm", size=12, color=GIVEN)
    f.label(add(along(B, -25, 75), (-14, -24)), "arm", size=12, color=GIVEN)
    f.label(P(-16, -26), "vertex", size=12, color=GIVEN, anchor="end")
    return f

@fig
def turn():
    f = Fig("turn")
    V = P(0, 0)
    ray(f, V, 0, 180, color=HELP); ray(f, V, 40, 180, color=INK)
    f.carc(V, 90, 2, 38, color=ASK, w=2)
    head(f, along(V, 38, 90), 128, color=ASK)
    f.label(P(185, -24), "starting position of the ray", size=11, color=HELP, anchor="end")
    f.label(add(along(V, 40, 180), (0, 12)), "after turning", size=11)
    f.label(P(100, 36), "the amount of turn", size=12, color=ASK, anchor="start")
    f.label(P(-8, -20), "vertex", size=11, anchor="end")
    return f

@fig
def scissors():
    """Our own picture for 'find the angles': an open pair of scissors, pivot D."""
    f = Fig("scissors")
    D = P(0, 0)
    B, C = along(D, 25, 150), along(D, -15, 150)
    A, E = along(D, 205, 70), along(D, 165, 70)
    f.seg(D, B, w=3); f.seg(D, C, w=3); f.seg(D, A, w=3); f.seg(D, E, w=3)
    for c in (A, E): f.circle(along(c, dirto(D, c), 14), 14, color=INK, w=2.4)
    for n, p, d in [("D", D, (0, -24)), ("B", B, (8, 6)), ("C", C, (8, -18)), ("A", A, (-34, -12)), ("E", E, (-34, 4))]: pt(f, p, n, *d)
    f.angle(D, -15, 25, "", expect=40, r=34, color=ASK)
    return f

@fig
def name_q3():
    f = Fig("name_q3")
    Pv = P(0, 0)
    for a, n in [(35, "A"), (0, "B"), (-35, "C")]:
        ray(f, Pv, a, 160); pt(f, along(Pv, a, 110), n, dy=12 if a >= 0 else -24)
    pt(f, Pv, "P", dx=-12, dy=-4)
    return f

@fig
def name_q4():
    f = Fig("name_q4")
    T = P(0, 0)
    for a, n in [(100, "P"), (60, "Q"), (0, "R")]:
        ray(f, T, a, 150); pt(f, along(T, a, 120), n, dx=12 if a else 0, dy=0 if a else -22)
    pt(f, T, "T", dx=-12, dy=-14)
    f.angle(T, 0, 60, "", expect=60, r=24, color=GIVEN)
    f.angle(T, 0, 100, "", expect=100, r=34, color=ASK)
    return f

@fig
def three_points():
    f = Fig("three_points")
    A, B, C = P(0, 0), P(180, 10), P(70, 120)
    for p, q in [(A, B), (B, C), (C, A)]: line2(f, p, q, ext=30, w=1.8)
    pt(f, A, "A", dx=-10, dy=-22); pt(f, B, "B", dx=12, dy=-22); pt(f, C, "C", dx=-14, dy=4)
    f.angle(A, dirto(A, B), dirto(A, C), "", r=22); f.angle(B, dirto(B, C), dirto(B, A), "", r=22); f.angle(C, dirto(C, A), dirto(C, B), "", r=22)
    return f

@fig
def four_points():
    f = Fig("four_points")
    pts = {"A": P(0, 0), "B": P(170, -10), "C": P(190, 120), "D": P(20, 130)}
    names = list(pts)
    for a, b in itertools.combinations(names, 2): line2(f, pts[a], pts[b], ext=22, w=1.4)
    # three points never on one line
    for a, b, c in itertools.combinations(names, 3):
        p, q, r = pts[a], pts[b], pts[c]
        assert abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) > 1
    cen = mul(add(add(pts["A"], pts["B"]), add(pts["C"], pts["D"])), 0.25)
    for n, p in pts.items():
        o = along(p, dirto(cen, p), 22); pt(f, p, n, o[0] - p[0], o[1] - p[1] + 4)
    assert len(list(itertools.combinations(names, 2))) == 6
    return f

# ---------------------------------------------------------------- 2.6 comparing
@fig
def superimpose():
    f = Fig("superimpose")
    B = P(0, 0); ray(f, B, 0, 110); ray(f, B, 30, 110)
    pt(f, B, "B", dy=-20); pt(f, along(B, 0, 80), "C", dy=-20); pt(f, along(B, 30, 80), "A", dy=8)
    f.angle(B, 0, 30, "30°", expect=30, r=30)
    Q = P(170, 0); ray(f, Q, 0, 110); ray(f, Q, 55, 110)
    pt(f, Q, "Q", dy=-20); pt(f, along(Q, 0, 80), "R", dy=-20); pt(f, along(Q, 55, 80), "P", dx=-10, dy=4)
    f.angle(Q, 0, 55, "55°", expect=55, r=30)
    S = P(340, 0); ray(f, S, 0, 110); ray(f, S, 30, 110, color=GIVEN); ray(f, S, 55, 110, color=ASK)
    f.label(P(360, -22), "B on Q, BC along QR", size=11, color=HELP, anchor="start")
    f.label(add(along(S, 30, 115), (8, 0)), "BA", size=12, color=GIVEN, anchor="start")
    f.label(add(along(S, 55, 115), (8, 0)), "QP", size=12, color=ASK, anchor="start")
    return f

@fig
def compare_q2():
    f = Fig("compare_q2")
    O = P(0, 0)
    for a, n, L in [(85, "A", 150), (60, "X", 170), (25, "Y", 170), (0, None, 200)]:
        ray(f, O, a, L)
        if n: pt(f, along(O, a, L - 30), n, dx=12 if a < 80 else -12)
    pt(f, P(80, 0), "B", dy=-22); pt(f, P(160, 0), "C", dy=-22); pt(f, O, "O", dx=-12, dy=-14)
    return f

@fig
def compare_q3():
    f = Fig("compare_q3")
    O = P(0, 0)
    ray(f, O, 0, 180); ray(f, O, 60, 160); ray(f, O, 25, 175, color=GIVEN); ray(f, O, 88, 150, color=GIVEN)
    pt(f, along(O, 0, 140), "B", dy=-22); pt(f, along(O, 60, 125), "A", dx=12)
    pt(f, along(O, 25, 145), "Y", dy=-24, color=GIVEN); pt(f, along(O, 88, 120), "X", dx=-12, color=GIVEN)
    pt(f, O, "O", dx=-12, dy=-14)
    return f

@fig
def circle_compare():
    """Compare two angles with a see-through circle centred on the vertex."""
    f = Fig("circle_compare")
    O = P(0, 0); R = 70
    f.circle(O, R, color=HELP, w=1.6); ray(f, O, -30, 140); ray(f, O, 20, 140)
    pt(f, along(O, -30, R), "A", dx=10, dy=-14); pt(f, along(O, 20, R), "B", dx=8, dy=6); pt(f, O, "O", dx=-12, dy=-4)
    f.label(P(0, -100), "crane 1: mark A and B on the circle", size=11, color=HELP)
    O2 = P(260, 0)
    f.circle(O2, R, color=HELP, w=1.6); ray(f, O2, -30, 140, color=GIVEN); ray(f, O2, 35, 140, color=GIVEN)
    pt(f, along(O2, -30, R), "A", dx=10, dy=-14); pt(f, along(O2, 20, R), "B", dx=10, dy=-10, color=ASK)
    pt(f, along(O2, 35, R), "Y", dx=-4, dy=10, color=GIVEN)
    f.label(P(260, -100), "crane 2's arm passes beyond B: its angle is bigger", size=11, color=HELP)
    assert 35 - (-30) > 20 - (-30)
    return f

# ---------------------------------------------------------------- 2.8 straight and right angles
@fig
def straight_bisect():
    f = Fig("straight_bisect")
    O = P(0, 0)
    A, B = P(-130, 0), P(130, 0)
    f.seg(A, B); pt(f, A, "A", dy=-22); pt(f, B, "B", dy=-22); pt(f, O, "O", dy=-22)
    ray(f, O, 90, 110, color=ASK); pt(f, P(0, 95), "C", dx=12, color=ASK)
    f.right(O, 0, s=13); f.right(O, 90, s=13)
    f.label(P(70, 30), "90°", size=13, color=GIVEN); f.label(P(-70, 30), "90°", size=13, color=GIVEN)
    f.label(P(0, -46), "fold OB onto OA: the crease OC halves the straight angle", size=11, color=HELP)
    return f

GRID_W, GRID_H, GU = 7, 6, 22

def grid(f, x0, A, B, answers=(), good=None):
    for i in range(GRID_W):
        for j in range(GRID_H):
            disc(f, P(x0 + i * GU, j * GU), 2.4, INK, n=10)
    a, b = P(x0 + A[0] * GU, A[1] * GU), P(x0 + B[0] * GU, B[1] * GU)
    f.seg(a, b, color=ASK, w=2.4)
    f.label(add(a, (-8, 8)), "A", size=12, bold=True); f.label(add(b, (8, 6)), "B", size=12, bold=True)
    for q in answers:
        c = P(x0 + q[0] * GU, q[1] * GU)
        f.seg(a, c, color=ANS, w=2.2); disc(f, c, 4, GREEN, color=ANS, n=12)
        if good: assert good(A, B, q), (A, B, q)

def ang_at(A, B, Q):
    return (math.degrees(math.atan2(Q[1] - A[1], Q[0] - A[0]) - math.atan2(B[1] - A[1], B[0] - A[0]))) % 360

GA1, GB1 = (2, 3), (5, 3)          # A and B in the left grid
GA2, GB2 = (2, 4), (4, 2)          # and in the right grid
def inside(q): return 0 <= q[0] < GRID_W and 0 <= q[1] < GRID_H

def straight_pts(A, B):
    d = (B[0] - A[0], B[1] - A[1]); g = math.gcd(*map(abs, d)); d = (d[0] // g, d[1] // g)
    out, k = [], 1
    while inside((A[0] - k * d[0], A[1] - k * d[1])): out.append((A[0] - k * d[0], A[1] - k * d[1])); k += 1
    return out

def right_pts(A, B):
    d = (B[0] - A[0], B[1] - A[1]); g = math.gcd(*map(abs, d)); d = (-d[1] // g, d[0] // g)
    out = []
    for s in (1, -1):
        k = 1
        while inside((A[0] + s * k * d[0], A[1] + s * k * d[1])): out.append((A[0] + s * k * d[0], A[1] + s * k * d[1])); k += 1
    return out

@fig
def grids_question():
    f = Fig("grids_question")
    grid(f, 0, GA1, GB1); grid(f, 200, GA2, GB2)
    return f

@fig
def grids_straight():
    f = Fig("grids_straight")
    g = lambda A, B, q: abs(ang_at(A, B, q) - 180) < 1e-6
    grid(f, 0, GA1, GB1, straight_pts(GA1, GB1), g); grid(f, 200, GA2, GB2, straight_pts(GA2, GB2), g)
    return f

@fig
def grids_right():
    f = Fig("grids_right")
    g = lambda A, B, q: abs(ang_at(A, B, q) - 90) < 1e-6 or abs(ang_at(A, B, q) - 270) < 1e-6
    grid(f, 0, GA1, GB1, right_pts(GA1, GB1), g); grid(f, 200, GA2, GB2, right_pts(GA2, GB2), g)
    return f

@fig
def grids_types():
    """Acute, obtuse and reflex answers in the two grids (one each), checked by measuring."""
    f = Fig("grids_types")
    picks = [("acute", (4, 5), (4, 4), lambda a: 0 < a < 90),
             ("obtuse", (0, 5), (0, 4), lambda a: 90 < a < 180),
             ("reflex", (1, 0), (4, 5), lambda a: 180 < a < 360)]
    for r, (name, q1, q2, ok) in enumerate(picks):
        y = -r * 150
        for x0, A, B, q in [(0, GA1, GB1, q1), (200, GA2, GB2, q2)]:
            a = ang_at(A, B, q)
            if name != "reflex": a = min(a, 360 - a)
            else: a = max(a, 360 - a)
            assert ok(a), (name, A, B, q, a)
            for i in range(GRID_W):
                for j in range(GRID_H): disc(f, P(x0 + i * GU, y + j * GU), 2.4, INK, n=10)
            pa, pb, pq = P(x0 + A[0] * GU, y + A[1] * GU), P(x0 + B[0] * GU, y + B[1] * GU), P(x0 + q[0] * GU, y + q[1] * GU)
            f.seg(pa, pb, color=ASK, w=2.4); f.seg(pa, pq, color=ANS, w=2.4)
            a1, a2 = dirto(pa, pb), dirto(pa, pq)
            if name == "reflex":
                s, e = (a1, a2) if (a2 - a1) % 360 > 180 else (a2, a1)
            else:
                s, e = (a1, a2) if (a2 - a1) % 360 < 180 else (a2, a1)
            f.carc(pa, 11, s, e, color=GIVEN, w=2)
            f.label(P(x0 + 66, y - 22), f"{name}: {a:.0f}°", size=12, bold=True)
    return f

@fig
def fold_perpendicular():
    f = Fig("fold_perpendicular")
    O = P(0, 0)
    for a in (30, 210): ray(f, O, a, 120, color=INK)
    for a in (120, 300): ray(f, O, a, 100, color=ASK)
    for a in (30, 120, 210, 300): f.right(O, a, s=11)
    f.label(P(0, -130), "fold the crease onto itself: 4 right angles", size=11, color=HELP)
    return f

# ---------------------------------------------------------------- classifying
def tri_pattern(levels):
    """Segments of the nested-triangle pattern: an equilateral triangle; each level joins the
    midpoints of the previous middle triangle."""
    T = [P(0, 0), P(160, 0), P(80, 160 * math.sqrt(3) / 2)]
    segs = [(T[0], T[1]), (T[1], T[2]), (T[2], T[0])]
    cur = T
    for _ in range(levels):
        m = [mul(add(cur[i], cur[(i + 1) % 3]), 0.5) for i in range(3)]
        segs += [(m[0], m[1]), (m[1], m[2]), (m[2], m[0])]
        cur = m
    return segs

def count_acute(segs):
    pts = []
    def key(p): return (round(p[0], 6), round(p[1], 6))
    for s in segs:
        for p in s:
            if key(p) not in [key(q) for q in pts]: pts.append(p)
    total = 0
    for v in pts:
        dirs = set()
        for a, b in segs:
            for p, q in ((a, b), (b, a)):
                # v on segment pq (endpoint or inside)?
                cross = (q[0] - p[0]) * (v[1] - p[1]) - (q[1] - p[1]) * (v[0] - p[0])
                if abs(cross) > 1e-6: continue
                t = ((v[0] - p[0]) * (q[0] - p[0]) + (v[1] - p[1]) * (q[1] - p[1])) / dist(p, q) ** 2
                if -1e-9 <= t < 1 - 1e-9: dirs.add(round(dirto(v, q), 4))
        for a, b in itertools.combinations(sorted(dirs), 2):
            d = min((b - a) % 360, (a - b) % 360)
            if d < 90 - 1e-6: total += 1
    return total

PATTERN_COUNTS = [count_acute(tri_pattern(k)) for k in range(4)]
assert PATTERN_COUNTS == [3, 12, 21, 30], PATTERN_COUNTS

def draw_pattern(f, k, x0):
    for p, q in tri_pattern(k): f.seg(add(p, (x0, 0)), add(q, (x0, 0)), w=1.8)

@fig
def acute_pattern():
    f = Fig("acute_pattern")
    for k in range(3): draw_pattern(f, k, k * 200)
    return f

@fig
def acute_pattern_next():
    f = Fig("acute_pattern_next")
    draw_pattern(f, 3, 0)
    f.label(P(80, -24), f"{PATTERN_COUNTS[3]} acute angles", size=13, bold=True)
    return f

def vee(f, v, a1, a2, L=70, color=INK, mark=True):
    ray(f, v, a1, L, color=color, w=2); ray(f, v, a2, L, color=color, w=2)
    sweep = (a2 - a1) % 360
    if mark:
        if abs(sweep - 90) < 1e-9: f.right(v, a1, s=10)
        else: f.angle(v, a1, a2, "", expect=sweep, r=16)

@fig
def angle_groups():
    f = Fig("angle_groups")
    groups = [("acute (less than a right angle)", [(10, 50), (100, 130), (200, 275), (300, 340)]),
              ("right", [(0, 90), (45, 135), (160, 250), (290, 20)]),
              ("obtuse (between right and straight)", [(0, 120), (60, 210), (190, 330), (250, 20)])]
    for g, (name, angs) in enumerate(groups):
        x0 = g * 260
        for k, (a1, a2) in enumerate(angs):
            v = P(x0 + 60 + (k % 2) * 120, -(k // 2) * 120)
            sweep = (a2 - a1) % 360
            assert (g == 0 and sweep < 90) or (g == 1 and sweep == 90) or (g == 2 and 90 < sweep < 180)
            vee(f, v, a1, a2, L=50)
        f.label(P(x0 + 120, 80), name, size=12, bold=True)
    return f

# ---------------------------------------------------------------- 2.9 degrees and protractors
@fig
def thirty_units():
    f = Fig("thirty_units")
    O = P(0, 0)
    for d in range(0, 31): f.seg(O, along(O, d, 150), color=HELP if 0 < d < 30 else INK, w=0.8 if 0 < d < 30 else 2.2)
    f.label(P(160, 40), "30 one-degree parts = 30°", size=12, anchor="start")
    return f

@fig
def circle_parts():
    f = Fig("circle_parts")
    for k, n in enumerate([1, 2, 3, 4, 5, 6, 8, 9, 10, 12]):
        c = P((k % 5) * 110, -(k // 5) * 120); R = 42
        f.circle(c, R, color=INK, w=1.8)
        if n > 1:
            for i in range(n): f.seg(c, along(c, 90 - 360 * i / n, R), w=1.4)
        f.label(P(c[0], c[1] - R - 22), f"{n} part" + ("s" if n > 1 else ""), size=11, color=HELP)
    return f

@fig
def circle_parts_answer():
    f = Fig("circle_parts_answer")
    for k, n in enumerate([1, 2, 3, 4, 5, 6, 8, 9, 10, 12]):
        c = P((k % 5) * 110, -(k // 5) * 120); R = 42
        f.circle(c, R, color=INK, w=1.8)
        if n > 1:
            for i in range(n): f.seg(c, along(c, 90 - 360 * i / n, R), w=1.4)
        assert 360 % n == 0
        f.label(P(c[0], c[1] - R - 22), f"{n}: {360 // n}° each", size=11, bold=True)
    return f

def protractor(f, c, R=110, rot=0, inner_scale=True, labels=True, light=False):
    """A half-circle protractor centred at c, its 0-180 line along direction rot (0° mark at
    angle rot, 180° mark at rot + 180). Outer numbers count from the rot side; inner numbers from
    the other side."""
    col = HELP if light else INK
    f.carc(c, R, rot, rot + 180, color=col, w=1.6)
    f.seg(along(c, rot, R), along(c, rot + 180, R), color=col, w=1.6)
    f.carc(c, R * 0.18, rot, rot + 180, color=col, w=1.2)
    for d in range(0, 181):
        a = rot + d
        L = 11 if d % 10 == 0 else 7 if d % 5 == 0 else 3.5
        f.seg(along(c, a, R - L), along(c, a, R), color=col, w=0.6)
        if d % 10 == 0 and 0 < d < 180:
            f.seg(along(c, a, R * 0.18), along(c, a, R - 30), color="#cfd8dc", w=0.6)
        if labels and d % 10 == 0:
            q = along(c, a, R - 18); f.text(P(q[0], q[1] - 3), str(d), size=7, color=col)
            if inner_scale:
                q = along(c, a, R - 28); f.text(P(q[0], q[1] - 3), str(180 - d), size=7, color=GIVEN)

def reading(rot, a):
    """Outer-scale reading of an arm at angle a on a protractor turned by rot."""
    return round((a - rot) % 360, 6)

@fig
def protractor_unlabelled():
    f = Fig("protractor_unlabelled")
    A = P(0, 0); R = 110
    protractor(f, A, R, rot=-90, labels=False)
    arms = {"L": 0, "K": 30, "W": -50, "T": -90}
    for n, a in arms.items():
        ray(f, A, a, R + 40, color=ASK, w=1.8)
        f.label(add(along(A, a, R + 52), (0, -5)), n, size=13, bold=True, color=ASK)
    pt(f, A, "A", dx=-12, dy=-4)
    assert (arms["K"] - arms["L"], arms["L"] - arms["W"], arms["K"] - arms["T"]) == (30, 50, 120)
    return f

PQRSTU = {"P": 0, "Q": 35, "R": 95, "S": 125, "T": 160, "U": 180}

@fig
def protractor_labelled():
    f = Fig("protractor_labelled")
    O = P(0, 0); R = 130
    protractor(f, O, R)
    for n, a in PQRSTU.items():
        ray(f, O, a, R + 30, color=ASK, w=1.6)
        f.label(add(along(O, a, R + 44), (0, -5)), n, size=13, bold=True, color=ASK)
    pt(f, O, "O", dy=-22)
    f.label(P(0, -46), "black numbers count from P's side (0 at the right); blue numbers count from U's side", size=11, color=HELP)
    return f

@fig
def protractor_aob():
    f = Fig("protractor_aob")
    O = P(0, 0); R = 120
    protractor(f, O, R)
    ray(f, O, 0, R + 30, color=ASK); ray(f, O, 80, R + 30, color=ASK)
    pt(f, O, "O", dy=-22); f.label(P(R + 40, -20), "B", size=13, bold=True, color=ASK)
    f.label(add(along(O, 80, R + 44), (8, -5)), "A", size=13, bold=True, color=ASK)
    assert reading(0, 80) == 80
    return f

@fig
def paper_protractor():
    f = Fig("paper_protractor")
    O = P(0, 0); R = 140
    f.carc(O, R, 0, 180, color=INK, w=2); f.seg(along(O, 0, R), along(O, 180, R), w=2)
    names = "ABCDEFGHI"
    for k in range(9):
        a = 22.5 * k
        if 0 < k < 8: f.seg(O, along(O, a, R), color=HELP, w=1.4, dash="5 4")
        q = along(O, a, R + 16); f.label(P(q[0], q[1] - 5), names[k], size=13, bold=True)
        lab = f"{a:g}°"
        q = along(O, a, R - 26); f.text(P(q[0], q[1] - 4), lab, size=10, color=GIVEN)
    pt(f, O, "O", dy=-22)
    assert 180 / 8 == 22.5
    return f

def measure_angle(f, v, a1, a2, label, L=110, color=INK, names=None, r=24):
    ray(f, v, a1, L, color=color, w=2); ray(f, v, a2, L, color=color, w=2)
    sweep = (a2 - a1) % 360
    f.angle(v, a1, a2, label, expect=sweep, r=r)
    if names:
        pt(f, v, names[0], dx=-12, dy=-14)
        pt(f, along(v, a1, L - 20), names[1], dx=10, dy=-18)
        pt(f, along(v, a2, L - 20), names[2], dx=-10, dy=8)

@fig
def measure_q1():
    f = Fig("measure_q1")
    measure_angle(f, P(0, 0), 43, 90, "", names="HJI")
    measure_angle(f, P(190, 90), 247, 270, "", names="HJI")       # thin angle at the top
    measure_angle(f, P(330, 30), -54, 54, "", names="HJI")
    return f

@fig
def measure_q3():
    f = Fig("measure_q3")
    measure_angle(f, P(0, 0), -48, -6, "", L=150, names="HJI")
    measure_angle(f, P(220, 0), -14, 102, "", L=130, names="HJI")
    return f

@fig
def measure_reflex():
    f = Fig("measure_reflex")
    v = P(0, 0)
    ray(f, v, 40, 120); ray(f, v, -60, 120)
    f.angle(v, 40, 300, "", expect=260, r=22)
    return f

Q5 = [(20, 100), (200, 320), (-30, 30), (140, 270), (10, 140), (240, 300)]   # a-f: 80, 120, 60, 130, 130, 60

@fig
def measure_q5():
    f = Fig("measure_q5")
    for k, (a1, a2) in enumerate(Q5):
        v = P((k % 3) * 200, -(k // 3) * 190)
        ray(f, v, a1, 80, w=2); ray(f, v, a2, 80, w=2)
        f.angle(v, a1, a2, "", expect=(a2 - a1) % 360, r=16)
        f.label(P(v[0] - 70, v[1] + 60), "abcdef"[k] + ".", size=14, bold=True)
    return f

@fig
def protractor_q6():
    f = Fig("protractor_q6")
    X = P(0, 0); R = 130
    protractor(f, X, R)
    arms = {"E": 0, "C": 85, "B": 115, "A": 180}
    for n, a in arms.items():
        ray(f, X, a, R + 30, color=ASK, w=1.6)
        f.label(add(along(X, a, R + 44), (0, -5)), n, size=13, bold=True, color=ASK)
    pt(f, X, "X", dy=-22)
    assert (arms["B"] - arms["E"], arms["C"] - arms["E"], arms["A"] - arms["B"], arms["B"] - arms["C"]) == (115, 85, 65, 30)
    return f

PQ7 = {"P": 165, "R": 120, "S": 65, "T": 15}

@fig
def measure_q7():
    f = Fig("measure_q7")
    Q = P(0, 0)
    for n, a in PQ7.items():
        ray(f, Q, a, 150)
        pt(f, along(Q, a, 125), n, dx=12 if a < 90 else -12)
    pt(f, Q, "Q", dy=-22)
    assert (PQ7["P"] - PQ7["R"], PQ7["P"] - PQ7["S"], PQ7["P"] - PQ7["T"]) == (45, 100, 150)
    return f

TRI_ANGLES = [(60, 55), (55, 30), (40, 78)]      # angles at A and B; C gets the rest

def tri_from(base, a, b):
    A, B = P(0, 0), P(base, 0)
    return [A, B, meet(A, a, B, 180 - b)]

TRIS = [tri_from(140, *t) for t in TRI_ANGLES]

def draw_triangles(f, labels):
    for k, T in enumerate(TRIS):
        T = [add(p, (k * 210, 0)) for p in T]
        f.poly(T, fill=[YELLOW, PINK, BLUE][k])
        tot = 0
        for i, nm in enumerate("ABC"):
            v, p, q = T[i], T[(i + 1) % 3], T[(i + 2) % 3]
            a1, a2 = dirto(v, p), dirto(v, q)
            s_ = (a2 - a1) % 360
            if s_ > 180: a1, a2, s_ = a2, a1, 360 - s_
            tot += s_
            f.angle(v, a1, a2, f"{round(s_)}°" if labels else "", expect=s_, r=20, lr=36)
            c = mul(add(add(T[0], T[1]), T[2]), 1 / 3)
            o = along(v, dirto(c, v), 14); f.label(P(o[0], o[1] - 5), nm, size=12, bold=True)
        assert abs(tot - 180) < 1e-6
        f.label(P(k * 210 + 70, -40), f"({'abc'[k]})", size=13, bold=True)

@fig
def triangles_q():
    f = Fig("triangles_q"); draw_triangles(f, False); return f

@fig
def triangles_sum():
    f = Fig("triangles_sum"); draw_triangles(f, True); return f

# --- six ways of misusing a protractor (our own)
def misuse(f, c, rot, arms, vertex=None, R=80, title="", marked=None):
    protractor(f, c, R, rot=rot, light=False)
    v = vertex or c
    for a in arms: ray(f, v, a, R + 30, color=ASK, w=1.8)
    if marked:
        f.carc(v, 16, marked[0], marked[1], color=GIVEN, w=2)
    disc(f, v, 2.6, ASK, color=ASK, n=10)
    f.label(P(c[0] - R, c[1] + R + 26), title, anchor="start", size=13, bold=True)

@fig
def mistakes():
    f = Fig("mistakes")
    R = 80
    # U: only one arm read; the other arm is not on the 0-line
    misuse(f, P(0, 0), 0, [35, -25], title="∠U = 35°")
    # V: protractor tilted, neither arm on the 0-line; the student read where one arm crosses
    misuse(f, P(260, 0), -30, [50, -15], title="∠V = 80°")
    assert reading(-30, 50) == 80 and reading(-30, -15) == 15
    # W: vertex not at the centre
    d = R * math.cos(math.radians(70))
    misuse(f, P(0, -250), 0, [0, 90], vertex=P(d, -250), title="∠W = 70°")
    cross = along(P(d, -250), 90, R * math.sin(math.radians(70)))
    assert abs(dirto(P(0, -250), cross) - 70) < 1e-6
    # X: wrong scale (arm along the 180 side, read the outer number)
    misuse(f, P(260, -250), 0, [180, 150], title="∠X = 150°")
    assert reading(0, 150) == 150 and 180 - 150 == 30
    # Y: the angle opens below the protractor; the student read the backward extension of an arm
    misuse(f, P(0, -500), 0, [0, -60], title="∠Y = 120°", marked=(-60, 0))
    f.seg(P(0, -500), along(P(0, -500), 120, R + 10), color=ASK, w=1, dash="4 4")
    assert reading(0, 120) == 120
    # Z: the marked angle is the reflex one
    misuse(f, P(260, -500), 0, [0, 85], title="∠Z = 85°", marked=(85, 360))
    return f

@fig
def clocks():
    f = Fig("clocks")
    for k, h in enumerate([1, 2, 4]):
        c = P(k * 190, 0); R = 75
        f.circle(c, R, color=INK, w=2)
        for t in range(12):
            a = 90 - 30 * t
            f.seg(along(c, a, R - 6), along(c, a, R), w=1.4)
            q = along(c, a, R - 16); f.text(P(q[0], q[1] - 4), str(t if t else 12), size=10, color=HELP)
        f.seg(c, along(c, 90, R - 12), w=2.2)                     # minute hand at 12
        f.seg(c, along(c, 90 - 30 * h, R - 26), w=3.4)            # hour hand
        f.angle(c, 90 - 30 * h, 90, f"{30 * h}°", expect=30 * h, r=16, lr=28, color=ASK, bold=True)
        f.label(P(c[0], c[1] - R - 22), f"{h} o'clock", size=12, bold=True)
    return f

LINES23_ANG = (70, 84, 105)        # direction of each crossing line, measured from the bottom line
def x_at(p, q, y): return p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])

@fig
def fig_lines_cut():
    f = Fig("fig_lines_cut")
    yt, yb = 90, 0
    line2(f, P(-10, yt), P(260, yt), ext=20); line2(f, P(-10, yb), P(260, yb), ext=20)
    C, L, S = P(20, yb), P(100, yb), P(170, yb)
    A, Pp, R = on_y(C, LINES23_ANG[0], yt), on_y(L, LINES23_ANG[1], yt), on_y(S, LINES23_ANG[2], yt)
    for v, a in [(C, LINES23_ANG[0]), (L, LINES23_ANG[1]), (S, LINES23_ANG[2])]:
        assert abs(dirto(v, on_y(v, a, yt)) - a) < 1e-9
    for p, q in [(A, C), (Pp, L), (R, S)]: line2(f, p, q, ext=22)
    for n, p, d in [("A", A, (-10, 8)), ("P", Pp, (-12, 8)), ("R", R, (12, 8)), ("B", P(230, yt), (0, 10)),
                    ("C", C, (-12, -20)), ("D", P(60, yb), (0, -20)), ("L", L, (12, -20)), ("S", S, (12, -20))]:
        pt(f, p, n, *d)
    return f

@fig
def copy_angle():
    f = Fig("copy_angle")
    H = P(0, 0)
    ray(f, H, -15, 130); ray(f, H, 235, 140)
    pt(f, H, "H", dy=10); pt(f, along(H, -15, 100), "J", dy=8); pt(f, along(H, 235, 100), "I", dx=-12)
    f.angle(H, 235, 345, "", expect=110, r=22)
    return f

@fig
def drawing_30():
    f = Fig("drawing_30")
    I = P(0, 0); R = 120
    protractor(f, I, R)
    ray(f, I, 0, R + 30, color=ASK); ray(f, I, 30, R + 30, color=ANS)
    pt(f, I, "I", dy=-22); f.label(P(R + 40, -20), "N", size=13, bold=True)
    q = along(I, 30, R + 44); f.label(P(q[0] + 4, q[1] - 5), "T", size=13, bold=True, color=ANS)
    assert reading(0, 30) == 30
    return f

@fig
def type_examples():
    f = Fig("type_examples")
    rows = [("acute", [(0, 40), (250, 300), (100, 175)]), ("obtuse", [(0, 110), (200, 330)]), ("reflex", [(0, 220), (60, 330)])]
    for r, (name, angs) in enumerate(rows):
        f.label(P(-30, -r * 150 + 10), name, anchor="end", size=13, bold=True)
        for k, (a1, a2) in enumerate(angs):
            v = P(k * 170, -r * 150)
            s = (a2 - a1) % 360
            assert (name == "acute" and s < 90) or (name == "obtuse" and 90 < s < 180) or (name == "reflex" and 180 < s < 360)
            ray(f, v, a1, 65, w=2); ray(f, v, a2, 65, w=2)
            f.angle(v, a1, a2, f"{s:g}°", expect=s, r=16, lr=34)
    return f

PTRQW = {"W": 0, "Q": 42, "R": 72, "P": 102}

@fig
def angles_t():
    f = Fig("angles_t")
    T = P(0, 0)
    for n, a in PTRQW.items():
        ray(f, T, a, 140); pt(f, along(T, a, 115), n, dx=12 if a < 90 else -12, dy=0 if a else -22)
    pt(f, T, "T", dx=-12, dy=-14)
    assert (PTRQW["P"] - PTRQW["R"], PTRQW["P"] - PTRQW["Q"], PTRQW["P"] - PTRQW["W"], 360 - PTRQW["P"]) == (30, 60, 102, 258)
    return f

@fig
def bet():
    f = Fig("bet")
    E = P(0, 0)
    B, R = P(-130, 0), P(130, 0)
    f.seg(B, R); pt(f, B, "B", dy=-22); pt(f, R, "R", dy=-22); pt(f, E, "E", dy=-22)
    ray(f, E, 90, 120); ray(f, E, 80, 125)
    pt(f, along(E, 90, 105), "S", dx=-12); pt(f, along(E, 80, 108), "T", dx=12)
    f.angle(E, 0, 80, "80°", expect=80, r=30)
    f.right(E, 90, s=11)
    return f

# ---------------------------------------------------------------- end exercises
END_Q2 = [(20, 55), (10, 160), (0, 90), (195, 225), (300, 10), (25, 5)]   # a-f; f is the reflex one (340°)

@fig
def estimate_end():
    f = Fig("estimate_end")
    for k, (a1, a2) in enumerate(END_Q2):
        v = P((k % 3) * 200, -(k // 3) * 170)
        ray(f, v, a1, 85, w=2); ray(f, v, a2, 85, w=2)
        f.angle(v, a1, a2, "", expect=(a2 - a1) % 360, r=16)
        f.label(P(v[0] - 60, v[1] + 70), "abcdef"[k] + ".", size=14, bold=True)
    return f

def path_with_bends(start, first, bends, step=70):
    """A zigzag: at each corner the path turns so that the angle between the two pieces is the
    given bend. Returns the corner points."""
    pts, a, sgn = [start, along(start, first, step)], first, 1
    for b in bends:
        a = a + sgn * (180 - b); sgn = -sgn
        pts.append(along(pts[-1], a, step))
    return pts

ZIG = [40, 120, 60, 90, 150, 70]

@fig
def mixed_angles():
    f = Fig("mixed_angles")
    pts = path_with_bends(P(0, 0), 20, ZIG, step=75)
    for p, q in zip(pts, pts[1:]): f.seg(p, q, w=2.4)
    for i, b in enumerate(ZIG):
        v = pts[i + 1]; a1, a2 = dirto(v, pts[i]), dirto(v, pts[i + 2])
        if (a2 - a1) % 360 > 180: a1, a2 = a2, a1
        if b == 90: f.right(v, a1, s=10)
        else: f.angle(v, a1, a2, f"{b}°", expect=b, r=16, lr=32)
    assert sum(1 for b in ZIG if b < 90) == 3 and ZIG.count(90) == 1 and sum(1 for b in ZIG if 90 < b < 180) == 2
    return f

@fig
def letter_m():
    f = Fig("letter_m")
    Mid = P(0, 0); L, h = 110, 170
    T1, T2 = along(Mid, 120, L), along(Mid, 60, L)       # the two slanting strokes meet at 60°
    B1, B2 = along(T1, 260, h), along(T2, 280, h)        # the legs make 40° with the strokes
    for p, q in [(B1, T1), (T1, Mid), (Mid, T2), (T2, B2)]: f.seg(p, q, w=3)
    f.angle(T1, 260, 300, "40°", expect=40, r=24, lr=40)
    f.angle(T2, 240, 280, "40°", expect=40, r=24, lr=40)
    f.angle(Mid, 60, 120, "60°", expect=60, r=22, lr=38)
    return f

@fig
def letter_y():
    f = Fig("letter_y")
    J = P(0, 0)
    f.seg(J, along(J, 270, 110), w=3); f.seg(J, along(J, 60, 100), w=3); f.seg(J, along(J, 120, 100), w=3)
    f.angle(J, 270, 60, "150°", expect=150, r=22, lr=40)
    f.angle(J, 60, 120, "60°", expect=60, r=22, lr=40)
    f.angle(J, 120, 270, "150°", expect=150, r=28, lr=44)
    return f

@fig
def chakra():
    f = Fig("chakra")
    c = P(0, 0); R = 100
    f.circle(c, R, color="#1a237e", w=3); f.circle(c, 12, color="#1a237e", w=2)
    for k in range(24): f.seg(along(c, 360 * k / 24, 12), along(c, 360 * k / 24, R), color="#1a237e", w=1.6)
    f.angle(c, 0, 15, "15°", expect=15, r=46, lr=62, color=ASK)
    f.angle(c, 90, 165, "75°", expect=75, r=30, lr=48, color=ANS)
    assert 360 / 24 == 15 and max(15 * k for k in range(1, 24) if 15 * k < 90) == 75
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
