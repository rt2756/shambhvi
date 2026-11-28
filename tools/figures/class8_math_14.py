"""Figures for class 8 maths Ch 14, Area. Every shape is drawn from coordinates in units, and
every area or length written on a picture is recomputed from those coordinates (shoelace formula,
distances, perpendicular heights), so no label can disagree with its picture."""
import math, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "14")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, RED, SKY = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0", "#e53935", "#29b6f6"

def area(pts):
    s = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2

def S(pts, k, o=(0, 0)):
    return [P(o[0] + x * k, o[1] + y * k) for x, y in pts]

def shape(f, pts, k, o=(0, 0), fill="#ffffff", color=INK):
    f.poly(S(pts, k, o), fill=fill, color=color)

def name(f, p, s, k, o=(0, 0), d=(0, 0)):
    f.label(P(o[0] + p[0] * k + d[0], o[1] + p[1] * k + d[1] - 5), s, size=13, bold=True)

def dim(f, p, q, text, off=(0, 0), color=GIVEN, size=12, bars=True):
    f.seg(p, q, color=color, w=1.2)
    if bars:
        a = dirto(p, q)
        for e in (p, q): f.seg(along(e, a + 90, 4), along(e, a - 90, 4), color=color, w=1.2)
    m = mul(add(p, q), 0.5)
    f.label(add(m, off), text, size=size, color=color)

def hatch(f, pts_px, gap=10, color=HELP):
    """45° hatching clipped to a convex polygon given in pixel coordinates."""
    xs = [p[0] for p in pts_px]; ys = [p[1] for p in pts_px]
    lo, hi = min(x - y for x, y in pts_px), max(x - y for x, y in pts_px)
    c = lo + gap / 2
    edges = list(zip(pts_px, pts_px[1:] + pts_px[:1]))
    while c < hi:
        # line x - y = c ; intersect with polygon edges
        hits = []
        for (x1, y1), (x2, y2) in edges:
            d1, d2 = x1 - y1 - c, x2 - y2 - c
            if d1 == d2: continue
            t = d1 / (d1 - d2)
            if 0 <= t <= 1: hits.append(P(x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
        hits.sort()
        if len(hits) >= 2: f.seg(hits[0], hits[-1], color=color, w=1)
        c += gap

def grid(f, x0, y0, w, h, k, color="#cfd8dc"):
    for i in range(w + 1): f.seg(P(x0 + i * k, y0), P(x0 + i * k, y0 + h * k), color=color, w=1)
    for j in range(h + 1): f.seg(P(x0, y0 + j * k), P(x0 + w * k, y0 + j * k), color=color, w=1)

# ---------------------------------------------------------------- 14.1 rectangles
@fig
def two_rectangles():
    f = Fig("two_rectangles")
    k = 22
    grid(f, 0, 0, 7, 4, k); shape(f, [(0, 0), (7, 0), (7, 4), (0, 4)], k, fill="none")
    grid(f, 200, 0, 8, 3, k); shape(f, [(0, 0), (8, 0), (8, 3), (0, 3)], k, o=(200, 0), fill="none")
    f.label(P(77, -18), "7 cm × 4 cm: 28 unit squares", size=12, color=ANS)
    f.label(P(288, -18), "8 cm × 3 cm: 24 unit squares", size=12, color=ANS)
    assert 7 * 4 == 28 and 8 * 3 == 24
    return f

@fig
def perimeter_vs_area():
    f = Fig("perimeter_vs_area")
    k = 16
    R1 = [(0, 0), (12, 0), (12, 1), (0, 1)]       # perimeter 26, area 12
    R2 = [(0, 0), (5, 0), (5, 5), (0, 5)]         # perimeter 20, area 25
    grid(f, 0, 0, 12, 1, k); shape(f, R1, k, fill="none")
    grid(f, 250, 0, 5, 5, k); shape(f, R2, k, o=(250, 0), fill="none")
    per = lambda w, h: 2 * (w + h)
    assert per(12, 1) > per(5, 5) and area(R1) < area(R2)
    f.label(P(96, -18), "12 × 1: perimeter 26, area 12", size=12, color=ASK)
    f.label(P(290, -18), "5 × 5: perimeter 20, area 25", size=12, color=ANS)
    return f

@fig
def missing_sides():
    f = Fig("missing_sides")
    k = 14
    # (i): 28 = 4 x 7 (top), 21 = 7 x 3 (right), 35 = 7 x 5 (left), 14 = 2 x 7 (bottom strip)
    A = [(3, 5), (7, 5), (7, 12), (3, 12)]; B = [(7, 5), (14, 5), (14, 8), (7, 8)]
    C = [(0, 0), (7, 0), (7, 5), (0, 5)]; D = [(7, -2), (9, -2), (9, 5), (7, 5)]
    for pts, a in [(A, 28), (B, 21), (C, 35), (D, 14)]:
        assert area(pts) == a
        shape(f, pts, k, fill="#ffffff")
        cx = sum(x for x, y in pts) / 4; cy = sum(y for x, y in pts) / 4
        f.text(P(cx * k, cy * k - 6), f"{a} in²", size=11)
    dim(f, P(7.6 * k, 8 * k), P(7.6 * k, 12 * k), "4 in", off=(16, -4))
    dim(f, P(7 * k, 4.4 * k), P(14 * k, 4.4 * k), "7 in", off=(0, -16))
    dim(f, P(0, 5.6 * k), P(3 * k, 5.6 * k), "3 in", off=(0, 6))
    dim(f, P(6.4 * k, -2 * k), P(6.4 * k, 0), "2 in", off=(-16, -4))
    dim(f, P(7 * k, -2.6 * k), P(9 * k, -2.6 * k), "?", off=(0, -16), color=ASK)
    f.label(P(-10, 12 * k), "(i)", anchor="start", bold=True, size=13)
    # (ii): a 10 x 5 rectangle of area 50: top 4 m tall split 29 | 11, bottom 1 m
    o = (260, 0)
    k2 = 18
    T1 = [(0, 1), (7.25, 1), (7.25, 5), (0, 5)]; T2 = [(7.25, 1), (10, 1), (10, 5), (7.25, 5)]; Bm = [(0, 0), (10, 0), (10, 1), (0, 1)]
    assert area(T1) == 29 and area(T2) == 11 and area(T1) + area(T2) + area(Bm) == 50
    shape(f, T1, k2, o, fill="#ffffff"); shape(f, T2, k2, o, fill=GREY); shape(f, Bm, k2, o, fill="#ffffff")
    f.text(P(o[0] + 3.6 * k2, o[1] + 3 * k2 - 6), "29 m²", size=12)
    f.text(P(o[0] + 8.6 * k2, o[1] + 3 * k2 - 6), "11 m²", size=12)
    dim(f, P(o[0] - 10, o[1] + k2), P(o[0] - 10, o[1] + 5 * k2), "4 m", off=(-18, -4))
    f.label(P(o[0] + 3.6 * k2, o[1] + 5 * k2 + 10), "?", size=13, color=ASK); f.label(P(o[0] + 8.6 * k2, o[1] + 5 * k2 + 10), "?", size=13, color=ASK)
    f.label(P(o[0] + 10 * k2 + 12, o[1] + 0.2 * k2), "?", size=13, color=ASK)
    f.label(P(o[0] + 5 * k2, o[1] - 20), "whole rectangle: 50 m²", size=12, color=GIVEN)
    f.label(P(o[0] - 10, o[1] + 6.5 * k2), "(ii)", anchor="start", bold=True, size=13)
    return f

@fig
def park_path():
    f = Fig("park_path")
    k = 10
    outer = [(0, 0), (30, 0), (30, 20), (0, 20)]; inner = [(4, 3), (26, 3), (26, 17), (4, 17)]
    shape(f, outer, k, fill="#dce775"); shape(f, inner, k, fill="#66bb6a")
    for p, n, d in [((0, 0), "A", (-10, -10)), ((30, 0), "B", (10, -10)), ((30, 20), "C", (10, 8)), ((0, 20), "D", (-10, 8)),
                    ((4, 3), "E", (8, 6)), ((26, 3), "F", (-8, 6)), ((26, 17), "G", (-8, -10)), ((4, 17), "H", (8, -10))]:
        name(f, p, n, k, d=d)
    assert area(outer) - area(inner) == 600 - 308
    return f

@fig
def cross_path():
    f = Fig("cross_path")
    k = 14
    shape(f, [(0, 0), (14, 0), (14, 12), (0, 12)], k, fill=GREEN)
    shape(f, [(6, 0), (8, 0), (8, 12), (6, 12)], k, fill=YELLOW)
    shape(f, [(0, 5), (14, 5), (14, 6.5), (0, 6.5)], k, fill=YELLOW)
    shape(f, [(6, 5), (8, 5), (8, 6.5), (6, 6.5)], k, fill=ORANGE)
    dim(f, P(0, -10), P(14 * k, -10), "14 m", off=(0, -16))
    dim(f, P(-10, 0), P(-10, 12 * k), "12 m", off=(-20, -4))
    dim(f, P(6 * k, 12 * k + 10), P(8 * k, 12 * k + 10), "a", off=(0, 6))
    dim(f, P(14 * k + 10, 5 * k), P(14 * k + 10, 6.5 * k), "b", off=(10, -4))
    a, b = 2, 1.5
    assert 14 * b + 12 * a - a * b == area([(6, 0), (8, 0), (8, 12), (6, 12)]) + area([(0, 5), (14, 5), (14, 6.5), (0, 6.5)]) - a * b
    return f

SPIRAL = [((0, 19), (20, 20)), ((19, 0), (20, 20)), ((0, 0), (20, 1)), ((0, 0), (1, 15)), ((0, 14), (15, 15)),
          ((14, 5), (15, 15)), ((5, 5), (15, 6)), ((5, 5), (6, 10)), ((5, 9), (10, 10))]

def spiral_cells():
    cells = set()
    for (x1, y1), (x2, y2) in SPIRAL:
        cells |= {(x, y) for x in range(x1, x2) for y in range(y1, y2)}
    return cells

@fig
def spiral():
    f = Fig("spiral")
    k = 10
    for (x, y) in spiral_cells():
        f.poly([P(x * k, y * k), P((x + 1) * k, y * k), P((x + 1) * k, (y + 1) * k), P(x * k, (y + 1) * k)], fill="#ef9a9a", color="#ef9a9a")
    lengths = [20, 20, 20, 15, 15, 10, 10, 5, 5]
    assert len(spiral_cells()) == sum(lengths) - 8 == 112
    dim(f, P(0, 21 * k), P(20 * k, 21 * k), "20", off=(0, 6), size=11)
    dim(f, P(21 * k, 0), P(21 * k, 20 * k), "20", off=(12, -4), size=11)
    dim(f, P(0, -10), P(20 * k, -10), "20", off=(0, -16), size=11)
    dim(f, P(-10, 0), P(-10, 15 * k), "15", off=(-14, -4), size=11)
    dim(f, P(0, 15.6 * k), P(15 * k, 15.6 * k), "15", off=(0, 4), size=11)
    dim(f, P(15.6 * k, 5 * k), P(15.6 * k, 15 * k), "10", off=(12, -4), size=11)
    dim(f, P(5 * k, 4.4 * k), P(15 * k, 4.4 * k), "10", off=(0, -14), size=11)
    dim(f, P(4.4 * k, 5 * k), P(4.4 * k, 10 * k), "5", off=(-10, -4), size=11)
    dim(f, P(5 * k, 10.6 * k), P(10 * k, 10.6 * k), "5", off=(0, 4), size=11)
    f.label(P(10 * k, -38), "tube 1 unit wide; lengths are outer edges", size=11, color=HELP)
    return f

@fig
def bent_tube():
    f = Fig("bent_tube")
    k = 16
    L = [(0, 0), (1, 0), (1, 4), (5, 4), (5, 5), (0, 5)]
    assert area(L) == 9
    shape(f, L, k, fill="#ef9a9a")
    shape(f, [(9, 0), (10, 0), (10, 9), (9, 9)], k, fill="#ef9a9a")
    dim(f, P(0, 5.6 * k), P(5 * k, 5.6 * k), "5", off=(0, 4), size=11)
    dim(f, P(-8, 0), P(-8, 5 * k), "5", off=(-10, -4), size=11)
    dim(f, P(10.6 * k, 0), P(10.6 * k, 9 * k), "9", off=(12, -4), size=11, color=ANS)
    f.label(P(5 * k, -20), "both have area 9 (5 + 5 − 1, the corner counted once)", size=11, color=ANS)
    return f

@fig
def square_regions():
    f = Fig("square_regions")
    for s, x0 in [(4, 0), (8, 110)]:
        k = 12
        sq = [(0, 0), (s, 0), (s, s), (0, s)]
        shape(f, sq, k, (x0, 0))
        f.seg(P(x0, s * k), P(x0 + s * k, 0), w=1.6)                 # diagonal
        f.seg(P(x0 + s * k / 2, s * k / 2), P(x0 + s * k, s * k), w=1.6)  # from centre to a corner
        f.label(P(x0 + s * k * 0.25, s * k * 0.3), "1", size=12, bold=True)
        f.label(P(x0 + s * k * 0.55, s * k * 0.82), "2", size=12, bold=True)
        f.label(P(x0 + s * k * 0.8, s * k * 0.45), "3", size=12, bold=True)
        f.label(P(x0 + s * k / 2, -18), f"side {s}", size=11, color=GIVEN)
    return f

@fig
def four_pieces():
    f = Fig("four_pieces")
    k = 26
    # a 4 x 4 square cut by two perpendicular lines through its centre, tilted
    c = P(2, 2); a = math.radians(25)
    d1 = (math.cos(a), math.sin(a)); d2 = (-math.sin(a), math.cos(a))
    shape(f, [(0, 0), (4, 0), (4, 4), (0, 4)], k)
    for d in (d1, d2):
        t = 2 / max(abs(d[0]), abs(d[1]))
        f.seg(P((c[0] - d[0] * t) * k, (c[1] - d[1] * t) * k), P((c[0] + d[0] * t) * k, (c[1] + d[1] * t) * k), w=1.8)
    f.right(P(c[0] * k, c[1] * k), 25)
    return f

# ---------------------------------------------------------------- triangles
@fig
def tri_in_rect():
    f = Fig("tri_in_rect")
    k = 22
    for i, (X, Xn) in enumerate([((1.5, 4), "X"), ((3.7, 4), "Y")]):
        o = (i * 160, 0)
        shape(f, [(0, 0), (5, 0), (5, 4), (0, 4)], k, o)
        shape(f, [(0, 0), (5, 0), X], k, o, fill=BLUE)
        for p, n, d in [((0, 4), "A", (-10, 6)), ((5, 4), "B", (10, 6)), ((5, 0), "C", (10, -8)), ((0, 0), "D", (-10, -8)), (X, Xn, (0, 10))]:
            name(f, p, n, k, o, d)
        assert area([(0, 0), (5, 0), X]) == area([(0, 0), (5, 0), (5, 4), (0, 4)]) / 2
    return f

@fig
def tri_rect_7_1():
    f = Fig("tri_rect_7_1")
    k = 26
    X = (1.6, 4); Y = (1.6, 0)
    shape(f, [(0, 0), (5, 0), (5, 4), (0, 4)], k)
    shape(f, [(0, 0), (5, 0), X], k, fill=BLUE)
    f.seg(P(X[0] * k, X[1] * k), P(Y[0] * k, 0), dash="4,3", color=HELP)
    f.right(P(Y[0] * k, 0), 0, s=8)
    for p, n, d in [((0, 4), "A", (-10, 6)), ((5, 4), "B", (10, 6)), ((5, 0), "C", (10, -8)), ((0, 0), "D", (-10, -8)), (X, "X", (0, 10)), (Y, "Y", (0, -14))]:
        name(f, p, n, k, d=d)
    dim(f, P(5.4 * k, 0), P(5.4 * k, 4 * k), "4", off=(10, -4))
    dim(f, P(0, -26), P(5 * k, -26), "5", off=(0, -16))
    assert area([(0, 0), (5, 0), X]) == 10
    return f

@fig
def tri_height():
    f = Fig("tri_height")
    k = 24
    B, C, A = (0, 0), (6, 0), (2, 4)
    shape(f, [B, C, (6, 4), (0, 4)], k, fill="#ffffff", color=HELP)
    shape(f, [B, C, A], k, fill=BLUE)
    f.seg(P(2 * k, 4 * k), P(2 * k, 0), dash="4,3", color=ASK)
    f.right(P(2 * k, 0), 0, s=8)
    for p, n, d in [(B, "B", (-10, -8)), (C, "C", (10, -8)), (A, "A", (0, 10)), ((2, 0), "X", (0, -14)), ((0, 4), "E", (-10, 6)), ((6, 4), "D", (10, 6))]:
        name(f, p, n, k, d=d)
    f.label(P(2 * k + 8, 2 * k - 5), "height", anchor="start", size=11, color=ASK)
    f.label(P(3 * k, -30), "base", size=11, color=GIVEN)
    assert area([B, C, A]) == 0.5 * 6 * 4
    # obtuse case
    o = (200, 0)
    Bb, Cc, Aa, Dd = (2, 0), (6, 0), (0, 4), (0, 0)
    shape(f, [Bb, Cc, Aa], k, o, fill=BLUE)
    f.seg(P(o[0], 0), P(o[0] + 2 * k, 0), dash="4,3", color=HELP)
    f.seg(P(o[0], 0), P(o[0], 4 * k), dash="4,3", color=ASK)
    f.right(P(o[0], 0), 0, s=8)
    for p, n, d in [(Bb, "B", (0, -14)), (Cc, "C", (10, -8)), (Aa, "A", (-10, 6)), (Dd, "D", (-10, -8))]:
        name(f, p, n, k, o, d)
    f.label(P(o[0] + 8, 2 * k - 5), "h", anchor="start", size=12, color=ASK)
    assert area([Bb, Cc, Aa]) == area([Dd, Cc, Aa]) - area([Dd, Bb, Aa]) == 0.5 * 4 * 4
    return f

@fig
def altitude_by():
    f = Fig("altitude_by")
    k = 34
    # triangle with AX = 3 (height to BC = 5) and AC = 4: a 3-4-5 right triangle at A
    B, C = (0, 0), (5, 0)
    A = (5 - math.sqrt(7), 3)                # height AX = 3 above BC, and AC = 4
    assert abs(dist(A, C) - 4) < 1e-9
    shape(f, [B, C, A], k, fill=BLUE)
    X = (A[0], 0)
    f.seg(P(A[0] * k, A[1] * k), P(X[0] * k, 0), dash="4,3", color=ASK)
    # foot of perpendicular from B to AC
    ax, ay = C[0] - A[0], C[1] - A[1]
    t = ((B[0] - A[0]) * ax + (B[1] - A[1]) * ay) / (ax * ax + ay * ay)
    Y = (A[0] + t * ax, A[1] + t * ay)
    f.seg(P(0, 0), P(Y[0] * k, Y[1] * k), dash="4,3", color=GIVEN)
    BY = dist(B, Y)
    assert abs(0.5 * A[1] * 5 - 0.5 * 4 * BY) < 1e-9 and abs(BY - 3.75) < 1e-9
    for p, n, d in [(B, "B", (-10, -8)), (C, "C", (10, -8)), (A, "A", (0, 10)), (X, "X", (0, -14)), (Y, "Y", (8, 6))]:
        name(f, p, n, k, d=d)
    f.label(P(A[0] * k + 6, A[1] * k / 2 - 5), f"AX = {A[1]:g}", anchor="start", size=11, color=ASK)
    f.label(P(2.5 * k, -32), "BC = 5, AC = 4", size=11, color=GIVEN)
    return f

@fig
def diag_triangles():
    f = Fig("diag_triangles")
    k = 30
    A, B, C, D = (0, 4), (6, 4), (6, 0), (0, 0)
    O = (3, 2)
    for tri, col, lab in [([A, B, O], BLUE, "2"), ([B, C, O], GREEN, "3"), ([C, D, O], ORANGE, "4"), ([D, A, O], PINK, "1")]:
        shape(f, tri, k, fill=col)
        cx = sum(p[0] for p in tri) / 3; cy = sum(p[1] for p in tri) / 3
        f.text(P(cx * k, cy * k - 6), lab, size=14, bold=True)
        assert area(tri) == 6
    for p, n, d in [(A, "A", (-10, 6)), (B, "B", (10, 6)), (C, "C", (10, -8)), (D, "D", (-10, -8)), (O, "O", (0, -16))]:
        name(f, p, n, k, d=d)
    return f

@fig
def min_perimeter():
    f = Fig("min_perimeter")
    k = 30
    B, C = (0, 0), (4, 0)
    Bp, Cp = (0, 6), (4, 6)
    f.seg(P(-1 * k, 3 * k), P(6 * k, 3 * k), w=1.6)
    f.label(P(6 * k + 8, 3 * k - 5), "l", anchor="start", size=13, bold=True)
    A = (2, 3)
    for p, q, col in [(B, A, INK), (A, C, INK), (A, Cp, ASK), (B, C, INK)]:
        f.seg(P(p[0] * k, p[1] * k), P(q[0] * k, q[1] * k), color=col, w=2)
    f.seg(P(4 * k, 0), P(4 * k, 6 * k), color=HELP, dash="4,4")
    A2 = (3.3, 3)
    for p, q in [(B, A2), (A2, C)]:
        f.seg(P(p[0] * k, p[1] * k), P(q[0] * k, q[1] * k), color=HELP, w=1.4, dash="3,3")
    for p, n, d in [(B, "B", (-10, -8)), (C, "C", (10, -8)), (Cp, "C′", (12, 4)), (A, "A", (-12, 6)), (A2, "A′", (12, 6))]:
        name(f, p, n, k, d=d)
    per = lambda a: dist(B, a) + dist(a, C)
    assert per(A) < per(A2) and abs(per(A) - dist(B, Cp)) < 1e-9
    return f

@fig
def fio_triangles():
    f = Fig("fio_triangles")
    k = 30
    # (i) base BC 4, height AE 3
    o = (0, 0)
    shape(f, [(0, 0), (4, 0), (1.3, 3)], k, o, fill=BLUE)
    f.seg(P(1.3 * k, 3 * k), P(1.3 * k, 0), dash="4,3", color=ASK); f.right(P(1.3 * k, 0), 0, s=7)
    for p, n, d in [((0, 0), "B", (-10, -8)), ((4, 0), "C", (10, -8)), ((1.3, 3), "A", (0, 10)), ((1.3, 0), "E", (0, -14))]:
        name(f, p, n, k, o, d)
    f.label(P(1.3 * k + 6, 1.5 * k - 5), "3 cm", anchor="start", size=11, color=ASK); f.label(P(2 * k, -30), "BC = 4 cm", size=11, color=GIVEN)
    assert area([(0, 0), (4, 0), (1.3, 3)]) == 6
    # (ii) side EF = 5, height from D to EF = 3.2
    o = (170, 0)
    D = (0.0, 0.0)
    # choose E so that EF = 5 and the distance from D to line EF is 3.2
    Fp = (5.0, 0.0); ang = math.asin(3.2 / 5.0)          # angle EFD
    E = (5 - 5 * math.cos(ang), 5 * math.sin(ang))
    shape(f, [D, Fp, E], k, o, fill=BLUE)
    t = ((D[0] - E[0]) * (Fp[0] - E[0]) + (D[1] - E[1]) * (Fp[1] - E[1])) / 25
    N = (E[0] + t * (Fp[0] - E[0]), E[1] + t * (Fp[1] - E[1]))
    f.seg(P(o[0], 0), P(o[0] + N[0] * k, N[1] * k), dash="4,3", color=ASK)
    assert abs(dist(D, N) - 3.2) < 1e-9 and abs(dist(E, Fp) - 5) < 1e-9 and abs(area([D, Fp, E]) - 8) < 1e-9
    for p, n, d in [(D, "D", (-10, -8)), (Fp, "F", (10, -8)), (E, "E", (0, 10)), (N, "N", (8, 6))]:
        name(f, p, n, k, o, d)
    f.label(P(o[0] + N[0] * k / 2 - 30, N[1] * k / 2), "3.2 cm", size=11, color=ASK)
    f.label(P(o[0] + 4 * k, 2.2 * k), "EF = 5 cm", anchor="start", size=11, color=GIVEN)
    # (iii) right angle at A, AN = 4, AT = 3
    o = (390, 0)
    shape(f, [(0, 0), (3, 0), (0, 4)], k, o, fill=BLUE); f.right(P(o[0], 0), 0, s=8)
    for p, n, d in [((0, 0), "A", (-10, -8)), ((3, 0), "T", (10, -8)), ((0, 4), "N", (-10, 6))]:
        name(f, p, n, k, o, d)
    f.label(P(o[0] - 8, 2 * k - 5), "4 cm", anchor="end", size=11, color=GIVEN); f.label(P(o[0] + 1.5 * k, -20), "3 cm", size=11, color=GIVEN)
    for i, x in enumerate([60, 260, 430]): f.label(P(x, -54), f"({['i','ii','iii'][i]})", size=12, bold=True)
    return f

@fig
def fio_altitude():
    f = Fig("fio_altitude")
    k = 26
    X, A = (0, 0), (0, 4)
    C = (math.sqrt(64 - 16), 0); B = (C[0] - 6, 0)     # AC = 8 and BC = 6, with A 4 above line BC
    assert abs(dist(A, C) - 8) < 1e-9 and B[0] > 0
    shape(f, [B, C, A], k, fill=BLUE)
    f.seg(P(0, 0), P(B[0] * k, 0), dash="4,3", color=HELP); f.seg(P(0, 0), P(0, 4 * k), dash="4,3", color=ASK); f.right(P(0, 0), 0, s=8)
    ax, ay = C[0] - A[0], C[1] - A[1]
    t = ((B[0] - A[0]) * ax + (B[1] - A[1]) * ay) / 64
    Y = (A[0] + t * ax, A[1] + t * ay)
    f.seg(P(B[0] * k, 0), P(Y[0] * k, Y[1] * k), dash="4,3", color=GIVEN)
    BY = dist(B, Y)
    assert abs(BY - 3) < 1e-9
    for p, n, d in [(X, "X", (-10, -8)), (B, "B", (0, -14)), (C, "C", (10, -8)), (A, "A", (-10, 6)), (Y, "Y", (8, 6))]:
        name(f, p, n, k, d=d)
    f.label(P(-16, 2 * k - 5), "4", anchor="end", size=11, color=ASK)
    f.label(P((B[0] + C[0]) / 2 * k, -24), "BC = 6", size=11, color=GIVEN)
    f.label(P(C[0] / 2 * k + 10, 2.4 * k), "AC = 8", anchor="start", size=11, color=GIVEN)
    return f

@fig
def isosceles_sub():
    f = Fig("isosceles_sub")
    k = 16
    U, B, S_ = (0, 0), (12, 0), (6, 8)
    shape(f, [U, B, S_], k, fill="#ffffff")
    shape(f, [(6, 0), B, S_], k, fill=BLUE)
    f.seg(P(6 * k, 8 * k), P(6 * k, 0), w=1.6); f.right(P(6 * k, 0), 0, s=8)
    f.ticks(P(0, 0), P(6 * k, 8 * k)); f.ticks(P(12 * k, 0), P(6 * k, 8 * k))
    for p, n, d in [(U, "U", (-10, -8)), (B, "B", (10, -8)), (S_, "S", (0, 10)), ((6, 0), "E", (0, -14))]:
        name(f, p, n, k, d=d)
    assert area([(6, 0), B, S_]) == 24 and area([U, B, S_]) == 48
    return f

@fig
def three_squares():
    f = Fig("three_squares")
    k = 26
    s = 4
    for sq in ([(0, 0), (s, 0), (s, s), (0, s)], [(s, 0), (2 * s, 0), (2 * s, s), (s, s)], [(s, s), (2 * s, s), (2 * s, 2 * s), (s, 2 * s)]):
        shape(f, sq, k)
    red = [(0, 0), (s, 0), (s, 2 * s)]
    blue = [(0, 0), (s / 2, s), (0, s)]
    shape(f, red, k, fill="#e53935"); shape(f, blue, k, fill="#1e40af")
    for p, n, d in [((0, s), "A", (-10, 6)), ((s, s), "B", (8, 8)), ((s, 0), "C", (0, -14)), ((0, 0), "D", (-10, -8)), ((2 * s, 0), "E", (10, -8)),
                    ((2 * s, s), "F", (10, 0)), ((2 * s, 2 * s), "G", (10, 6)), ((s, 2 * s), "H", (-6, 10))]:
        name(f, p, n, k, d=d)
    assert area(red) == s * s and area(blue) == s * s / 4
    return f

@fig
def midpoint_triangle():
    f = Fig("midpoint_triangle")
    k = 34
    X, Y, Z = (2, 4), (0, 0), (6, 0)
    M, N = mul(add(X, Y), .5), mul(add(X, Z), .5)
    shape(f, [X, Y, Z], k, fill="#ffffff"); shape(f, [X, M, N], k, fill=BLUE)
    f.seg(P(N[0] * k, N[1] * k), P(0, 0), dash="4,3", color=HELP)
    for p, n, d in [(X, "X", (0, 10)), (Y, "Y", (-10, -8)), (Z, "Z", (10, -8)), (M, "M", (-12, 0)), (N, "N", (12, 0))]:
        name(f, p, n, k, d=d)
    assert area([X, M, N]) == area([X, Y, Z]) / 4
    return f

@fig
def river():
    f = Fig("river")
    k = 26
    f.poly([P(-k, 5 * k), P(11 * k, 5 * k), P(11 * k, 6 * k), P(-k, 6 * k)], fill="#81d4fa", color="#81d4fa")
    f.label(P(10 * k, 5.3 * k), "river", anchor="end", size=12, color=GIVEN)
    H, T = (1, 1), (8, 2)
    Tp = (8, 8)                               # reflection of the tank in the river bank y = 5
    t = (5 - H[1]) / (Tp[1] - H[1])
    R = (H[0] + t * (Tp[0] - H[0]), 5)
    f.seg(P(H[0] * k, H[1] * k), P(R[0] * k, R[1] * k), color=ASK, w=2.4)
    f.seg(P(R[0] * k, R[1] * k), P(T[0] * k, T[1] * k), color=ASK, w=2.4)
    f.seg(P(R[0] * k, R[1] * k), P(Tp[0] * k, Tp[1] * k), color=HELP, w=1.2, dash="4,4")
    for p, n, d in [(H, "house", (0, -16)), (T, "tank", (0, -16)), (Tp, "tank's mirror image", (0, 10)), (R, "R", (-10, -14))]:
        f.dot(P(p[0] * k, p[1] * k)); f.label(P(p[0] * k + d[0], p[1] * k + d[1] - 5), n, size=11)
    other = (3, 5)
    assert dist(H, R) + dist(R, T) < dist(H, other) + dist(other, T)
    return f

# ---------------------------------------------------------------- polygons
@fig
def quad_ac():
    f = Fig("quad_ac")
    k = 18
    A, C = (0, 0), (22, 0)
    B, D = (19, 3), (1.5, -3)
    shape(f, [A, D, C, B], k, fill=BLUE)
    f.seg(P(0, 0), P(22 * k, 0), w=1.4)
    f.seg(P(19 * k, 3 * k), P(19 * k, 0), dash="4,3", color=ASK); f.seg(P(1.5 * k, -3 * k), P(1.5 * k, 0), dash="4,3", color=ASK)
    for p, n, d in [(A, "A", (-10, 0)), (C, "C", (10, 0)), (B, "B", (8, 6)), (D, "D", (-6, -10)), ((19, 0), "M", (0, -14)), ((1.5, 0), "N", (0, 10))]:
        name(f, p, n, k, d=d)
    assert area([A, D, C, B]) == 66
    f.label(P(11 * k, 8), "AC = 22 cm", size=11, color=GIVEN)
    f.label(P(19 * k + 6, 1.5 * k - 5), "3", anchor="start", size=11, color=ASK); f.label(P(1.5 * k + 6, -1.5 * k - 5), "3", anchor="start", size=11, color=ASK)
    return f

@fig
def shaded_rect():
    f = Fig("shaded_rect")
    k = 16
    A, B, C, D = (0, 10), (18, 10), (18, 0), (0, 0)
    E, Fp = (10, 10), (0, 4)
    shape(f, [A, B, C, D], k)
    reg = [Fp, E, C, D]
    hatch(f, S(reg, k), gap=8)
    shape(f, reg, k, fill="none")
    assert area(reg) == 180 - 30 - 40 == 110
    for p, n, d in [(A, "A", (-10, 6)), (B, "B", (10, 6)), (C, "C", (10, -8)), (D, "D", (-10, -8)), (E, "E", (0, 10)), (Fp, "F", (-12, 0))]:
        name(f, p, n, k, d=d)
    dim(f, P(0, 10 * k + 22), P(10 * k, 10 * k + 22), "10 cm", off=(0, 6)); dim(f, P(10 * k, 10 * k + 22), P(18 * k, 10 * k + 22), "8 cm", off=(0, 6))
    dim(f, P(-26, 4 * k), P(-26, 10 * k), "6 cm", off=(-22, -4)); dim(f, P(-26, 0), P(-26, 4 * k), "4 cm", off=(-22, -4))
    dim(f, P(18 * k + 18, 0), P(18 * k + 18, 10 * k), "10 cm", off=(24, -4)); dim(f, P(0, -22), P(18 * k, -22), "18 cm", off=(0, -16))
    return f

@fig
def blue_fraction():
    f = Fig("blue_fraction")
    k = 26
    W, H = 6, 4
    Pt = (4.6, 1.8)
    shape(f, [(0, 0), (W, 0), (W, H), (0, H)], k)
    shape(f, [(0, H), (W, H), Pt], k, fill=SKY); shape(f, [(0, 0), (W, 0), Pt], k, fill=SKY)
    assert area([(0, H), (W, H), Pt]) + area([(0, 0), (W, 0), Pt]) == W * H / 2
    return f

# ---------------------------------------------------------------- parallelograms
@fig
def para_to_rect():
    f = Fig("para_to_rect")
    k = 24
    A, B, C, D = (2, 3), (8, 3), (6, 0), (0, 0)
    X, Y = (2, 0), (8, 0)
    shape(f, [D, C, B, A], k, fill=BLUE)
    shape(f, [D, X, A], k, fill=ORANGE)
    shape(f, [C, Y, B], k, fill="none", color=HELP)
    f.seg(P(6 * k, 0), P(8 * k, 0), dash="4,3", color=HELP)
    f.right(P(2 * k, 0), 0, s=7); f.right(P(8 * k, 0), 90, s=7)
    for p, n, d in [(A, "A", (-8, 8)), (B, "B", (8, 8)), (C, "C", (0, -14)), (D, "D", (-10, -8)), (X, "X", (0, -14)), (Y, "Y", (10, -8))]:
        name(f, p, n, k, d=d)
    assert area([D, C, B, A]) == area([X, Y, B, A]) == 18
    f.label(P(4 * k, -34), "cut off triangle AXD and slide it to BYC: rectangle ABYX", size=11, color=ANS)
    return f

@fig
def para_grid():
    f = Fig("para_grid")
    k = 16
    x0 = 0
    shifts = [0, 1, 2, 3, -1, -2]
    pers = []
    for i, sft in enumerate(shifts):
        o = (x0, 0)
        pts = [(0, 0), (4, 0), (4 + sft, 3), (sft, 3)]
        shape(f, pts, k, o, fill=BLUE)
        assert area(pts) == 12
        per = 2 * (4 + math.hypot(sft, 3))
        pers.append(per)
        f.label(P(x0 + (2 + sft / 2) * k, -18), f"({'abcdef'[i]})", size=11, bold=True)
        x0 += (5 + abs(sft)) * k + 10
    assert min(pers) == pers[0]
    f.label(P(0, -40), "all: base 4, height 3 (on a grid of unit squares)", anchor="start", size=11, color=HELP)
    return f

@fig
def para_areas():
    f = Fig("para_areas")
    k = 20
    # (i) base 7 height 4 ; (ii) base 5 height 3 ; (iii) side 5, height to it 4.8 ; (iv) side 2, height to it 4.4
    o = (0, 0)
    shape(f, [(0, 0), (7, 0), (8.5, 4), (1.5, 4)], k, o, fill=BLUE)
    f.seg(P(1.5 * k, 4 * k), P(1.5 * k, 0), dash="4,3", color=ASK)
    f.label(P(1.5 * k + 6, 2 * k - 5), "4 cm", anchor="start", size=11, color=ASK); f.label(P(3.5 * k, -18), "7 cm", size=11, color=GIVEN)
    o = (210, 0)
    shape(f, [(0, 0), (5, 0), (6.5, 3), (1.5, 3)], k, o, fill=BLUE)
    f.seg(P(o[0] + 1.5 * k, 3 * k), P(o[0] + 1.5 * k, 0), dash="4,3", color=ASK)
    f.label(P(o[0] + 1.5 * k + 6, 1.5 * k - 5), "3 cm", anchor="start", size=11, color=ASK); f.label(P(o[0] + 2.5 * k, -18), "5 cm", size=11, color=GIVEN)
    # (iii): side of length 5 (vertical-ish) with perpendicular distance 4.8 to the opposite side
    o = (0, -150)
    pts = [(0, 0), (4.8, 0), (4.8, 5), (0, 5)]
    sh = 1.4
    pts = [(0, 0), (4.8, sh), (4.8, 5 + sh), (0, 5)]
    shape(f, pts, k, o, fill=BLUE)
    f.seg(P(o[0], o[1]), P(o[0] + 4.8 * k, o[1]), dash="4,3", color=ASK)
    f.label(P(o[0] + 2.4 * k, o[1] - 16), "4.8 cm", size=11, color=ASK); f.label(P(o[0] + 4.8 * k + 10, o[1] + (2.5 + sh) * k), "5 cm", anchor="start", size=11, color=GIVEN)
    assert area(pts) == 4.8 * 5
    o = (210, -150)
    pts = [(0, 0), (4.4, 0.6), (4.4, 2.6), (0, 2)]
    shape(f, pts, k, o, fill=BLUE)
    f.seg(P(o[0], o[1]), P(o[0] + 4.4 * k, o[1]), dash="4,3", color=ASK)
    f.label(P(o[0] + 2.2 * k, o[1] - 16), "4.4 cm", size=11, color=ASK); f.label(P(o[0] + 4.4 * k + 10, o[1] + 1.6 * k), "2 cm", anchor="start", size=11, color=GIVEN)
    assert abs(area(pts) - 8.8) < 1e-9
    for i, (x, y) in enumerate([(70, 110), (270, 110), (50, -60), (250, -90)]):
        f.label(P(x, y), f"({['i','ii','iii','iv'][i]})", size=12, bold=True)
    return f

@fig
def find_qn():
    f = Fig("find_qn")
    k = 22
    S_, R = (0, 0), (12, 0)
    # PS = 7.6 and height 6: P is 6 above SR, at distance 7.6 from S
    px = math.sqrt(7.6 ** 2 - 36)
    Pp = (-px, 6); Q = (12 - px, 6)            # the parallelogram leans to the left
    shape(f, [S_, R, Q, Pp], k, fill=BLUE)
    f.seg(P(Q[0] * k, 6 * k), P(Q[0] * k, 0), dash="4,3", color=ASK)
    # N: foot of perpendicular from Q to line PS
    dx, dy = Pp[0], Pp[1]
    t = (Q[0] * dx + Q[1] * dy) / (dx * dx + dy * dy)
    N = (t * dx, t * dy)
    f.seg(P(Q[0] * k, Q[1] * k), P(N[0] * k, N[1] * k), dash="4,3", color=GIVEN)
    QN = dist(Q, N)
    assert abs(QN - 72 / 7.6) < 1e-9
    for p, n, d in [(S_, "S", (-10, -8)), (R, "R", (10, -8)), (Q, "Q", (8, 8)), (Pp, "P", (-8, 8)), ((Q[0], 0), "M", (0, -14)), (N, "N", (-16, 12))]:
        name(f, p, n, k, d=d)
    f.label(P(Q[0] * k + 6, 3 * k - 5), "6 cm", anchor="start", size=11, color=ASK)
    f.label(P(6 * k, -24), "SR = 12 cm", size=11, color=GIVEN); f.label(P(-px / 2 * k - 50, 3 * k), "PS = 7.6 cm", size=11, color=GIVEN)
    return f

@fig
def rect_vs_para():
    f = Fig("rect_vs_para")
    k = 30
    shape(f, [(0, 0), (5, 0), (5, 4), (0, 4)], k, fill="#ffffff")
    a = math.radians(60)
    tx, ty = 4 * math.cos(a), 4 * math.sin(a)
    shape(f, [(0, 0), (5, 0), (5 + tx, ty), (tx, ty)], k, fill="none", color=GIVEN)
    assert 5 * ty < 5 * 4
    f.label(P(2.5 * k, -18), "5 cm", size=11, color=GIVEN)
    f.label(P(-10, 2 * k - 5), "4 cm", anchor="end", size=11)
    f.label(P(tx / 2 * k + 14, ty / 2 * k), "4 cm", anchor="start", size=11, color=GIVEN)
    return f

@fig
def rhombus_rect():
    f = Fig("rhombus_rect")
    k = 22
    A, B, C, D = (4, 6), (0, 3), (4, 0), (8, 3)
    shape(f, [A, B, C, D], k, fill=BLUE)
    f.seg(P(4 * k, 6 * k), P(4 * k, 0), dash="4,3", color=HELP); f.seg(P(0, 3 * k), P(8 * k, 3 * k), dash="4,3", color=HELP)
    for p, n, d in [(A, "A", (0, 10)), (B, "B", (-10, 0)), (C, "C", (0, -14)), (D, "D", (10, 0)), ((4, 3), "O", (8, 6))]:
        name(f, p, n, k, d=d)
    o = (230, 0)
    shape(f, [(0, 0), (6, 0), (6, 4), (0, 4)], k, o, fill=BLUE)
    f.label(P(o[0] + 3 * k, -18), "half of BD", size=11, color=GIVEN); f.label(P(o[0] + 6 * k + 8, 2 * k - 5), "AC", anchor="start", size=11, color=GIVEN)
    assert area([A, B, C, D]) == 0.5 * 6 * 8 == 4 * 6
    f.text(P(200, 3 * k - 6), "→", size=22, bold=True, color=ASK)
    return f

@fig
def trapezium_formula():
    f = Fig("trapezium_formula")
    k = 22
    Z, Y, X, W = (0, 0), (12, 0), (9, 4), (2, 4)
    shape(f, [Z, Y, X, W], k, fill=BLUE)
    for xx in (2, 9):
        f.seg(P(xx * k, 4 * k), P(xx * k, 0), dash="4,3", color=ASK); f.right(P(xx * k, 0), 0 if xx == 2 else 90, s=7)
    for p, n, d in [(Z, "Z", (-10, -8)), (Y, "Y", (10, -8)), (X, "X", (8, 8)), (W, "W", (-8, 8)), ((2, 0), "M", (0, -14)), ((9, 0), "N", (0, -14))]:
        name(f, p, n, k, d=d)
    f.label(P(5.5 * k, 4 * k + 10), "a", size=13, color=GIVEN); f.label(P(1 * k, -16), "x", size=12, color=GIVEN); f.label(P(10.5 * k, -16), "y", size=12, color=GIVEN)
    f.label(P(2 * k + 6, 2 * k - 5), "h", anchor="start", size=13, color=ASK)
    a, b, h = 7, 12, 4
    assert area([Z, Y, X, W]) == F(1, 2) * h * (a + b)
    return f

@fig
def trapezium_doubled():
    f = Fig("trapezium_doubled")
    k = 22
    T = [(0, 0), (7, 0), (5, 3), (1, 3)]             # bottom 7, top 4
    T2 = [(7, 0), (11, 0), (12, 3), (5, 3)]          # the copy turned round: top 7, bottom 4
    shape(f, T, k, fill=BLUE); shape(f, T2, k, fill=ORANGE)
    big = [(0, 0), (11, 0), (12, 3), (1, 3)]
    assert area(T) + area(T2) == area(big) == 3 * 11
    f.label(P(3.5 * k, -16), "b", size=12, color=GIVEN); f.label(P(9 * k, -16), "a", size=12, color=GIVEN)
    f.label(P(3 * k, 3 * k + 8), "a", size=12, color=GIVEN); f.label(P(8.5 * k, 3 * k + 8), "b", size=12, color=GIVEN)
    f.label(P(6 * k, -36), "two copies make a parallelogram with base a + b and the same height", size=11, color=ANS)
    return f

@fig
def fio_trapeziums():
    f = Fig("fio_trapeziums")
    k = 9
    figs = [  # (pts, area, label position)
        ([(0, 0), (16, 0), (16, 7), (0, 10)], 136),     # (i) parallel sides 10 and 7, 16 apart
        ([(0, 0), (36, 0), (24, 14), (0, 14)], 420),    # (ii) parallel sides 36 and 24, height 14
        ([(0, 0), (10, 4), (10, 10), (0, 14)], 100),    # (iii) parallel sides 14 and 6, 10 apart
        ([(0, 0), (18, 0), (14, 8), (2, 8)], 120),      # (iv) parallel sides 18 and 12, height 8
    ]
    xs = [0, 220, 0, 220]; ys = [0, 0, -190, -190]
    labels = [[("10 ft", (-1.5, 5)), ("7 ft", (17.5, 3.5)), ("16 ft", (8, -2.2))],
              [("36 m", (18, -2.2)), ("24 m", (12, 15.4)), ("14 m", (25.5, 7))],
              [("14 in", (-2.4, 7)), ("6 in", (11.6, 7)), ("10 in", (5, 7.5))],
              [("18 ft", (9, -2.2)), ("12 ft", (8, 9.4)), ("8 ft", (3.6, 4))]]
    for i, (pts, a) in enumerate(figs):
        o = (xs[i], ys[i])
        assert area(pts) == a
        shape(f, pts, k * (0.55 if i == 1 else 1), o, fill=BLUE)
        kk = k * (0.55 if i == 1 else 1)
        for txt, (lx, ly) in labels[i]:
            f.label(P(o[0] + lx * kk, o[1] + ly * kk - 5), txt, size=11, color=GIVEN)
        f.label(P(o[0] + 40, o[1] - 34), f"({['i','ii','iii','iv'][i]})", size=12, bold=True)
    return f

@fig
def hexagon_split():
    f = Fig("hexagon_split")
    k = 50
    H = [(math.cos(math.radians(60 * i)), math.sin(math.radians(60 * i))) for i in range(6)]
    trap = [H[3], H[4], H[5], H[0]]            # lower half
    tri = [H[0], H[1], (0, 0)]
    rho = [(0, 0), H[1], H[2], H[3]]
    shape(f, trap, k, fill=BLUE); shape(f, tri, k, fill=ORANGE); shape(f, rho, k, fill=GREEN)
    a1, a2, a3 = area(trap), area(tri), area(rho)
    assert abs(a1 / a2 - 3) < 1e-9 and abs(a3 / a2 - 2) < 1e-9
    return f

@fig
def trapezium_triangle():
    f = Fig("trapezium_triangle")
    k = 24
    Z, Y, X, W = (1, 4), (5, 4), (8, 0), (0, 0)
    A = mul(add(X, Y), .5)
    # B: where line ZA meets line WX extended
    t = (0 - Z[1]) / (A[1] - Z[1])
    B = (Z[0] + t * (A[0] - Z[0]), 0)
    shape(f, [W, X, Y, Z], k, fill=BLUE)
    shape(f, [A, X, B], k, fill=ORANGE)
    f.seg(P(Z[0] * k, Z[1] * k), P(B[0] * k, 0), w=1.6, color=ASK)
    f.seg(P(8 * k, 0), P(B[0] * k, 0), dash="4,3", color=HELP)
    for p, n, d in [(Z, "Z", (-8, 8)), (Y, "Y", (8, 8)), (X, "X", (0, -14)), (W, "W", (-10, -8)), (A, "A", (10, 4)), (B, "B", (10, -8))]:
        name(f, p, n, k, d=d)
    assert abs(area([W, X, Y, Z]) - area([Z, W, B])) < 1e-9
    return f

@fig
def trap_to_rect():
    f = Fig("trap_to_rect")
    k = 26
    A, B, C, D = (2, 4), (7, 4), (9, 0), (0, 0)
    I, J = mul(add(A, D), .5), mul(add(B, C), .5)
    H, E = (I[0], 4), (J[0], 4); G, Fp = (I[0], 0), (J[0], 0)
    shape(f, [D, C, B, A], k, fill=BLUE)
    shape(f, [G, Fp, E, H], k, fill="none", color=ASK)
    assert abs(area([D, C, B, A]) - area([G, Fp, E, H])) < 1e-9
    for p, n, d in [(A, "A", (0, 10)), (B, "B", (0, 10)), (C, "C", (10, -8)), (D, "D", (-10, -8)), (H, "H", (-10, 6)), (E, "E", (10, 6)),
                    (G, "G", (0, -14)), (Fp, "F", (0, -14)), (I, "I", (-12, 0)), (J, "J", (12, 0))]:
        name(f, p, n, k, d=d)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
