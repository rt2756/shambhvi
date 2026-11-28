"""Figures for class 8 maths Ch 4, Quadrilaterals.
Every shape is built from its given measurements (1 cm = CM units). Every labelled angle is
asserted against the drawn geometry (geo.Fig.angle), ticked sides are asserted equal, right-angle
squares are asserted to be 90°, and parallel arrows are asserted parallel."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "4")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

CM = 26
FILL1, FILL2, PAPER, WOOD = "#c8e6c9", "#ffe0b2", "#fce4ec", "#8d6e63"

# ---------------------------------------------------------------- helpers
def C(x, y, k=CM, o=(0, 0)): return P(x * k + o[0], y * k + o[1])
def sh(pts, dx, dy): return [add(p, (dx, dy)) for p in pts]
def mid(p, q): return mul(add(p, q), 0.5)
def centroid(pts): return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))

def area2(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))

def shape(f, pts, names="", fill=None, color=INK, dots=True, off=15, w=2.2):
    if fill: f.poly(list(pts), fill=fill, color=color)
    else:
        for i in range(len(pts)): f.seg(pts[i], pts[(i + 1) % len(pts)], color=color, w=w)
    g = centroid(pts)
    for i, p in enumerate(pts):
        if dots: f.dot(p, color=color)
        if names and names[i] != " ": f.label(along(p, dirto(g, p), off), names[i])

def ang(f, V, P1, P2, label, expect=None, r=20, color=GIVEN, lr=None, size=None):
    """Mark the smaller angle P1-V-P2."""
    a1, a2 = dirto(V, P1), dirto(V, P2)
    if (a2 - a1) % 360 > 180: a1, a2 = a2, a1
    f.angle(V, a1, a2, label, expect, r=r, color=color, lr=lr)

def rang(f, V, P1, P2, label, expect=None, r=20, color=GIVEN, lr=None):
    """Mark the angle swept counter-clockwise from ray V->P1 to ray V->P2 (may be reflex)."""
    f.angle(V, dirto(V, P1), dirto(V, P2), label, expect, r=r, color=color, lr=lr)

def angle_of(V, P1, P2):
    a = (dirto(V, P2) - dirto(V, P1)) % 360
    return min(a, 360 - a)

def rmark(f, V, P1, P2, s=10, color=INK):
    a1, a2 = dirto(V, P1), dirto(V, P2)
    if (a2 - a1) % 360 > 180: a1, a2 = a2, a1
    assert abs((a2 - a1) % 360 - 90) < 1e-6, f"{f.name}: right-angle mark on {(a2 - a1) % 360:.2f}°"
    f.right(V, a1, s, color=color)

def eq_ticks(f, pairs, n=1, color=INK):
    L = [dist(p, q) for p, q in pairs]
    assert max(L) - min(L) < 1e-6, f"{f.name}: ticked sides differ {L}"
    for p, q in pairs: f.ticks(p, q, n, color=color)

def arcs(f, V, P1, P2, n=1, r=16, color=INK):
    for k in range(n): ang(f, V, P1, P2, "", r=r + 5 * k, color=color)

def eq_arcs(f, triples, n=1, r=16, color=INK):
    A = [angle_of(*t) for t in triples]
    assert max(A) - min(A) < 1e-6, f"{f.name}: arcs marked equal differ {A}"
    for t in triples: arcs(f, *t, n=n, r=r, color=color)

def par(f, pairs, n=1, color=INK):
    """Parallel arrows on each segment, after checking they really are parallel."""
    d0 = dirto(*pairs[0]) % 180
    for p, q in pairs:
        d = dirto(p, q) % 180
        assert min(abs(d - d0), 180 - abs(d - d0)) < 1e-6, f"{f.name}: arrows on non-parallel sides"
        f.arrows(along(mid(p, q), dirto(p, q), -4 * n), dirto(p, q), n, color=color)

def side(f, p, q, s, g, color=GIVEN, off=11, size=13):
    m = mid(p, q); n = dirto(p, q) + 90
    if dist(along(m, n, 1), g) < dist(along(m, n + 180, 1), g): n += 180
    w = len(s) * size * 0.56
    f.label(along(m, n, off + w / 2 * abs(math.cos(d2r(n)))), s, color=color, size=size)

def caption(f, x, y, s, size=13, color=INK, bold=False):
    f.label(P(x, y), s, size=size, color=color, bold=bold)

def ellipse(f, c, rx, ry, color=INK, fill="none", n=90):
    f.poly([add(c, (rx * math.cos(2 * math.pi * i / n), ry * math.sin(2 * math.pi * i / n))) for i in range(n)], fill=fill, color=color)

def bez_arc(p, q, bulge, n=24):
    """Points on a circular arc from p to q; bulge = height of the arc's middle above the chord
    (positive = to the left of p->q)."""
    m, L = mid(p, q), dist(p, q) / 2
    R = (L * L + bulge * bulge) / (2 * abs(bulge))
    nrm = dirto(p, q) + (90 if bulge > 0 else -90)
    c = along(m, nrm, abs(bulge) - R)
    a1, a2 = dirto(c, p), dirto(c, q)
    sweep = (a2 - a1) % 360
    if sweep > 180: sweep -= 360
    return [along(c, a1 + sweep * k / n, R) for k in range(n + 1)]

def polyline(f, pts, color=INK, w=2.2, dash=None):
    for i in range(len(pts) - 1): f.seg(pts[i], pts[i + 1], color=color, w=w, dash=dash)

def rect(w, h, rot=0, o=(0, 0), k=CM):
    """Rectangle corners (bottom-left, bottom-right, top-right, top-left), turned by rot degrees."""
    a = P(0, 0); b = along(a, rot, w * k); d = along(a, rot + 90, h * k); c = add(b, sub(d, a))
    return sh([a, b, c, d], *o)

def sub(p, q): return (p[0] - q[0], p[1] - q[1])

def from_diagonals(d1, d2, theta, o=(0, 0), k=CM, rot=0):
    """Quadrilateral whose diagonals d1, d2 (cm) bisect each other at angle theta.
    Returns (A, B, C, D, O) with diagonal AC along rot and BD at rot + theta."""
    O = P(*o)
    A, Cc = along(O, rot + 180, d1 / 2 * k), along(O, rot, d1 / 2 * k)
    B, D = along(O, rot + theta, d2 / 2 * k), along(O, rot + theta + 180, d2 / 2 * k)
    return A, B, Cc, D, O

def tri_sss(a, b, c, k=CM):
    """Triangle with base PQ = a along the x-axis, QR = b, RP = c; R above the base."""
    Pp, Q = P(0, 0), P(a * k, 0)
    x = (a * a + c * c - b * b) / (2 * a)
    return Pp, Q, P(x * k, math.sqrt(c * c - x * x) * k)

def reflect(p, a, b):
    d = unit(dirto(a, b)); v = sub(p, a); t = v[0] * d[0] + v[1] * d[1]
    foot = add(a, mul(d, t))
    return add(foot, sub(foot, p))

def halfturn(p, a, b):
    m = mid(a, b); return add(m, sub(m, p))

def is_convex(pts):
    s = [((pts[(i + 1) % 4][0] - pts[i][0]) * (pts[(i + 2) % 4][1] - pts[(i + 1) % 4][1])
          - (pts[(i + 1) % 4][1] - pts[i][1]) * (pts[(i + 2) % 4][0] - pts[(i + 1) % 4][0])) for i in range(4)]
    return all(x > 0 for x in s) or all(x < 0 for x in s)

def interior_sum(pts):
    """Sum of the interior angles of a simple polygon given counter-clockwise."""
    assert area2(pts) > 0
    tot = 0
    for i in range(len(pts)):
        V, N, Pv = pts[i], pts[(i + 1) % len(pts)], pts[(i - 1) % len(pts)]
        tot += (dirto(V, Pv) - dirto(V, N)) % 360
    return tot

def qang(f, pts, i, label, expect=None, r=20, color=GIVEN, lr=None):
    """Interior angle at vertex i of a counter-clockwise polygon."""
    assert area2(pts) > 0, f"{f.name}: polygon not counter-clockwise"
    V, N, Pv = pts[i], pts[(i + 1) % len(pts)], pts[(i - 1) % len(pts)]
    f.angle(V, dirto(V, N), dirto(V, Pv), label, expect, r=r, color=color, lr=lr)

def dots_grid(f, n, m, k, o=(0, 0)):
    for i in range(n + 1):
        for j in range(m + 1): f.dot(C(i, j, k, o), color=HELP)

# ---------------------------------------------------------------- what is a quadrilateral
@fig
def intro_shapes():
    f = Fig("intro_shapes")
    shapes = [
        [P(0, 20), P(95, 0), P(125, 70), P(30, 105)],
        [P(160, 35), P(255, 0), P(290, 60), P(200, 100)],
        [P(330, 0), P(395, 55), P(420, 110), P(440, 25)][::-1],
    ]
    shapes[2] = [P(330, 0), P(440, 25), P(392, 48), P(420, 110)]
    for k, pts in enumerate(shapes):
        if area2(pts) < 0: pts = pts[::-1]
        assert abs(interior_sum(pts) - 360) < 1e-6
        shape(f, pts, dots=False)
        for i in range(4): qang(f, pts, i, "", r=12, color=INK)
        caption(f, centroid(pts)[0], -28, ["(i)", "(ii)", "(iii)"][k])
    # (iv) three straight sides and one curved side
    a, b, c, d = P(500, 0), P(580, 0), P(585, 75), P(490, 105)
    polyline(f, [d, a, b, c]); polyline(f, bez_arc(c, d, 16))
    caption(f, 540, -28, "(iv)")
    # (v) two straight sides and two curved sides
    a, b, c, m = P(625, 90), P(690, 0), P(760, 95), P(695, 75)
    polyline(f, [a, b, c]); polyline(f, bez_arc(c, m, -10)); polyline(f, bez_arc(m, a, -10))
    caption(f, 692, -28, "(v)")
    return f

# ---------------------------------------------------------------- 4.1 rectangles
W8, H8 = 6.4, 4.8          # a rectangle whose diagonal is 8 cm (6.4² + 4.8² = 64)

@fig
def carpenter():
    f = Fig("carpenter")
    A, D, Cc, B = rect(W8, H8, k=32)
    assert abs(dist(A, Cc) - 8 * 32) < 1e-6
    O = mid(A, Cc)
    for p, q in ((A, D), (D, Cc), (Cc, B), (B, A)): f.seg(p, q, color=ASK, w=1.6, dash="6 5")
    f.seg(A, Cc, color=WOOD, w=8); f.seg(B, D, color=WOOD, w=8)
    for p, n, o in ((A, "A", (-12, -10)), (B, "B", (-12, 10)), (Cc, "C", (12, 10)), (D, "D", (12, -10)), (O, "O", (0, -18))):
        f.dot(p); f.label(add(p, o), n)
    f.label(add(mid(A, D), (0, -18)), "strip AC = 8 cm", color=GIVEN, size=13)
    f.label(add(mid(B, Cc), (0, 18)), "strip BD = ?", color=ASK, size=13)
    caption(f, W8 * 16, -44, "dashed red = the thread through the four ends", size=12, color=ASK)
    return f

def rect_named(k=CM, o=(0, 0), w=W8, h=H8):
    A, D, Cc, B = rect(w, h, k=k, o=o)     # book-style naming: A bottom-left, D bottom-right
    return A, B, Cc, D

@fig
def ded1():
    f = Fig("ded1")
    for j, (tri, fill, cap) in enumerate((("ADC", FILL1, "∆ADC"), ("DAB", FILL2, "∆DAB"))):
        A, B, Cc, D = rect_named(k=24, o=(j * 200, 0))
        pts = {"A": A, "B": B, "C": Cc, "D": D}
        f.poly([pts[c] for c in tri], fill=fill)
        shape(f, [A, D, Cc, B], "ADCB")
        rmark(f, A, D, B); rmark(f, D, A, Cc)
        eq_ticks(f, [(A, B), (D, Cc)], 1)
        f.seg(A, D, color=GIVEN, w=3.5)
        caption(f, mid(A, D)[0], -26, cap + "  (AD is shared)", size=13)
    return f

@fig
def ded2():
    f = Fig("ded2")
    A, B, Cc, D = rect_named(k=34)
    O = mid(A, Cc)
    shape(f, [A, D, Cc, B], "ADCB"); f.seg(A, Cc); f.seg(B, D)
    f.dot(O); f.label(add(O, (0, -20)), "O")
    eq_ticks(f, [(A, B), (D, Cc)], 1)
    ang(f, B, A, O, "1", expect=angle_of(B, A, O), r=24, lr=36)
    ang(f, B, O, Cc, "3", expect=angle_of(B, O, Cc), r=28, lr=40)
    ang(f, D, O, Cc, "2", expect=angle_of(B, A, O), r=24, lr=36)
    assert abs(angle_of(B, A, O) + angle_of(B, O, Cc) - 90) < 1e-6
    arcs(f, O, A, B, r=14, color=GIVEN); arcs(f, O, Cc, D, r=14, color=GIVEN)
    return f

def diag_quad(f, x, half=4, k=30, rot=0, labels=True):
    """Equal diagonals of length 2*half bisecting each other at x°, book naming A top-left, B top-right,
    C bottom-right, D bottom-left, with angle AOB = x at the top."""
    O = P(0, 0)
    A, B = along(O, 90 + x / 2, half * k), along(O, 90 - x / 2, half * k)
    Cc, D = along(O, 270 + x / 2, half * k), along(O, 270 - x / 2, half * k)
    shape(f, [D, Cc, B, A], "DCBA"); f.seg(A, Cc); f.seg(B, D)
    f.dot(O)
    return A, B, Cc, D, O

@fig
def ded3_60():
    f = Fig("ded3_60")
    A, B, Cc, D, O = diag_quad(f, 60, k=36)
    eq_ticks(f, [(O, A), (O, B), (O, Cc), (O, D)], 1)
    ang(f, O, A, B, "60°", 60, r=18, lr=34); ang(f, O, Cc, D, "60°", 60, r=18, lr=34)
    ang(f, O, B, Cc, "120°", 120, r=14, lr=40); ang(f, O, D, A, "120°", 120, r=14, lr=40)
    for V, p, q, e in ((A, O, B, 60), (B, O, A, 60), (A, O, D, 30), (B, O, Cc, 30),
                       (Cc, O, D, 60), (D, O, Cc, 60), (Cc, O, B, 30), (D, O, A, 30)):
        ang(f, V, p, q, f"{e}°", e, r=22 if e == 60 else 34, lr=40 if e == 60 else 52, color=ANS)
    return f

@fig
def ded3_x():
    f = Fig("ded3_x")
    x = 70
    A, B, Cc, D, O = diag_quad(f, x, k=40)
    ang(f, O, A, B, "x", x, r=18, lr=32); ang(f, O, Cc, D, "x", x, r=18, lr=32)
    ang(f, O, B, Cc, "180° − x", 180 - x, r=14, lr=54); ang(f, O, D, A, "180° − x", 180 - x, r=14, lr=54)
    for V, p, q in ((A, O, B), (B, O, A), (Cc, O, D), (D, O, Cc)):
        ang(f, V, p, q, "90° − x/2", 90 - x / 2, r=22, lr=62, color=ANS)
    for V, p, q in ((A, O, D), (B, O, Cc), (Cc, O, B), (D, O, A)):
        ang(f, V, p, q, "x/2", x / 2, r=34, lr=58, color=ANS)
    return f

@fig
def strips_angles():
    f = Fig("strips_angles")
    for j, th in enumerate((40, 75, 125)):
        k = 17; o = (j * 190, 0)
        A, B, Cc, D, O = from_diagonals(8, 8, th, o=o, k=k, rot=-th / 2)
        for p, q in ((A, B), (B, Cc), (Cc, D), (D, A)): f.seg(p, q, color=ASK, w=1.6, dash="6 5")
        f.seg(A, Cc, color=WOOD, w=6); f.seg(B, D, color=WOOD, w=6)
        for V, p, q in ((A, B, D), (B, Cc, A), (Cc, D, B), (D, A, Cc)): rmark(f, V, p, q, s=8, color=ASK)
        ang(f, O, Cc, B, f"{th}°", th, r=18, lr=34 if th > 50 else 44)
        caption(f, o[0], -86, f"strips at {th}°", size=13)
    return f

@fig
def ded4():
    f = Fig("ded4")
    A, B, Cc, D = rect_named(k=34, w=6, h=4.5)
    shape(f, [A, D, Cc, B], "ADCB"); f.seg(B, D)
    for V, p, q in ((A, D, B), (D, Cc, A), (Cc, B, D), (B, A, Cc)): rmark(f, V, p, q)
    ang(f, B, A, D, "1", expect=angle_of(B, A, D), r=26, lr=38)
    ang(f, B, D, Cc, "3", expect=angle_of(B, D, Cc), r=30, lr=44)
    ang(f, D, B, Cc, "2", expect=angle_of(B, A, D), r=26, lr=38)
    f.label(along(mid(B, D), dirto(B, D) + 90, 14), "common side BD", color=GIVEN, size=12)
    return f

@fig
def rect_parallel():
    f = Fig("rect_parallel")
    A, B, Cc, D = rect_named(k=30, w=6, h=4)
    shape(f, [A, D, Cc, B], "ADCB")
    f.seg(along(A, 270, 30), along(B, 90, 30), color=ASK, w=2.2)
    f.label(along(B, 90, 42), "transversal AB", color=ASK, size=12)
    par(f, [(A, D), (B, Cc)])
    ang(f, A, D, B, "90°", 90, r=18, lr=32); ang(f, B, A, Cc, "90°", 90, r=18, lr=32)
    return f

@fig
def special_rects():
    f = Fig("special_rects")
    k = 20
    data = [((5, 2), 0, (0, 0), "(i)"), ((6, 3.6), 12, (165, -10), "(ii)"), ((1, 5), 0, (355, -10), "(iii)"), ((4, 4), 30, (465, -15), "(iv)")]
    for (w, h), rot, o, cap in data:
        pts = rect(w, h, rot, o, k)
        shape(f, pts, dots=False)
        g = centroid(pts)
        for i in range(4): rmark(f, pts[i], pts[(i + 1) % 4], pts[i - 1], s=8)
        side(f, pts[0], pts[1], f"{w:g} cm", g); side(f, pts[1], pts[2], f"{h:g} cm", g)
        if cap == "(iv)":
            side(f, pts[2], pts[3], "4 cm", g); side(f, pts[3], pts[0], "4 cm", g)
        caption(f, g[0], -60, cap)
    return f

@fig
def venn_sq_rect():
    f = Fig("venn_sq_rect")
    ellipse(f, P(0, 0), 170, 90, color=GIVEN)
    ellipse(f, P(50, -12), 70, 45, color=ANS, fill="#e8f5e9")
    f.label(P(-85, 30), "Rectangles", color=GIVEN, bold=True)
    f.label(P(50, -16), "Squares", color=ANS, bold=True)
    return f

def square_book(k=36, s=6):
    """Square named as in the deductions: A top-left, B top-right, C bottom-right, D bottom-left."""
    D, Cc, B, A = rect(s, s, k=k)
    return A, B, Cc, D

@fig
def square_ded5():
    f = Fig("square_ded5")
    A, B, Cc, D = square_book()
    O = mid(A, Cc)
    f.poly([B, O, A], fill=FILL1); f.poly([B, O, Cc], fill=FILL2)
    shape(f, [D, Cc, B, A], "DCBA"); f.seg(A, Cc); f.seg(B, D)
    f.dot(O); f.label(add(O, (0, -24)), "O")
    eq_ticks(f, [(B, A), (B, Cc)], 1); eq_ticks(f, [(O, A), (O, Cc)], 2)
    f.seg(B, O, color=GIVEN, w=3.5)
    ang(f, O, B, A, "?", r=14, color=ASK, lr=26); ang(f, O, Cc, B, "?", r=14, color=ASK, lr=26)
    return f

@fig
def square_45():
    f = Fig("square_45")
    A, B, Cc, D = square_book(k=32)
    shape(f, [D, Cc, B, A], "DCBA"); f.seg(A, Cc)
    eq_ticks(f, [(A, D), (D, Cc)], 1)
    rmark(f, D, A, Cc)
    ang(f, A, D, Cc, "1", 45, r=26, lr=38); ang(f, A, Cc, B, "2", 45, r=26, lr=38)
    ang(f, Cc, A, D, "3", 45, r=26, lr=38); ang(f, Cc, B, A, "4", 45, r=26, lr=38)
    return f

def fio1_rects(f, answers):
    k = 40 if answers else 30
    # (i) rectangle ABCD, D top-left, with angle CAB = 30°
    A, B, Cc, D = rect(6 * math.cos(d2r(30)), 3, k=k)
    O = mid(A, Cc)
    shape(f, [A, B, Cc, D], "ABCD"); f.seg(A, Cc); f.seg(B, D); f.dot(O)
    eq_ticks(f, [(O, A), (O, B), (O, Cc), (O, D)], 1)
    ang(f, A, B, Cc, "30°", 30, r=30, lr=44)
    caption(f, mid(A, B)[0], -30, "(i)")
    if answers:
        for p, q, e in ((A, B, 120), (B, Cc, 60), (Cc, D, 120), (D, A, 60)):
            ang(f, O, p, q, f"{e}°", e, r=14, lr=28 if e == 60 else 30, color=ANS)
        for V, p, q, e in ((B, A, D, 30), (A, Cc, D, 60), (D, B, A, 60), (D, Cc, B, 30), (Cc, A, D, 30), (Cc, B, A, 60)):
            ang(f, V, p, q, f"{e}°", e, r=24 if e == 60 else 30, lr=40 if e == 60 else 46, color=ANS)
    # (ii) rectangle PSRQ, Q top-left, with angle QOR = 110°
    dx = 6.5 * k + (40 if answers else 0)
    h = 3.2
    O = P(dx + h * k * math.cos(d2r(35)), h * k * math.sin(d2r(35)))
    Q, R = along(O, 145, h * k), along(O, 35, h * k)
    Pp, S = along(O, 215, h * k), along(O, 325, h * k)
    shape(f, [Pp, S, R, Q], "PSRQ"); f.seg(Q, S); f.seg(R, Pp); f.dot(O)
    eq_ticks(f, [(O, Pp), (O, Q), (O, R), (O, S)], 1)
    ang(f, O, Q, R, "110°", 110, r=14, lr=30)
    caption(f, mid(Pp, S)[0], -30, "(ii)")
    if answers:
        for p, q, e in ((R, S, 70), (S, Pp, 110), (Pp, Q, 70)):
            ang(f, O, p, q, f"{e}°", e, r=14, lr=28 if e == 70 else 30, color=ANS)
        for V, p, q, e in ((Q, O, R, 35), (R, O, Q, 35), (R, O, S, 55), (S, O, R, 55),
                           (S, O, Pp, 35), (Pp, O, S, 35), (Pp, O, Q, 55), (Q, O, Pp, 55)):
            ang(f, V, p, q, f"{e}°", e, r=24 if e == 55 else 32, lr=40 if e == 55 else 50, color=ANS)

@fig
def fio94_1_q():
    f = Fig("fio94_1_q"); fio1_rects(f, False); return f

@fig
def fio94_1_a():
    f = Fig("fio94_1_a"); fio1_rects(f, True); return f

@fig
def fio94_2_a():
    f = Fig("fio94_2_a")
    for j, th in enumerate((30, 40, 90, 140)):
        k, o = 16, (j * 170, 0)
        A, B, Cc, D, O = from_diagonals(8, 8, th, o=o, k=k, rot=-th / 2)
        shape(f, [A, B, Cc, D] if area2([A, B, Cc, D]) > 0 else [A, D, Cc, B], dots=False)
        f.seg(A, Cc, color=HELP, w=1.6); f.seg(B, D, color=HELP, w=1.6)
        ang(f, O, Cc, B, f"{th}°", th, r=14, lr=30 if th > 60 else 40)
        if th == 90:
            for V, p, q in ((A, B, D), (B, Cc, A), (Cc, D, B), (D, A, Cc)): rmark(f, V, p, q, s=7)
        caption(f, o[0], -80, f"({'i ii iii iv'.split()[j]}) {th}°", size=13)
    return f

@fig
def fio94_3():
    f = Fig("fio94_3")
    k, r = 30, 3
    O = P(0, 0)
    A, Pp, M, L = along(O, 90, r * k), along(O, 180, r * k), along(O, 270, r * k), along(O, 0, r * k)
    f.circle(O, r * k)
    f.seg(Pp, L, color=HELP, w=1.6); f.seg(A, M, color=HELP, w=1.6)
    shape(f, [A, Pp, M, L], "APML")
    f.dot(O); f.label(add(O, (-13, -14)), "O")
    rmark(f, O, L, A)
    eq_ticks(f, [(O, A), (O, Pp), (O, M), (O, L)], 1)
    return f

@fig
def fio94_4():
    f = Fig("fio94_4")
    k = 30; O = P(0, 0)
    A, B = along(O, 180, 4 * k), along(O, 0, 4 * k)
    Cc, D = along(O, 65, 4 * k), along(O, 245, 4 * k)
    f.seg(A, B, color=WOOD, w=7); f.seg(Cc, D, color=WOOD, w=7)
    f.seg(A, Cc, color=ASK, w=1.8, dash="6 5"); f.seg(Cc, B, color=ASK, w=1.8, dash="6 5")
    for p, n, o in ((A, "A", (-14, 0)), (B, "B", (14, 0)), (Cc, "C", (0, 14)), (D, "D", (0, -16)), (O, "O", (6, -16))):
        f.dot(p); f.label(add(p, o), n)
    rmark(f, Cc, A, B)
    eq_ticks(f, [(O, A), (O, B), (O, Cc), (O, D)], 1)
    return f

@fig
def fio94_5_a():
    f = Fig("fio94_5_a")
    k = 30
    A, B = P(0, 0), P(5 * k, 0); D = along(A, 60, 3 * k); Cc = add(B, sub(D, A))
    shape(f, [A, B, Cc, D], "ABCD")
    par(f, [(A, B), (D, Cc)], 1); par(f, [(A, D), (B, Cc)], 2)
    ang(f, A, B, D, "60°", 60); ang(f, Cc, D, B, "60°", 60)
    ang(f, B, Cc, A, "120°", 120, r=16, lr=32); ang(f, D, A, Cc, "120°", 120, r=16, lr=32)
    return f

# ---------------------------------------------------------------- 4.2 angle sum
@fig
def angle_sum():
    f = Fig("angle_sum")
    S, E, M, O = C(0, 2.2, 34), C(3, 0, 34), C(6.6, 2.4, 34), C(3.8, 4.6, 34)
    pts = [S, E, M, O]
    f.poly([S, E, M], fill=FILL1); f.poly([S, M, O], fill=FILL2)
    shape(f, pts, "SEMO"); f.seg(S, M, color=GIVEN)
    a = {1: angle_of(S, E, M), 2: angle_of(E, S, M), 3: angle_of(M, S, E),
         4: angle_of(S, M, O), 5: angle_of(O, S, M), 6: angle_of(M, O, S)}
    assert abs(a[1] + a[2] + a[3] - 180) < 1e-6 and abs(a[4] + a[5] + a[6] - 180) < 1e-6
    ang(f, S, E, M, "1", a[1], r=26, lr=38); ang(f, E, S, M, "2", a[2], r=20, lr=32)
    ang(f, M, S, E, "3", a[3], r=30, lr=44); ang(f, S, M, O, "4", a[4], r=30, lr=42)
    ang(f, O, S, M, "5", a[5], r=20, lr=32); ang(f, M, O, S, "6", a[6], r=26, lr=38)
    assert abs(interior_sum(pts) - 360) < 1e-6
    return f

# ---------------------------------------------------------------- 4.3 parallelograms
def para(a, b, angle, k=CM, o=(0, 0)):
    A = P(*o); B = along(A, 0, a * k); D = along(A, angle, b * k); return A, B, add(B, sub(D, A)), D

@fig
def para_construct():
    f = Fig("para_construct")
    k = 30
    A, B, Cc, D = para(4, 5, 30, k)
    f.seg(A, B); f.seg(A, D)
    for p, n in ((A, "A"), (B, "B"), (D, "D")): f.dot(p)
    f.label(add(A, (-12, -8)), "A"); f.label(add(B, (10, -10)), "B"); f.label(add(D, (-6, 14)), "D")
    side(f, A, B, "4 cm", centroid([A, B, D])); side(f, A, D, "5 cm", P(200, -50))
    ang(f, A, B, D, "30°", 30, r=34, lr=50)
    caption(f, 2 * k, -34, "Step 1")
    A2, B2, C2, D2 = para(4, 5, 30, k, o=(250, 0))
    f.line(D2, 0, -30, 5 * k, color=HELP, w=1.6, dash="6 5"); f.line(B2, 30, -30, 6.2 * k, color=HELP, w=1.6, dash="6 5")
    shape(f, [A2, B2, C2, D2], "ABCD")
    par(f, [(A2, B2), (D2, C2)], 1); par(f, [(A2, D2), (B2, C2)], 2)
    ang(f, A2, B2, D2, "30°", 30, r=34, lr=50)
    caption(f, 250 + 2 * k, -34, "Step 2")
    return f

@fig
def para_angles():
    f = Fig("para_angles")
    A, B, Cc, D = para(4, 5, 30, 34)
    pts = [A, B, Cc, D]; g = centroid(pts)
    shape(f, pts, "ABCD")
    for i, e in enumerate((30, 150, 30, 150)): qang(f, pts, i, f"{e}°", e, r=14 if e == 150 else 34, lr=30 if e == 150 else 54)
    for i, s in enumerate(("4 cm", "5 cm", "4 cm", "5 cm")): side(f, pts[i], pts[(i + 1) % 4], s, g)
    return f

@fig
def para_x():
    f = Fig("para_x")
    x = 65
    Pp, E, A, R = para(5, 3.5, x, 34)
    pts = [Pp, E, A, R]
    shape(f, pts, "PEAR")
    par(f, [(Pp, E), (R, A)], 1); par(f, [(Pp, R), (E, A)], 2)
    qang(f, pts, 0, "x", x, r=22, lr=36); qang(f, pts, 2, "x", x, r=22, lr=36)
    qang(f, pts, 1, "180° − x", 180 - x, r=18, lr=50); qang(f, pts, 3, "180° − x", 180 - x, r=18, lr=50)
    return f

@fig
def para_sides():
    f = Fig("para_sides")
    A, B, Cc, D = para(5.5, 3.6, 60, 34)
    f.poly([A, B, D], fill=FILL1); f.poly([Cc, D, B], fill=FILL2)
    shape(f, [A, B, Cc, D], "ABCD"); f.seg(B, D, color=GIVEN, w=3.5)
    par(f, [(A, D), (B, Cc)], 2)
    eq_arcs(f, [(A, B, D), (Cc, D, B)], 1, r=18)
    eq_arcs(f, [(D, A, B), (B, Cc, D)], 2, r=22)
    caption(f, mid(A, B)[0], -30, "BD is a side of both triangles", size=12, color=GIVEN)
    return f

@fig
def para_diags():
    f = Fig("para_diags")
    E, Y, S, A = para(5.5, 3.6, 62, 36)
    O = mid(A, Y)
    assert dist(O, mid(E, S)) < 1e-6
    f.poly([A, O, E], fill=FILL1); f.poly([Y, O, S], fill=FILL2)
    shape(f, [E, Y, S, A], "EYSA"); f.seg(A, Y); f.seg(E, S)
    f.dot(O); f.label(add(O, (0, -20)), "O")
    eq_ticks(f, [(A, E), (S, Y)], 1)
    par(f, [(E, A), (Y, S)], 2)
    eq_arcs(f, [(A, O, E), (Y, O, S)], 1, r=20)
    eq_arcs(f, [(E, O, A), (S, O, Y)], 2, r=18)
    return f

@fig
def venn_para():
    f = Fig("venn_para")
    ellipse(f, P(0, 0), 200, 110, color=INK)
    ellipse(f, P(45, -12), 135, 72, color=GIVEN)
    ellipse(f, P(85, -22), 62, 40, color=ANS, fill="#e8f5e9")
    f.label(P(-110, 58), "Parallelograms", bold=True)
    f.label(P(-20, 30), "Rectangles", color=GIVEN, bold=True)
    f.label(P(85, -26), "Squares", color=ANS, bold=True)
    return f

# ---------------------------------------------------------------- 4.4 rhombus
@fig
def rhombus_construct():
    f = Fig("rhombus_construct")
    k = 34
    A, B, Cc, D = para(4, 4, 50, k)
    assert abs(dist(B, Cc) - 4 * k) < 1e-6 and abs(dist(D, Cc) - 4 * k) < 1e-6
    f.carc(B, 4 * k, dirto(B, Cc) - 14, dirto(B, Cc) + 14)
    f.carc(D, 4 * k, dirto(D, Cc) - 14, dirto(D, Cc) + 14)
    shape(f, [A, B, Cc, D], "ABCD")
    eq_ticks(f, [(A, B), (B, Cc), (Cc, D), (D, A)], 1)
    ang(f, A, B, D, "50°", 50, r=26, lr=40)
    return f

@fig
def rhombus_game():
    f = Fig("rhombus_game")
    G, A, M, E = para(4.5, 4.5, 55, 36)
    f.poly([G, A, E], fill=FILL1); f.poly([M, E, A], fill=FILL2)
    shape(f, [G, A, M, E], "GAME"); f.seg(A, E)
    eq_ticks(f, [(G, A), (A, M), (M, E), (E, G)], 1)
    e = (180 - 55) / 2
    ang(f, E, G, A, "a", e, r=24, lr=36); ang(f, E, A, M, "b", e, r=24, lr=36)
    ang(f, A, E, M, "c", e, r=24, lr=36); ang(f, A, G, E, "d", e, r=24, lr=36)
    return f

@fig
def rhombus_65():
    f = Fig("rhombus_65")
    A, B, Cc, D = para(4, 4, 50, 38)
    shape(f, [A, B, Cc, D], "ABCD"); f.seg(B, D)
    eq_ticks(f, [(A, B), (B, Cc), (Cc, D), (D, A)], 1)
    ang(f, A, B, D, "50°", 50, r=26, lr=40); ang(f, Cc, D, B, "50°", 50, r=26, lr=40)
    for V, p, q in ((D, A, B), (D, B, Cc), (B, D, A), (B, Cc, D)):
        ang(f, V, p, q, "65°", 65, r=20, lr=36, color=ANS)
    return f

@fig
def venn_rhombus():
    f = Fig("venn_rhombus")
    ellipse(f, P(0, 0), 230, 120, color=INK)
    ellipse(f, P(-60, -10), 120, 70, color=GIVEN)
    ellipse(f, P(60, -10), 120, 70, color=ASK)
    f.label(P(-150, 82), "Parallelograms", bold=True)
    f.label(P(-110, -10), "Rectangles", color=GIVEN, bold=True)
    f.label(P(110, -10), "Rhombuses", color=ASK, bold=True)
    f.label(P(0, -10), "Squares", color=ANS, bold=True)
    return f

@fig
def rhombus_perp():
    f = Fig("rhombus_perp")
    G, A, M, E = para(4.5, 4.5, 55, 36)
    O = mid(G, M)
    f.poly([G, E, O], fill=FILL1); f.poly([M, E, O], fill=FILL2)
    shape(f, [G, A, M, E], "GAME"); f.seg(G, M); f.seg(A, E)
    f.dot(O); f.label(add(O, (14, -12)), "O")
    eq_ticks(f, [(G, A), (A, M), (M, E), (E, G)], 1)
    eq_ticks(f, [(G, O), (O, M)], 2)
    f.seg(E, O, color=GIVEN, w=3.5)
    rmark(f, O, M, E, s=11, color=ASK)
    return f

def fio102(f, answers):
    k = 38
    # (i) parallelogram PEAR, angle P = 40
    Pp, E, A, R = para(4.5, 3.2, 40, k)
    pts = [Pp, E, A, R]; shape(f, pts, "PEAR")
    par(f, [(Pp, E), (R, A)], 1); par(f, [(Pp, R), (E, A)], 2)
    qang(f, pts, 0, "40°", 40, r=30, lr=46)
    if answers:
        qang(f, pts, 2, "40°", 40, r=30, lr=46, color=ANS)
        qang(f, pts, 1, "140°", 140, r=16, lr=34, color=ANS); qang(f, pts, 3, "140°", 140, r=16, lr=34, color=ANS)
    caption(f, 3.5 * k, -34, "(i)")
    # (ii) parallelogram PQRS, angle P = 110
    o = (9.4 * k, 0)
    Pp, Q, R, S = para(3.5, 3.2, 110, k, o)
    pts = [Pp, Q, R, S]; shape(f, pts, "PQRS")
    par(f, [(Pp, Q), (S, R)], 1); par(f, [(Pp, S), (Q, R)], 2)
    qang(f, pts, 0, "110°", 110, r=16, lr=34)
    if answers:
        qang(f, pts, 2, "110°", 110, r=16, lr=34, color=ANS)
        qang(f, pts, 1, "70°", 70, r=22, lr=38, color=ANS); qang(f, pts, 3, "70°", 70, r=22, lr=38, color=ANS)
    caption(f, o[0] + 0.6 * k, -34, "(ii)")
    # (iii) rhombus UVWX, diagonal XV, angle XVU = 30
    o = (0, -5.4 * k)
    U, V, W, X = para(3.5, 3.5, 120, k, o)
    pts = [U, V, W, X]; shape(f, pts, "UVWX"); f.seg(X, V)
    eq_ticks(f, [(U, V), (V, W), (W, X), (X, U)], 1)
    ang(f, V, U, X, "30°", 30, r=34, lr=50)
    if answers:
        ang(f, V, X, W, "30°", 30, r=34, lr=50, color=ANS)
        ang(f, X, U, V, "30°", 30, r=34, lr=50, color=ANS); ang(f, X, V, W, "30°", 30, r=34, lr=50, color=ANS)
        qang(f, pts, 0, "120°", 120, r=16, lr=34, color=ANS); qang(f, pts, 2, "120°", 120, r=16, lr=34, color=ANS)
    caption(f, o[0] + 1 * k, o[1] - 34, "(iii)")
    # (iv) rhombus AEIO, diagonal OE, angle OEA = 20
    o = (7.6 * k, -5.4 * k)
    A, E, I, Oo = para(4, 4, 140, k, o)
    pts = [A, E, I, Oo]; shape(f, pts, "AEIO"); f.seg(Oo, E)
    eq_ticks(f, [(A, E), (E, I), (I, Oo), (Oo, A)], 1)
    ang(f, E, A, Oo, "20°", 20, r=46, lr=64)
    if answers:
        ang(f, E, Oo, I, "20°", 20, r=46, lr=64, color=ANS)
        ang(f, Oo, A, E, "20°", 20, r=46, lr=64, color=ANS); ang(f, Oo, E, I, "20°", 20, r=46, lr=64, color=ANS)
        qang(f, pts, 0, "140°", 140, r=16, lr=34, color=ANS); qang(f, pts, 2, "140°", 140, r=16, lr=34, color=ANS)
    caption(f, o[0] - 0.5 * k, o[1] - 34, "(iv)")

@fig
def fio102_1_q():
    f = Fig("fio102_1_q"); fio102(f, False); return f

@fig
def fio102_1_a():
    f = Fig("fio102_1_a"); fio102(f, True); return f

def diag_construction(f, d1, d2, theta, k, names="ADBC"):
    """Diagonal AB = d1 drawn first, its midpoint O, a line at theta through O, OC = OD = d2/2."""
    O = P(0, 0)
    A, B = along(O, 180, d1 / 2 * k), along(O, 0, d1 / 2 * k)
    Cc, D = along(O, theta, d2 / 2 * k), along(O, theta + 180, d2 / 2 * k)
    f.line(O, theta, -(d2 / 2 + 1) * k, (d2 / 2 + 1) * k, color=HELP, w=1.4, dash="5 4")
    f.carc(O, d2 / 2 * k, theta - 12, theta + 12); f.carc(O, d2 / 2 * k, theta + 168, theta + 192)
    f.seg(A, B, color=HELP, w=1.6); f.seg(Cc, D, color=HELP, w=1.6)
    pts = [A, D, B, Cc]
    if area2(pts) < 0: pts = [A, Cc, B, D]
    shape(f, pts, dots=False)
    for p, n in zip((A, D, B, Cc), names):
        f.dot(p); f.label(along(p, dirto(O, p), 15), n)
    f.dot(O); f.label(add(O, (0, -18)), "O")
    return A, B, Cc, D, O

@fig
def fio102_2_a():
    f = Fig("fio102_2_a")
    k = 34
    A, B, Cc, D, O = diag_construction(f, 7, 5, 140, k)
    ang(f, O, B, Cc, "140°", 140, r=18, lr=36)
    caption(f, 0, -3.2 * k, "AB = 7 cm, so OA = OB = 3.5 cm;  CD = 5 cm, so OC = OD = 2.5 cm", size=12, color=GIVEN)
    return f

@fig
def fio102_3_a():
    f = Fig("fio102_3_a")
    k = 40
    A, B, Cc, D, O = diag_construction(f, 5, 4, 90, k)
    f.items = [it for it in f.items if not (it[0] == "text" and it[2] == "O")]
    f.label(add(O, (-13, -14)), "O")
    rmark(f, O, B, Cc)
    side(f, A, O, "2.5 cm", P(0, 300), size=12); side(f, O, B, "2.5 cm", P(0, 300), size=12)
    f.label(along(mid(O, Cc), 180, 26), "2 cm", color=GIVEN, size=12)
    f.label(along(mid(O, D), 180, 26), "2 cm", color=GIVEN, size=12)
    eq_ticks(f, [(A, D), (D, B), (B, Cc), (Cc, A)], 1)
    return f

# ---------------------------------------------------------------- 4.5 playing with quadrilaterals
@fig
def geoboard():
    f = Fig("geoboard")
    k = 22
    for j, (left, right) in enumerate(((2, 6), (0, 8))):
        o = (j * 10 * k, 0)
        dots_grid(f, 8, 8, k, o)
        a, b, c, d = C(left, 4, k, o), C(4, 6, k, o), C(right, 4, k, o), C(4, 2, k, o)
        f.seg(a, c, color=GIVEN, w=2.6); f.seg(b, d, color=GIVEN, w=2.6)
        shape(f, [a, d, c, b], dots=False, color=ASK)
        rmark(f, C(4, 4, k, o), c, b, s=8)
        eq_ticks(f, [(a, b), (b, c), (c, d), (d, a)], 1, color=ASK)
        caption(f, o[0] + 4 * k, -24, ["equal diagonals: a square", "one diagonal stretched: a rhombus"][j], size=13)
    return f

def join(f, tri, how, k, o, lens):
    """Two copies of a triangle joined along side PQ: 'mirror' (flip over PQ) or 'turn' (half-turn
    about the midpoint of PQ). tri = (P, Q, R) with R above PQ. Returns the quadrilateral."""
    Pp, Q, R = [add(p, o) for p in tri]
    R2 = reflect(R, Pp, Q) if how == "mirror" else halfturn(R, Pp, Q)
    f.poly([Pp, Q, R], fill=FILL1); f.poly([Q, Pp, R2], fill=FILL2)
    f.seg(Pp, Q, color=HELP, w=1.6, dash="5 4")
    quad = [Pp, R2, Q, R]
    g = centroid(quad)
    for (a, b) in ((Pp, R2), (R2, Q), (Q, R), (R, Pp)):
        side(f, a, b, f"{dist(a, b) / k:g} cm".replace(".0 cm", " cm"), g, size=12, off=9)
    return quad

def quad_kind(q):
    s = [round(dist(q[i], q[(i + 1) % 4]), 6) for i in range(4)]
    if not is_convex(q): return "dart (a kite with a dent)"
    if s[0] == s[1] == s[2] == s[3]: return "rhombus"
    if s[0] == s[2] and s[1] == s[3]: return "parallelogram"
    if (s[0] == s[1] and s[2] == s[3]) or (s[1] == s[2] and s[3] == s[0]): return "kite"
    return "other"

@fig
def join_equilateral():
    f = Fig("join_equilateral")
    k = 16
    q = join(f, tri_sss(8, 8, 8, k), "mirror", k, (0, 0), None)
    assert quad_kind(q) == "rhombus"
    for p in q: f.dot(p)
    return f

@fig
def join_isosceles():
    f = Fig("join_isosceles")
    k = 14
    cases = [((6, 8, 8), "mirror", "along the 6 cm side: rhombus"),
             ((8, 6, 8), "mirror", "8 cm side, flipped: kite"),
             ((8, 6, 8), "turn", "8 cm side, half-turned: parallelogram")]
    x = 0
    for tri, how, cap in cases:
        q = join(f, tri_sss(*tri, k), how, k, (x, 0), None)
        kind = quad_kind(q)
        assert kind in cap, (kind, cap)
        xs = [p[0] for p in q]
        caption(f, (min(xs) + max(xs)) / 2, min(p[1] for p in q) - 26, cap, size=12)
        x += max(xs) - min(xs) + 110
    return f

@fig
def join_scalene():
    f = Fig("join_scalene")
    k = 13
    cases = [((12, 9, 6), "mirror", "share 12 cm, flip: kite"), ((12, 9, 6), "turn", "share 12 cm, turn: parallelogram"),
             ((9, 12, 6), "mirror", "share 9 cm, flip: dart"), ((9, 12, 6), "turn", "share 9 cm, turn: parallelogram"),
             ((6, 12, 9), "mirror", "share 6 cm, flip: dart"), ((6, 12, 9), "turn", "share 6 cm, turn: parallelogram")]
    for i, (tri, how, cap) in enumerate(cases):
        o = ((i // 2) * 330, -(i % 2) * 300)
        q = join(f, tri_sss(*tri, k), how, k, o, None)
        kind = quad_kind(q)
        assert kind.split()[0] in cap, (kind, cap)
        xs = [p[0] for p in q]; ys = [p[1] for p in q]
        caption(f, (min(xs) + max(xs)) / 2, min(ys) - 24, cap, size=12)
    return f

# ---------------------------------------------------------------- 4.6 kite and trapezium
@fig
def kite():
    f = Fig("kite")
    k = 34
    B, A, D, Cc = C(0, 0, k), C(-2.6, 3.2, k), C(0, 6, k), C(2.6, 3.2, k)
    O = C(0, 3.2, k)
    f.poly([A, O, B], fill=FILL1); f.poly([Cc, O, B], fill=FILL2)
    shape(f, [B, Cc, D, A], "BCDA"); f.seg(A, Cc); f.seg(B, D)
    f.dot(O); f.label(add(O, (12, 12)), "O")
    eq_ticks(f, [(A, B), (B, Cc)], 1); eq_ticks(f, [(Cc, D), (D, A)], 2)
    return f

@fig
def trapezium():
    f = Fig("trapezium")
    k = 34
    S, R = C(0, 0, k), C(6.5, 0, k)
    h = 3
    Pp = along(S, 60, h * k / math.sin(d2r(60))); Q = along(R, 105, h * k / math.sin(d2r(75)))
    pts = [S, R, Q, Pp]; shape(f, pts, "SRQP")
    par(f, [(Pp, Q), (S, R)])
    qang(f, pts, 0, "60°", 60, r=24, lr=40); qang(f, pts, 1, "75°", 75, r=24, lr=40)
    qang(f, pts, 3, "?", 120, r=18, lr=32, color=ASK); qang(f, pts, 2, "?", 105, r=18, lr=32, color=ASK)
    return f

@fig
def iso_trap():
    f = Fig("iso_trap")
    k = 34
    U, V = C(0, 0, k), C(7, 0, k)
    X, W = along(U, 62, 3.6 * k), along(V, 118, 3.6 * k)
    Y, Z = P(X[0], 0), P(W[0], 0)
    f.poly([U, Y, X], fill=FILL1); f.poly([V, W, Z], fill=FILL2)
    shape(f, [U, V, W, X], "UVWX")
    f.seg(X, Y, dash="6 4"); f.seg(W, Z, dash="6 4")
    for p, n in ((Y, "Y"), (Z, "Z")): f.dot(p); f.label(add(p, (0, -16)), n)
    par(f, [(X, W), (U, V)])
    eq_ticks(f, [(U, X), (V, W)], 1)
    rmark(f, Y, X, Z); rmark(f, Z, Y, W)
    ang(f, X, W, Y, "a", 90, r=18, lr=30); ang(f, W, Z, X, "b", 90, r=18, lr=30)
    return f

# ---------------------------------------------------------------- end exercises
@fig
def ex1_a():
    f = Fig("ex1_a")
    k = 30
    A, B, Cc, D = para(4, 4, 60, k)
    f.poly([A, B, D], fill=FILL1); f.poly([B, Cc, D], fill=FILL2)
    shape(f, [A, B, Cc, D], "ABCD"); f.seg(B, D, dash="5 4", color=HELP)
    g = centroid([A, B, Cc, D])
    for p, q in ((A, B), (B, Cc), (Cc, D), (D, A)): side(f, p, q, "4 cm", g)
    for V, p, q in ((A, B, D), (Cc, D, B), (B, D, A), (B, Cc, D), (D, A, B), (D, B, Cc)):
        ang(f, V, p, q, "60°", 60, r=20, lr=34, color=ANS)
    return f

@fig
def ex2_a():
    f = Fig("ex2_a")
    k = 30
    Pp, Q, T = C(-3, 0, k), C(3, 0, k), C(0, 0, k)
    R, S = C(0, -2, k), C(0, 6, k)
    # perpendicular-bisector arcs: radius 5 cm from P and from Q, meeting 4 cm above and below PQ
    r = 5 * k
    for c, s in ((Pp, 1), (Q, -1)):
        base = 0 if s == 1 else 180
        top = math.degrees(math.acos(3 / 5))
        for a in (top, -top):
            aa = base + a * s
            f.carc(c, r, aa - 9, aa + 9)
    f.line(T, 90, -4.6 * k, 7 * k, color=HELP, w=1.4, dash="5 4")
    f.seg(Pp, Q, color=HELP, w=1.6); f.seg(R, S, color=HELP, w=1.6)
    pts = [Pp, R, Q, S]; shape(f, pts, "PRQS")
    f.dot(T); f.label(add(T, (14, 12)), "T")
    rmark(f, T, Q, S)
    eq_ticks(f, [(Pp, R), (R, Q)], 1); eq_ticks(f, [(Q, S), (S, Pp)], 2)
    f.label(add(mid(Pp, T), (0, -14)), "3 cm", color=GIVEN, size=12); f.label(add(mid(T, Q), (0, -14)), "3 cm", color=GIVEN, size=12)
    f.label(add(mid(T, R), (20, 0)), "2 cm", color=GIVEN, size=12); f.label(add(mid(T, S), (20, 0)), "6 cm", color=GIVEN, size=12)
    return f

def ex3(f, answers):
    k = 30
    # (i) trapezium PQRS, PQ || SR, angle S = 135, angle R = 105
    S, R = C(0, 0, k), C(2.4, 0, k)
    h = 3
    Pp = along(S, 135, h * k / math.sin(d2r(135))); Q = along(R, 75, h * k / math.sin(d2r(75)))
    pts = [S, R, Q, Pp]; shape(f, pts, "SRQP")
    par(f, [(Pp, Q), (S, R)])
    qang(f, pts, 0, "135°", 135, r=16, lr=34); qang(f, pts, 1, "105°", 105, r=16, lr=34)
    if answers:
        qang(f, pts, 3, "45°", 45, r=26, lr=42, color=ANS); qang(f, pts, 2, "75°", 75, r=22, lr=38, color=ANS)
    caption(f, mid(S, R)[0], -32, "(i)")
    # (ii) isosceles trapezium ABCD, AB || DC, AD = BC, angle A = 100, turned 15 degrees
    D0, C0 = P(0, 0), P(5.6 * k, 0)
    A0, B0 = along(D0, 80, 3.2 * k), along(C0, 100, 3.2 * k)
    o = P(7.2 * k, 0.4 * k)
    D, Cc, B, A = [add(o, (p[0] * math.cos(d2r(-15)) - p[1] * math.sin(d2r(-15)), p[0] * math.sin(d2r(-15)) + p[1] * math.cos(d2r(-15)))) for p in (D0, C0, B0, A0)]
    pts = [D, Cc, B, A]; shape(f, pts, "DCBA")
    par(f, [(A, B), (D, Cc)])
    eq_ticks(f, [(A, D), (B, Cc)], 1)
    qang(f, pts, 3, "100°", 100, r=18, lr=36)
    if answers:
        qang(f, pts, 2, "100°", 100, r=18, lr=36, color=ANS)
        qang(f, pts, 0, "80°", 80, r=20, lr=36, color=ANS); qang(f, pts, 1, "80°", 80, r=20, lr=36, color=ANS)
    caption(f, mid(D, Cc)[0], -2.0 * k, "(ii)")

@fig
def ex3_q():
    f = Fig("ex3_q"); ex3(f, False); return f

@fig
def ex3_a():
    f = Fig("ex3_a"); ex3(f, True); return f

@fig
def ex4_a():
    f = Fig("ex4_a")
    ellipse(f, P(0, 0), 210, 120, color=INK)                      # parallelograms
    ellipse(f, P(250, 0), 170, 95, color=ASK)                     # kites
    ellipse(f, P(70, -30), 115, 62, color=GIVEN)                  # rectangles
    # the lens where kites and parallelograms overlap is exactly the rhombuses
    f.label(P(-120, 70), "Parallelograms", bold=True)
    f.label(P(330, 60), "Kites", color=ASK, bold=True)
    f.label(P(10, -40), "Rectangles", color=GIVEN, bold=True)
    f.label(P(140, 45), "Rhombuses", color="#6a1b9a", bold=True)
    f.label(P(140, -40), "Squares", color=ANS, bold=True)
    caption(f, 140, -150, "Rhombuses = where Kites and Parallelograms overlap;  Squares = Rhombuses that are also Rectangles", size=12)
    return f

def ex5(f, answers):
    k = 30
    R, I = C(0, 0, k), C(7, 0, k)
    Pp, A = C(0, 5, k), C(7, 5, k)
    O = P(I[0], I[1] + 7 * k * math.tan(d2r(30)))
    assert O[1] < A[1]
    S = along(R, -60, 5 * k); D = add(O, sub(S, R))
    shape(f, [R, I, A, Pp], "RIAP", dots=True)
    f.seg(R, O); f.seg(O, D); f.seg(D, S); f.seg(S, R)
    for p, n, o in ((O, "O", (-12, 16)), (D, "D", (12, -8)), (S, "S", (0, -16))):
        f.dot(p); f.label(add(p, o), n)
    side(f, R, Pp, "5 cm", centroid([R, I, A, Pp])); side(f, R, S, "5 cm", centroid([R, O, D, S]))
    ang(f, R, I, O, "30°", 30, r=34, lr=50)
    if answers:
        rmark(f, I, R, O); rmark(f, O, R, D, color=INK)
        ang(f, O, R, I, "60°", 60, r=30, lr=48, color=ANS)
        ang(f, O, I, D, "30°", 30, r=46, lr=62, color=ANS)
    else:
        ang(f, O, I, D, "?", 30, r=38, lr=52, color=ASK)

@fig
def ex5_q():
    f = Fig("ex5_q"); ex5(f, False); return f

@fig
def ex5_a():
    f = Fig("ex5_a"); ex5(f, True); return f

@fig
def ex6_a():
    f = Fig("ex6_a")
    k = 34
    A, B, O = C(0, 0, k), C(6, 0, k), C(3, 0, k)
    r = 4 * k; t = math.degrees(math.acos(3 / 4))
    for a in (t, -t): f.carc(A, r, a - 9, a + 9); f.carc(B, r, 180 - a - 9, 180 - a + 9)
    f.line(O, 90, -4.2 * k, 4.2 * k, color=HELP, w=1.4, dash="5 4")
    f.carc(O, 3 * k, 80, 100); f.carc(O, 3 * k, 260, 280)
    Cc, D = C(3, 3, k), C(3, -3, k)
    f.seg(A, B, color=HELP, w=1.6)
    pts = [A, D, B, Cc]; shape(f, pts, "ADBC")
    f.dot(O); f.label(add(O, (-13, -14)), "O")
    rmark(f, O, B, Cc)
    for i in range(4): rmark(f, pts[i], pts[(i + 1) % 4], pts[i - 1], s=9)
    eq_ticks(f, [(O, A), (O, B), (O, Cc), (O, D)], 1)
    f.label(add(mid(A, O), (0, -14)), "3 cm", color=GIVEN, size=12); f.label(add(mid(O, B), (0, -14)), "3 cm", color=GIVEN, size=12)
    return f

def ex7(f, answers):
    k = 32; s = 5
    E, Ss, A, Cc = rect(s, s, k=k)
    U, X, W, V = mid(Cc, A), mid(A, Ss), mid(Ss, E), mid(E, Cc)
    shape(f, [E, Ss, A, Cc], "ESAC")
    shape(f, [W, X, U, V], "WXUV", off=14)
    if answers:
        eq_ticks(f, [(Cc, U), (U, A), (A, X), (X, Ss), (Ss, W), (W, E), (E, V), (V, Cc)], 1)
        for V0, p, q in ((U, Cc, V), (U, A, X), (V, Cc, U), (V, E, W)):
            ang(f, V0, p, q, "45°", 45, r=22, lr=36, color=ANS)
        for i, p in enumerate((W, X, U, V)):
            pts = [W, X, U, V]; rmark(f, p, pts[(i + 1) % 4], pts[i - 1], s=10, color=ANS)
    caption(f, s * k / 2, -30, "(a)")
    # (b) a tilted square: each corner of the inner square is t from a corner of the outer one
    o = (s * k + 70, 0); t = 1.6
    E2, S2, A2, C2 = rect(s, s, k=k, o=o)
    p1 = along(E2, 0, t * k); p2 = along(S2, 90, t * k); p3 = along(A2, 180, t * k); p4 = along(C2, 270, t * k)
    shape(f, [E2, S2, A2, C2], dots=False)
    inner = [p1, p2, p3, p4]; shape(f, inner, dots=False, color=GIVEN if answers else INK)
    L = [dist(inner[i], inner[(i + 1) % 4]) for i in range(4)]
    assert max(L) - min(L) < 1e-6
    for i in range(4): assert abs(angle_of(inner[i], inner[(i + 1) % 4], inner[i - 1]) - 90) < 1e-6
    if answers:
        eq_ticks(f, [(E2, p1), (S2, p2), (A2, p3), (C2, p4)], 1)
        eq_ticks(f, [(p1, S2), (p2, A2), (p3, C2), (p4, E2)], 2)
        for i in range(4): rmark(f, inner[i], inner[(i + 1) % 4], inner[i - 1], s=10, color=ANS)
    caption(f, o[0] + s * k / 2, -30, "(b)")

@fig
def ex7_q():
    f = Fig("ex7_q"); ex7(f, False); return f

@fig
def ex7_a():
    f = Fig("ex7_a"); ex7(f, True); return f

@fig
def ex9_a():
    f = Fig("ex9_a")
    k = 34
    B, Cc, D, A = para(5.5, 3.4, 65, k)
    shape(f, [B, Cc, D, A], "BCDA"); f.seg(A, Cc)
    eq_ticks(f, [(A, B), (Cc, D)], 1); eq_ticks(f, [(B, Cc), (A, D)], 2)
    a1, a2, a3, a4 = angle_of(A, B, Cc), angle_of(A, Cc, D), angle_of(Cc, A, B), angle_of(Cc, D, A)
    assert abs(a1 - a4) < 1e-6 and abs(a2 - a3) < 1e-6
    ang(f, A, B, Cc, "1", a1, r=24, lr=36); ang(f, A, Cc, D, "2", a2, r=30, lr=42)
    ang(f, Cc, A, B, "3", a3, r=30, lr=42); ang(f, Cc, D, A, "4", a4, r=24, lr=36)
    return f

@fig
def ex10_a():
    f = Fig("ex10_a")
    k = 34
    A, Cc, B, D = C(0, 0, k), C(6, 0, k), C(3, 6, k), C(3, 1.8, k)
    pts = [A, D, Cc, B]
    assert area2(pts) > 0 and not is_convex(pts)
    f.poly([A, D, B], fill=FILL1); f.poly([D, Cc, B], fill=FILL2)
    shape(f, pts, "ADCB"); f.seg(B, D, color=GIVEN, dash="6 4")
    a = {1: angle_of(B, A, D), 2: angle_of(B, D, Cc), 3: angle_of(A, D, B), 4: angle_of(Cc, B, D),
         5: angle_of(D, A, B), 6: angle_of(D, B, Cc)}
    assert abs(a[1] + a[3] + a[5] - 180) < 1e-6 and abs(a[2] + a[4] + a[6] - 180) < 1e-6
    ang(f, B, A, D, "1", a[1], r=40, lr=52); ang(f, B, D, Cc, "2", a[2], r=40, lr=52)
    ang(f, A, D, B, "3", a[3], r=30, lr=44); ang(f, Cc, B, D, "4", a[4], r=30, lr=44)
    ang(f, D, A, B, "5", a[5], r=18, lr=30); ang(f, D, B, Cc, "6", a[6], r=18, lr=30)
    assert abs(interior_sum(pts) - 360) < 1e-6
    rang(f, D, Cc, A, "", r=12, color=ASK)
    return f

@fig
def ex11_a():
    f = Fig("ex11_a")
    k = 24
    # (i) a rectangle that is not a square: equal diagonals that bisect each other
    A, B, Cc, D = rect(6, 3.5, k=k)
    O = mid(A, Cc)
    shape(f, [A, B, Cc, D], dots=False); f.seg(A, Cc, color=HELP); f.seg(B, D, color=HELP)
    eq_ticks(f, [(O, A), (O, B), (O, Cc), (O, D)], 1)
    caption(f, 3 * k, -28, "(i) not a square", size=12)
    # (iv) a kite: perpendicular diagonals, not a rhombus
    o = (8 * k, 0)
    Bk, Ak, Dk, Ck = C(0, 0, k, o), C(-2, 2.2, k, o), C(0, 5, k, o), C(2, 2.2, k, o)
    Bk, Ak, Dk, Ck = [add(p, (2.2 * k, -0.5 * k)) for p in (Bk, Ak, Dk, Ck)]
    Ok = P(Bk[0], Ak[1])
    shape(f, [Bk, Ck, Dk, Ak], dots=False); f.seg(Ak, Ck, color=HELP); f.seg(Bk, Dk, color=HELP)
    rmark(f, Ok, Ck, Dk, s=8)
    eq_ticks(f, [(Ak, Bk), (Bk, Ck)], 1); eq_ticks(f, [(Ck, Dk), (Dk, Ak)], 2)
    caption(f, Bk[0], -28, "(iv) not a rhombus", size=12)
    # (vii) an isosceles trapezium: one pair of parallel sides only
    o = P(14.5 * k, 0)
    U, V = o, add(o, (6 * k, 0)); X, W = along(U, 65, 3.6 * k), along(V, 115, 3.6 * k)
    shape(f, [U, V, W, X], dots=False)
    par(f, [(X, W), (U, V)]); eq_ticks(f, [(U, X), (V, W)], 1)
    caption(f, o[0] + 3 * k, -28, "(vii) not a parallelogram", size=12)
    return f

@fig
def which_quad():
    f = Fig("which_quad")
    k = 18
    for j, (a, b, n) in enumerate(((3, 2, 1), (4.2, 2.8, 3), (2.6, 2.6, 1))):
        o = (j * 11 * k, 0)
        W, H = 10, 7
        sheet = rect(W, H, k=k, o=o)
        f.poly(sheet, fill=PAPER, color=HELP)
        c = C(W / 2, H / 2, k, o)
        f.line(c, 0, -W / 2 * k, W / 2 * k, color=HELP, w=1.4, dash="5 4")
        f.line(c, 90, -H / 2 * k, H / 2 * k, color=HELP, w=1.4, dash="5 4")
        for i in range(n):
            s = 1 - 0.3 * i
            pts = [add(c, (a * s * k, 0)), add(c, (0, b * s * k)), add(c, (-a * s * k, 0)), add(c, (0, -b * s * k))]
            shape(f, pts, dots=False, color=ASK)
            L = [dist(pts[i2], pts[(i2 + 1) % 4]) for i2 in range(4)]
            assert max(L) - min(L) < 1e-6
        caption(f, c[0], -22, ["one crease: a rhombus", "several parallel creases", "equal cuts: a square"][j], size=12)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
