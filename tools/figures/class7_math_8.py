"""Figures for class 7 maths Ch 8, Working with Fractions. Every shaded area is computed with
exact fractions from the drawn cells or polygons and asserted against the value written in the
notes, so a picture can never disagree with its answer."""
import os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "8")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

BLUE, YELLOW, GREEN, ORANGE, GREY, RED = "#bbdefb", "#fff176", "#a5d6a7", "#ffcc80", "#eeeeee", "#ef9a9a"

def area(ps):
    """Exact shoelace area of a polygon given with Fraction coordinates."""
    s = F(0)
    for (x1, y1), (x2, y2) in zip(ps, ps[1:] + ps[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2

# ---------------------------------------------------------------- number-line pictures
@fig
def tortoise():
    f = Fig("tortoise"); L = 320
    f.seg(P(0, 0), P(L, 0), w=2)
    for i in range(5):
        x = L * i / 4
        f.seg(P(x, -6), P(x, 6), w=1.6)
        f.label(P(x, -20), ["0", "1/4", "2/4", "3/4", "1 km"][i], size=13)
    for i in range(3):
        a, b = L * i / 4, L * (i + 1) / 4
        f.seg(P(a + 4, 14), P(b - 4, 14), color=ANS, w=3)
        f.label(P((a + b) / 2, 28), f"hour {i + 1}", size=12, color=ANS)
    assert 3 * F(1, 4) == F(3, 4)
    return f

@fig
def aaron_fifths():
    f = Fig("aaron_fifths"); L = 330
    box(f, 0, 0, L, 26, fill=GREY)
    for i in range(5):
        box(f, L * i / 5, 0, L / 5, 26, fill=ORANGE if i < 2 else GREY)
        f.label(P(L * (i + 0.5) / 5, 13), "3/5 km", size=12)
    f.label(P(L / 2, 42), "3 km = distance in 1 hour", size=13)
    f.label(P(L * 1 / 5, -16), "2/5 hour: 2 × 3/5 = 6/5 km", size=13, color=ANS, bold=True)
    assert F(2, 5) * 3 == 2 * F(3, 5) == F(6, 5)
    return f

# ---------------------------------------------------------------- unit-square products
def product_square(name, a, b, c, d, s=150, label=True, whole=1):
    """Picture of (a/b) × (c/d): unit square cut into d rows and b columns; the multiplicand
    c/d is c rows (blue); the product is a columns of those rows (green)."""
    f = Fig(name)
    for k in range(whole):
        x0 = k * (s + 10)
        for col in range(b):
            for row in range(d):
                fill = "#ffffff"
                in_mult = row < c - k * d
                if in_mult: fill = BLUE
                if in_mult and col < a: fill = GREEN
                box(f, x0 + col * s / b, row * s / d, s / b, s / d, fill=fill, color="#90a4ae")
        f.poly([P(x0, 0), P(x0 + s, 0), P(x0 + s, s), P(x0, s)], fill="none", color=INK)
    cells = sum(1 for k in range(whole) for col in range(a) for row in range(d) if row < c - k * d)
    assert F(cells, b * d) == F(a, b) * F(c, d), name
    if label:
        f.label(P(-12, s * c / d / 2 if whole == 1 else s / 2), f"{c}/{d}", anchor="end", size=14, color=GIVEN, bold=True)
        f.label(P(s * a / b / 2, s + 14), f"{a}/{b}", size=14, color=ANS, bold=True)
        f.label(P((whole * s + (whole - 1) * 10) / 2, -18), f"{a}/{b} × {c}/{d} = {cells}/{b * d}", size=14, bold=True)
    return f

for nm, args in [("quarter_halved", (1, 2, 1, 4)), ("three_quarters_of_two_fifths", (3, 4, 2, 5)),
                 ("p_1_3_x_1_5", (1, 3, 1, 5)), ("p_1_4_x_1_3", (1, 4, 1, 3)), ("p_1_5_x_1_2", (1, 5, 1, 2)),
                 ("p_1_6_x_1_5", (1, 6, 1, 5)), ("p_2_3_x_4_5", (2, 3, 4, 5)), ("p_1_4_x_2_3", (1, 4, 2, 3)),
                 ("p_3_5_x_1_2", (3, 5, 1, 2)), ("p_4_6_x_3_5", (4, 6, 3, 5))]:
    FIGS.append((lambda nm=nm, args=args: product_square(nm, *args)))

@fig
def five_quarters_of_three_halves():
    # 3/2 is one whole and a half: two unit squares, 2 rows each, 4 columns; 3 rows shaded.
    f = product_square("five_quarters_of_three_halves", 1, 4, 3, 2, whole=2, label=False)
    f.label(P(160, -18), "3/2 split into 4 equal parts: each part is 3/8 (green)", size=13, bold=True)
    assert F(3, 2) / 4 == F(3, 8) and 5 * F(3, 8) == F(15, 8)
    return f

@fig
def rectangle_area():
    f = Fig("rectangle_area"); s = 160
    box(f, 0, 0, s, s, fill="#ffffff")
    box(f, 0, s - s / 4, s / 2, s / 4, fill=ORANGE)
    for i in range(1, 4): f.seg(P(0, s * i / 4), P(s, s * i / 4), color="#b0bec5", w=1)
    f.seg(P(s / 2, 0), P(s / 2, s), color="#b0bec5", w=1)
    f.label(P(s / 4, s + 14), "1/2", size=14, color=GIVEN, bold=True)
    f.label(P(-10, s - s / 8), "1/4", size=14, anchor="end", color=GIVEN, bold=True)
    f.label(P(s / 2, -16), "8 such rectangles fill the square: area 1/8", size=13, bold=True)
    assert F(1, 2) * F(1, 4) == F(1, 8)
    return f

@fig
def order_swap():
    f = Fig("order_swap"); s = 120
    for k, (w, h) in enumerate([(F(1, 2), F(1, 4)), (F(1, 4), F(1, 2))]):
        x0 = k * (s + 60)
        box(f, x0, 0, s, s)
        box(f, x0, s - s * float(h), s * float(w), s * float(h), fill=ORANGE)
        f.label(P(x0 + s / 2, -16), f"{w} × {h} = {w * h}", size=14, bold=True)
    assert F(1, 2) * F(1, 4) == F(1, 4) * F(1, 2)
    return f

# ---------------------------------------------------------------- fractional relations
def unit(f, s):
    box(f, 0, 0, s, s); return s

@fig
def relations_example():
    f = Fig("relations_example"); s = 200; h = F(1, 2)
    unit(f, s)
    S = lambda x, y: P(float(x) * s, float(y) * s)
    # the main lines: diagonal from top-left to bottom-right, a horizontal and vertical half-line
    f.seg(S(0, 1), S(1, 0)); f.seg(S(0, h), S(h, 0)); f.seg(S(h, h), S(1, h)); f.seg(S(h, h), S(h, 1))
    # top-right quarter: its diagonal and mid-lines
    q = lambda x, y: S(h + x * h, h + y * h)
    tri = [q(F(1, 2), 0), q(1, 0), q(1, 1), q(F(1, 2), F(1, 2))]
    exact = [(h + x * h, h + y * h) for (x, y) in [(F(1, 2), 0), (1, 0), (1, 1), (F(1, 2), F(1, 2))]]
    f.poly(tri, fill=ORANGE)
    f.seg(q(0, 0), q(1, 1)); f.seg(q(F(1, 2), 0), q(F(1, 2), 1)); f.seg(q(0, F(1, 2)), q(1, F(1, 2)))
    assert area(exact) == F(3, 32)
    f.poly([S(h, h), S(1, h), S(1, 1), S(h, 1)], fill="none", color=ASK)
    return f

@fig
def relations_a():
    f = Fig("relations_a"); s = 200; h = F(1, 2)
    S = lambda x, y: P(float(x) * s, float(y) * s)
    unit(f, s)
    band = [(F(0), F(1)), (F(0), h), (h, F(0)), (F(1), F(0))]   # between x + y = 1/2 and x + y = 1
    f.poly([S(*p) for p in band], fill=ORANGE)
    f.seg(S(0, 1), S(1, 0)); f.seg(S(0, h), S(h, 0)); f.seg(S(0, 0), S(h, h))
    f.seg(S(h, h), S(1, h)); f.seg(S(h, h), S(h, 1)); f.seg(S(h, 1), S(1, h))
    f.seg(S(F(3, 4), h), S(F(3, 4), 1)); f.seg(S(h, F(3, 4)), S(1, F(3, 4)))
    assert area(band) == F(3, 8)
    return f

@fig
def relations_b():
    f = Fig("relations_b"); s = 200; h = F(1, 2)
    S = lambda x, y: P(float(x) * s, float(y) * s)
    unit(f, s)
    f.seg(S(0, h), S(1, h)); f.seg(S(h, h), S(h, 1))
    q = lambda x, y: (x * h, h + y * h)                          # top-left quarter coordinates
    t1 = [q(F(1, 2), 1), q(1, 1), q(1, F(1, 2))]
    t2 = [q(1, F(1, 2)), q(1, 0), q(F(1, 2), 0)]
    for t in (t1, t2): f.poly([S(*p) for p in t], fill=ORANGE)
    f.poly([S(*q(F(1, 2), 1)), S(*q(1, F(1, 2))), S(*q(F(1, 2), 0)), S(*q(0, F(1, 2)))], fill="none")
    assert area(t1) + area(t2) == F(1, 16)
    return f

@fig
def relations_q10():
    f = Fig("relations_q10"); s = 200; h = F(1, 2)
    S = lambda x, y: P(float(x) * s, float(y) * s)
    unit(f, s)
    f.seg(S(0, h), S(1, h)); f.seg(S(h, 0), S(h, 1))
    q = lambda x, y: (h + x * h, y * h)                          # bottom-right quarter
    shaded = [q(0, 0), q(F(1, 2), 0), q(F(1, 2), F(1, 2)), q(0, 1)]
    f.poly([S(*p) for p in shaded], fill=ORANGE)
    f.seg(S(*q(0, 1)), S(*q(F(1, 2), F(1, 2)))); f.seg(S(*q(1, 1)), S(*q(F(1, 2), F(1, 2))))
    f.seg(S(*q(F(1, 2), F(1, 2))), S(*q(F(1, 2), 0)))
    assert area(shaded) == F(3, 32)
    return f

# ---------------------------------------------------------------- ants splitting
@fig
def ants():
    f = Fig("ants")
    nodes = {1: P(150, 40), 2: P(185, 110), 3: P(220, 190), 4: P(225, 250)}
    share = {1: F(1)}
    paths = [(1, "M", P(60, 300)), (1, 2, None), (2, "M", P(95, 300)), (2, 3, None),
             (3, "M", P(130, 300)), (3, "M", P(165, 300)), (3, 4, None), (3, "S", P(330, 300)),
             (4, "M", P(205, 300)), (4, "S", P(290, 300))]
    splits = {}
    for a, _, _ in paths: splits[a] = splits.get(a, 0) + 1
    got = {"M": F(0), "S": F(0)}
    f.seg(P(150, 0), nodes[1], color="#43a047", w=7)
    for a, b, end in paths:
        part = share[a] / splits[a]
        if isinstance(b, int):
            share[b] = part; f.seg(nodes[a], nodes[b], color="#43a047", w=7)
        else:
            got[b] += part; f.seg(nodes[a], end, color="#43a047", w=7)
    for k, p in nodes.items():
        f.dot(p, color="#b71c1c")
    box(f, 30, 300, 200, 22, fill="#c62828"); f.label(P(130, 311), "Mango tree", size=13, color="#ffffff", bold=True)
    box(f, 250, 300, 110, 22, fill="#c62828"); f.label(P(305, 311), "Sugarcane", size=13, color="#ffffff", bold=True)
    assert got["M"] == F(29, 32) and got["S"] == F(3, 32)
    return f

# ---------------------------------------------------------------- saplings
@fig
def saplings():
    f = Fig("saplings"); g = 90
    for i in range(4):
        x = i * g
        f.poly([P(x - 8, 0), P(x + 8, 0), P(x, 22)], fill="#81c784")
        f.seg(P(x, 0), P(x, -8), color="#6d4c41", w=3)
    for i in range(3):
        f.seg(P(i * g + 10, -18), P((i + 1) * g - 10, -18), color=GIVEN, w=1.6)
        f.label(P(i * g + g / 2, -30), "3/4 m", size=13, color=GIVEN, bold=True)
    assert 3 * F(3, 4) == F(9, 4)
    f.label(P(1.5 * g, 38), "4 saplings, but only 3 gaps", size=13, color=ASK, bold=True)
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
