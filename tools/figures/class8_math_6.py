"""Figures for class 8 maths Ch 6, We Distribute, Yet Things Multiply. Area pictures are drawn to
scale from the numbers on them and assert that the parts add up to the whole; dot and tile
patterns are built from their step rule and counted, so a label can never disagree with its picture."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "6")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, PURPLE = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0", "#ce93d8"

def rect(f, x, y, w, h, fill="#ffffff", color=INK):
    """Rectangle with bottom-left corner (x, y)."""
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, 30)], fill=fill, color=color)

def hatch(f, x, y, w, h, gap=12, color=HELP):
    """Slanting lines (45°) clipped to the rectangle."""
    k = -h
    while k < w:
        # line x - x0 = (y - y0) + k, i.e. points (x + k + t, y + t)
        pts = []
        for t in (0, h):
            pts.append(P(x + k + t, y + t))
        (x1, y1), (x2, y2) = pts
        # clip to [x, x + w]
        if x1 < x: y1 += x - x1; x1 = x
        if x2 > x + w: y2 -= x2 - (x + w); x2 = x + w
        if x1 < x2: f.seg(P(x1, y1), P(x2, y2), color=color, w=1.2)
        k += gap

def dim(f, p, q, text, off=(0, 0), color=GIVEN, size=13):
    """A dimension line with end bars and a label beside its middle."""
    f.seg(p, q, color=color, w=1.3)
    a = dirto(p, q)
    for e in (p, q):
        f.seg(along(e, a + 90, 5), along(e, a - 90, 5), color=color, w=1.3)
    m = mul(add(p, q), 0.5)
    f.label(add(m, off), text, size=size, color=color)

# ---------------------------------------------------------------- 6.1 the distributive property
@fig
def distributive_dots():
    f = Fig("distributive_dots")
    a, b, c, u = 3, 5, 2, 18
    n = 0
    for i in range(a):
        for j in range(b + c):
            x = j * u + (12 if j >= b else 0)
            disc(f, P(x, -i * u), 6, BLUE if j < b else ORANGE); n += 1
    assert n == a * (b + c) == a * b + a * c == 21
    f.seg(P(b * u + 2, 12), P(b * u + 2, -a * u + 6), color=ASK, w=1.6, dash="5,4")
    f.label(P((b - 1) * u / 2, 22), f"b = {b} columns", size=13, color=GIVEN)
    f.label(P(b * u + 12 + (c - 1) * u / 2, 22), f"c = {c}", size=13, color=ANS)
    f.label(P(-14, -u - 5), f"a = {a} rows", anchor="end", size=13, color=INK)
    f.label(P(0, -a * u - 14), f"{a} × ({b} + {c}) = {a} × {b} + {a} × {c} = {a*b} + {a*c} = {n}", anchor="start", size=14, bold=True)
    return f

@fig
def identity1_area():
    f = Fig("identity1_area")
    a, m, b, n = 150, 60, 210, 80             # drawn lengths (not to any number scale)
    rect(f, 0, m, b, a, fill=BLUE); rect(f, b, m, n, a, fill=ORANGE)
    rect(f, 0, 0, b, m, fill=GREEN); rect(f, b, 0, n, m, fill=PINK)
    f.text(P(b / 2, m + a / 2 - 6), "ab", size=20, bold=True)
    f.text(P(b + n / 2, m + a / 2 - 6), "an", size=20, bold=True)
    f.text(P(b / 2, m / 2 - 6), "mb", size=20, bold=True)
    f.text(P(b + n / 2, m / 2 - 6), "mn", size=20, bold=True)
    dim(f, P(0, m + a + 14), P(b, m + a + 14), "b", off=(0, 6))
    dim(f, P(b, m + a + 14), P(b + n, m + a + 14), "n", off=(0, 6))
    dim(f, P(-14, m), P(-14, m + a), "a", off=(-12, -5))
    dim(f, P(-14, 0), P(-14, m), "m", off=(-12, -5))
    assert (a + m) * (b + n) == a * b + a * n + m * b + m * n
    f.label(P((b + n) / 2, -26), "(a + m)(b + n) = ab + an + mb + mn", size=15, bold=True)
    return f

# ---------------------------------------------------------------- 6.2 squares of sums and differences
@fig
def square_65():
    f = Fig("square_65")
    A, B = 60, 5
    s = 3.2                                    # pixels per unit
    rect(f, 0, B * s, A * s, A * s, fill=BLUE)
    rect(f, A * s, B * s, B * s, A * s, fill=ORANGE)
    rect(f, 0, 0, A * s, B * s, fill=ORANGE)
    rect(f, A * s, 0, B * s, B * s, fill=PINK)
    parts = [A * A, A * B, B * A, B * B]
    assert sum(parts) == (A + B) ** 2 == 4225
    f.text(P(A * s / 2, B * s + A * s / 2 - 6), f"60 × 60 = {A*A}", size=15, bold=True)
    f.label(P(A * s + B * s + 8, B * s + A * s / 2 - 5), f"60 × 5 = {A*B}", anchor="start", size=13)
    f.label(P(A * s / 2, -20), f"5 × 60 = {A*B}", size=13)
    f.label(P(A * s + B * s + 8, -2), f"5 × 5 = {B*B}", anchor="start", size=13)
    dim(f, P(0, (A + B) * s + 14), P(A * s, (A + B) * s + 14), "60", off=(0, 6))
    dim(f, P(A * s, (A + B) * s + 14), P((A + B) * s, (A + B) * s + 14), "5", off=(0, 6))
    f.label(P((A + B) * s / 2, -46), f"65² = 3600 + 300 + 300 + 25 = {sum(parts)}", size=14, bold=True, color=ANS)
    return f

@fig
def square_55():
    f = Fig("square_55")
    A, B = 60, 5
    s = 3.2
    rect(f, 0, 0, A * s, A * s, fill="#ffffff")
    rect(f, 0, B * s, (A - B) * s, (A - B) * s, fill=BLUE)
    rect(f, (A - B) * s, 0, B * s, A * s, fill=ORANGE)       # strip 5 × 60 on the right
    rect(f, 0, 0, A * s, B * s, fill=ORANGE)                 # strip 60 × 5 at the bottom
    rect(f, (A - B) * s, 0, B * s, B * s, fill=PINK)         # the corner, inside both strips
    assert A * A - A * B - B * A + B * B == (A - B) ** 2 == 3025
    f.text(P((A - B) * s / 2, B * s + (A - B) * s / 2 - 6), "55 × 55", size=16, bold=True)
    f.label(P(A * s + 8, A * s / 2 - 5), "remove 60 × 5", anchor="start", size=13, color=ASK)
    f.label(P(A * s / 2 - 20, -20), "remove 5 × 60", size=13, color=ASK)
    f.label(P(A * s + 8, -2), "5 × 5 removed twice: add it back once", anchor="start", size=12, color=ANS)
    dim(f, P(0, A * s + 14), P(A * s, A * s + 14), "60", off=(0, 6))
    f.label(P(A * s / 2, -46), f"55² = 3600 − 300 − 300 + 25 = {A*A - 2*A*B + B*B}", size=14, bold=True, color=ANS)
    return f

@fig
def diff_squares():
    f = Fig("diff_squares")
    a, b = 150, 60
    # left: a square a × a with a b × b corner removed, cut into two rectangles
    rect(f, 0, 0, a - b, a, fill=BLUE)                       # (a − b) wide, a tall
    rect(f, a - b, b, b, a - b, fill=ORANGE)                 # b wide, (a − b) tall
    rect(f, a - b, 0, b, b, fill="#ffffff", color=HELP)      # the removed corner
    f.text(P(a - b + b / 2, b / 2 - 6), "b²", size=14, color=HELP)
    f.text(P((a - b) / 2, a / 2 - 6), "A", size=18, bold=True)
    f.text(P(a - b + b / 2, b + (a - b) / 2 - 6), "B", size=18, bold=True)
    dim(f, P(0, a + 14), P(a, a + 14), "a", off=(0, 6))
    dim(f, P(a - b, -14), P(a, -14), "b", off=(0, -20))
    dim(f, P(-14, 0), P(-14, a), "a", off=(-12, -5))
    f.label(P(a / 2, -52), "a² − b²", size=15, bold=True)
    # right: piece B turned and moved under piece A: one rectangle (a + b) by (a − b)
    x0 = a + 90
    rect(f, x0, 0, a - b, a, fill=BLUE)
    rect(f, x0, a, a - b, b, fill=ORANGE)
    f.text(P(x0 + (a - b) / 2, a / 2 - 6), "A", size=18, bold=True)
    f.text(P(x0 + (a - b) / 2, a + b / 2 - 6), "B", size=18, bold=True)
    dim(f, P(x0 + a - b + 14, 0), P(x0 + a - b + 14, a + b), "a + b", off=(24, -5))
    dim(f, P(x0, -14), P(x0 + a - b, -14), "a − b", off=(0, -20))
    area_left = a * a - b * b
    area_right = (a + b) * (a - b)
    assert area_left == area_right
    f.label(P(x0 + (a - b) / 2, -52), "(a + b)(a − b)", size=15, bold=True)
    f.text(P(a + 45, a / 2 - 6), "→", size=26, bold=True, color=ASK)
    return f

# ---------------------------------------------------------------- 6.4 patterns
@fig
def circles_pattern():
    f = Fig("circles_pattern")
    u, x = 15, 0
    for k in range(1, 5):
        # draw as (k + 1)² − 1: a (k + 1) square missing its bottom-right dot
        pts = [(i, j) for i in range(k + 1) for j in range(k + 1) if not (i == k and j == k)]
        assert len(pts) == k * (k + 2) == k * k + 2 * k
        for i, j in pts:
            disc(f, P(x + j * u, -i * u), 6, INK)
        f.label(P(x + k * u / 2, 22), f"Step {k}", size=13, color=GIVEN)
        f.label(P(x + k * u / 2, -(k + 1) * u - 6), f"{len(pts)} circles", size=12, color=ANS)
        x += (k + 1) * u + 40
    return f

@fig
def circles_four_ways():
    f = Fig("circles_four_ways")
    u, k = 15, 3
    titles = ["(k + 1)² − 1", "k² + 2k", "k(k + 1) + k", "k(k + 2)"]
    for m in range(4):
        x0 = m * 120
        sq = [(i, j) for i in range(k + 1) for j in range(k + 1) if (i, j) != (k, k)]
        if m == 0:                             # a (k + 1) square with one circle missing
            cells = [(c, BLUE) for c in sq]
        elif m == 1:                           # a k × k square and 2k more
            cells = [((i, j), BLUE if i < k and j < k else ORANGE) for i, j in sq]
        elif m == 2:                           # k rows of (k + 1), and k more
            cells = [((i, j), BLUE if i < k else GREEN) for i, j in sq]
        else:                                  # the last row moved up to make k rows of (k + 2)
            cells = [((i, j), PINK) for i in range(k) for j in range(k + 2)]
        assert len(cells) == k * k + 2 * k == 15
        for (i, j), col in cells:
            disc(f, P(x0 + j * u, -i * u), 6, col)
        f.label(P(x0 + k * u / 2, 22), titles[m], size=13, bold=True)
    f.label(P(0, -(k + 1) * u - 10), "Step 3 read four ways; every way counts 15 = 3² + 2 × 3.", anchor="start", size=12, color=HELP)
    return f

@fig
def tile_frames():
    f = Fig("tile_frames")
    u, x = 14, 0
    for n in range(1, 4):
        side = n + 2
        cnt = 0
        for i in range(side):
            for j in range(side):
                if i in (0, side - 1) or j in (0, side - 1):
                    rect(f, x + j * u, -i * u, u, u, fill=PINK); cnt += 1
        assert cnt == (n + 2) ** 2 - n * n == 4 * n + 4
        f.label(P(x + side * u / 2, u + 20), f"Step {n}", size=13, color=GIVEN)
        f.label(P(x + side * u / 2, -side * u + u - 18), f"{cnt} tiles", size=12, color=ANS)
        x += side * u + 40
    return f

@fig
def pinwheel():
    f = Fig("pinwheel")
    m, n = 40, 150
    S = m + n
    rect(f, 0, 0, S, S, fill="#ffffff")
    rect(f, 0, 0, n, m, fill=PINK)            # bottom
    rect(f, n, 0, m, n, fill=PINK)            # right
    rect(f, m, n, n, m, fill=PINK)            # top
    rect(f, 0, m, m, n, fill=PINK)            # left
    rect(f, m, m, n - m, n - m, fill=YELLOW)
    hatch(f, m, m, n - m, n - m, gap=14)
    assert S * S - 4 * m * n == (n - m) ** 2
    dim(f, P(0, S + 14), P(m, S + 14), "m", off=(0, 6))
    dim(f, P(m, S + 14), P(S, S + 14), "n", off=(0, 6))
    dim(f, P(S + 14, 0), P(S + 14, n), "n", off=(12, -5))
    f.label(P(S / 2, -24), "Four equal m × n rectangles round a square", size=13)
    return f

@fig
def i_beam():
    f = Fig("i_beam")
    x, y = 160, 36                             # drawn lengths for x and y
    rect(f, 0, 0, x, y, fill=YELLOW)          # bottom bar x by y
    rect(f, 0, y + x, x, y, fill=YELLOW)      # top bar x by y
    hatch(f, 0, y, x, x, gap=12)
    rect(f, (x - y) / 2, y, y, x, fill=YELLOW)  # middle bar y by x
    f.seg(P(0, y), P(0, y + x), color=HELP, w=1.2, dash="4,4")
    f.seg(P(x, y), P(x, y + x), color=HELP, w=1.2, dash="4,4")
    total = x * (x + 2 * y); bars = 3 * x * y
    assert total - bars == x * x - x * y == 2 * x * (x - y) / 2
    dim(f, P(0, 2 * y + x + 14), P(x, 2 * y + x + 14), "x", off=(0, 6))
    dim(f, P(x + 14, y + x), P(x + 14, 2 * y + x), "y", off=(12, -5))
    dim(f, P(-14, y), P(-14, y + x), "x", off=(-12, -5))
    dim(f, P((x - y) / 2, y + x / 2), P((x + y) / 2, y + x / 2), "", off=(0, 0), color=ASK)
    f.label(P(x / 2, y + x / 2 + 10), "y", size=13, color=ASK)
    f.label(P(x / 2, -24), "three equal x × y rectangles", size=13)
    return f

@fig
def l_region():
    f = Fig("l_region")
    k = 22                                     # pixels per unit
    p, r, s = 6, 3.5, 9
    rect(f, 0, 0, s * k, r * k, fill=PINK)
    rect(f, (s - r) * k, r * k, r * k, (p - r) * k, fill=PINK)
    hatch(f, 0, r * k, (s - r) * k, (p - r) * k, gap=14, color=INK)
    f.seg(P(0, r * k), P(0, p * k), color=HELP, w=1.2, dash="4,4")
    f.seg(P(0, p * k), P((s - r) * k, p * k), color=HELP, w=1.2, dash="4,4")
    hatched = (s - r) * (p - r)
    assert hatched == p * s - p * r - s * r + r * r == 13.75
    dim(f, P(0, -14), P(s * k, -14), "s", off=(0, -20))
    dim(f, P(s * k + 14, 0), P(s * k + 14, p * k), "p", off=(12, -5))
    dim(f, P(-14, 0), P(-14, r * k), "r", off=(-12, -5))
    dim(f, P((s - r) * k, p * k + 14), P(s * k, p * k + 14), "r", off=(0, 6))
    return f

@fig
def park():
    f = Fig("park")
    g, w = 90, 22
    L, Bt = 2 * g + 4 * w, g + 2 * w
    rect(f, 0, 0, L, Bt, fill="#e6ee9c")
    rect(f, w, w, g, g, fill=GREEN)
    rect(f, w + g + 2 * w, w, g, g, fill=GREEN)
    f.text(P(w + g / 2, w + g / 2 - 6), "g²", size=16, bold=True)
    f.text(P(3 * w + 1.5 * g, w + g / 2 - 6), "g²", size=16, bold=True)
    dim(f, P(w, w + g + 12), P(w + g, w + g + 12), "g", off=(0, 4), size=12)
    dim(f, P(L + 12, w + g), P(L + 12, Bt), "w", off=(12, -6), size=12)
    dim(f, P(L + 12, 0), P(L + 12, w), "w", off=(12, -6), size=12)
    dim(f, P(0, Bt / 2 - 30), P(w, Bt / 2 - 30), "w", off=(0, -18), size=12)
    dim(f, P(w + g, Bt / 2 - 30), P(3 * w + g, Bt / 2 - 30), "2w", off=(0, -18), size=12)
    dim(f, P(3 * w + 2 * g, Bt / 2 - 30), P(L, Bt / 2 - 30), "w", off=(0, -18), size=12)
    tiled = L * Bt - 2 * g * g
    assert tiled == 8 * w * (w + g)
    f.label(P(L / 2, -22), "Path (light) all round each plot, w wide; 2w between the plots", size=12, color=HELP)
    return f

def stair(n):
    """Pattern (a): a block n rows by (n + 2) columns, with a tail of (n + 2) squares hanging below
    its left column and one of (n + 2) rising above its right column."""
    cells = {(r, c) for r in range(n) for c in range(n + 2)}
    cells |= {(-1 - t, 0) for t in range(n + 2)}
    cells |= {(n + t, n + 1) for t in range(n + 2)}
    return cells

def blue_block(n):
    """Pattern (b): an (n + 1) × (n + 1) square with n more squares in a row underneath."""
    cells = {(r, c) for r in range(n + 1) for c in range(n + 1)}
    cells |= {(-1, c) for c in range(n)}
    return cells

@fig
def unit_patterns():
    f = Fig("unit_patterns")
    u, x = 11, 0
    for n in range(1, 5):
        cells = stair(n)
        assert len(cells) == (n + 2) ** 2
        for r, c in cells:
            rect(f, x + c * u, r * u, u, u, fill=YELLOW)
        f.label(P(x + (n + 2) * u / 2, -6 * u - 22), f"Step {n}: {len(cells)}", size=12, color=GIVEN)
        x += (n + 2) * u + 26
    f.label(P(0, (2 * 4 + 2) * u + 16), "(a)", anchor="start", bold=True, size=14)
    y0 = -6 * u - 120
    x = 0
    for n in range(1, 5):
        cells = blue_block(n)
        assert len(cells) == (n + 1) ** 2 + n
        for r, c in cells:
            rect(f, x + c * (u + 3), y0 + r * (u + 3), u, u, fill=BLUE)
        f.label(P(x + (n + 1) * (u + 3) / 2, y0 - 2 * (u + 3) - 14), f"Step {n}: {len(cells)}", size=12, color=GIVEN)
        x += (n + 1) * (u + 3) + 40
    f.label(P(0, y0 + 5 * (u + 3) + 10), "(b)", anchor="start", bold=True, size=14)
    return f

# ---------------------------------------------------------------- Coin Conjoin
@fig
def coin_flip():
    f = Fig("coin_flip")
    u, h = 30, 30 * 0.866
    rows = 4
    # lattice coordinates: a point (q, r) sits at x = q + r / 2, y = r (in units of u and h)
    up = {(q, r) for r in range(rows) for q in range(rows - r)}          # 4 at the bottom, 1 at the top
    # the upside-down triangle: 4 on top, 1 at the bottom, placed to overlap the start as much as possible
    best = None
    for dq in range(-4, 5):
        for dr in range(-4, 5):
            dn = {(q + r + dq, -r + dr) for r in range(rows) for q in range(rows - r)}
            ov = len(up & dn)
            if best is None or ov > best[0]: best = (ov, dn)
    ov, down = best
    moves = len(up - down)
    assert ov == 7 and moves == 3 == 10 // 3
    def xy(q, r): return P((q + r / 2) * u, r * h)
    for x0, S, hot, title in [(0, up, up - down, "start"), (190, down, down - up, "after 3 moves")]:
        for q, r in S:
            c = xy(q, r)
            disc(f, P(x0 + c[0], c[1]), 12, ORANGE if (q, r) in hot else YELLOW)
        f.label(P(x0 + 1.5 * u, 4 * h + 4), title, size=13, bold=True)
    f.label(P(0, -2 * h), "Orange: the 3 corner coins that move. The 7 yellow coins stay put.", anchor="start", size=12, color=HELP)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
