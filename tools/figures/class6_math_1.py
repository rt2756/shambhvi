"""Figures for class 6 maths Ch 1, Patterns in Mathematics. Every picture counts what it draws:
dot pictures count their dots (and each coloured part), shape sequences count their sides, lines,
little squares/triangles and Koch segments, so a number written under a picture can never disagree
with it."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class6", "math", "1")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, PURPLE, TEAL = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0", "#ce93d8", "#80cbc4"
LCOLS = ["#ef9a9a", "#90caf9", "#ffcc80", "#a5d6a7", "#ce93d8", "#80cbc4", "#fff59d", "#f8bbd0", "#bcaaa4", "#b0bec5"]
C30 = math.cos(math.radians(30))

def disc(f, c, r, fill, color=INK):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, 30)], fill=fill, color=color)

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def tri(n): return n * (n + 1) // 2
def hexn(n): return 3 * n * (n - 1) + 1

# ---------------------------------------------------------------- dot shapes (return dot centres)
def tri_dots(x0, n, g=18):
    """Triangle with rows 1, 2, ..., n, apex on top; bottom row at y = 0."""
    pts = []
    for r in range(n):                       # r = 0 is the top row with 1 dot
        y = (n - 1 - r) * g * C30 * 1.12
        for k in range(r + 1):
            pts.append(P(x0 + (k - r / 2) * g, y))
    return pts

def sq_dots(x0, n, g=18):
    return [P(x0 + j * g, i * g) for i in range(n) for j in range(n)]

def put(f, pts, fill, r=5.5):
    for p in pts: disc(f, p, r, fill)

# ---------------------------------------------------------------- 1.3 pictures of the sequences
@fig
def seq_lines():
    """All 1's, counting numbers, odd and even numbers as dot pictures."""
    f = Fig("seq_lines")
    g, row_h = 16, 92
    rows = [("All 1's", lambda n: [P(0, 0)], [1] * 5),
            ("Counting numbers", lambda n: [P(0, i * g) for i in range(n)], [1, 2, 3, 4, 5]),
            ("Odd numbers", lambda n: [P(j * g, 0) for j in range((n + 1) // 2)] + [P(j * g, g) for j in range(n // 2)], [1, 3, 5, 7, 9]),
            ("Even numbers", lambda n: [P(j * g, 0) for j in range(n // 2)] + [P(j * g, g) for j in range(n // 2)], [2, 4, 6, 8, 10])]
    for ri, (name, shape, nums) in enumerate(rows):
        y0 = -ri * row_h
        f.label(P(-20, y0 + 30), name, anchor="end", bold=True, size=13)
        for k, n in enumerate(nums):
            x0 = k * 100
            pts = [P(x0 + p[0], y0 + p[1]) for p in shape(n)]
            assert len(pts) == n, (name, n)
            put(f, pts, [GREY, BLUE, ORANGE, GREEN][ri])
            f.label(P(x0 + 18, y0 - 22), str(n), size=13, bold=True)
    f.label(P(-150, -4 * row_h + 40), "Odd = pairs plus one dot left over; even = pairs with nothing left over.", anchor="start", size=12, color=HELP)
    return f

@fig
def triangular():
    f = Fig("triangular")
    x = 0
    for n in range(1, 6):
        pts = tri_dots(x, n); assert len(pts) == tri(n)
        put(f, pts, ORANGE)
        f.label(P(x, -24), str(len(pts)), size=14, bold=True)
        x += n * 18 + 46
    return f

@fig
def squares():
    f = Fig("squares")
    x = 0
    for n in range(1, 6):
        pts = sq_dots(x, n); assert len(pts) == n * n
        put(f, pts, BLUE)
        f.label(P(x + (n - 1) * 9, -24), f"{n} × {n} = {n * n}", size=13, bold=True)
        x += n * 18 + 50
    return f

def iso(x, y, z, u):
    return P((x + y) * C30 * u, (z + (y - x) / 2) * u)

def draw_cubes(f, cubes, x0=0, u=14, cols=("#fff9c4", "#ffe082", "#ffb300")):
    """Isometric unit cubes (painter's order; only faces that can be seen are drawn)."""
    S = set(cubes)
    def Q(x, y, z): q = iso(x, y, z, u); return P(q[0] + x0, q[1])
    for (x, y, z) in sorted(S, key=lambda c: (c[0] - c[1] + c[2], c[2])):
        if (x, y, z + 1) not in S:
            f.poly([Q(x, y, z + 1), Q(x + 1, y, z + 1), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)], fill=cols[0])
        if (x, y - 1, z) not in S:
            f.poly([Q(x, y, z), Q(x + 1, y, z), Q(x + 1, y, z + 1), Q(x, y, z + 1)], fill=cols[1])
        if (x + 1, y, z) not in S:
            f.poly([Q(x + 1, y, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x + 1, y, z + 1)], fill=cols[2])

def block(n): return {(x, y, z) for x in range(n) for y in range(n) for z in range(n)}

def seen(n):
    """Little cubes of an n-cube that show a face when looked at from the top-front-right corner."""
    return {c for c in block(n) if c[2] == n - 1 or c[1] == 0 or c[0] == n - 1}

@fig
def cubes():
    f = Fig("cubes")
    x = 0
    for n in range(1, 6):
        draw_cubes(f, block(n), x0=x, u=12)
        assert len(block(n)) == n ** 3
        f.label(P(x + n * 12 * C30, -n * 6 - 22), f"{n}×{n}×{n} = {n ** 3}", size=12, bold=True)
        x += 2 * n * 12 * C30 + 40
    return f

@fig
def next_pictures():
    """The picture after the last one shown for each sequence."""
    f = Fig("next_pictures")
    g = 16
    # all 1's -> 1, counting -> 6, odd -> 11, even -> 12
    put(f, [P(0, 0)], GREY); f.label(P(0, -24), "1", size=13, bold=True); f.label(P(0, 120), "All 1's", size=12, color=HELP)
    pts = [P(70, i * g) for i in range(6)]; assert len(pts) == 6
    put(f, pts, BLUE); f.label(P(70, -24), "6", size=13, bold=True); f.label(P(70, 120), "Counting", size=12, color=HELP)
    pts = [P(130 + j * g, 0) for j in range(6)] + [P(130 + j * g, g) for j in range(5)]; assert len(pts) == 11
    put(f, pts, ORANGE); f.label(P(170, -24), "11", size=13, bold=True); f.label(P(170, 120), "Odd", size=12, color=HELP)
    pts = [P(250 + j * g, 0) for j in range(6)] + [P(250 + j * g, g) for j in range(6)]; assert len(pts) == 12
    put(f, pts, GREEN); f.label(P(290, -24), "12", size=13, bold=True); f.label(P(290, 120), "Even", size=12, color=HELP)
    # triangular 21, square 36
    pts = tri_dots(400, 6, g=16); assert len(pts) == 21
    put(f, pts, ORANGE, r=5); f.label(P(400, -24), "21", size=13, bold=True); f.label(P(400, 120), "Triangular", size=12, color=HELP)
    pts = sq_dots(470, 6, g=16); assert len(pts) == 36
    put(f, pts, BLUE, r=5); f.label(P(510, -24), "6 × 6 = 36", size=13, bold=True); f.label(P(510, 120), "Square", size=12, color=HELP)
    draw_cubes(f, block(6), x0=600, u=9)
    f.label(P(600 + 6 * 9 * C30, -24 - 27), "6 × 6 × 6 = 216", size=13, bold=True); f.label(P(655, 120), "Cube", size=12, color=HELP)
    return f

@fig
def both_36():
    f = Fig("both_36")
    pts = tri_dots(0, 8, g=17); assert len(pts) == 36 == tri(8)
    put(f, pts, ORANGE)
    f.label(P(0, -24), "1 + 2 + … + 8 = 36", size=13, bold=True)
    pts = sq_dots(110, 6, g=17); assert len(pts) == 36
    put(f, pts, BLUE)
    f.label(P(110 + 42, -24), "6 × 6 = 36", size=13, bold=True)
    return f

def hex_points(n):
    """Hexagonal number n: all points of a triangular lattice within n - 1 steps of the centre."""
    out = []
    R = n - 1
    for q in range(-R, R + 1):
        for r in range(-R, R + 1):
            if max(abs(q), abs(r), abs(q + r)) <= R: out.append((q, r))
    return out

def axial(q, r, g):
    return P(g * (q + r / 2), g * r * C30)

@fig
def hexagonal():
    f = Fig("hexagonal")
    x = 0
    for n in range(1, 5):
        pts = hex_points(n); assert len(pts) == hexn(n)
        put(f, [add(P(x, 0), axial(q, r, 17)) for q, r in pts], PURPLE)
        f.label(P(x, -(n - 1) * 17 * C30 - 26), str(len(pts)), size=14, bold=True)
        x += (2 * n - 1) * 17 / 2 + (2 * n + 1) * 17 / 2 + 20
    return f

def sector(q, r):
    """Which of the six 60° wedges (0-5) a non-centre lattice point is in (each wedge holds one edge)."""
    p = axial(q, r, 1)
    a = (math.degrees(math.atan2(p[1], p[0])) + 360 - 1e-9) % 360
    return int(a // 60)

@fig
def hexagonal_next():
    """Hexagonal number 61, split into one centre dot and six triangles of 10 dots each."""
    f = Fig("hexagonal_next")
    pts = hex_points(5); assert len(pts) == 61
    count = [0] * 6
    for q, r in pts:
        if (q, r) == (0, 0):
            disc(f, axial(0, 0, 20), 6, "#ffffff"); continue
        s = sector(q, r); count[s] += 1
        disc(f, axial(q, r, 20), 6, LCOLS[s])
    assert count == [tri(4)] * 6, count
    f.label(P(0, -4 * 20 * C30 - 28), "1 + 6 × 10 = 61", size=14, bold=True)
    return f

@fig
def hex_six_triangles():
    """Hexagonal numbers 7, 19, 37: the centre dot plus six equal triangles (1, 3, 6 dots each)."""
    f = Fig("hex_six_triangles")
    x = 0
    for n in (2, 3, 4):
        pts = hex_points(n)
        count = [0] * 6
        for q, r in pts:
            c = add(P(x, 0), axial(q, r, 18))
            if (q, r) == (0, 0): disc(f, c, 5.5, "#ffffff"); continue
            s = sector(q, r); count[s] += 1; disc(f, c, 5.5, LCOLS[s])
        assert count == [tri(n - 1)] * 6 and len(pts) == 6 * tri(n - 1) + 1
        f.label(P(x, -(n - 1) * 18 * C30 - 26), f"6 × {tri(n - 1)} + 1 = {len(pts)}", size=13, bold=True)
        x += (2 * n - 1) * 9 + (2 * n + 3) * 9 + 50
    return f

@fig
def powers2():
    """Each picture is two copies of the one before."""
    f = Fig("powers2")
    g, x = 15, 0
    # rows x cols, and whether the new copy sits beside (cols split) or on top (rows split)
    shapes = [(1, 1, None), (1, 2, "cols"), (2, 2, "rows"), (2, 4, "cols"), (4, 4, "rows")]
    for k, (rows, cols, split) in enumerate(shapes):
        n = rows * cols; assert n == 2 ** k
        if k: assert (rows, cols) == ((shapes[k-1][0], 2 * shapes[k-1][1]) if split == "cols" else (2 * shapes[k-1][0], shapes[k-1][1]))
        for i in range(rows):
            for j in range(cols):
                new = (j >= cols // 2) if split == "cols" else (i >= rows // 2) if split == "rows" else False
                disc(f, P(x + j * g, i * g), 5, GREEN if new else BLUE)
        f.label(P(x + (cols - 1) * g / 2, -22), str(n), size=14, bold=True)
        x += cols * g + 40
    f.label(P(0, -46), "Each picture = two copies of the one before (blue copy + green copy).", anchor="start", size=12, color=HELP)
    return f

@fig
def powers3():
    f = Fig("powers3")
    g, x = 13, 0
    def grid(x0, y0, rows, cols, fill):
        for i in range(rows):
            for j in range(cols): disc(f, P(x0 + j * g, y0 + i * g), 4.5, fill)
        return rows * cols
    n = grid(0, 0, 1, 1, BLUE); assert n == 1
    f.label(P(0, -22), "1", size=14, bold=True)
    n = sum(grid(40 + c * g, 0, 1, 1, [BLUE, GREEN, ORANGE][c]) for c in range(3)); assert n == 3
    f.label(P(40 + g, -22), "3", size=14, bold=True)
    n = sum(grid(110, i * g, 1, 3, [BLUE, GREEN, ORANGE][i]) for i in range(3)); assert n == 9
    f.label(P(110 + g, -22), "9", size=14, bold=True)
    n = sum(grid(180 + c * (3 * g + 10), 0, 3, 3, [BLUE, GREEN, ORANGE][c]) for c in range(3)); assert n == 27
    f.label(P(180 + 4 * g + 10, -22), "27", size=14, bold=True)
    f.label(P(0, -46), "Each picture = three copies of the one before.", anchor="start", size=12, color=HELP)
    return f

# ---------------------------------------------------------------- 1.4 relations
def odd_L(f, n, x0=0, g=20, r=7):
    counts = []
    for layer in range(1, n + 1):
        cells = [(i, j) for i in range(n) for j in range(n) if max(i, j) == layer - 1]
        counts.append(len(cells))
        for i, j in cells:
            disc(f, P(x0 + j * g, i * g), r, LCOLS[(layer - 1) % len(LCOLS)])
    assert counts == [2 * k - 1 for k in range(1, n + 1)] and sum(counts) == n * n
    return counts

@fig
def odd_squares():
    f = Fig("odd_squares")
    counts = odd_L(f, 6)
    f.label(P(50, -26), " + ".join(map(str, counts)) + " = 36", size=14, bold=True)
    for k, c in enumerate(counts):
        f.label(P(6 * 20 + 14, k * 20 - 5), f"L {k + 1}: {c} dot" + ("s" if c > 1 else ""), anchor="start", size=12, color=HELP)
    return f

@fig
def odd_squares_10():
    f = Fig("odd_squares_10")
    counts = odd_L(f, 10, g=15, r=5.2)
    assert sum(counts) == 100
    f.label(P(68, -24), "1 + 3 + 5 + … + 19 = 10 × 10 = 100", size=14, bold=True)
    return f

@fig
def up_down():
    """A square of dots tipped onto its corner: its rows hold 1, 2, ..., n, ..., 2, 1 dots."""
    f = Fig("up_down")
    x = 0
    for n in (3, 4, 5):
        rows = {}
        for i in range(n):
            for j in range(n):
                y = i + j; rows[y] = rows.get(y, 0) + 1
                disc(f, P(x + (i - j) * 12, -(i + j) * 12), 5.5, LCOLS[y % len(LCOLS)])
        cnt = [rows[y] for y in sorted(rows)]
        assert cnt == list(range(1, n + 1)) + list(range(n - 1, 0, -1)) and sum(cnt) == n * n
        f.label(P(x, -(2 * n - 2) * 12 - 26), " + ".join(map(str, cnt)), size=12, bold=True)
        f.label(P(x, -(2 * n - 2) * 12 - 44), f"= {n} × {n} = {n * n}", size=12, bold=True)
        x += 2 * n * 12 + 40
    return f

@fig
def staircase():
    """Adding counting numbers: a staircase of rows 1, 2, 3, 4, 5."""
    f = Fig("staircase")
    x = 0
    for n in (1, 2, 3, 4, 5):
        tot = 0
        for r in range(n):
            for k in range(r + 1):
                disc(f, P(x + k * 15, -r * 15), 5, LCOLS[r]); tot += 1
        assert tot == tri(n)
        f.label(P(x + (n - 1) * 7.5, -n * 15 - 14), str(tot), size=14, bold=True)
        x += n * 15 + 30
    return f

@fig
def tri_pairs():
    """A square of dots cut along a staircase: two neighbouring triangular numbers."""
    f = Fig("tri_pairs")
    g, x0 = 20, 0
    for n in (2, 3, 4, 5):
        a = b = 0
        for i in range(n):
            for j in range(n):
                lower = j <= i
                a += lower; b += not lower
                disc(f, P(x0 + j * g, -i * g), 6.5, ORANGE if lower else BLUE)
        assert (a, b) == (tri(n), tri(n - 1))
        pts = []
        for i in range(n):
            pts += [P(x0 + (i + 0.5) * g, -(i - 0.5) * g), P(x0 + (i + 0.5) * g, -(i + 0.5) * g)]
        for p, q in zip(pts[:-1], pts[1:-1]):
            f.seg(p, q, color=ASK, w=2)
        f.label(P(x0 + (n - 1) * g / 2, -n * g - 6), f"{b} + {a} = {n * n}", size=13, bold=True)
        x0 += n * g + 34
    return f

@fig
def powers2_sum():
    """1 + 1 + 2 + 4 + 8 = 16: the extra 1 (grey) makes each part double into the next."""
    f = Fig("powers2_sum")
    u = 26
    # cells of a 4 x 4 square, numbered so that each part is a rectangle
    parts = [("extra 1", GREY, [(0, 0)]), ("1", BLUE, [(1, 0)]), ("2", GREEN, [(0, 1), (1, 1)]),
             ("4", ORANGE, [(i, j) for i in range(2) for j in range(2, 4)]),
             ("8", PURPLE, [(i, j) for i in range(2, 4) for j in range(4)])]
    seen_cells = set()
    for name, col, cells in parts:
        xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
        x0, x1, y0, y1 = min(xs), max(xs) + 1, min(ys), max(ys) + 1
        assert (x1 - x0) * (y1 - y0) == len(cells)          # each part is one rectangle
        for c in cells:
            assert c not in seen_cells; seen_cells.add(c)
        box(f, x0 * u, y0 * u, (x1 - x0) * u, (y1 - y0) * u, fill=col)
        f.text(P((x0 + x1) / 2 * u, (y0 + y1) / 2 * u - 5), name if name != "extra 1" else "+1", size=13, bold=True)
    assert seen_cells == {(i, j) for i in range(4) for j in range(4)}
    assert 1 + 1 + 2 + 4 + 8 == 16
    f.label(P(4 * u + 20, 3 * u), "1 + 2 + 4 + 8 = 15", anchor="start", size=14, bold=True)
    f.label(P(4 * u + 20, 2 * u), "add the extra 1:", anchor="start", size=13, color=HELP)
    f.label(P(4 * u + 20, 1.2 * u), "1 + 1 = 2, 2 + 2 = 4,", anchor="start", size=13)
    f.label(P(4 * u + 20, 0.4 * u), "4 + 4 = 8, 8 + 8 = 16", anchor="start", size=13)
    return f

@fig
def cube_shells():
    """An n-cube seen from a corner shows a hexagon of 3n² − 3n + 1 little cubes (its outer shell)."""
    f = Fig("cube_shells")
    x, u = 0, 15
    for n in range(1, 5):
        sh = seen(n)
        assert len(sh) == hexn(n) == n ** 3 - (n - 1) ** 3
        draw_cubes(f, block(n), x0=x, u=u)
        f.label(P(x + n * u * C30, -n * u / 2 - 22), f"{n ** 3} = {(n - 1) ** 3} + {len(sh)}", size=12, bold=True)
        x += 2 * n * u * C30 + 44
    f.label(P(0, -100), "From the corner you see only the outer shell: 1, 7, 19, 37 little cubes, a hexagon each time.", anchor="start", size=12, color=HELP)
    return f

@fig
def even_rects():
    """Adding even numbers: 2, 2 + 4, 2 + 4 + 6, ... make rectangles n × (n + 1)."""
    f = Fig("even_rects")
    g, x = 16, 0
    for n in range(1, 5):
        cnt, layers = 0, []
        for layer in range(1, n + 1):          # layer k: an L of 2k dots round the (k-1) × k rectangle
            cells = [(i, j) for i in range(n) for j in range(n + 1) if max(i, j - 1) == layer - 1]
            layers.append(len(cells)); cnt += len(cells)
            for i, j in cells: disc(f, P(x + j * g, i * g), 5.5, LCOLS[layer - 1])
        assert layers == [2 * k for k in range(1, n + 1)] and cnt == n * (n + 1)
        f.label(P(x + n * g / 2, -22), " + ".join(map(str, layers)), size=12, bold=True)
        f.label(P(x + n * g / 2, -40), f"= {n} × {n + 1} = {cnt}", size=12, bold=True)
        x += (n + 1) * g + 46
    return f

# ---------------------------------------------------------------- 1.5 shape sequences
@fig
def polygons():
    f = Fig("polygons")
    names = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon"}
    for k, n in enumerate(range(3, 11)):
        c = P((k % 4) * 120, -(k // 4) * 130)
        ps = [along(c, -90 + 180 / n + 360 * i / n, 40) for i in range(n)]
        sides = list(zip(ps, ps[1:] + ps[:1]))
        L = [dist(p, q) for p, q in sides]
        assert len(sides) == n == len(ps) and max(L) - min(L) < 1e-9     # n equal sides, n corners
        f.poly(ps, fill=LCOLS[k])
        for p in ps: f.dot(p)
        f.label(P(c[0], c[1] - 60), f"{names[n]}: {n}", size=12, bold=True)
    return f

def complete(f, c, n, R=34, hi=None):
    ps = [along(c, 90 + 360 * i / n, R) for i in range(n)] if n > 2 else [add(c, (-R, 0)), add(c, (R, 0))]
    lines = 0
    for i in range(n):
        for j in range(i + 1, n):
            col = ASK if hi is not None and (i == hi or j == hi) else INK
            f.seg(ps[i], ps[j], color=col, w=2.4 if col == ASK else 1.6); lines += 1
    for p in ps: disc(f, p, 4.5, "#ffffff")
    assert lines == n * (n - 1) // 2
    return lines, ps

@fig
def complete_graphs():
    f = Fig("complete_graphs")
    for k, n in enumerate(range(2, 7)):
        c = P(k * 105, 0)
        lines, _ = complete(f, c, n)
        f.label(P(c[0], -52), f"K{n}: {lines} line" + ("s" if lines > 1 else ""), size=12, bold=True)
    return f

@fig
def complete_new_dot():
    """K5 drawn so the newest (5th) dot's 4 lines stand out."""
    f = Fig("complete_new_dot")
    lines, ps = complete(f, P(0, 0), 5, R=50, hi=4)
    assert lines == 10
    f.label(P(70, 20), "the 5th dot joins the 4", anchor="start", size=12, color=ASK)
    f.label(P(70, 4), "dots already there: 4 new lines", anchor="start", size=12, color=ASK)
    f.label(P(70, -20), "1 + 2 + 3 + 4 = 10 lines", anchor="start", size=13, bold=True)
    return f

@fig
def stacked_squares():
    f = Fig("stacked_squares")
    x, u = 0, 13
    for n in range(1, 6):
        cnt = 0
        for i in range(n):
            for j in range(n):
                box(f, x + j * u, i * u, u, u, fill=BLUE); cnt += 1
        assert cnt == n * n
        f.label(P(x + n * u / 2, -20), str(cnt), size=14, bold=True)
        x += n * u + 30
    return f

def stacked_tri(f, x0, n, u=16, colour_rows=True):
    """Triangle of side n made of n² little triangles; returns the count in each row (top first)."""
    h = u * C30
    rows = []
    for r in range(n):                      # r = 0 is the top row
        y_top = (n - r) * h; y_bot = y_top - h
        cnt = 0
        for k in range(r + 1):              # upward triangles
            xl = x0 + (k - r / 2) * u - u / 2
            f.poly([P(xl, y_bot), P(xl + u, y_bot), P(xl + u / 2, y_top)], fill=LCOLS[r] if colour_rows else ORANGE); cnt += 1
        for k in range(r):                  # downward triangles between them
            xl = x0 + (k - r / 2) * u
            f.poly([P(xl, y_top), P(xl + u, y_top), P(xl + u / 2, y_bot)], fill="#ffffff"); cnt += 1
        rows.append(cnt)
    assert rows == [2 * r + 1 for r in range(n)] and sum(rows) == n * n
    return rows

@fig
def stacked_triangles():
    f = Fig("stacked_triangles")
    x = 0
    for n in range(1, 6):
        rows = stacked_tri(f, x, n, colour_rows=False)
        f.label(P(x, -18), str(sum(rows)), size=14, bold=True)
        x += n * 16 / 2 + (n + 1) * 16 / 2 + 26
    return f

@fig
def stacked_triangle_rows():
    f = Fig("stacked_triangle_rows")
    n, u = 4, 30
    rows = stacked_tri(f, 0, n, u=u)
    for r, c in enumerate(rows):
        f.label(P(n * u / 2 + 30, (n - r - 0.5) * u * C30 - 5), f"row {r + 1}: {c}", anchor="start", size=13)
    f.label(P(0, -20), " + ".join(map(str, rows)) + f" = {sum(rows)}", size=14, bold=True)
    return f

def koch(pts):
    out = []
    for p, q in zip(pts, pts[1:]):
        a = dirto(p, q); L = dist(p, q) / 3
        p1 = along(p, a, L); p3 = along(p, a, 2 * L); p2 = along(p1, a + 60, L)
        out += [p, p1, p2, p3]
    return out + [pts[-1]]

@fig
def koch_snowflake():
    f = Fig("koch_snowflake")
    R = 52
    for k in range(4):
        c = P(k * 140, 0)
        pts = [along(c, 90 - 120 * i, R) for i in range(3)]; pts.append(pts[0])
        for _ in range(k): pts = koch(pts)
        segs = len(pts) - 1
        assert segs == 3 * 4 ** k
        f.poly(pts[:-1], fill=BLUE)
        f.label(P(c[0], -R - 30), f"{segs} segments", size=13, bold=True)
    return f

@fig
def speed_bump():
    f = Fig("speed_bump")
    f.seg(P(0, 0), P(90, 0), w=2.6)
    f.text(P(45, -24), "1 segment", size=13)
    f.seg(P(120, 0), P(150, 0), w=1.4, color=HELP)
    pts = koch([P(180, 0), P(270, 0)])
    assert len(pts) - 1 == 4
    for p, q in zip(pts, pts[1:]): f.seg(p, q, w=2.6, color=ASK)
    f.label(P(225, -24), "becomes 4 segments", size=13, color=ASK)
    f.seg(P(144, 6), P(150, 0), w=1.4, color=HELP); f.seg(P(144, -6), P(150, 0), w=1.4, color=HELP)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
