"""Figures for class 8 maths Ch 10, Proportional Reasoning - 2. Pie charts are cut from the data
(each angle = share × 360° and the angles must total 360°), triangles are drawn from their sides or
angles and checked, the map triangle is drawn to its scale, and the inverse-proportion graph plots
points that all satisfy speed × time = 90, so no label can disagree with its picture."""
import math, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "10")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

COLS = ["#90caf9", "#ffcc80", "#a5d6a7", "#f8bbd0", "#ce93d8", "#fff59d", "#80cbc4", "#bcaaa4"]
NAVY, GOLD = "#3949ab", "#f9a825"

def disc(f, c, r, fill, color=INK):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, 10)], fill=fill, color=color)

def pie(f, c, R, items, start=90, label_r=None, show_angle=True, size=12):
    """items: list of (label, value). Slices go anticlockwise from `start`. Returns the angles."""
    total = sum(v for _, v in items)
    angles = [F(v) / total * 360 for _, v in items]
    assert sum(angles) == 360
    a = start
    for (lab, _), ang, col in zip(items, angles, COLS):
        ang = float(ang)
        pts = [c] + [along(c, a + ang * k / 30, R) for k in range(31)]
        f.poly(pts, fill=col)
        mid = a + ang / 2
        t = f"{lab}" + (f" {fmt(ang)}°" if show_angle else "")
        f.label(along(P(c[0], c[1] - 5), mid, label_r or R * 0.62), t, size=size, bold=False)
        a += ang
    return angles

def fmt(v):
    v = float(v)
    return str(int(v)) if v == int(v) else f"{v:g}"

# ---------------------------------------------------------------- 10.2 a map to scale
@fig
def map_scale():
    f = Fig("map_scale")
    cm = 50                                    # drawn pixels per "map cm"
    bc, mc, bm = 4.8, 9.7, 5.0                 # map distances in cm (1 cm = 60 km)
    C = P(0, 0); M = P(-mc * cm, 0)
    # Bengaluru: |BC| = bc, |BM| = bm
    x = (bm ** 2 - bc ** 2 - mc ** 2) / (-2 * mc)        # distance from C towards M along the axis
    y = math.sqrt(bc ** 2 - x ** 2)
    Bp = P(-x * cm, -y * cm)
    assert abs(dist(Bp, C) / cm - bc) < 1e-9 and abs(dist(Bp, M) / cm - bm) < 1e-9
    for p, name, off in [(C, "Chennai", (0, 10)), (M, "Mangaluru", (0, 10)), (Bp, "Bengaluru", (0, -26))]:
        disc(f, p, 6, "#e53935")
        f.label(add(p, off), name, size=13, bold=True)
    for p, q, d in [(Bp, C, bc), (M, C, mc), (M, Bp, bm)]:
        f.seg(p, q, color=GIVEN, w=1.4, dash="6,4")
        m = mul(add(p, q), 0.5)
        f.label(add(m, (0, 8) if d == mc else (0, -24)), f"{d} cm", size=12, color=GIVEN)
    # scale bar
    y0 = -y * cm - 60
    for i in range(3):
        f.poly([P(i * cm - mc * cm, y0), P((i + 1) * cm - mc * cm, y0), P((i + 1) * cm - mc * cm, y0 + 8), P(i * cm - mc * cm, y0 + 8)],
               fill=INK if i % 2 == 0 else "#ffffff")
        f.label(P((i + 1) * cm - mc * cm, y0 - 18), f"{(i + 1) * 60}", size=11)
    f.label(P(-mc * cm, y0 - 18), "0", size=11)
    f.label(P(-mc * cm + 3 * cm + 16, y0 - 18), "km", anchor="start", size=11)
    f.label(P(-mc * cm + 4 * cm, y0 - 2), "RF 1 : 60,00,000 (1 map cm = 60 km)", anchor="start", size=12, bold=True)
    return f

# ---------------------------------------------------------------- 10.4 triangles from ratios
def tri_from_angles(A, B):
    a1, b1 = A, B
    P0, P1 = P(0, 0), P(240, 0)
    top = meet(P0, a1, P1, 180 - b1)
    return P0, P1, top

@fig
def triangle_135():
    f = Fig("triangle_135")
    angs = [F(180) * k / 9 for k in (1, 3, 5)]
    assert angs == [20, 60, 100]
    A, B, C = tri_from_angles(20, 60)
    f.poly([A, B, C], fill="#e3f2fd")
    f.angle(A, 0, 20, "20°", expect=20, r=40, lr=62)
    f.angle(B, 120, 180, "60°", expect=60, r=24)
    f.angle(C, dirto(C, A), dirto(C, B), "100°", expect=100, r=16, lr=34)
    for p, n, o in [(A, "A", (-12, -12)), (B, "B", (12, -12)), (C, "C", (0, 8))]:
        f.label(add(p, o), n, size=14, bold=True)
    return f

@fig
def triangle_345():
    f = Fig("triangle_345")
    x0 = 0
    for k, u in [(1, 24), (2, 24)]:
        a, b, c = 3 * k, 4 * k, 5 * k
        A = P(x0, 0); B = P(x0 + b * u, 0); C = P(x0, a * u)
        assert abs(dist(B, C) / u - c) < 1e-9
        f.poly([A, B, C], fill="#e8f5e9")
        f.right(A, 0)
        f.label(P(x0 - 14, a * u / 2 - 5), f"{a} cm", anchor="end", size=12, color=GIVEN)
        f.label(P(x0 + b * u / 2, -20), f"{b} cm", size=12, color=GIVEN)
        f.label(P(x0 + b * u / 2 + 14, a * u / 2 + 4), f"{c} cm", anchor="start", size=12, color=GIVEN)
        x0 += b * u + 90
    f.label(P(0, -46), "Same shape (ratio 3 : 4 : 5), different sizes: similar, not congruent", anchor="start", size=12, color=ANS)
    return f

@fig
def triangle_135_sides():
    f = Fig("triangle_135_sides")
    u = 40
    A, B = P(0, 0), P(5 * u, 0)
    f.seg(A, B, w=2.4)
    f.label(P(2.5 * u, -20), "5", size=13, color=GIVEN)
    for p, r in [(A, 1), (B, 3)]:
        f.circle(p, r * u, color=HELP, dash="4,4")
        f.seg(p, along(p, 60 if p == A else 120, r * u), color=GIVEN, w=2)
    f.label(P(-6, u + 10), "1", size=13, color=GIVEN)
    f.label(P(5 * u - 1.5 * u - 10, 3 * u * 0.87 / 2 + 10), "3", size=13, color=GIVEN)
    assert 1 + 3 < 5
    f.label(P(2.5 * u, -3 * u - 22), "1 + 3 = 4 < 5: the two short sides can't reach each other", size=12, color=ASK)
    return f

# ---------------------------------------------------------------- 10.5 pie charts
@fig
def pie_grades():
    f = Fig("pie_grades")
    items = [("A", 12), ("B", 10), ("C", 8), ("D", 6), ("E", 4)]
    angs = pie(f, P(0, 0), 110, items)
    assert [int(a) for a in angs] == [108, 90, 72, 54, 36]
    f.label(P(0, 128), "Grades of 40 students", size=13, bold=True)
    return f

@fig
def pie_seasons():
    f = Fig("pie_seasons")
    angs = pie(f, P(0, 0), 100, [("Summer", 90), ("Rainy", 120), ("Winter", 150)])
    assert [int(a) for a in angs] == [90, 120, 150]
    return f

@fig
def pie_tv():
    f = Fig("pie_tv")
    angs = pie(f, P(0, 0), 100, [("Entertainment", 50), ("Sports", 25), ("News", 15), ("Info", 10)], size=11)
    assert [int(a) for a in angs] == [180, 90, 54, 36]
    return f

CLASS = [("Language", 6), ("Maths", 9), ("Science", 8), ("Arts", 3), ("Vocational", 2), ("Social Sc.", 5), ("PE", 3)]

@fig
def pie_class():
    f = Fig("pie_class")
    angs = pie(f, P(0, 0), 115, CLASS, label_r=80, size=10)
    assert sum(v for _, v in CLASS) == 36 and [int(a) for a in angs] == [60, 90, 80, 30, 20, 50, 30]
    return f

@fig
def pie_transport():
    f = Fig("pie_transport")
    items = [("Walk", 90), ("Cycle", 60), ("Car", 30), ("Two-wheeler", 60), ("Bus", 120)]
    a = 90
    c, R = P(0, 0), 110
    for (lab, ang), col in zip(items, COLS):
        pts = [c] + [along(c, a + ang * k / 30, R) for k in range(31)]
        f.poly(pts, fill=col)
        mid = a + ang / 2
        f.label(along(P(0, -5), mid, R * 0.66), lab, size=11)
        if lab != "Car":
            f.label(along(P(0, -5), mid, R * 0.3), f"{ang}°", size=11, color=GIVEN)
        a += ang
    assert sum(v for _, v in items) == 360
    f.label(P(0, -R - 20), "the Car slice's angle is not written", size=11, color=HELP)
    return f

# ---------------------------------------------------------------- 10.6 inverse proportion
@fig
def speed_time():
    f = Fig("speed_time")
    kx, ky = 6, 14
    pts = [(5, 18), (15, 6), (30, 3), (60, 1.5)]
    for s, t in pts: assert s * t == 90
    f.seg(P(0, 0), P(65 * kx, 0), w=1.6); f.seg(P(0, 0), P(0, 20 * ky), w=1.6)
    for s in range(0, 61, 10):
        f.label(P(s * kx, -18), str(s), size=11, color=HELP)
    for t in range(0, 19, 3):
        f.label(P(-8, t * ky - 5), str(t), anchor="end", size=11, color=HELP)
    curve = [P(s * kx, 90 / s * ky) for s in [4.6 + i * 0.5 for i in range(112)] if 90 / s <= 19.6]
    for p, q in zip(curve, curve[1:]):
        f.seg(p, q, color=GIVEN, w=1.6)
    names = {5: "walk", 15: "bicycle", 30: "motorcycle", 60: "car"}
    for s, t in pts:
        disc(f, P(s * kx, t * ky), 5, "#e53935")
        f.label(P(s * kx + 8, t * ky + 6), f"{names[s]}: {s} km/h, {fmt(t)} h", anchor="start", size=11)
    f.label(P(32 * kx, -40), "speed (km/h)", size=12)
    f.label(P(0, 20 * ky + 12), "time (hours)", size=12)
    f.label(P(30 * kx, 14 * ky), "speed × time = 90 km every time", size=13, bold=True, color=ANS)
    return f

# ---------------------------------------------------------------- sleep charts
SLEEP = [("giraffe", 2.5), ("elephant", 3.5), ("adult human", 8), ("dog", 10.5), ("cat", 13), ("squirrel", 15), ("python", 18), ("bat", 20)]

def donut(f, c, hours, name, show):
    R, r = 38, 24
    frac = hours / 24
    a0 = 90
    for col, start, sweep in [(NAVY, a0, 360 * frac), (GOLD, a0 + 360 * frac, 360 * (1 - frac))]:
        outer = [along(c, start + sweep * k / 40, R) for k in range(41)]
        inner = [along(c, start + sweep * (40 - k) / 40, r) for k in range(41)]
        f.poly(outer + inner, fill=col, color=col)
    f.label(P(c[0], c[1] - R - 18), name, size=12, bold=True)
    if show: f.text(P(c[0], c[1] - 6), f"{fmt(hours)} h", size=13, bold=True, color=NAVY)

@fig
def sleep_charts():
    f = Fig("sleep_charts")
    order = [0, 4, 2, 7, 3, 6, 1, 5]           # shuffled so the answer isn't the reading order
    for i, k in enumerate(order):
        name, h = SLEEP[k]
        donut(f, P((i % 4) * 110, -(i // 4) * 120), h, name, False)
    f.label(P(-40, 60), "Blue: the part of a 24-hour day spent asleep", anchor="start", size=12, color=HELP)
    return f

@fig
def sleep_answers():
    f = Fig("sleep_answers")
    order = [0, 4, 2, 7, 3, 6, 1, 5]
    for i, k in enumerate(order):
        name, h = SLEEP[k]
        donut(f, P((i % 4) * 110, -(i // 4) * 120), h, name, True)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
