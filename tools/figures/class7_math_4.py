"""Figures for class 7 maths Ch 4, Expressions using Letter-Numbers. Every count drawn here
(matchsticks, squares, pieces, minutes) is computed and asserted against the formula written
in the notes, so a picture can never disagree with its expression."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "4")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

STICK, HEAD = "#d4a017", "#b71c1c"
GREEN, RED, BLUE, YELLOW, GREY, ORANGE = "#81c784", "#e57373", "#64b5f6", "#fff176", "#cfd8dc", "#fb8c00"

def stick(f, p, q, color=STICK):
    f.seg(p, q, color=color, w=5)
    f.dot(q, color=HEAD)

# ---------------------------------------------------------------- matchstick Ls
@fig
def ls_pattern():
    f = Fig("ls_pattern"); L = 40; n = 5; sticks = 0
    for i in range(n):
        x = i * 34
        stick(f, P(x, L), P(x, 0)); stick(f, P(x, 0), P(x + 26, 0)); sticks += 2
    assert sticks == 2 * n
    f.label(P((n - 1) * 34 / 2 + 13, -22), f"{n} Ls use 2 × {n} = {2 * n} matchsticks", size=14, bold=True)
    return f

# ---------------------------------------------------------------- calendar 2 × 3 block
@fig
def calendar_2x3():
    f = Fig("calendar_2x3"); s = 56
    cells = {(0, 0): "w − 1", (1, 0): "w"}         # (column, row) with row 0 at the bottom
    for c in range(3):
        for r in range(2):
            box(f, c * s, r * s, s, s, fill="#fff8e1" if (c, r) in cells else "#ffffff", color=RED)
            f.label(P(c * s + s / 2, r * s + s / 2), cells.get((c, r), "?"), size=16,
                    color=INK if (c, r) in cells else ASK, bold=(c, r) not in cells)
    return f

# ---------------------------------------------------------------- area: distributive property
@fig
def area_split():
    f = Fig("area_split"); k = 30; h = 2.2 * k
    box(f, 0, 0, 4 * k, h, fill="#bbdefb"); box(f, 4 * k, 0, 3 * k, h, fill="#c8e6c9")
    f.label(P(2 * k, h / 2), "4v", size=16, bold=True); f.label(P(5.5 * k, h / 2), "3v", size=16, bold=True)
    f.label(P(2 * k, -14), "4", size=15); f.label(P(5.5 * k, -14), "3", size=15)
    f.label(P(-12, h / 2), "v", size=15, color=GIVEN, bold=True)
    f.seg(P(0, -34), P(7 * k, -34), color=HELP, w=1.4)
    f.label(P(3.5 * k, -48), "whole width 4 + 3 = 7, so area = 7v", size=13, color=ANS, bold=True)
    assert 4 + 3 == 7
    return f

@fig
def area_cut():
    f = Fig("area_cut"); k = 18; h = 3.4 * k
    AB, EB = 12, 4; AE = AB - EB
    box(f, 0, 0, AE * k, h, fill="#bbdefb"); box(f, AE * k, 0, EB * k, h, fill="#eeeeee")
    for name, p, anc, dy in [("A", P(0, 0), "end", -10), ("E", P(AE * k, 0), "middle", -14), ("B", P(AB * k, 0), "start", -10),
                             ("D", P(0, h), "end", 10), ("F", P(AE * k, h), "middle", 14), ("C", P(AB * k, h), "start", 10)]:
        f.label(add(p, (0, dy)), name, anchor=anc, bold=True, size=15)
    f.label(P(-12, h / 2), "n", color=GIVEN, bold=True, anchor="end")
    f.label(P(AE * k / 2, h / 2), "8n", size=16, bold=True, color=ANS)
    f.label(P((AE + EB / 2) * k, h / 2), "4n", size=15)
    f.label(P((AE + EB / 2) * k, h + 14), "4", size=14)
    f.seg(P(0, -30), P(AB * k, -30), color=HELP, w=1.4)
    f.label(P(AB * k / 2, -44), "AB = 12", size=14)
    assert AE == 8 and AB * 1 - EB * 1 == AE
    return f

# ---------------------------------------------------------------- saree border
@fig
def saree():
    f = Fig("saree"); s = 44
    designs = "ABCABCABC"
    for i, d in enumerate(designs):
        x = i * s
        box(f, x, 0, s, s, fill={"A": "#ffcdd2", "B": "#c8e6c9", "C": "#bbdefb"}[d])
        cx, cy = x + s / 2, s / 2
        if d == "A":   f.poly([P(cx, cy + 14), P(cx + 14, cy), P(cx, cy - 14), P(cx - 14, cy)], fill="#e57373")
        elif d == "B": f.poly([P(cx - 13, cy - 11), P(cx + 13, cy - 11), P(cx, cy + 13)], fill="#66bb6a")
        else:          box(f, cx - 11, cy - 11, 22, 22, fill="#42a5f5")
        f.label(P(cx, -12), str(i + 1), size=13)
        f.label(P(cx, s + 12), d, size=13, bold=True)
    assert [i + 1 for i, d in enumerate(designs) if d == "C"] == [3 * n for n in (1, 2, 3)]
    assert [i + 1 for i, d in enumerate(designs) if d == "B"] == [3 * n - 1 for n in (1, 2, 3)]
    f.label(P(len(designs) * s + 8, s / 2), "…", anchor="start", size=18)
    return f

# ---------------------------------------------------------------- triangles in a strip
def tri_strip(f, x0, n, s=30, color_by_kind=True):
    """n triangles in a row, alternating up and down. Returns (flat, slanting) stick counts."""
    h = s * 0.866; hor = sl = 0
    B = lambda j: P(x0 + j * s, 0)            # bottom corners
    T = lambda j: P(x0 + j * s + s / 2, h)    # top corners
    flat, slant = (ORANGE, BLUE) if color_by_kind else (STICK, STICK)
    stick(f, B(0), T(0), slant); sl += 1
    for i in range(n):
        j = i // 2
        if i % 2 == 0:                        # pointing up: new bottom stick, new slant down to B(j+1)
            stick(f, B(j), B(j + 1), flat); stick(f, T(j), B(j + 1), slant)
        else:                                 # pointing down: new top stick, new slant up to T(j+1)
            stick(f, T(j), T(j + 1), flat); stick(f, B(j + 1), T(j + 1), slant)
        hor += 1; sl += 1
    return hor, sl

@fig
def triangles():
    f = Fig("triangles"); x = 0
    for n in (1, 2, 3, 4):
        hor, sl = tri_strip(f, x, n)
        assert hor == n and sl == n + 1 and hor + sl == 2 * n + 1
        f.label(P(x + ((n + 1) // 2) * 15 + 7, -18), f"Step {n}: {2 * n + 1}", size=13, bold=True)
        x += ((n + 1) // 2) * 30 + 15 + 40
    f.label(P(x / 2, -42), "orange = flat sticks, blue = slanting sticks", size=13, color=HELP)
    return f

# ---------------------------------------------------------------- Q5 path puzzle
@fig
def paths():
    f = Fig("paths")
    def oval(p, s, ask=False):
        w = 84
        f.poly([P(p[0] - w / 2, p[1] - 14), P(p[0] + w / 2, p[1] - 14), P(p[0] + w / 2, p[1] + 14), P(p[0] - w / 2, p[1] + 14)],
               fill="#eeeeee", color=INK)
        f.label(p, s, size=14, bold=ask, color=ASK if ask else INK)
    def op(p, s):
        box(f, p[0] - 20, p[1] - 16, 40, 32, fill="#fff9c4"); f.label(p, s, size=14)
    centre = P(0, 0); oval(centre, "w + 2")
    rows = [(+1, +1, ["+3", "w + 5", "×4", "4w + 20"]),
            (+1, -1, ["−5", "w − 3", "×3", "?"]),
            (-1, -1, ["−8", "?", "−4", "?"]),
            (-1, +1, ["−4", "?", "×3", "3w − 6"])]
    for vy, sx, items in rows:
        y = 70 * vy
        f.seg(P(sx * 40, vy * 14), P(sx * 100, y - vy * 16), color=INK, w=1.6)
        xs = [100, 200, 300, 400]
        for x, it in zip(xs, items):
            p = P(sx * x, y)
            (op if it[0] in "+−×" else oval)(p, it) if it != "?" else oval(p, "?", ask=True)
        for a, b in zip(xs, xs[1:]):
            f.seg(P(sx * (a + (20 if a in (100, 300) else 42)), y), P(sx * (b - (42 if b in (200, 400) else 20)), y), color=INK, w=1.6)
    return f

# ---------------------------------------------------------------- rope folded and cut
@fig
def rope():
    f = Fig("rope"); H = 110
    for k, folds in enumerate((0, 1, 2)):
        x0 = k * 120; strands = folds + 1
        pts = []
        for j in range(strands):
            x = x0 + j * 14
            top, bot = (H, 0) if j % 2 == 0 else (0, H)
            f.seg(P(x, top), P(x, bot), color="#a1887f", w=5)
            if j > 0:
                yj = 0 if (j - 1) % 2 == 0 else H           # joins where the previous strand ended
                f.seg(P(x - 14, yj), P(x, yj), color="#a1887f", w=5)
        f.seg(P(x0 - 18, 40), P(x0 + strands * 14 + 8, 64), color=ASK, w=2, dash="6,4")
        pieces = strands + 1
        assert pieces == folds + 2
        f.label(P(x0 + (strands - 1) * 7, -18), f"folded {folds}×: {pieces} pieces", size=13, bold=True)
    return f

# ---------------------------------------------------------------- matchstick squares in a row
@fig
def squares_row():
    f = Fig("squares_row"); s = 36; x = 0
    for n in (1, 2, 3):
        count = 0
        for i in range(n):
            a = x + i * s
            if i == 0: stick(f, P(a, 0), P(a, s)); count += 1
            stick(f, P(a, s), P(a + s, s)); stick(f, P(a + s, 0), P(a + s, s)); stick(f, P(a, 0), P(a + s, 0)); count += 3
        assert count == 3 * n + 1
        f.label(P(x + n * s / 2, -18), f"{n} square{'s' if n > 1 else ''}: {count}", size=13, bold=True)
        x += n * s + 40
    return f

# ---------------------------------------------------------------- traffic signal sequence
@fig
def traffic():
    f = Fig("traffic"); seq = ["R", "Y", "G", "Y", "R", "Y", "G", "Y"]
    col = {"R": "#ef5350", "Y": "#ffee58", "G": "#66bb6a"}
    for i, c in enumerate(seq):
        x = i * 44; r = 17
        ring = [P(x + r * math.cos(d2r(a)), r * math.sin(d2r(a))) for a in range(0, 360, 15)]
        f.poly(ring, fill=col[c]); f.label(P(x, -30), str(i + 1), size=13)
    for i, c in enumerate(seq, 1):
        if c == "R": assert (i + 3) % 4 == 0
        if c == "G": assert (i + 1) % 4 == 0
        if c == "Y": assert i % 2 == 0
    f.label(P(len(seq) * 44 - 10, 0), "…", anchor="start", size=18)
    return f

# ---------------------------------------------------------------- X of squares
@fig
def x_squares():
    f = Fig("x_squares"); s = 16; x0 = 0
    for n in (1, 2, 3):
        cells = {(0, 0)}
        for k in range(1, n + 1):
            cells |= {(k, k), (-k, k), (k, -k), (-k, -k)}
        assert len(cells) == 4 * n + 1
        for (i, j) in cells:
            box(f, x0 + i * s, j * s, s, s, fill=ORANGE, color="#e65100")
        f.label(P(x0 + s / 2, -4 * s - 12), f"Step {n}: {len(cells)}", size=13, bold=True)
        x0 += (2 * n + 1) * s + 2 * (n + 2) * s / 2 + 20
    return f

# ---------------------------------------------------------------- train line (answer figure)
@fig
def train():
    f = Fig("train"); gap = 90
    names = ["Yahapur", "S1", "S2", "S3", "Vahapur"]
    for i, nm in enumerate(names):
        x = i * gap
        f.dot(P(x, 0), color=GIVEN if nm[0] in "YV" else INK)
        f.label(P(x, -18), nm, size=13, bold=nm[0] in "YV")
        if 0 < i < 4: f.label(P(x, 18), "stop 2", size=12, color=ASK)
    for i in range(4):
        f.seg(P(i * gap + 6, 0), P((i + 1) * gap - 6, 0), color=INK, w=2.4)
        f.label(P(i * gap + gap / 2, 12), "t", size=14, color=GIVEN, bold=True)
    assert 4 * 4 + 3 * 2 == 22
    f.label(P(2 * gap, -44), "4 runs of t + 3 stops of 2 = 4t + 6 minutes", size=13, color=ANS, bold=True)
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
