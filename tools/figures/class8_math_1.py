"""Figures for class 8 maths Ch 1, A Square and a Cube. Every count written on a picture is
recomputed from what is drawn (lockers are toggled person by person, dots and tiles are counted,
cube layers are counted), so no label can disagree with its picture."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "1")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

GREEN, GREY, BLUE, ORANGE, PURPLE = "#a5d6a7", "#eceff1", "#90caf9", "#ffcc80", "#ce93d8"
LCOLS = ["#ef9a9a", "#90caf9", "#ffcc80", "#a5d6a7", "#ce93d8", "#80cbc4"]

def issq(n): return math.isqrt(n) ** 2 == n

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, 30)], fill=fill, color=color)

# ---------------------------------------------------------------- the locker puzzle
@fig
def lockers():
    f = Fig("lockers")
    state = [False] * 101                       # False = closed
    for person in range(1, 101):
        for k in range(person, 101, person):
            state[k] = not state[k]
    open_ = [k for k in range(1, 101) if state[k]]
    assert open_ == [n * n for n in range(1, 11)]
    w, h = 34, 30
    for k in range(1, 101):
        r, c = divmod(k - 1, 10)
        x, y = c * (w + 4), -r * (h + 4)
        box(f, x, y, w, h, fill=GREEN if state[k] else GREY, color=INK if state[k] else HELP)
        f.text(P(x + w / 2, y + h / 2 - 5), str(k), size=13, bold=state[k], color=ANS if state[k] else HELP)
    f.label(P(0, 44), "Green = open at the end (toggled an odd number of times)", anchor="start", size=13, color=ANS)
    return f

@fig
def factor_pairs():
    """Rectangles of tiles for each factor pair of 12 and of 16."""
    f = Fig("factor_pairs")
    u = 13
    def rect(x0, y0, a, b, fill):
        assert a * b in (12, 16)
        for i in range(a):
            for j in range(b):
                box(f, x0 + j * u, y0 - i * u, u, u, fill=fill)
        f.label(P(x0 + b * u / 2, y0 - a * u - 6), f"{a} × {b}", size=13)
    f.label(P(-10, 30), "12:", anchor="end", bold=True, size=15)
    x = 0
    for a, b in [(1, 12), (2, 6), (3, 4)]:
        rect(x, 30, a, b, BLUE); x += b * u + 28
    f.label(P(x, 22), "3 pairs → 6 factors (even)", anchor="start", size=13, color=GIVEN)
    f.label(P(-10, -60), "16:", anchor="end", bold=True, size=15)
    x = 0
    for a, b in [(1, 16), (2, 8), (4, 4)]:
        rect(x, -60, a, b, ORANGE if a != b else GREEN); x += b * u + 28
    assert [d for d in range(1, 17) if 16 % d == 0] == [1, 2, 4, 8, 16]
    f.label(P(x, -68), "4 × 4 pairs 4 with itself → 5 factors (odd)", anchor="start", size=13, color=ANS)
    return f

# ---------------------------------------------------------------- square numbers
@fig
def square_areas():
    f = Fig("square_areas")
    u, x = 16, 0
    for n in range(1, 6):
        for i in range(n):
            for j in range(n):
                box(f, x + j * u, i * u, u, u, fill=BLUE)
        tiles = n * n
        f.label(P(x + n * u / 2, -16), f"{n} × {n} = {tiles}", size=13)
        x += max(n * u, 80) + 26
    return f

@fig
def odd_ls():
    """A 5 × 5 square of dots built from inverted L-shapes 1, 3, 5, 7, 9."""
    f = Fig("odd_ls")
    n, g = 5, 26
    counts = [0] * n
    for i in range(n):            # i = row from the top-left corner
        for j in range(n):
            k = max(i, j)          # which L the dot belongs to
            counts[k] += 1
            disc(f, P(j * g, -i * g), 8, LCOLS[k])
    assert counts == [1, 3, 5, 7, 9] and sum(counts) == 25
    for k in range(n):                       # legend: colour of each L and its number of dots
        y = -k * 30 - 4
        disc(f, P(n * g + 30, y), 8, LCOLS[k])
        f.label(P(n * g + 46, y - 5), f"L-shape {k+1}: {counts[k]} dot{'s' if counts[k] > 1 else ''}", anchor="start", size=13)
    f.label(P(2 * g, -n * g - 8), "1 + 3 + 5 + 7 + 9 = 25 = 5 × 5", size=14, bold=True, color=ANS)
    return f

def tri_sq(f, n, x0):
    """n × n dots cut by a staircase into triangle T(n) (below/on the diagonal) and T(n-1)."""
    g = 22
    a = b = 0
    for i in range(n):
        for j in range(n):
            lower = j <= i
            a += lower; b += not lower
            disc(f, P(x0 + j * g, -i * g), 7, ORANGE if lower else BLUE)
    tn, tm = n * (n + 1) // 2, (n - 1) * n // 2
    assert (a, b) == (tn, tm) and a + b == n * n
    # staircase cut line
    pts = []
    for i in range(n):
        pts += [P(x0 + (i + 0.5) * g, -(i - 0.5) * g), P(x0 + (i + 0.5) * g, -(i + 0.5) * g)]
    for p, q in zip(pts, pts[1:]):
        f.seg(p, q, color=ASK, w=2)
    f.label(P(x0 + (n - 1) * g / 2, -n * g - 4), f"{tm} + {tn} = {n * n} = {n}²", size=13, bold=True)
    return x0 + n * g + 34

@fig
def tri_square():
    f = Fig("tri_square")
    x = 0
    for n in (2, 3, 4):
        x = tri_sq(f, n, x)
    return f

@fig
def tri_square_next():
    f = Fig("tri_square_next")
    tri_sq(f, 5, 0)
    return f

# ---------------------------------------------------------------- square roots
@fig
def root_side():
    f = Fig("root_side")
    u, n = 14, 7
    for i in range(n):
        for j in range(n):
            box(f, j * u, i * u, u, u, fill=GREEN)
    assert n * n == 49
    f.label(P(n * u / 2, -16), "side = 7 cm", size=14, bold=True, color=ANS)
    f.label(P(n * u + 12, n * u / 2 - 5), "area = 49 sq cm", anchor="start", size=14, color=GIVEN)
    return f

def root_line(f, lo, hi, marks, y=0, k=46):
    """Number line of roots from lo to hi; squares written underneath each whole number."""
    f.seg(P(0, y), P((hi - lo) * k, y))
    for r in range(lo, hi + 1):
        x = (r - lo) * k
        f.seg(P(x, y - 6), P(x, y + 6))
        f.label(P(x, y + 12), str(r), size=13, bold=True)
        f.label(P(x, y - 24), str(r * r), size=12, color=HELP)
    for val, s, col in marks:
        x = (val - lo) * k
        f.dot(P(x, y), color=col)
        f.label(P(x, y + 34), s, size=13, bold=True, color=col)

@fig
def estimate_1936():
    f = Fig("estimate_1936")
    assert 40 ** 2 < 1936 < 50 ** 2 and 45 ** 2 == 2025 > 1936 and 44 ** 2 == 1936
    f.seg(P(0, 0), P(10 * 40, 0))
    for r in range(40, 51):
        x = (r - 40) * 40
        big = r in (40, 44, 45, 50)
        f.seg(P(x, -6), P(x, 6), w=2.2 if big else 1.4)
        f.label(P(x, 12), str(r), size=13, bold=big, color=INK if big else HELP)
        if r in (40, 45, 50):
            f.label(P(x, -24), f"{r}² = {r*r}", size=12, color=GIVEN)
    f.dot(P(4 * 40, 0), color=ANS)
    f.label(P(4 * 40, 34), "44² = 1936 ✓", size=13, bold=True, color=ANS)
    f.label(P(6 * 40, 34), "46: too big", size=12, color=ASK)
    f.label(P(0, -46), "Root ends in 4 or 6 (1936 ends in 6), and it is below 45", anchor="start", size=12, color=HELP)
    return f

@fig
def estimate_250():
    f = Fig("estimate_250")
    v = 15 + (250 - 225) / (256 - 225)         # where 250 sits between 225 and 256
    assert 15 ** 2 < 250 < 16 ** 2 and abs(v - math.sqrt(250)) < 0.01
    root_line(f, 13, 18, [(v, "√250 ≈ 15.8", ANS)])
    f.label(P(0, -46), "squares:", anchor="start", size=11, color=HELP)
    return f

@fig
def handkerchief():
    f = Fig("handkerchief")
    k = 16
    s = math.sqrt(125)
    box(f, 0, 0, s * k, s * k, fill="#ffb74d")
    box(f, 0, 0, 11 * k, 11 * k, fill=GREEN)
    f.seg(P(0, 12 * k), P(12 * k, 12 * k), color=ASK, dash="6 4")
    f.seg(P(12 * k, 0), P(12 * k, 12 * k), color=ASK, dash="6 4")
    assert 11 ** 2 <= 125 < 12 ** 2 < 15 ** 2
    f.label(P(5.5 * k, 5.5 * k - 5), "11 cm × 11 cm", size=14, bold=True, color=ANS)
    f.label(P(5.5 * k, 4.2 * k - 5), "= 121 sq cm", size=13, color=ANS)
    f.label(P(s * k / 2, -18), "cloth: 125 sq cm (side ≈ 11.2 cm)", size=13, color=INK)
    f.label(P(12 * k + 8, 12 * k - 4), "12 cm needs 144 sq cm: too big", anchor="start", size=12, color=ASK)
    return f

@fig
def tiny_squares():
    """A 9 × 9 pattern of tiles; every tile is a 5 × 5 grid of tiny squares, alternately upright
    and turned (a diamond)."""
    f = Fig("tiny_squares")
    T, n, cell = 40, 5, 6.0
    side = n * cell
    total = 0
    box(f, -6, -6, 9 * T + 2, 9 * T + 2, fill="#3d9a62", color="#3d9a62")
    for r in range(9):
        for c in range(9):
            cx, cy = c * T + T / 2 - 4, (8 - r) * T + T / 2 - 4
            turned = (r + c) % 2 == 0
            ang = 45 if turned else 0
            sz = side * (0.92 if turned else 0.8)
            st = sz / n
            def pt(a, b):  # a, b in [0, sz] measured from the tile's corner, rotated about centre
                x, y = a - sz / 2, b - sz / 2
                ca, sa = math.cos(d2r(ang)), math.sin(d2r(ang))
                return P(cx + x * ca - y * sa, cy + x * sa + y * ca)
            f.poly([pt(0, 0), pt(sz, 0), pt(sz, sz), pt(0, sz)], fill="#ffffff", color="#ffffff")
            for i in range(1, n):
                f.seg(pt(i * st, 0), pt(i * st, sz), color="#3d9a62", w=1.4)
                f.seg(pt(0, i * st), pt(sz, i * st), color="#3d9a62", w=1.4)
            total += n * n
    assert total == 2025 == 45 * 45 == 3 ** 4 * 5 ** 2
    return f

# ---------------------------------------------------------------- cubes
def cube(f, x0, n, u=20, d=(0.5, 0.38), fill=("#bbdefb", "#90caf9", "#64b5f6")):
    """Draw an n × n × n cube of unit cubes (front, top and right faces, with grid lines)."""
    dx, dy = d[0] * u, d[1] * u
    def F(i, j): return P(x0 + i * u, j * u)                      # front face point
    def D(p, k): return P(p[0] + k * dx, p[1] + k * dy)           # pushed k units back
    front = [F(0, 0), F(n, 0), F(n, n), F(0, n)]
    top = [F(0, n), F(n, n), D(F(n, n), n), D(F(0, n), n)]
    right = [F(n, 0), D(F(n, 0), n), D(F(n, n), n), F(n, n)]
    f.poly(front, fill=fill[0]); f.poly(top, fill=fill[1]); f.poly(right, fill=fill[2])
    for i in range(1, n):
        f.seg(F(i, 0), F(i, n), w=1.2); f.seg(F(0, i), F(n, i), w=1.2)              # front grid
        f.seg(F(i, n), D(F(i, n), n), w=1.2); f.seg(D(F(0, n), i), D(F(n, n), i), w=1.2)  # top grid
        f.seg(D(F(n, 0), i), D(F(n, n), i), w=1.2); f.seg(F(n, i), D(F(n, i), n), w=1.2)  # right grid
    f.label(P(x0 + n * u / 2, -18), f"{n} × {n} × {n} = {n**3}", size=13, bold=True)
    return x0 + max(n * u + n * dx, 110) + 30

@fig
def cubes_123():
    f = Fig("cubes_123")
    x = 0
    for n in (1, 2, 3):
        x = cube(f, x, n)
    return f

@fig
def cube_layers_4():
    f = Fig("cube_layers_4")
    x, total = 0, 0
    for layer in range(4):
        u = 16
        for i in range(4):
            for j in range(4):
                box(f, x + j * u, i * u, u, u, fill=LCOLS[layer])
                total += 1
        f.label(P(x + 2 * u, -16), f"layer {layer+1}: 16", size=12)
        x += 4 * u + 24
    assert total == 4 * 4 * 4 == 64
    f.label(P(x, 2 * 16 - 5), "4 layers × 16 = 64", anchor="start", size=14, bold=True, color=ANS)
    return f

# ---------------------------------------------------------------- square pairs puzzle
ROW17 = [16, 9, 7, 2, 14, 11, 5, 4, 12, 13, 3, 6, 10, 15, 1, 8, 17]
CIRCLE32 = [1, 8, 28, 21, 4, 32, 17, 19, 30, 6, 3, 13, 12, 24, 25, 11, 5, 31, 18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15]

def all_rows(N, cycle=False):
    adj = {i: [j for j in range(1, N + 1) if j != i and issq(i + j)] for i in range(1, N + 1)}
    found = []
    def go(p, used):
        if len(p) == N:
            if not cycle or issq(p[-1] + p[0]): found.append(p[:])
            return
        for j in adj[p[-1]]:
            if j not in used:
                used.add(j); p.append(j); go(p, used); p.pop(); used.discard(j)
    for s in ([1] if cycle else range(1, N + 1)):
        go([s], {s})
    return found

@fig
def square_pairs_row():
    f = Fig("square_pairs_row")
    rows = all_rows(17)
    assert sorted(rows) == sorted([ROW17, ROW17[::-1]])         # only these two orders
    g = 40
    for i, v in enumerate(ROW17):
        disc(f, P(i * g, 0), 14, GREEN if v in (16, 17) else "#ffffff")
        f.text(P(i * g, -5), str(v), size=13, bold=True)
        if i:
            s = ROW17[i - 1] + v; assert issq(s)
            f.label(P(i * g - g / 2, 24), str(s), size=11, color=GIVEN)
    f.label(P(0, -34), "16 and 17 each have only one partner (9 and 8), so they must be at the ends.", anchor="start", size=12, color=ANS)
    return f

@fig
def square_pairs_circle():
    f = Fig("square_pairs_circle")
    found = all_rows(32, cycle=True)
    assert len(found) == 2 and CIRCLE32 in found               # one circle, read either way round
    R, N = 170, len(CIRCLE32)
    pts = [along(P(0, 0), 90 - 360 * i / N, R) for i in range(N)]
    for i in range(N):
        a, b = CIRCLE32[i], CIRCLE32[(i + 1) % N]
        assert issq(a + b)
        f.seg(pts[i], pts[(i + 1) % N], color=HELP, w=1.6)
        m = mul(add(pts[i], pts[(i + 1) % N]), 0.5)
        f.label(along(P(0, 0), dirto(P(0, 0), m), R - 22), str(a + b), size=10, color=GIVEN)
    for i, v in enumerate(CIRCLE32):
        disc(f, pts[i], 13, "#ffffff")
        f.text(P(pts[i][0], pts[i][1] - 5), str(v), size=12, bold=True)
    f.label(P(0, 8), "blue numbers:", size=12, color=GIVEN)
    f.label(P(0, -10), "neighbour sums", size=12, color=GIVEN)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
