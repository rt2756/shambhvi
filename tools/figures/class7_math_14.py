"""Figures for class 7 maths Ch 14, Constructions and Tilings. Every construction is carried out
here with exact circle intersections, the way it would be done with ruler and compass, and the
result is asserted (right angles are 90°, bisected angles are halves, copied angles are equal,
constructed lines are parallel). Tilings are found by a search and drawn tile by tile, and the
colour counts in the chessboard arguments are counted from the drawn squares."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "14")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

ARC = "#8a969c"

def inter(c1, r1, c2, r2):
    """The two meeting points of circles (c1, r1) and (c2, r2): (left of c1->c2, right of it)."""
    d = dist(c1, c2)
    assert abs(r1 - r2) < d < r1 + r2, "circles do not meet"
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    m = along(c1, dirto(c1, c2), a)
    return along(m, dirto(c1, c2) + 90, h), along(m, dirto(c1, c2) - 90, h)

def tick_arc(f, c, p, sweep=14, color=ARC):
    """A short compass arc centred at c passing through p (how a construction mark looks)."""
    a = dirto(c, p)
    f.carc(c, dist(c, p), a - sweep, a + sweep, color=color, w=1.5)

def ang(o, p, q):
    """Angle pOq in degrees (0..180)."""
    a = abs(dirto(o, p) - dirto(o, q)) % 360
    return min(a, 360 - a)

def pt(f, p, name, dx=0, dy=12, color=INK):
    f.dot(p, color=color)
    if name: f.label(add(p, (dx, dy)), name, size=14, bold=True, color=color)

def rect(f, x, y, w, h, fill, color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def poly_reg(c, r, n, a0=90):
    return [along(c, a0 + 360 * k / n, r) for k in range(n)]

def closed(f, pts, color=INK, w=2.2, dash=None):
    for i in range(len(pts)):
        f.seg(pts[i], pts[(i + 1) % len(pts)], color=color, w=w, dash=dash)

# ================================================================ perpendicular bisector
@fig
def perp_bisector():
    f = Fig("perp_bisector")
    X, Y, r = P(0, 0), P(200, 0), 140
    A, B = inter(X, r, Y, r)
    f.seg(X, Y)
    for c in (X, Y):
        tick_arc(f, c, A, 12); tick_arc(f, c, B, 12)
    O = meet(A, dirto(A, B), X, 0)
    assert abs(dist(O, X) - dist(O, Y)) < 1e-9 and abs(ang(O, A, X) - 90) < 1e-9
    f.seg(along(A, 90, 20), along(B, 270, 20), color=ANS, w=2.2)
    f.right(O, 0)
    pt(f, X, "X", -14, 0); pt(f, Y, "Y", 14, 0); pt(f, A, "A", 14, 8); pt(f, B, "B", 14, -8)
    pt(f, O, "O", -12, -14)
    return f

@fig
def eye():
    f = Fig("eye")
    X, Y, r = P(0, 0), P(200, 0), 150
    A, B = inter(X, r, Y, r)
    f.seg(X, Y, color=ARC, w=1.2, dash="5,4")
    a = dirto(A, X)
    f.carc(A, r, dirto(A, X), dirto(A, Y), color=INK, w=2.6)   # lower lid, centre above
    f.carc(B, r, dirto(B, Y), dirto(B, X), color=INK, w=2.6)   # upper lid, centre below
    f.circle(P(100, 0), 22, color=GIVEN, w=2.5)
    for p, n, dy in ((A, "A", 12), (B, "B", -14), (X, "X", 0), (Y, "Y", 0)):
        pt(f, p, n, -14 if n == "X" else (14 if n == "Y" else 0), dy)
    f.seg(A, X, color=ARC, w=1, dash="3,3"); f.seg(B, X, color=ARC, w=1, dash="3,3")
    assert abs(dist(A, X) - dist(B, Y)) < 1e-9
    return f

@fig
def perp_proof():
    f = Fig("perp_proof")
    X, Y, r = P(0, 0), P(200, 0), 150
    A, B = inter(X, r, Y, r)
    O = P(100, 0)
    for p, q in ((A, X), (A, Y), (B, X), (B, Y)): f.seg(p, q, color=GIVEN, w=2)
    f.seg(X, Y); f.seg(A, B, color=ANS)
    f.ticks(A, X, 1); f.ticks(A, Y, 1); f.ticks(B, X, 2); f.ticks(B, Y, 2)
    f.right(O, 0)
    pt(f, X, "X", -14, 0); pt(f, Y, "Y", 14, 0); pt(f, A, "A", 0, 14); pt(f, B, "B", 0, -16)
    pt(f, O, "O", 12, 12)
    return f

@fig
def eyes_cd():
    f = Fig("eyes_cd")
    X, Y = P(0, 0), P(200, 0)
    A, B = inter(X, 150, Y, 150)
    C, D = inter(X, 190, Y, 190)
    f.seg(X, Y, color=ARC, w=1.2, dash="5,4")
    f.seg(along(C, 90, 10), along(D, 270, 10), color=ANS, w=1.6, dash="6,4")
    f.carc(C, 190, dirto(C, X), dirto(C, Y), color=INK, w=2.4)
    f.carc(D, 190, dirto(D, Y), dirto(D, X), color=INK, w=2.4)
    for p, n in ((A, "A"), (B, "B"), (C, "C"), (D, "D")):
        assert abs(dist(p, X) - dist(p, Y)) < 1e-9 and abs(p[0] - 100) < 1e-9
        pt(f, p, n, 14, 0)
    pt(f, X, "X", -14, 0); pt(f, Y, "Y", 14, 0)
    f.label(P(100, -210), "centres C and D: a flatter eye", size=12, color=HELP)
    return f

@fig
def bisector_unequal_radii():
    f = Fig("bisector_unequal_radii")
    X, Y = P(0, 0), P(200, 0)
    A, _ = inter(X, 160, Y, 160); _, B = inter(X, 115, Y, 115)
    f.seg(X, Y)
    tick_arc(f, X, A); tick_arc(f, Y, A); tick_arc(f, X, B); tick_arc(f, Y, B)
    f.seg(along(A, 90, 15), along(B, 270, 15), color=ANS)
    assert abs(A[0] - 100) < 1e-9 and abs(B[0] - 100) < 1e-9
    pt(f, X, "X", -14, 0); pt(f, Y, "Y", 14, 0); pt(f, A, "A", 14, 6); pt(f, B, "B", 14, -6)
    f.label(P(100, -110), "radius above 160, below 115: still the bisector", size=12, color=HELP)
    return f

@fig
def bisector_same_side():
    f = Fig("bisector_same_side")
    X, Y = P(0, 0), P(200, 0)
    A, _ = inter(X, 180, Y, 180); C, _ = inter(X, 125, Y, 125)
    f.seg(X, Y)
    for p in (A, C): tick_arc(f, X, p); tick_arc(f, Y, p)
    f.seg(along(A, 90, 15), P(100, -40), color=ANS)
    assert abs(A[0] - C[0]) < 1e-9
    pt(f, X, "X", -14, 0); pt(f, Y, "Y", 14, 0); pt(f, A, "A", 14, 6); pt(f, C, "C", 14, 6)
    pt(f, P(100, 0), "O", 12, -12)
    return f

@fig
def bisector_wrong():
    f = Fig("bisector_wrong")
    X, Y = P(0, 0), P(200, 0)
    A, _ = inter(X, 170, Y, 110)
    f.seg(X, Y)
    tick_arc(f, X, A); tick_arc(f, Y, A)
    f.seg(P(100, -30), P(100, 190), color=ANS, w=1.6, dash="6,4")
    f.seg(X, A, color=ARC, w=1, dash="3,3"); f.seg(Y, A, color=ARC, w=1, dash="3,3")
    assert A[0] > 100 + 20
    pt(f, X, "X", -14, 0); pt(f, Y, "Y", 14, 0); pt(f, A, "A", 14, 6, color=ASK)
    f.label(P(40, 110), "170", size=12, color=HELP); f.label(P(190, 70), "110", size=12, color=HELP)
    f.label(P(100, -50), "dashed: the true bisector; A is not on it", size=12, color=HELP)
    return f

@fig
def four_petals():
    f = Fig("four_petals"); s = 70
    O = P(0, 0)
    f.seg(P(-2 * s - 15, 0), P(2 * s + 15, 0), color=ARC, w=1, dash="5,4")
    f.seg(P(0, -2 * s - 15), P(0, 2 * s + 15), color=ARC, w=1, dash="5,4")
    for a in (0, 90, 180, 270):
        X, Y = O, along(O, a, 2 * s)
        r = 1.2 * s
        A, B = inter(X, r, Y, r)
        for c, p, q in ((A, X, Y), (B, Y, X)):
            f.carc(c, r, dirto(c, p), dirto(c, q), color=INK, w=2.4)
    return f

@fig
def right_angle_at_O():
    f = Fig("right_angle_at_O")
    O = P(0, 0); d = 70
    X, Y = P(-d, 0), P(d, 0)
    f.seg(P(-130, 0), P(130, 0))
    f.carc(O, d, 170, 190, color=ARC); f.carc(O, d, -10, 10, color=ARC)
    A, _ = inter(X, 110, Y, 110)
    tick_arc(f, X, A); tick_arc(f, Y, A)
    f.seg(O, along(A, 90, 15), color=ANS)
    assert abs(ang(O, A, Y) - 90) < 1e-9
    f.right(O, 0)
    pt(f, O, "O", 12, -14); pt(f, X, "X", 0, -16); pt(f, Y, "Y", 0, -16); pt(f, A, "A", 14, 6)
    return f

@fig
def rope():
    f = Fig("rope")
    X, Y, L = P(0, 0), P(200, 0), 260
    A, B = inter(X, L / 2, Y, L / 2)
    f.seg(X, Y)
    rope_c = "#a1887f"
    for p in (A, B):
        f.seg(X, p, color=rope_c, w=3); f.seg(p, Y, color=rope_c, w=3)
    f.seg(A, B, color=ANS, w=1.8, dash="6,4")
    for p in (X, Y): rect(f, p[0] - 3, p[1] - 3, 6, 14, "#5d4037", "#5d4037")
    pt(f, X, "X", -16, 0); pt(f, Y, "Y", 16, 0)
    pt(f, A, "A (middle of the rope)", 0, 14); pt(f, B, "B", 0, -16)
    assert abs(dist(X, A) - dist(Y, A)) < 1e-9
    return f

# ================================================================ angle bisector and copying
def bisect(f, O, a1, a2, r=90, r2=80, show=True, names=("A", "B", "C")):
    A, B = along(O, a1, r), along(O, a2, r)
    C = inter(A, r2, B, r2)[0 if (a2 - a1) % 360 < 180 else 1]
    if show:
        f.carc(O, r, a1 - 6, a2 + 6, color=ARC)
        tick_arc(f, A, C); tick_arc(f, B, C)
    assert abs(ang(O, A, C) - ang(O, B, C)) < 1e-9
    return A, B, C

@fig
def angle_bisector():
    f = Fig("angle_bisector")
    O = P(0, 0)
    f.seg(O, along(O, 0, 220)); f.seg(O, along(O, 70, 220))
    A, B, C = bisect(f, O, 0, 70, r=100, r2=90)
    f.seg(O, along(O, dirto(O, C), 230), color=ANS)
    assert abs(dirto(O, C) - 35) < 1e-9
    f.angle(O, 0, 35, "35°", expect=35, r=40, lr=62, color=GIVEN)
    f.angle(O, 35, 70, "35°", expect=35, r=48, lr=70, color=GIVEN)
    pt(f, O, "O", -12, -12); pt(f, A, "A", 4, -16); pt(f, B, "B", -14, 4); pt(f, C, "C", 14, 2)
    f.label(along(O, 0, 230), "Y", size=14, bold=True); f.label(along(O, 70, 232), "X", size=14, bold=True)
    return f

@fig
def bisector_far_side():
    f = Fig("bisector_far_side")
    O = P(0, 0); r = 80
    f.seg(O, along(O, 0, 200)); f.seg(O, along(O, 70, 200))
    A, B = along(O, 0, r), along(O, 70, r)
    C = min(inter(A, 110, B, 110), key=lambda q: dist(q, O))   # the meeting point on O's side
    assert dist(C, O) < dist(C, along(O, 35, 200))
    tick_arc(f, A, C); tick_arc(f, B, C); f.carc(O, r, -6, 76, color=ARC)
    f.seg(C, along(O, 35, 210), color=ANS)
    assert abs((dirto(C, O) - 35) % 180) < 1e-6
    pt(f, O, "O", 6, -16); pt(f, A, "A", 4, -16); pt(f, B, "B", -14, 4); pt(f, C, "C", -14, -4)
    f.label(along(O, 0, 210), "Y", size=14, bold=True); f.label(along(O, 70, 212), "X", size=14, bold=True)
    return f

@fig
def eight_petals():
    f = Fig("eight_petals"); R = 130
    O = P(0, 0)
    for k in range(8):
        f.seg(O, along(O, 45 * k, R + 10), color=ARC, w=1, dash="5,4")
    for k in range(8):
        a = 45 * k
        X, Y = O, along(O, a, R)
        rho = 1.1 * R
        A, B = inter(X, rho, Y, rho)
        f.carc(A, rho, dirto(A, X), dirto(A, Y), color=INK, w=2.2)
        f.carc(B, rho, dirto(B, Y), dirto(B, X), color=INK, w=2.2)
    f.angle(O, 0, 45, "45°", expect=45, r=34, lr=52, color=GIVEN)
    return f

@fig
def petals_square():
    f = Fig("petals_square"); s = 200; h = s / 2
    rect(f, -h, -h, s, s, "#ffffff")
    f.seg(P(-h, 0), P(h, 0), color=ARC, w=1, dash="5,4"); f.seg(P(0, -h), P(0, h), color=ARC, w=1, dash="5,4")
    # each petal: two quarter circles of radius h, centred at a corner and at the centre's opposite
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        c1 = P(sx * h, 0); c2 = P(0, sy * h)
        a1 = dirto(c1, P(0, 0)); a2 = dirto(c1, P(sx * h, sy * h))
        f.carc(c1, h, min(a1, a2) if abs(a1 - a2) < 180 else max(a1, a2), (max(a1, a2) if abs(a1 - a2) < 180 else min(a1, a2) + 360), color=INK, w=2.4)
        b1 = dirto(c2, P(0, 0)); b2 = dirto(c2, P(sx * h, sy * h))
        f.carc(c2, h, min(b1, b2) if abs(b1 - b2) < 180 else max(b1, b2), (max(b1, b2) if abs(b1 - b2) < 180 else min(b1, b2) + 360), color=INK, w=2.4)
    for p in (P(h, 0), P(0, h), P(-h, 0), P(0, -h)): f.dot(p, color=GIVEN)
    f.label(P(h + 8, 0), "M", anchor="start", size=13, bold=True, color=GIVEN)
    return f

@fig
def copy_angle():
    f = Fig("copy_angle"); r = 70
    A = P(0, 0); a = 48
    f.seg(A, along(A, 0, 170)); f.seg(A, along(A, a, 170))
    C, B = along(A, 0, r), along(A, a, r)
    f.carc(A, r, -8, a + 8, color=ARC)
    X = P(260, 0)
    f.seg(X, along(X, 0, 170))
    Z = along(X, 0, r)
    f.carc(X, r, -8, a + 20, color=ARC)
    Yp = inter(X, r, Z, dist(B, C))[0]
    f.carc(Z, dist(B, C), dirto(Z, Yp) - 12, dirto(Z, Yp) + 12, color=GIVEN, w=1.6)
    f.seg(X, along(X, dirto(X, Yp), 170), color=ANS)
    assert abs(dirto(X, Yp) - a) < 1e-9
    f.seg(B, C, color=GIVEN, w=1.4, dash="4,3"); f.seg(Yp, Z, color=GIVEN, w=1.4, dash="4,3")
    for p, n, dx, dy in ((A, "A", -12, -12), (B, "B", -12, 8), (C, "C", 4, -16), (X, "X", -12, -12),
                         (Yp, "Y", -12, 8), (Z, "Z", 4, -16)):
        pt(f, p, n, dx, dy)
    return f

@fig
def fig_units():
    """The repeating unit: a 'fan' of radius r and angle 70°, copied upright and upside down."""
    f = Fig("fig_units"); r = 80; a = 70
    for i in range(3):
        V = P(i * 2 * r * math.sin(math.radians(a / 2)) * 1.0, 0)
        Vt = along(V, 90 - a / 2, r)
        # upward fan: vertex at bottom
        f.seg(V, along(V, 90 - a / 2, r)); f.seg(V, along(V, 90 + a / 2, r))
        f.carc(V, r, 90 - a / 2, 90 + a / 2, color=INK, w=2.2)
    for i in range(2):
        V = P((2 * i + 1) * r * math.sin(math.radians(a / 2)), r * math.cos(math.radians(a / 2)))
        f.seg(V, along(V, 270 - a / 2, r)); f.seg(V, along(V, 270 + a / 2, r))
        f.carc(V, r, 270 - a / 2, 270 + a / 2, color=INK, w=2.2)
    w = 2 * r * math.sin(math.radians(a / 2))
    # neighbouring units share a straight edge: the up-fan's right arm is the down-fan's left arm
    up_right_tip = along(P(0, 0), 90 - a / 2, r)
    assert abs(up_right_tip[0] - w / 2) < 1e-9 and abs(up_right_tip[1] - r * math.cos(math.radians(a / 2))) < 1e-9
    return f

# ================================================================ parallel line
@fig
def parallel_line():
    f = Fig("parallel_line"); t = 38; r = 50
    A = P(0, 0); B = along(A, t, 150)
    f.seg(P(-120, 0), P(220, 0)); f.label(P(230, 0), "m", anchor="start", size=14, bold=True)
    f.seg(along(A, t + 180, 90), along(A, t, 260)); f.label(along(A, t, 272), "l", size=14, bold=True)
    C, D = along(A, 0, r), along(A, t, r)
    E, F = along(B, 0, r), along(B, t, r)
    f.carc(A, r, -8, t + 10, color=ARC); f.carc(B, r, -8, t + 10, color=ARC)
    tick_arc(f, F, E, 18, color=GIVEN)
    assert abs(dist(E, F) - dist(C, D)) < 1e-9 and abs(dirto(B, E)) < 1e-9
    f.seg(along(B, 180, 220), along(B, 0, 120), color=ANS); f.label(along(B, 0, 130), "n", anchor="start", size=14, bold=True, color=ANS)
    for p, n, dx, dy in ((A, "A", -6, -16), (B, "B", -12, 10), (C, "C", 6, -14), (D, "D", -12, 8),
                         (E, "E", 6, -14), (F, "F", -12, 8)):
        pt(f, p, n, dx, dy)
    f.label(P(60, -40), "m ∥ n", size=14, bold=True, color=ANS)
    return f

@fig
def star8():
    f = Fig("star8"); r = 70
    O = P(0, 0)
    inner = [along(O, 90 + 45 * k, r) for k in range(8)]     # A at the top, then H, G, ... going left
    names_in = ["A", "H", "G", "F", "E", "D", "C", "B"]
    names_out = ["S", "Z", "Y", "X", "W", "V", "U", "T"]
    for k in range(8):
        p, q = inner[k], inner[(k + 1) % 8]
        tip = add(p, sub(q, O)) if False else (p[0] + q[0] - O[0], p[1] + q[1] - O[1])
        assert abs(dirto(p, tip) - dirto(O, q)) < 1e-6 and abs(dirto(q, tip) - dirto(O, p)) < 1e-6
        f.poly([O, p, tip], fill="#9e9e9e", color=INK)
        f.poly([O, tip, q], fill="#ffffff", color=INK)
        f.label(along(O, dirto(O, tip), dist(O, tip) + 14), names_out[k], size=13, bold=True)
        f.label(along(O, 90 + 45 * k + 12, r - 2), names_in[k], size=12, bold=True, color=GIVEN)
    return f

# ================================================================ arches
@fig
def trefoil_arch():
    f = Fig("trefoil_arch")
    A, D = P(0, 0), P(200, 0); t = 60
    B, C = along(A, t, 90), along(D, 180 - t, 90)
    for p, q in ((A, B), (B, C), (C, D), (A, D)): f.seg(p, q, color=ARC, w=1.2, dash="5,4")
    assert abs(dist(A, B) - dist(C, D)) < 1e-9 and abs(B[1] - C[1]) < 1e-9
    # three half-circle lobes, one on each support line, bulging away from the middle
    for p, q in ((A, B), (B, C), (C, D)):
        m = mul(add(p, q), 0.5)
        f.carc(m, dist(p, q) / 2, dirto(m, q), dirto(m, q) + 180, color=INK, w=2.6)
    f.seg(A, P(0, -120), w=2.6); f.seg(D, P(200, -120), w=2.6)
    for p, n, dx, dy in ((A, "A", -14, -6), (B, "B", -14, 4), (C, "C", 14, 4), (D, "D", 14, -6)):
        pt(f, p, n, dx, dy, color=GIVEN)
    return f

@fig
def pointed_arch():
    f = Fig("pointed_arch"); L = 160
    A, B = P(0, 0), P(L, 0)
    f.seg(A, B, color=ARC, w=1.2, dash="5,4")
    T = inter(A, L, B, L)[0]
    f.carc(A, L, 0, 60, color=INK, w=2.6); f.carc(B, L, 120, 180, color=INK, w=2.6)
    f.seg(A, P(0, -130), w=2.6); f.seg(B, P(L, -130), w=2.6)
    assert abs(ang(A, B, T) - 60) < 1e-9
    pt(f, A, "A", -12, -12, color=GIVEN); pt(f, B, "B", 12, -12, color=GIVEN); pt(f, T, "", 0, 0)
    f.label(P(L / 2, -150), "arcs: centre A through B, and centre B through A", size=12, color=HELP)
    return f

# ================================================================ hexagons and 60°
@fig
def hexagon_triangles():
    f = Fig("hexagon_triangles"); r = 100
    O = P(0, 0)
    V = poly_reg(O, r, 6, 90)
    names = ["A", "F", "E", "D", "C", "B"]
    for i, p in enumerate(V):
        q = V[(i + 1) % 6]
        f.poly([O, p, q], fill="#e3f2fd" if i % 2 else "#ffffff", color=INK)
        assert abs(dist(O, p) - dist(p, q)) < 1e-9
        f.label(along(O, dirto(O, p), r + 14), names[i], size=14, bold=True)
    f.angle(O, 90, 150, "60°", expect=60, r=24, lr=40)
    f.angle(V[1], dirto(V[1], V[2]), dirto(V[1], V[0]), "120°", expect=120, r=22, lr=40, color=ANS)
    pt(f, O, "O", 10, -14)
    return f

@fig
def angles_round_point():
    f = Fig("angles_round_point"); O = P(0, 0); R = 110
    parts = [("40°", 40), ("60°", 60), ("50°", 50), ("30°", 30), ("40°", 40), ("90°", 90)]
    a = 225
    for lab, d in parts:
        f.seg(O, along(O, a, R))
        f.angle(O, a, a + d, lab, expect=d, r=28 + (d < 45) * 10, lr=48 + (d < 45) * 14)
        a += d
    f.seg(O, along(O, a, R))
    gap = 360 - sum(d for _, d in parts)
    assert gap == 50
    f.angle(O, a, a + gap, "gap = ?", expect=gap, r=60, lr=86, color=ASK)
    return f

@fig
def sixty():
    f = Fig("sixty"); r = 100
    A = P(0, 0); B = along(A, 0, r)
    f.seg(A, P(200, 0))
    f.carc(A, r, -5, 75, color=ARC)
    C = inter(A, r, B, r)[0]
    tick_arc(f, B, C, 14)
    f.seg(A, along(A, dirto(A, C), 170), color=ANS)
    f.seg(B, C, color=GIVEN, w=1.4, dash="4,3")
    assert abs(dirto(A, C) - 60) < 1e-9
    f.angle(A, 0, 60, "60°", expect=60, r=30, lr=48, color=ANS)
    pt(f, A, "A", -10, -14); pt(f, B, "B", 0, -16); pt(f, C, "C", -14, 6)
    f.label(P(205, 0), "X", anchor="start", size=14, bold=True)
    return f

@fig
def hexagon_construction():
    f = Fig("hexagon_construction"); r = 100
    O = P(0, 0)
    f.circle(O, r, color=ARC)
    V = [along(O, 90 - 60 * k, r) for k in range(6)]
    for k in range(6):
        tick_arc(f, V[k], V[(k + 1) % 6], 14, color=GIVEN)
        assert abs(dist(V[k], V[(k + 1) % 6]) - r) < 1e-9
    closed(f, V, color=ANS, w=2.6)
    pt(f, O, "O", 10, -12)
    for k, p in enumerate(V): pt(f, p, "", 0, 0)
    f.seg(O, V[0], color=HELP, w=1.2, dash="4,3"); f.label(P(10, 50), "r", anchor="start", size=13, color=HELP)
    return f

@fig
def thirty_fifteen():
    f = Fig("thirty_fifteen"); r = 110
    A = P(0, 0); f.seg(A, P(220, 0))
    C = along(A, 60, r)
    f.seg(A, along(A, 60, 200), color=GIVEN)
    _, _, c30 = bisect(f, A, 0, 60, r=r, r2=80)
    f.seg(A, along(A, dirto(A, c30), 210), color=ANS)
    _, _, c15 = bisect(f, A, 0, 30, r=r * 0.7, r2=60)
    f.seg(A, along(A, dirto(A, c15), 210), color=ANS, dash="6,4")
    assert abs(dirto(A, c30) - 30) < 1e-9 and abs(dirto(A, c15) - 15) < 1e-9
    f.label(along(A, 60, 212), "60°", size=13, color=GIVEN, bold=True)
    f.label(along(A, 30, 222), "30°", size=13, color=ANS, bold=True)
    f.label(along(A, 15, 228), "15°", size=13, color=ANS, bold=True)
    pt(f, A, "A", -10, -14)
    return f

@fig
def star6():
    f = Fig("star6"); r = 120
    O = P(0, 0)
    T1 = poly_reg(O, r, 3, 90); T2 = poly_reg(O, r, 3, 270)
    closed(f, T1, w=2.4); closed(f, T2, w=2.4)
    outer = poly_reg(O, r, 6, 90)
    names = ["A", "F", "E", "D", "C", "B"]
    for p, n in zip(outer, names): f.label(along(O, dirto(O, p), r + 14), n, size=14, bold=True)
    inner = poly_reg(O, r / math.sqrt(3), 6, 120)
    inames = ["G", "L", "K", "J", "I", "H"]
    for p, n in zip(inner, inames):
        f.label(along(O, dirto(O, p), r / math.sqrt(3) - 14), n, size=12, bold=True, color=GIVEN)
    # each point triangle is equilateral: check A, G, H
    A, G, H = outer[0], inner[0], inner[5]
    assert abs(dist(A, G) - dist(G, H)) < 1e-6 and abs(dist(A, H) - dist(G, H)) < 1e-6
    closed(f, inner, color=GIVEN, w=1.4, dash="5,4")
    return f

@fig
def star_in_hexagon():
    f = Fig("star_in_hexagon"); r = 110
    O = P(0, 0)
    V = poly_reg(O, r, 6, 90)
    closed(f, V, w=2.4)
    closed(f, [V[0], V[2], V[4]], w=2.2); closed(f, [V[1], V[3], V[5]], w=2.2)
    f.angle(V[0], dirto(V[0], V[2]), dirto(V[0], V[4]), "60°", expect=60, r=24, lr=40, color=ANS)
    f.angle(V[1], dirto(V[1], V[2]), dirto(V[1], V[0]), "120°", expect=120, r=20, lr=36, color=GIVEN)
    return f

@fig
def inflexed_arc():
    f = Fig("inflexed_arc"); w = 160; r = w / 2
    L, R = P(0, 0), P(w, 0)
    f.seg(L, P(0, -170), w=2.6); f.seg(R, P(w, -170), w=2.6)
    c1, c2 = P(0, r), P(w, r)
    f.carc(c1, r, 270, 360, color=INK, w=2.6)
    f.carc(c2, r, 180, 270, color=INK, w=2.6)
    f.seg(L, R, color=ARC, w=1.2, dash="5,4")
    f.seg(c1, c2, color=ARC, w=1.2, dash="5,4")
    pt(f, c1, "P", -12, 6, color=GIVEN); pt(f, c2, "Q", 12, 6, color=GIVEN)
    pt(f, P(r, r), "T", 0, 14, color=ANS)
    assert abs(dist(c1, P(r, r)) - r) < 1e-9
    return f

@fig
def flower():
    f = Fig("flower"); r = 60; s = 0.56 * r
    O = P(0, 0)
    f.circle(O, r, color=INK, w=2.4)
    pts = [along(O, 90 + 60 * k, r) for k in range(6)]
    for k in range(6):
        assert abs(dist(pts[k], pts[(k + 1) % 6]) - r) < 1e-9
        p = pts[k]; d = dirto(O, p)
        q1, q2 = inter(p, s, O, r)
        a1, a2 = dirto(p, q1), dirto(p, q2)
        lo, hi = sorted((a1, a2))
        start, end = (lo, hi) if lo < d % 360 < hi or lo < d % 360 + 360 < hi else (hi, lo + 360)
        f.carc(p, s, start, end, color=INK, w=2.4)
        f.dot(p, color=GIVEN)
    assert 2 * s > r            # neighbouring petals overlap a little
    return f

@fig
def hexagon_in_circle():
    f = Fig("hexagon_in_circle"); r = 90
    f.circle(P(0, 0), r, color=INK, w=2.4)
    closed(f, poly_reg(P(0, 0), r, 6, 0), w=2.4)
    return f

@fig
def six_circles():
    f = Fig("six_circles"); r = 34
    for k in range(6):
        c = along(P(0, 0), 60 * k, 2 * r)
        f.circle(c, r, color=INK, w=2.4)
        n = along(P(0, 0), 60 * (k + 1), 2 * r)
        assert abs(dist(c, n) - 2 * r) < 1e-9    # neighbours just touch
    f.circle(P(0, 0), r, color=ARC, w=1.2, dash="4,3")
    return f

@fig
def hexagon_lattice():
    f = Fig("hexagon_lattice"); r = 120
    O = P(0, 0)
    V = poly_reg(O, r, 6, 0)
    closed(f, V, w=2.4)
    for k in range(3): f.seg(V[k], V[k + 3], w=1.6)
    M = [mul(add(V[k], V[(k + 1) % 6]), 0.5) for k in range(6)]
    for k in range(6):
        f.seg(M[k], M[(k + 2) % 6], w=1.4)
        f.seg(V[k], M[(k + 2) % 6], w=1.0, color=GIVEN); f.seg(V[k], M[(k + 3) % 6], w=1.0, color=GIVEN)
    return f

@fig
def illusion():
    f = Fig("illusion"); r = 26
    T = poly_reg(P(0, 0), 110, 3, 90)          # corners of the "white triangle we seem to see"
    T2 = poly_reg(P(0, 0), 80, 3, 270)         # corners of the outline triangle
    for c in T:
        a = dirto(c, P(0, 0))
        pts = [c] + [along(c, a + 30 + 300 * i / 24, r) for i in range(25)]
        f.poly(pts, fill="#212121", color="#212121")
    for i, c in enumerate(T2):
        for j in (1, 2):
            q = T2[(i + j) % 3]
            f.seg(c, along(c, dirto(c, q), 40), w=2.6)
    return f

@fig
def perp_from_P():
    f = Fig("perp_from_P")
    P0 = P(0, 120)
    f.seg(P(-160, 0), P(160, 0)); f.label(P(170, 0), "l", anchor="start", size=14, bold=True)
    r = 150
    X, Y = (-math.sqrt(r * r - 120 * 120), 0), (math.sqrt(r * r - 120 * 120), 0)
    f.carc(P0, r, 270 - 45, 270 + 45, color=ARC)
    Q = inter(X, 130, Y, 130)[1]
    tick_arc(f, X, Q); tick_arc(f, Y, Q)
    f.seg(P0, Q, color=ANS)
    assert abs(Q[0]) < 1e-9
    f.right(P(0, 0), 0)
    pt(f, P0, "P", 12, 6); pt(f, X, "X", 0, -16); pt(f, Y, "Y", 0, -16); pt(f, Q, "Q", 12, -4)
    return f

# ================================================================ tilings
def grid(f, cells, u=26, fill="#ffffff", colour=False, x0=0, y0=0):
    for r, c in cells:
        black = colour and (r + c) % 2 == 1
        rect(f, x0 + c * u, y0 - r * u - u, u, u, "#37474f" if black else fill)

def draw_tiles(f, tiles, u=26, x0=0, y0=0, fills=("#ffcc80", "#90caf9", "#a5d6a7", "#f48fb1", "#ce93d8", "#fff59d")):
    for i, t in enumerate(tiles):
        for r, c in t:
            rect(f, x0 + c * u, y0 - r * u - u, u, u, fills[i % len(fills)], color=fills[i % len(fills)])
        # inner borders: draw outline of the tile only
        cells = set(t)
        for r, c in t:
            x, y = x0 + c * u, y0 - r * u - u
            if (r - 1, c) not in cells: f.seg(P(x, y + u), P(x + u, y + u), w=2.2)
            if (r + 1, c) not in cells: f.seg(P(x, y), P(x + u, y), w=2.2)
            if (r, c - 1) not in cells: f.seg(P(x, y), P(x, y + u), w=2.2)
            if (r, c + 1) not in cells: f.seg(P(x + u, y), P(x + u, y + u), w=2.2)

DOM = [[(0, 0), (0, 1)], [(0, 0), (1, 0)]]
LTRI = [[(0, 0), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0)], [(0, 0), (0, 1), (1, 1)], [(0, 1), (1, 0), (1, 1)]]

def tile(cells, shapes):
    cells = frozenset(cells)
    def rec(rem):
        if not rem: return []
        c = min(rem)
        for sh in shapes:
            for an in sh:
                pl = frozenset((a + c[0] - an[0], b + c[1] - an[1]) for a, b in sh)
                if pl <= rem:
                    r = rec(rem - pl)
                    if r is not None: return [sorted(pl)] + r
        return None
    return rec(cells)

def grid_cells(m, n): return [(r, c) for r in range(m) for c in range(n)]

@fig
def tiling_4x6():
    f = Fig("tiling_4x6")
    t = tile(grid_cells(4, 6), DOM); assert t and len(t) == 12
    draw_tiles(f, t)
    return f

@fig
def tiling_4x7():
    f = Fig("tiling_4x7")
    cells = grid_cells(4, 7)
    tiles = [[(r, c), (r + 1, c)] for c in range(7) for r in (0, 2)]
    assert sorted(x for t in tiles for x in t) == sorted(cells)
    draw_tiles(f, tiles)
    return f

@fig
def tiling_3x5_even_odd():
    f = Fig("tiling_3x5_even_odd")
    # 4 rows (even) x 5 columns (odd): vertical tiles down every column
    tiles = [[(r, c), (r + 1, c)] for c in range(5) for r in (0, 2)]
    draw_tiles(f, tiles)
    return f

def removed(name, rm, ans=True):
    f = Fig(name)
    cells = [x for x in grid_cells(5, 3) if x != rm]
    t = tile(cells, DOM)
    assert (t is not None) == ans, (name, rm)
    if t: draw_tiles(f, t)
    else: grid(f, cells)
    return f

@fig
def removed_corner(): return removed("removed_corner", (0, 2))
@fig
def removed_centre(): return removed("removed_centre", (1, 1))
@fig
def removed_edge(): return removed("removed_edge", (0, 1), ans=False)

@fig
def removed_edge_coloured():
    f = Fig("removed_edge_coloured")
    cells = [x for x in grid_cells(5, 3) if x != (0, 1)]
    grid(f, cells, colour=True)
    black = sum((r + c) % 2 for r, c in cells); white = len(cells) - black
    assert (white, black) == (8, 6)
    f.label(P(40, -5 * 26 - 18), "8 white, 6 black", size=13, bold=True, color=ASK)
    return f

@fig
def which_squares():
    f = Fig("which_squares"); u = 30
    for r, c in grid_cells(5, 3):
        ok = tile([x for x in grid_cells(5, 3) if x != (r, c)], DOM) is not None
        assert ok == ((r + c) % 2 == 0)
        rect(f, c * u, -r * u - u, u, u, "#c8e6c9" if ok else "#ffcdd2")
        f.label(P(c * u + u / 2, -r * u - u / 2), "✓" if ok else "✗", size=14, bold=True, color=ANS if ok else ASK)
    return f

@fig
def l_region():
    f = Fig("l_region")
    cells = [(0, 0), (0, 1), (1, 0), (1, 1)] + [(r, c) for r in (2, 3) for c in range(4)]
    t = tile(cells, LTRI); assert t and len(t) == 4
    draw_tiles(f, t)
    f.label(P(-10, -52), "4 L-tiles", anchor="end", size=13, bold=True, color=ANS)
    return f

@fig
def board_corners():
    f = Fig("board_corners"); u = 22
    cells = [x for x in grid_cells(8, 8) if x not in ((0, 7), (7, 0))]
    grid(f, cells, u=u, colour=True)
    black = sum((r + c) % 2 for r, c in cells)
    assert (len(cells) - black, black) == (32, 30)
    f.label(P(4 * u, -8 * u - 18), "62 squares: 32 white, 30 black", size=13, bold=True, color=ASK)
    return f

@fig
def plane_tilings():
    f = Fig("plane_tilings"); s = 30
    # triangles
    for r in range(4):
        for c in range(7):
            x = c * s / 2; y = r * s * math.sqrt(3) / 2
            up = (r + c) % 2 == 0
            pts = [P(x, y), P(x + s, y), P(x + s / 2, y + s * math.sqrt(3) / 2)] if up else \
                  [P(x, y + s * math.sqrt(3) / 2), P(x + s, y + s * math.sqrt(3) / 2), P(x + s / 2, y)]
            f.poly(pts, fill="#fff9c4" if up else "#ffe0b2")
    # squares
    for r in range(4):
        for c in range(4):
            rect(f, 160 + c * s, r * s, s, s, "#c8e6c9" if (r + c) % 2 else "#e8f5e9")
    # hexagons
    h = s * 0.62
    for r in range(3):
        for c in range(3):
            cx = 320 + c * 1.5 * h; cy = r * h * math.sqrt(3) + (c % 2) * h * math.sqrt(3) / 2 + h
            f.poly(poly_reg(P(cx, cy), h, 6, 0), fill="#bbdefb" if (r + c) % 2 else "#e3f2fd")
    f.label(P(60, -16), "triangles: 6 × 60°", size=12, bold=True)
    f.label(P(220, -16), "squares: 4 × 90°", size=12, bold=True)
    f.label(P(360, -16), "hexagons: 3 × 120°", size=12, bold=True)
    assert 6 * 60 == 4 * 90 == 3 * 120 == 360
    return f

@fig
def pentagons_gap():
    f = Fig("pentagons_gap"); s = 70
    O = P(0, 0); R = s / (2 * math.sin(math.radians(36)))
    a = 90
    for k in range(3):
        alpha = a + 108 * k                      # edges from O at alpha and alpha + 108
        c = along(O, alpha + 54, R)
        base = dirto(c, O)
        pts = [along(c, base + 72 * i, R) for i in range(5)]
        assert dist(pts[0], O) < 1e-6 and abs(dist(pts[0], pts[1]) - s) < 1e-6
        f.poly(pts, fill="#e1bee7")
    assert 360 - 3 * 108 == 36
    f.angle(O, a + 324, a + 360, "36° gap", expect=36, r=40, lr=70, color=ASK)
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
