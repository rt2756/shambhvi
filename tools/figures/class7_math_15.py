"""Figures for class 7 maths Ch 15, Finding the Unknown. Every mobile and balance is drawn from a
list of items, and the solved weights are asserted to balance it; stick and tile patterns are
counted from the drawn pieces; triangle angles are asserted against their algebra labels."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "15")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

COL = {"tri": "#43a047", "circ": "#8e24aa", "sq": "#1e88e5", "dia": "#e53935", "star": "#fb8c00",
       "hex": "#6d4c41", "plus": "#fdd835"}
SACK, BLOCK = "#c8a27a", "#ef9a9a"

def rect(f, x, y, w, h, fill, color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def shape(f, kind, c, r=11):
    fill = COL[kind]
    if kind == "tri": pts = [along(c, 90 + 120 * k, r * 1.2) for k in range(3)]
    elif kind == "circ": pts = [along(c, 30 * k, r) for k in range(12)]
    elif kind == "sq": pts = [along(c, 45 + 90 * k, r * 1.3) for k in range(4)]
    elif kind == "dia": pts = [along(c, 90 * k, r * 1.3) for k in range(4)]
    elif kind == "hex": pts = [along(c, 60 * k, r * 1.15) for k in range(6)]
    elif kind == "star": pts = [along(c, 90 + 36 * k, r * 1.35 if k % 2 == 0 else r * 0.6) for k in range(10)]
    elif kind == "plus":
        a, b = r * 1.1, r * 0.4
        pts = [P(-b, a), P(b, a), P(b, b), P(a, b), P(a, -b), P(b, -b), P(b, -a), P(-b, -a), P(-b, -b),
               P(-a, -b), P(-a, b), P(-b, b)]
        pts = [add(c, p) for p in pts]
    f.poly(pts, fill=fill, color=INK)

# ---------------------------------------------------------------- mobiles
def weight(item, W):
    if isinstance(item, tuple): return sum(weight(i, W) for i in item[0]) + sum(weight(i, W) for i in item[1])
    return W[item]

def hang(f, x, y, items, W, step=32):
    """Hang a column of items from (x, y) downward. A tuple (left, right) is a sub-mobile."""
    f.seg(P(x, y), P(x, y - 14), w=1.3)
    y -= 14
    for idx, it in enumerate(items):
        if isinstance(it, tuple):
            bar = 50
            f.seg(P(x - bar / 2, y), P(x + bar / 2, y), w=3)
            assert sum(weight(i, W) for i in it[0]) == sum(weight(i, W) for i in it[1])
            hang(f, x - bar / 2, y, it[0], W); hang(f, x + bar / 2, y, it[1], W)
            return
        shape(f, it, P(x, y - 13))
        if idx < len(items) - 1: f.seg(P(x, y - 26), P(x, y - step), w=1.3)
        y -= step

def mobile(name, total, left, right, W, known, unknown, bar=110):
    f = Fig(name)
    L = sum(weight(i, W) for i in left); R = sum(weight(i, W) for i in right)
    assert L == R, (name, L, R)
    if total is not None:
        assert L + R == total, (name, L + R, total)
        f.circle(P(0, 30), 15, color=INK, w=2)
        f.label(P(0, 30), str(total), bold=True, size=15)
        f.seg(P(0, 15), P(0, 0), w=2)
    else:
        f.seg(P(0, 18), P(0, 0), w=2)
        f.label(P(0, 30), "(no total given)", size=11, color=HELP)
    f.seg(P(-bar / 2, 0), P(bar / 2, 0), w=3.5)
    hang(f, -bar / 2, 0, left, W); hang(f, bar / 2, 0, right, W)
    # key
    y, x = -200, -bar / 2 - 30
    for k in known + unknown:
        shape(f, k, P(x, y), r=9)
        f.label(P(x + 14, y), f"= {W[k]}" if k in known else "= ?", anchor="start", size=14,
                bold=True, color=INK if k in known else ASK)
        x += 62
    return f

@fig
def mobile_rule():
    f = Fig("mobile_rule")
    for x0, tot, a, b, tilt in ((0, 4, 2, 2, 0), (220, 7, 4, 3, -8)):
        assert a + b == tot
        f.circle(P(x0, 40), 15, color=INK, w=2); f.label(P(x0, 40), str(tot), bold=True)
        f.seg(P(x0, 25), P(x0, 10), w=2)
        l, r = along(P(x0, 10), 180 + tilt, 65), along(P(x0, 10), tilt, 65)
        f.seg(l, r, w=3.5)
        for p, v in ((l, a), (r, b)):
            f.seg(p, add(p, (0, -20)), w=1.3)
            rect(f, p[0] - 16, p[1] - 52, 32, 32, "#fff3e0")
            f.label(P(p[0], p[1] - 36), str(v), bold=True)
        f.label(P(x0, -80), "level: both sides equal" if a == b else "tilts to the heavier side", size=12,
                color=ANS if a == b else ASK, bold=True)
    return f

MOBILES = [
    ("mobile_1", 16, ["tri", "circ", "tri"], ["star"], {"tri": 3, "circ": 2, "star": 8}, ["tri"], ["circ", "star"]),
    ("mobile_2", 24, ["dia", "sq", "dia"], ["sq", "hex"], {"dia": 2, "sq": 8, "hex": 4}, ["dia"], ["sq", "hex"]),
    ("mobile_3", 8, ["circ"], [(["tri"], ["tri"])], {"circ": 4, "tri": 2}, [], ["circ", "tri"]),
    ("mobile_4", 18, ["star", "sq", "sq", "sq", "sq"], ["dia", "dia", "dia"], {"star": 5, "sq": 1, "dia": 3}, ["star"], ["sq", "dia"]),
    ("mobile_5", 40, ["tri"] + ["circ"] * 5, ["tri"] * 4, {"tri": 5, "circ": 3}, [], ["tri", "circ"]),
    ("mobile_6", None, ["sq"] * 3, ["circ"] * 2, {"sq": 2, "circ": 3}, ["sq"], ["circ"]),
    ("mobile_7", None, ["plus"] * 4, ["circ", "plus", "circ"], {"plus": 4, "circ": 6}, ["plus"], ["circ"]),
    ("mobile_8", None, ["hex"], ["tri", "circ", "tri"], {"hex": 10, "circ": 4, "tri": 3}, ["hex", "circ"], ["tri"]),
]
for spec in MOBILES:
    FIGS.append(lambda s=spec: mobile(*s))

# ---------------------------------------------------------------- pan balances
def sack(f, c, label="?"):
    pts = [add(c, (14 * math.cos(math.radians(a)) * (1 if a % 360 < 180 else 1.1), 17 * math.sin(math.radians(a)))) for a in range(0, 360, 30)]
    f.poly(pts, fill=SACK, color=INK)
    f.seg(add(c, (-5, 17)), add(c, (-8, 24)), w=1.6); f.seg(add(c, (5, 17)), add(c, (8, 24)), w=1.6)
    f.label(c, label, bold=True, size=12)

def block(f, x, y, kg):
    w = 30 if kg < 50 else 46
    rect(f, x, y, w, w * 0.8, BLOCK)
    f.label(P(x + w / 2, y + w * 0.4), f"{kg} kg", bold=True, size=11)
    return w

def balance(name, left, right, s, note=None):
    """left/right: lists of 'S' (sack) or kg numbers. Asserts both pans weigh the same with sack = s."""
    f = Fig(name)
    wt = lambda side: sum(s if i == "S" else i for i in side)
    assert wt(left) == wt(right), (name, wt(left), wt(right))
    f.seg(P(-150, 110), P(150, 110), w=4)
    f.poly([P(0, 110), P(-14, 80), P(14, 80)], fill="#90a4ae")
    f.seg(P(0, 80), P(0, -10), w=4); f.seg(P(-30, -10), P(30, -10), w=4)
    for cx, side in ((-150, left), (150, right)):
        f.seg(P(cx - 60, 0), P(cx + 60, 0), w=4)
        f.seg(P(cx - 55, 2), P(cx, 108), w=1, color=HELP); f.seg(P(cx + 55, 2), P(cx, 108), w=1, color=HELP)
        x = cx - 55
        for it in side:
            if it == "S":
                sack(f, P(x + 14, 20)); x += 30
            else:
                x += block(f, x, 2, it) + 3
    f.label(P(0, -28), note or "the scale is level", size=12, color=HELP)
    return f

@fig
def scale_1(): return balance("scale_1", ["S", 2], [10, 2], 10)
@fig
def scale_2(): return balance("scale_2", ["S", "S"], [10, 4, "S"], 14)
@fig
def scale_3(): return balance("scale_3", ["S"] * 5, [1, 10, 10, "S", "S"], 7)
@fig
def scale_4():
    f = Fig("scale_4"); s = 15
    assert 90 * s + 50 == 60 * s + 500
    f.seg(P(-150, 110), P(150, 110), w=4)
    f.poly([P(0, 110), P(-14, 80), P(14, 80)], fill="#90a4ae")
    f.seg(P(0, 80), P(0, -10), w=4); f.seg(P(-30, -10), P(30, -10), w=4)
    for cx in (-150, 150):
        f.seg(P(cx - 60, 0), P(cx + 60, 0), w=4)
    for i in range(3): sack(f, P(-195 + 22 * i, 20), "")
    f.label(P(-172, 52), "90 sacks", bold=True, size=13)
    block(f, -140, 2, 50)
    for i in range(3): sack(f, P(105 + 22 * i, 20), "")
    f.label(P(128, 52), "60 sacks", bold=True, size=13)
    block(f, 160, 2, 500)
    f.label(P(0, -28), "the scale is level; all sacks weigh the same", size=12, color=HELP)
    return f

# ---------------------------------------------------------------- patterns
def stick(f, p, q, color="#f9a825"):
    f.seg(p, q, color=color, w=4)

@fig
def match_triangles():
    f = Fig("match_triangles"); s = 40; h = s * math.sqrt(3) / 2
    x0 = 0
    for n in range(1, 5):
        edges = set()
        for i in range(n):
            if i % 2 == 0:   # upward triangle
                a, b, c = P(x0 + i / 2 * s, 0), P(x0 + (i / 2 + 1) * s, 0), P(x0 + (i / 2 + 0.5) * s, h)
            else:            # downward triangle between two upward ones
                a, b, c = P(x0 + (i - 1) / 2 * s + s / 2, h), P(x0 + (i + 1) / 2 * s + s / 2, h), P(x0 + (i + 1) / 2 * s, 0)
            for e in ((a, b), (b, c), (c, a)):
                edges.add(tuple(sorted((tuple(round(v, 3) for v in e[0]), tuple(round(v, 3) for v in e[1])))))
        assert len(edges) == 2 * n + 1, (n, len(edges))
        for p, q in edges: stick(f, p, q)
        f.label(P(x0 + (n + 1) / 4 * s, -18), f"{n}: {2 * n + 1} sticks", size=12, bold=True)
        x0 += (n + 1) / 2 * s + 40
    return f

@fig
def t_tiles():
    f = Fig("t_tiles"); u = 18; x0 = 0
    for k in range(1, 4):
        cells = {(c, 0) for c in range(2 * k + 1)} | {(k, -r) for r in range(1, k + 1)}
        assert len(cells) == 3 * k + 1
        for c, r in cells:
            rect(f, x0 + c * u, r * u, u, u, "#ffe0b2" if r == 0 else "#bbdefb")
        f.label(P(x0 + (2 * k + 1) * u / 2, 32), f"Step {k}: {3 * k + 1} tiles", size=12, bold=True)
        x0 += (2 * k + 1) * u + 40
    return f

def house_edges(n):
    E = set()
    for i in range(n):
        for e in (((i, 0), (i + 1, 0)), ((i, 1), (i + 1, 1)), ((i, 0), (i, 1)), ((i + 1, 0), (i + 1, 1))):
            E.add(e)
    E.add(((n, 0), (n + 0.8, 0.5))); E.add(((n, 1), (n + 0.8, 0.5)))
    return E

def stair_cells(n):
    cells = {(0, 0), (1, 0)}
    for r in range(1, n):
        cells |= {(2 * r - 1, -r), (2 * r, -r), (2 * r + 1, -r)}
    cells |= {(2 * n - 1, -n), (2 * n, -n)}
    return cells

def cell_edges(cells):
    E = set()
    for c, r in cells:
        for e in (((c, r), (c + 1, r)), ((c, r + 1), (c + 1, r + 1)), ((c, r), (c, r + 1)), ((c + 1, r), (c + 1, r + 1))):
            E.add(e)
    return E

HOUSE = lambda n: (n, len(house_edges(n)))
STAIR = lambda n: (len(stair_cells(n)), len(cell_edges(stair_cells(n))))

@fig
def stick_houses():
    f = Fig("stick_houses"); u = 30; x0 = 0
    for n in range(1, 4):
        E = house_edges(n)
        assert len(E) == 3 * n + 3
        for (a, b) in E: stick(f, P(x0 + a[0] * u, a[1] * u), P(x0 + b[0] * u, b[1] * u))
        f.label(P(x0 + (n + 0.8) * u / 2, -16), f"Position {n}", size=12, bold=True)
        x0 += (n + 0.8) * u + 36
    return f

@fig
def stick_stairs():
    f = Fig("stick_stairs"); u = 15; x0 = 0
    for n in range(1, 4):
        sq, st = STAIR(n)
        assert sq == 3 * n + 1 and st == 9 * n + 4, (n, sq, st)
        for (a, b) in cell_edges(stair_cells(n)): stick(f, P(x0 + a[0] * u, a[1] * u), P(x0 + b[0] * u, b[1] * u))
        f.label(P(x0 + (2 * n + 1) * u / 2, 30), f"Position {n}", size=12, bold=True)
        x0 += (2 * n + 1) * u + 30
    return f

# ---------------------------------------------------------------- bar models, blobs, machines
@fig
def marbles():
    f = Fig("marbles"); k = 4; y = 15; d = 30
    assert y + (y + d) == 60
    rect(f, 0, 40, y * k, 24, "#bbdefb"); f.label(P(y * k / 2, 52), "y", bold=True)
    f.label(P(-8, 52), "Suresh", anchor="end", size=13, bold=True)
    rect(f, 0, 0, y * k, 24, "#bbdefb"); f.label(P(y * k / 2, 12), "y", bold=True)
    rect(f, y * k, 0, d * k, 24, "#ffe0b2"); f.label(P(y * k + d * k / 2, 12), "30", bold=True)
    f.label(P(-8, 12), "Ramesh", anchor="end", size=13, bold=True)
    f.label(P((y + d) * k + 20, 32), "together: 60", anchor="start", size=13, color=ASK, bold=True)
    return f

@fig
def party():
    f = Fig("party"); k = 0.7
    assert 25 * 18 + 50 == 500
    for i in range(18):
        rect(f, i * 25 * k, 0, 25 * k, 26, "#c5e1a5")
    rect(f, 18 * 25 * k, 0, 50 * k, 26, "#ffcc80")
    f.label(P(18 * 25 * k + 25 * k, 13), "50", size=11, bold=True)
    f.seg(P(0, 36), P(500 * k, 36), color=ASK, w=1.6)
    f.label(P(250 * k, 48), "₹500 in all", size=13, color=ASK, bold=True)
    f.label(P(225 * k, -14), "one ₹25 plate per person: ₹450", size=12, color=ANS, bold=True)
    f.label(P(475 * k, -14), "delivery", size=12, color=HELP, bold=True)
    return f

@fig
def blobs():
    f = Fig("blobs"); b = 7
    def splat(c, r):
        pts = [along(c, 24 * i, r * (1 if i % 2 == 0 else 0.55)) for i in range(15)]
        f.poly(pts, fill="#212121", color="#212121")
    for c in (P(0, 60), P(130, 55), P(55, -10)): splat(c, 42)
    dots = [P(70, 75), P(-10, 0), P(75, 30), P(125, -25)]
    for d in dots:
        f.poly([along(d, 30 * i, 7) for i in range(12)], fill="#29b6f6", color="#29b6f6")
    assert 3 * b + len(dots) == 25
    f.label(P(160, 110), "25 dots in all", anchor="end", size=13, bold=True)
    return f

def box(f, x, y, text, fill, w=56):
    rect(f, x, y - 16, w, 32, fill)
    f.label(P(x + w / 2, y), text, bold=True, size=14)
    return x + w

def arrow(f, p, q, color=INK):
    f.seg(p, q, color=color, w=1.8)
    a = dirto(p, q)
    for d in (25, -25): f.seg(along(q, a + 180 + d, 8), q, color=color, w=1.8)

@fig
def machine_a():
    f = Fig("machine_a")
    rule = lambda x: (x + 3) * 4 - 5
    assert rule(12) == 55 and rule(9) == 43 and rule(17) == 75
    for row, (inp, out) in enumerate(((12, 55), ("?", 43), ("?", 75))):
        y = -row * 50
        f.label(P(0, y), str(inp), bold=True, color=ASK if inp == "?" else INK, size=15)
        arrow(f, P(14, y), P(40, y))
        x = box(f, 40, y, "+ 3", "#bbdefb"); arrow(f, P(x, y), P(x + 26, y))
        x = box(f, x + 26, y, "× 4", "#ffcc80"); arrow(f, P(x, y), P(x + 26, y))
        x = box(f, x + 26, y, "− 5", "#dcedc8")
        f.label(P(x + 16, y), "=", size=15)
        f.label(P(x + 40, y), str(out), bold=True, size=15)
        if row == 0:
            f.label(P(118, y + 26), "15", size=12, color=HELP); f.label(P(200, y + 26), "60", size=12, color=HELP)
    return f

@fig
def machine_b():
    f = Fig("machine_b")
    rule = lambda x: 3 * x - (x + 3)
    assert rule(12) == 21 and rule(33) == 63 and rule(115) == 227
    f.label(P(0, 0), "input", bold=True, size=14)
    arrow(f, P(26, 0), P(60, 0))
    f.seg(P(60, 0), P(60, 50), w=1.8); f.seg(P(60, 0), P(60, -50), w=1.8)
    arrow(f, P(60, 50), P(90, 50)); arrow(f, P(60, -50), P(90, -50))
    x1 = box(f, 90, 50, "× 3", "#ffcc80"); x2 = box(f, 90, -50, "+ 3", "#bbdefb")
    f.seg(P(x1, 50), P(200, 50), w=1.8); arrow(f, P(200, 50), P(200, 18))
    f.seg(P(x2, -50), P(200, -50), w=1.8); arrow(f, P(200, -50), P(200, -18))
    box(f, 172, 0, "top − bottom", "#dcedc8", w=100)
    f.label(P(290, 0), "= output", anchor="start", bold=True, size=14)
    f.label(P(205, 70), "12 → 36", size=12, color=HELP, anchor="start")
    f.label(P(205, -70), "12 → 15", size=12, color=HELP, anchor="start")
    f.label(P(160, -100), "input 12 gives 36 − 15 = 21", size=12, color=HELP)
    return f

@fig
def machine_5():
    f = Fig("machine_5")
    assert 45 / 3 / 3 == 5 and -3 - 4 - 4 == -11
    for row, (ops, out) in enumerate(((("÷ 3", "÷ 3"), "5"), (("− 4", "− 4"), "−11"))):
        y = -row * 50
        f.label(P(0, y), "?", bold=True, color=ASK)
        arrow(f, P(12, y), P(38, y))
        x = box(f, 38, y, ops[0], "#f8bbd0"); arrow(f, P(x, y), P(x + 26, y))
        x = box(f, x + 26, y, ops[1], "#f8bbd0")
        f.label(P(x + 16, y), "=", size=15); f.label(P(x + 40, y), out, bold=True)
    return f

@fig
def window():
    f = Fig("window"); k = 7; W = 24
    frame, rod, n_rods, H = 3, 2, 5, 34
    gaps = n_rods + 1
    g = (H - 2 * frame - n_rods * rod) / gaps
    assert g == 3
    y = H
    rect(f, 0, 0, W * k, H * k, "#90a4ae")
    y = H - frame
    for i in range(gaps):
        rect(f, 6, (y - g) * k, W * k - 12, g * k, "#e0f7fa", color="#90a4ae")
        y -= g
        if i < n_rods: y -= rod
    assert abs(y - frame) < 1e-9
    def dim(y0, y1, text, x, left=False):
        f.seg(P(x, y0 * k), P(x, y1 * k), color=ASK, w=1.4)
        for yy in (y0, y1): f.seg(P(x - 5, yy * k), P(x + 5, yy * k), color=ASK, w=1.4)
        f.label(P(x - 8 if left else x + 8, (y0 + y1) / 2 * k), text, anchor="end" if left else "start",
                size=12, color=ASK, bold=True)
    dim(0, H, "34 cm", -14, left=True)
    dim(H - frame, H, "3 cm (frame)", W * k + 12)
    y_rod_top = H - frame - g
    dim(y_rod_top - rod, y_rod_top, "2 cm (rod)", W * k + 12)
    dim(y_rod_top - rod - g, y_rod_top - rod, "gap = ?", W * k + 100)
    dim(0, frame, "3 cm (frame)", W * k + 12)
    return f

def tri(name, A, B, labels):
    """Triangle with base angles A (left) and B (right); labels = (apex, left, right) text."""
    f = Fig(name); base = 160
    C = 180 - A - B
    L, R = P(0, 0), P(base, 0)
    T = meet(L, A, R, 180 - B)
    f.seg(L, R); f.seg(L, T); f.seg(R, T)
    f.angle(L, 0, A, labels[1], expect=A, r=26, lr=58)
    f.angle(R, 180 - B, 180, labels[2], expect=B, r=26, lr=58)
    f.angle(T, 180 + A, 360 - B, labels[0], expect=C, r=24, lr=42)
    return f, T, L, R

@fig
def triangle_y():
    y = 50
    assert y + 2 * (y + 15) == 180
    f, T, L, R = tri("triangle_y", y + 15, y + 15, ("y", "y + 15", "y + 15"))
    f.ticks(L, T); f.ticks(R, T)
    assert abs(dist(L, T) - dist(R, T)) < 1e-6
    return f

@fig
def triangle_x():
    x = 60
    assert x + (x - 10) + (x + 10) == 180
    f, *_ = tri("triangle_x", x - 10, x + 10, ("x", "x − 10", "x + 10"))
    return f

# ---------------------------------------------------------------- maze
MAZE = [["8x = 20 + 3x", "−7 = 11 − 3x", "15 = 19 − 4x"],
        ["2x − 9 = −3", "−2x = −42", "2x + 3 = x + 5"],
        ["8m + 8 = −72", "2(x + 1) − 10 = 18", "2x + 5 = 3(x − 1)"],
        ["−4 = 16 − 5k", "2x − 9 = 3 − x", "30 = 4 − 50n"]]
SOL = [[4, 6, 1], [3, 21, 2], [-10, 13, 8], [4, 4, None]]
DOORS = {((0, 0), (0, 1)): "−4", ((0, 1), (0, 2)): "−1", ((0, 0), (1, 0)): "4", ((0, 0), (1, 1)): "5",
         ((0, 1), (1, 1)): "−44", ((0, 2), (1, 1)): "21", ((0, 2), (1, 2)): "1", ((1, 0), (1, 1)): "3",
         ((1, 1), (1, 2)): "−2", ((1, 0), (2, 0)): "6", ((1, 0), (2, 1)): "8", ((1, 1), (2, 1)): "5",
         ((1, 2), (2, 1)): "−8", ((1, 2), (2, 2)): "2", ((2, 0), (2, 1)): "13", ((2, 1), (2, 2)): "8",
         ((2, 0), (3, 0)): "−10", ((2, 1), (3, 0)): "−10", ((2, 1), (3, 1)): "−5", ((2, 1), (3, 2)): "−4",
         ((3, 0), (3, 1)): "+4", ((3, 1), (3, 2)): "4", ((2, 2), (3, 2)): ""}

def solve_path():
    def val(s): return str(s) if s < 0 else str(s)
    path, cur, seen = [(0, 0)], (0, 0), {(0, 0)}
    while SOL[cur[0]][cur[1]] is not None:
        v = SOL[cur[0]][cur[1]]
        nxt = [b if a == cur else a for (a, b), lab in DOORS.items() if cur in (a, b)
               and lab.replace("+", "").replace("−", "-") == str(v) and (b if a == cur else a) not in seen]
        assert len(nxt) == 1, (cur, v, nxt)
        cur = nxt[0]; path.append(cur); seen.add(cur)
    return path

@fig
def maze():
    f = Fig("maze"); cw, ch = 150, 80
    path = solve_path()
    assert len(path) == 11 and (0, 1) not in path and path[-1] == (3, 2)
    order = {c: i + 1 for i, c in enumerate(path)}
    for r in range(4):
        for c in range(3):
            x, y = c * (cw + 30), -r * (ch + 30)
            rect(f, x, y - ch, cw, ch, "#f3e5c5" if (r, c) != (0, 0) else "#c5e1a5", color="#8d6e63")
            f.label(P(x + cw / 2, y - ch / 2), MAZE[r][c], size=13, bold=True)
            if (r, c) == (0, 0): f.label(P(x + 30, y - 12), "START", size=11, bold=True, color=ANS)
            if (r, c) == (3, 2): f.label(P(x + cw - 24, y - ch + 10), "END", size=11, bold=True, color=ASK)
    def centre(rc): return P(rc[1] * (cw + 30) + cw / 2, -rc[0] * (ch + 30) - ch / 2)
    for (a, b), lab in DOORS.items():
        pa, pb = centre(a), centre(b)
        m = mul(add(pa, pb), 0.5)
        if a[0] != b[0] and a[1] != b[1]:
            m = add(m, (0, 0))
        f.poly([along(m, 30 * i, 15) for i in range(12)], fill="#ffffff", color="#8d6e63")
        f.label(m, lab if lab else "→", size=12, bold=True)
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
