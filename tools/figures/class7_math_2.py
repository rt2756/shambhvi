"""Figures for class 7 maths Ch 2, Arithmetic Expressions. Counts and lengths drawn here are
computed and asserted against the expressions written in the notes."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "2")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

GREEN, RED, BLUE, YELLOW, GREY = "#81c784", "#e57373", "#64b5f6", "#fff176", "#cfd8dc"

# ---------------------------------------------------------------- comparing sums with bar models
@fig
def marbles_sum():
    f = Fig("marbles_sum"); k = 0.25          # 1 marble = 0.25 units (bars not to scale beyond this)
    # Raja: 1023 + 125, Joy: 1022 + 128. Draw the common 1022 part, then the differences.
    base = 1022 * k * 0.3
    def bar(y, name, parts):
        x = 0
        for w, label, col in parts:
            box(f, x, y, w, 30, fill=col); f.label(P(x + w / 2, y + 15), label, size=13)
            x += w
        f.label(P(-10, y + 15), name, anchor="end", size=14, bold=True)
        return x
    r = bar(50, "Raja", [(base, "1022", GREY), (22, "1", RED), (125 * 0.6, "125", GREEN)])
    j = bar(0, "Joy", [(base, "1022", GREY), (125 * 0.6, "125", GREEN), (22, "1", BLUE), (22, "1", BLUE), (22, "1", BLUE)])
    assert 1023 + 125 + 2 == 1022 + 128
    f.label(P(j + 8, 15), "Joy has 2 more", anchor="start", color=ANS, size=13, bold=True)
    return f

# ---------------------------------------------------------------- 5 × 2 + 3 versus 2 × (5 + 3)
def squares(f, x0, cols, s=18):
    for c, (n, colour) in enumerate(cols):
        for r in range(n):
            box(f, x0 + c * (s + 6), r * s, s, s, fill=colour)

@fig
def arrangements():
    f = Fig("arrangements")
    left = [(2, GREEN)] * 5 + [(3, RED)]
    squares(f, 0, left)
    assert sum(n for n, _ in left) == 5 * 2 + 3 == 13
    f.label(P(70, -22), "5 × 2 + 3 = 13", size=14, bold=True)
    x0 = 230
    for c in range(2):
        for r in range(3): box(f, x0 + c * 24, r * 18, 18, 18, fill=BLUE)
        for r in range(3, 8): box(f, x0 + c * 24, r * 18, 18, 18, fill=YELLOW)
    assert 2 * (5 + 3) == 16
    f.label(P(x0 + 21, -22), "2 × (5 + 3) = 16", size=14, bold=True)
    return f

# ---------------------------------------------------------------- the window
@fig
def window():
    f = Fig("window"); k = 6                   # 1 cm = 6 units
    border, grill, gap, n_grill = 3, 2, 5, 6
    n_gap = n_grill + 1
    parts = [("border", border)] + [x for _ in range(n_grill) for x in (("gap", gap), ("grill", grill))] + [("gap", gap), ("border", border)]
    total = sum(h for _, h in parts)
    assert total == 2 * border + n_grill * grill + n_gap * gap == 53
    y = 0; W = 150
    for name, h in reversed(parts):
        col = {"border": "#8d6e63", "grill": "#455a64", "gap": "#bbdefb"}[name]
        box(f, 0, y * k, W, h * k, fill=col, color=col if name == "gap" else INK)
        y += h
    # labels on the right for the top three pieces
    tops = [("Border 3 cm", total - border / 2), ("Gap 5 cm", total - border - gap / 2), ("Grill 2 cm", total - border - gap - grill / 2)]
    for label, yy in tops:
        f.seg(P(W + 4, yy * k), P(W + 24, yy * k), color=HELP, w=1.2); f.label(P(W + 28, yy * k), label, anchor="start", size=13)
    f.seg(P(-16, 0), P(-16, total * k), color=ASK, w=1.6)
    f.label(P(-22, total * k / 2), "total height ?", anchor="end", color=ASK, size=13, bold=True)
    return f

# ---------------------------------------------------------------- scouts and guides
@fig
def parade():
    f = Fig("parade"); s = 26
    for r in range(7):
        for c in range(5):
            f.dot(P(c * s, -r * s), color=BLUE if r < 4 else RED)
    f.label(P(5 * s, -1.5 * s), "4 rows of 5 scouts: 4 × 5", anchor="start", size=13, color=BLUE)
    f.label(P(5 * s, -5 * s), "3 rows of 5 guides: 3 × 5", anchor="start", size=13, color=RED)
    f.label(P(2 * s, -7.3 * s), "(4 + 3) × 5 = 4 × 5 + 3 × 5 = 35", size=14, bold=True)
    assert (4 + 3) * 5 == 4 * 5 + 3 * 5 == 35
    return f

# ---------------------------------------------------------------- number pictures (sums two ways)
def grid(f, x0, rows, colours, s=34):
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            p = P(x0 + c * s, -r * s)
            box(f, p[0] - 13, p[1] - 13, 26, 26, fill=colours[v])
            f.label(p, str(v), size=15, bold=True)

@fig
def number_pictures():
    f = Fig("number_pictures")
    I = [[4, 8, 4], [8, 4, 8], [4, 8, 4]]
    II = [[5, 6, 6, 5], [6, 5, 5, 6], [6, 5, 5, 6], [5, 6, 6, 5]]
    grid(f, 0, I, {4: YELLOW, 8: BLUE}); grid(f, 190, II, {5: BLUE, 6: RED})
    f.label(P(34, -118), "Picture I", size=13, bold=True); f.label(P(190 + 51, -152), "Picture II", size=13, bold=True)
    assert sum(map(sum, I)) == 5 * 4 + 4 * 8 == 52 and sum(map(sum, II)) == 8 * (5 + 6) == 88
    return f

# ---------------------------------------------------------------- the snail
@fig
def snail():
    f = Fig("snail"); kx, ky = 44, 16
    for h in range(0, 11, 2):
        f.seg(P(-6, h * ky), P(0, h * ky), w=1.2); f.label(P(-10, h * ky), str(h), anchor="end", size=12)
    f.seg(P(0, 0), P(0, 10.6 * ky), w=1.4); f.seg(P(0, 0), P(8.4 * kx, 0), w=1.4)
    f.seg(P(0, 10 * ky), P(8.4 * kx, 10 * ky), color=ANS, w=1.4, dash="6,4")
    f.label(P(8.5 * kx, 10 * ky), "top (10 cm)", anchor="start", color=ANS, size=12)
    h, x, day = 0, 0.0, 0
    while True:
        day += 1
        top = h + 3
        f.seg(P(x * kx, h * ky), P((x + 0.5) * kx, top * ky), color=BLUE, w=2.4)
        f.label(P((day - 0.5) * kx, -14), str(day), size=12)
        if top >= 10:
            f.dot(P((x + 0.5) * kx, top * ky), color=ASK); break
        f.seg(P((x + 0.5) * kx, top * ky), P((x + 1) * kx, (top - 2) * ky), color=RED, w=2.4)
        h, x = top - 2, x + 1
    assert day == 8 and h == 7
    f.label(P(4 * kx, -32), "day", size=12)
    f.label(P(-34, 5 * ky), "cm", size=12, anchor="end")
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
