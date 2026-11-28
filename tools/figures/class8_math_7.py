"""Figures for class 8 maths Ch 7, Proportional Reasoning - 1. Rectangles are drawn to scale from
their stated sizes, bar models and counters assert that the parts add up to the whole in the given
ratio, brick walls count their own bricks, and the Binairo puzzles are generated and checked by a
solver to have exactly one solution, so no label can disagree with its picture."""
import math, os, sys, random
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "7")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, BROWN, RED = "#90caf9", "#fff59d", "#a5d6a7", "#cfd8dc", "#ffcc80", "#f8bbd0", "#c58a4a", "#e57373"

def rect(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def rot_rect(f, c, w, h, ang, fill="#ffffff"):
    pts = []
    for dx, dy in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        a = d2r(ang)
        pts.append(P(c[0] + dx * math.cos(a) - dy * math.sin(a), c[1] + dx * math.sin(a) + dy * math.cos(a)))
    f.poly(pts, fill=fill)
    return pts

def ellipse(f, c, rx, ry, fill, color=INK):
    f.poly([P(c[0] + rx * math.cos(d2r(a)), c[1] + ry * math.sin(d2r(a))) for a in range(0, 360, 10)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK):
    ellipse(f, c, r, r, fill, color)

def simplest(a, b):
    g = math.gcd(a, b); return a // g, b // g

# ---------------------------------------------------------------- 7.1 five pictures
@fig
def five_images():
    f = Fig("five_images")
    sizes = {"A": (60, 40), "B": (40, 20), "C": (30, 20), "D": (90, 60), "E": (60, 60)}
    s, x = 1.6, 0
    for name, (w, h) in sizes.items():
        W, H = w * s, h * s
        rect(f, x, 0, W, H, fill="#e3f2fd")
        # a face stretched with the picture: it looks right only if w : h = 3 : 2
        c = P(x + W / 2, H / 2)
        ellipse(f, c, W * 0.28, H * 0.38, ORANGE)
        for sx in (-1, 1):
            disc(f, P(c[0] + sx * W * 0.1, c[1] + H * 0.1), 2.5, INK)
        f.seg(P(c[0] - W * 0.08, c[1] - H * 0.15), P(c[0] + W * 0.08, c[1] - H * 0.15), w=1.6)
        same = simplest(w, h) == (3, 2)
        f.label(P(x + W / 2, H + 10), f"{name}", size=14, bold=True)
        f.label(P(x + W / 2, -18), f"{w} × {h} mm", size=12, color=GIVEN)
        f.label(P(x + W / 2, -34), f"{simplest(w, h)[0]} : {simplest(w, h)[1]}", size=12, color=ANS if same else ASK)
        x += W + 24
    return f

# ---------------------------------------------------------------- 7.4 coffee strengths
@fig
def coffee_bars():
    f = Fig("coffee_bars")
    rows = [("regular", 15, 35), ("strong", 20, 30), ("light", 10, 40)]
    k = 5
    for i, (name, dec, milk) in enumerate(rows):
        y = -i * 34
        rect(f, 0, y, dec * k, 22, fill=BROWN)
        rect(f, dec * k, y, milk * k, 22, fill="#fff8e1")
        f.label(P(-10, y + 6), name, anchor="end", size=13, bold=True)
        f.text(P(dec * k / 2, y + 6), f"{dec}", size=12, bold=True, color="#ffffff")
        f.text(P(dec * k + milk * k / 2, y + 6), f"{milk}", size=12)
        part = F(dec, dec + milk)
        f.label(P(50 * k + 10, y + 6), f"decoction is {part.numerator}/{part.denominator} of the cup", anchor="start", size=12, color=GIVEN)
        assert dec + milk == 50
    f.label(P(0, 36), "mL of decoction (brown) and milk (cream) in one 50 mL cup", anchor="start", size=12, color=HELP)
    return f

# ---------------------------------------------------------------- rectangles: which are similar?
RECTS = {"A": (2, 4, 90), "B": (4, 3, 0), "C": (3, 6, 30), "D": (6, 2, 15), "E": (1.5, 3, -40)}

@fig
def rectangles_q4():
    f = Fig("rectangles_q4")
    k = 26
    centres = {"A": P(0, 0), "B": P(160, 30), "C": P(310, 10), "D": P(490, 30), "E": P(610, -10)}
    for name, (w, h, ang) in RECTS.items():
        c = centres[name]
        pts = rot_rect(f, c, w * k, h * k, ang, fill="#ffffff")
        f.text(P(c[0], c[1] - 6), name, size=15, bold=True)
        # side labels at the midpoints of two neighbouring sides
        m1 = mul(add(pts[0], pts[1]), 0.5); m2 = mul(add(pts[1], pts[2]), 0.5)
        out1 = along(m1, dirto(c, m1), 14); out2 = along(m2, dirto(c, m2), 16)
        f.label(P(out1[0], out1[1] - 5), f"{w:g} cm", size=12, color=GIVEN)
        f.label(P(out2[0], out2[1] - 5), f"{h:g} cm", size=12, color=GIVEN)
    sim = [n for n, (w, h, _) in RECTS.items() if F(w).limit_denominator() / F(h).limit_denominator() in (F(1, 2), F(2, 1))]
    assert sim == ["A", "C", "E"]
    return f

@fig
def rectangle_scaled():
    f = Fig("rectangle_scaled")
    k = 22
    x = 0
    for (w, h, lab) in [(4, 3, "given 4 × 3"), (2, 1.5, "half: 2 × 1.5"), (8, 6, "double: 8 × 6"), (6, 5, "6 × 5: not similar")]:
        rect(f, x, 0, w * k, h * k, fill=GREEN if F(w).limit_denominator() / F(h).limit_denominator() == F(4, 3) else PINK)
        f.label(P(x + w * k / 2, -18), lab, size=12, color=ANS if w / h == 4 / 3 else ASK)
        x += w * k + 30
    return f

# ---------------------------------------------------------------- brick walls
def wall(f, x0, y0, rows, colour, title):
    bw, bh = 28, 12
    grey = col = 0
    for r, row in enumerate(rows):
        off = 0 if r % 2 == 0 else bw / 2
        for i, ch in enumerate(row):
            fill = colour if ch == "x" else GREY
            rect(f, x0 + off + i * bw, y0 - r * bh, bw, bh, fill=fill, color="#ffffff")
            if ch == "x": col += 1
            else: grey += 1
    f.label(P(x0 - 12, y0 - len(rows) * bh / 2 + 2), title, anchor="end", size=14, bold=True)
    return grey, col

@fig
def brick_walls():
    f = Fig("brick_walls")
    unit_a = ["xxx..", ".xx..", "..x.."]            # one repeat: 15 bricks, 6 coloured
    unit_b = ["x...xx.", "xx...x.", ".xx...x", "..xxx.."]   # one repeat: 28 bricks, 12 coloured
    for u in unit_b: assert len(u) == 7
    rows_a = [r * 3 for r in unit_a]
    rows_b = [r * 2 for r in unit_b]
    g, c = wall(f, 0, 0, rows_a, RED, "(a)")
    assert (g, c) == (27, 18) and simplest(g, c) == (3, 2)
    g2, c2 = wall(f, 0, -70, rows_b, BROWN, "(b)")
    assert (g2, c2) == (32, 24) and simplest(g2, c2) == (4, 3)
    f.label(P(0, -140), "Each wall goes on with the same pattern in both directions.", anchor="start", size=12, color=HELP)
    return f

@fig
def brick_units():
    f = Fig("brick_units")
    g, c = wall(f, 0, 0, ["xxx..", ".xx..", "..x.."], RED, "(a)")
    assert (g, c) == (9, 6)
    f.label(P(160, -8), f"one repeat: {g} grey, {c} red → {g} : {c} = 3 : 2", anchor="start", size=12, color=ANS)
    g, c = wall(f, 0, -60, ["x...xx.", "xx...x.", ".xx...x", "..xxx.."], BROWN, "(b)")
    assert (g, c) == (16, 12)
    f.label(P(220, -78), f"one repeat: {g} grey, {c} brown → {g} : {c} = 4 : 3", anchor="start", size=12, color=ANS)
    return f

# ---------------------------------------------------------------- the house plan
@fig
def house_plan():
    f = Fig("house_plan")
    k = 12
    walls = [((0, 0), (24, 0)), ((0, 12), (24, 12)), ((0, 0), (0, 12)), ((24, 0), (24, 12)), ((9, 0), (9, 12)),
             ((9, 0), (9, -9)), ((15, 0), (15, -9)), ((9, -9), (15, -9))]
    total = 0
    for (a, b) in walls:
        f.seg(P(a[0] * k, a[1] * k), P(b[0] * k, b[1] * k), w=4)
        total += abs(a[0] - b[0]) + abs(a[1] - b[1])
    assert total == 108
    f.label(P(4.5 * k, 12 * k + 10), "9 ft", size=12, color=GIVEN)
    f.label(P(16.5 * k, 12 * k + 10), "15 ft", size=12, color=GIVEN)
    f.label(P(-8, 6 * k - 5), "12 ft", anchor="end", size=12, color=GIVEN)
    f.label(P(12 * k, -9 * k - 18), "6 ft", size=12, color=GIVEN)
    f.label(P(15 * k + 8, -4.5 * k - 5), "9 ft", anchor="start", size=12, color=GIVEN)
    f.label(P(4.5 * k, 6 * k - 5), "room 1", size=12, color=HELP)
    f.label(P(16.5 * k, 6 * k - 5), "room 2", size=12, color=HELP)
    f.label(P(12 * k, -4.5 * k - 5), "room 3", size=12, color=HELP)
    return f

# ---------------------------------------------------------------- sharing in a ratio
@fig
def share_12():
    f = Fig("share_12")
    u = 26
    for rnd in range(3):
        y = -rnd * 34
        for i in range(3):
            disc(f, P(i * u, y), 10, BLUE)
        disc(f, P(4 * u, y), 10, ORANGE)
        f.label(P(-20, y - 5), f"round {rnd + 1}", anchor="end", size=12, color=HELP)
    partner, you = 3 * 3, 3 * 1
    assert partner + you == 12 and simplest(partner, you) == (3, 1)
    f.label(P(u, 26), "partner (3 each round)", size=12, color=GIVEN)
    f.label(P(4 * u + 20, 26), "you (1)", size=12, color=ANS)
    f.label(P(-60, -3 * 34 - 4), f"partner {partner}, you {you}: 9 : 3 = 3 : 1", anchor="start", size=13, bold=True)
    return f

def bar_model(f, y, whole, m, n, unit_w=36, labels=("", "")):
    size = F(whole, m + n)
    for i in range(m + n):
        rect(f, i * unit_w, y, unit_w, 24, fill=BLUE if i < m else ORANGE)
        f.text(P(i * unit_w + unit_w / 2, y + 7), f"{size}" if size.denominator == 1 else f"{float(size):g}", size=12, bold=True)
    a, b = m * size, n * size
    assert a + b == whole and F(a, b) == F(m, n)
    grp = lambda k: "group" if k == 1 else "groups"
    f.label(P(0, y + 34), f"{labels[0]} {m} {grp(m)} = {a}", anchor="start", size=12, color=GIVEN)
    f.label(P((m + n) * unit_w + 10, y + 6), f"{labels[1]} {n} {grp(n)} = {b}", anchor="start", size=12, color=ANS)
    return a, b

@fig
def share_42():
    f = Fig("share_42")
    a, b = bar_model(f, 0, 42, 4, 3, labels=("partner:", "you:"))
    assert (a, b) == (24, 18)
    f.label(P(0, -22), "42 ÷ (4 + 3) = 6 in each group", anchor="start", size=13, bold=True)
    return f

@fig
def sand_cement():
    f = Fig("sand_cement")
    a, b = bar_model(f, 0, 40, 3, 1, unit_w=44, labels=("sand:", "cement:"))
    assert (a, b) == (30, 10)
    f.label(P(0, -22), "40 kg in the ratio 3 : 1: each part is 10 kg", anchor="start", size=13, bold=True)
    # new mixture: sand stays 30 = 5 parts of 6; cement must be 2 parts of 6 = 12
    y = -100
    part = F(30, 5)
    for i in range(7):
        rect(f, i * 30, y, 30, 24, fill=BLUE if i < 5 else ORANGE)
        f.text(P(i * 30 + 15, y + 7), str(part), size=12, bold=True)
    assert 2 * part == 12 and 12 - 10 == 2
    f.label(P(0, y + 34), "sand: 5 parts = 30", anchor="start", size=12, color=GIVEN)
    f.label(P(220, y + 6), "cement: 2 parts = 12", anchor="start", size=12, color=ANS)
    f.label(P(0, y - 22), "new ratio 5 : 2 with the same 30 kg of sand: add 12 − 10 = 2 kg cement", anchor="start", size=13, bold=True)
    return f

# ---------------------------------------------------------------- Binairo
N = 6
def valid_line(line):
    for i in range(len(line) - 2):
        if line[i] is not None and line[i] == line[i + 1] == line[i + 2]: return False
    for s in (0, 1):
        if line.count(s) > len(line) // 2: return False
    return True

def solve(grid, limit=2):
    """Return up to `limit` solutions of a partly filled grid (None = empty)."""
    sols = []
    g = [row[:] for row in grid]
    cells = [(r, c) for r in range(N) for c in range(N) if g[r][c] is None]
    def ok(r, c):
        row = g[r]; col = [g[i][c] for i in range(N)]
        if not valid_line(row) or not valid_line(col): return False
        if None not in row:
            if sum(1 for rr in g if rr == row) > 1: return False
        if None not in col:
            cols = [[g[i][j] for i in range(N)] for j in range(N)]
            if sum(1 for cc in cols if cc == col) > 1: return False
        return True
    def rec(k):
        if len(sols) >= limit: return
        if k == len(cells):
            sols.append([row[:] for row in g]); return
        r, c = cells[k]
        for v in (0, 1):
            g[r][c] = v
            if ok(r, c): rec(k + 1)
            g[r][c] = None
    rec(0)
    return sols

def make_puzzle(seed):
    rnd = random.Random(seed)
    empty = [[None] * N for _ in range(N)]
    # a full solution: solve the empty grid with shuffled value order
    sol = None
    while sol is None:
        g = [[None] * N for _ in range(N)]
        for _ in range(4):
            r, c = rnd.randrange(N), rnd.randrange(N); g[r][c] = rnd.randrange(2)
        s = solve(g, limit=1)
        sol = s[0] if s else None
    puzzle = [row[:] for row in sol]
    order = [(r, c) for r in range(N) for c in range(N)]
    rnd.shuffle(order)
    for r, c in order:
        keep = puzzle[r][c]; puzzle[r][c] = None
        if len(solve(puzzle, limit=2)) != 1: puzzle[r][c] = keep
    assert len(solve(puzzle, limit=2)) == 1
    return puzzle, sol

PUZZLES = [make_puzzle(7), make_puzzle(21)]

def draw_grid(f, x0, grid, given=None):
    u = 30
    for r in range(N):
        for c in range(N):
            x, y = x0 + c * u, -r * u
            is_given = given is not None and given[r][c] is not None
            rect(f, x, y, u, u, fill="#fff9c4" if (given is None or is_given) else "#ffffff")
            v = grid[r][c]
            if v is None: continue
            col = INK if (given is None or is_given) else ANS
            if v == 0: f.seg(P(x + 8, y + u / 2), P(x + u - 8, y + u / 2), color=col, w=3.2)
            else: f.seg(P(x + u / 2, y + 7), P(x + u / 2, y + u - 7), color=ASK if col == INK else ANS, w=3.2)

@fig
def binairo_puzzles():
    f = Fig("binairo_puzzles")
    for i, (puz, _) in enumerate(PUZZLES):
        draw_grid(f, i * 230, puz)
        f.label(P(i * 230 + 90, 44), f"Puzzle ({'ab'[i]})", size=14, bold=True)
    return f

@fig
def binairo_solutions():
    f = Fig("binairo_solutions")
    for i, (puz, sol) in enumerate(PUZZLES):
        for row in sol: assert row.count(0) == row.count(1) == 3
        draw_grid(f, i * 230, sol, given=puz)
        f.label(P(i * 230 + 90, 44), f"Solution ({'ab'[i]})", size=14, bold=True)
    f.label(P(0, -6 * 30 - 4), "Yellow cells were given; green lines are the ones you fill in.", anchor="start", size=12, color=HELP)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
