"""Figures for class 8 maths Ch 13, Algebra Play. Number pyramids are filled by the rule (each box
is the sum of the two below) and every given number is checked against the filled pyramid; the
calendar is built from the real weekday of 1 August 2025; the shape grids are checked against their
row and column sums; the flower and coin stories are replayed step by step, so no label can
disagree with its picture."""
import math, os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "13")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, PURPLE, RED = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0", "#7b1fa2", "#e53935"

def rect(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def build(bottom):
    rows = [list(bottom)]
    while len(rows[-1]) > 1:
        r = rows[-1]
        rows.append([r[i] + r[i + 1] for i in range(len(r) - 1)])
    return rows                                   # rows[0] = bottom

def pyramid(f, x0, rows, shown=None, w=40, h=28, hl=None):
    """Draw rows (bottom first). `shown` is a set of (row, col) whose numbers are printed (None = all).
    `hl` is a set of boxes to colour as answers. Text entries (strings) are printed as they are."""
    n = len(rows)
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            x = x0 + c * w + r * w / 2
            y = r * h
            ans = hl is not None and (r, c) in hl
            rect(f, x, y, w, h, fill=GREEN if ans else ("#ffffff" if shown is not None and (r, c) not in shown and not ans else YELLOW))
            if shown is None or (r, c) in shown or ans:
                f.text(P(x + w / 2, y + h / 2 - 6), str(v), size=13, bold=True, color=ANS if ans else INK)
    return n * w

def check_given(rows, given):
    for (r, c), v in given.items():
        assert rows[r][c] == v, (r, c, rows[r][c], v)

# ---------------------------------------------------------------- 13.2 number pyramids
@fig
def pyramid_rule():
    f = Fig("pyramid_rule")
    rows = build([1, 9, 4])
    assert rows[-1] == [23]
    pyramid(f, 0, rows)
    f.label(P(60, -18), "each box = the sum of the two boxes under it", size=12, color=HELP)
    return f

@fig
def pyramid_first():
    f = Fig("pyramid_first")
    x = 0
    for bottom in ([6, 2], [3, 4, 3], [5, 4, 5, 0]):
        rows = build(bottom)
        given = {(0, c) for c in range(len(bottom))}
        pyramid(f, x, rows, shown=given)
        x += len(bottom) * 40 + 40
    return f

@fig
def pyramid_first_ans():
    f = Fig("pyramid_first_ans")
    x = 0
    tops = []
    for bottom in ([6, 2], [3, 4, 3], [5, 4, 5, 0]):
        rows = build(bottom)
        given = {(0, c) for c in range(len(bottom))}
        hl = {(r, c) for r in range(1, len(rows)) for c in range(len(rows[r]))}
        pyramid(f, x, rows, shown=given, hl=hl)
        tops.append(rows[-1][0])
        x += len(bottom) * 40 + 40
    assert tops == [8, 14, 32]
    return f

@fig
def pyramid_60():
    f = Fig("pyramid_60")
    rows = build([12, 20, 8])
    check_given(rows, {(2, 0): 60})
    pyramid(f, 0, [[12, "c", 8], ["a", "b"], [60]])
    pyramid(f, 200, rows, shown={(0, 0), (0, 2), (2, 0)}, hl={(0, 1), (1, 0), (1, 1)})
    f.text(P(160, 30), "→", size=22, bold=True, color=GIVEN)
    return f

PUZ = [([4, 9, 6, 1], {(0, 0): 4, (0, 2): 6, (2, 1): 22, (3, 0): 50}),
       ([5, 14, 7, 2], {(0, 0): 5, (0, 2): 7, (1, 2): 9, (2, 0): 40}),
       ([3, 5, 5, 2], {(0, 0): 3, (0, 1): 5, (1, 2): 7, (3, 0): 35})]

@fig
def pyramid_puzzles():
    f = Fig("pyramid_puzzles")
    x = 0
    for bottom, given in PUZ:
        rows = build(bottom)
        check_given(rows, given)
        pyramid(f, x, rows, shown=set(given))
        x += 4 * 40 + 30
    return f

@fig
def pyramid_puzzles_ans():
    f = Fig("pyramid_puzzles_ans")
    x = 0
    for bottom, given in PUZ:
        rows = build(bottom)
        hl = {(r, c) for r in range(4) for c in range(len(rows[r]))} - set(given)
        pyramid(f, x, rows, shown=set(given), hl=hl)
        x += 4 * 40 + 30
    return f

@fig
def pyramid_letters():
    f = Fig("pyramid_letters")
    w = 70
    pyramid(f, 0, [["a", "b", "c"], ["a + b", "b + c"], ["a + 2b + c"]], w=w)
    pyramid(f, 3 * w + 40, [["a", "b", "c", "d"], ["a + b", "b + c", "c + d"], ["a + 2b + c", "b + 2c + d"], ["a + 3b + 3c + d"]], w=w + 14)
    # check the coefficient rows against numbers
    rows = build([1, 10, 100, 1000])
    assert rows[-1] == [1331] and build([1, 10, 100]) [-1] == [121]
    return f

@fig
def pyramid_fib():
    f = Fig("pyramid_fib")
    rows = build([1, 2, 3, 5])
    fib = [1, 2, 3, 5, 8, 13, 21, 34]
    assert all(v in fib for row in rows for v in row) and rows[-1] == [21]
    pyramid(f, 0, rows)
    f.label(P(80, -18), "bottom: 1, 2, 3, 5; every box is a Virahāṅka–Fibonacci number", size=12, color=ANS)
    return f

# ---------------------------------------------------------------- 13.3 grids
@fig
def calendar_aug():
    f = Fig("calendar_aug")
    w, h = 44, 30
    first = datetime.date(2025, 8, 1)
    start = (first.weekday() + 1) % 7          # Sunday = 0
    assert start == 5                           # 1 August 2025 was a Friday
    for i, d in enumerate("SUN MON TUE WED THU FRI SAT".split()):
        rect(f, i * w, 0, w, h, fill="#7e57c2")
        f.text(P(i * w + w / 2, 8), d, size=11, bold=True, color="#ffffff")
    box = {6, 7, 13, 14}
    for day in range(1, 32):
        k = start + day - 1
        r, c = divmod(k, 7)
        rect(f, c * w, -(r + 1) * h, w, h, fill=YELLOW if day in box else "#ffffff")
        f.text(P(c * w + w / 2, -(r + 1) * h + 8), str(day), size=12, bold=day in box)
    assert sum(box) == 40
    f.label(P(7 * w + 12, -2 * h), "6 + 7 + 13 + 14 = 40", anchor="start", size=13, bold=True, color=ANS)
    f.label(P(3.5 * w, 40), "AUGUST 2025", size=13, bold=True)
    return f

def shape(f, c, kind):
    if kind == "S":
        f.poly([add(c, (-9, -9)), add(c, (9, -9)), add(c, (9, 9)), add(c, (-9, 9))], fill="#5c6bc0", color="#5c6bc0")
    elif kind == "C":
        f.poly([P(c[0] + 10 * math.cos(d2r(a)), c[1] + 10 * math.sin(d2r(a))) for a in range(0, 360, 20)], fill=RED, color=RED)
    elif kind == "O":
        f.poly([P(c[0] + 10 * math.cos(d2r(a)), c[1] + 10 * math.sin(d2r(a))) for a in range(0, 360, 20)], fill="#5c6bc0", color="#5c6bc0")
    elif kind == "D":
        f.poly([add(c, (0, -12)), add(c, (12, 0)), add(c, (0, 12)), add(c, (-12, 0))], fill=PURPLE, color=PURPLE)

def grid(f, x0, rows, values, show_sums, extra_row=False, answers=False):
    u = 40
    n = len(rows[0])
    for r, row in enumerate(rows):
        for c, k in enumerate(row):
            rect(f, x0 + c * u, -r * u, u, u)
            shape(f, P(x0 + c * u + u / 2, -r * u + u / 2), k)
        tot = sum(values[k] for k in row)
        rect(f, x0 + n * u, -r * u, u, u, fill=GREEN if (answers and r not in show_sums) else "#ffffff")
        if r in show_sums or answers:
            f.text(P(x0 + n * u + u / 2, -r * u + u / 2 - 6), str(tot), size=13, bold=True, color=ANS if r not in show_sums else INK)
    if extra_row:
        r = len(rows)
        cols = [sum(values[rows[i][c]] for i in range(len(rows))) for c in range(n)]
        for c in range(n + 1):
            rect(f, x0 + c * u, -r * u, u, u, fill=GREEN if answers else "#ffffff")
            if answers:
                v = cols[c] if c < n else sum(cols)
                f.text(P(x0 + c * u + u / 2, -r * u + u / 2 - 6), str(v), size=13, bold=True, color=ANS)
        assert sum(cols) == sum(sum(values[k] for k in row) for row in rows)

G1 = ([["S", "S", "C"], ["C", "C", "S"], ["C", "S", "C"]], {"S": 11, "C": 5})
G2 = ([["O", "D", "D"], ["D", "O", "O"], ["D", "O", "O"]], {"O": 4, "D": 7})

@fig
def shape_grids():
    f = Fig("shape_grids")
    rows, v = G1
    assert [sum(v[k] for k in r) for r in rows[:2]] == [27, 21]
    grid(f, 0, rows, v, show_sums={0, 1})
    rows, v = G2
    assert [sum(v[k] for k in r) for r in rows[:2]] == [18, 15]
    grid(f, 230, rows, v, show_sums={0, 1}, extra_row=True)
    return f

@fig
def shape_grids_ans():
    f = Fig("shape_grids_ans")
    grid(f, 0, G1[0], G1[1], show_sums={0, 1}, answers=True)
    grid(f, 230, G2[0], G2[1], show_sums={0, 1}, extra_row=True, answers=True)
    f.label(P(0, -4 * 40 - 20), "square 11, red circle 5;   blue circle 4, diamond 7", anchor="start", size=12, color=ANS)
    return f

# ---------------------------------------------------------------- stories
@fig
def shrines():
    f = Fig("shrines")
    x, s = 7, 8
    steps = []
    have = x
    for k in range(3):
        have *= 2
        steps.append((have, s))
        have -= s
    assert have == 0
    xx = 0
    rect(f, xx, 0, 60, 34, fill=YELLOW); f.text(P(xx + 30, 10), f"{x}", size=15, bold=True)
    f.label(P(xx + 30, -18), "start", size=11, color=HELP)
    xx += 60
    for k, (doubled, give) in enumerate(steps):
        f.text(P(xx + 22, 10), "× 2", size=13, bold=True, color=GIVEN)
        xx += 44
        rect(f, xx, 0, 60, 34, fill=BLUE); f.text(P(xx + 30, 10), f"{doubled}", size=15, bold=True)
        f.label(P(xx + 30, -18), f"pond {k + 1}", size=11, color=HELP)
        f.label(P(xx + 30, 46), f"− {give} to shrine {k + 1}", size=11, color=ASK)
        xx += 60
        if k < 2:
            f.text(P(xx + 22, 10), "→", size=15, bold=True)
            xx += 44
            rect(f, xx, 0, 40, 34, fill=YELLOW); f.text(P(xx + 20, 10), f"{doubled - give}", size=15, bold=True)
            xx += 40
    f.label(P(xx + 10, 10), "0 left", anchor="start", size=13, bold=True, color=ANS)
    return f

@fig
def karim():
    f = Fig("karim")
    coins, fee = 7, 8
    xx = 0
    rect(f, xx, 0, 50, 34, fill=YELLOW); f.text(P(xx + 25, 10), str(coins), size=15, bold=True)
    xx += 50
    for k in range(3):
        coins *= 2
        f.text(P(xx + 24, 10), "× 2", size=13, bold=True, color=GIVEN); xx += 48
        rect(f, xx, 0, 50, 34, fill=BLUE); f.text(P(xx + 25, 10), str(coins), size=15, bold=True)
        f.label(P(xx + 25, -18), f"round {k + 1}", size=11, color=HELP)
        xx += 50
        coins -= fee
        f.text(P(xx + 24, 10), "− 8", size=13, bold=True, color=ASK); xx += 48
        rect(f, xx, 0, 50, 34, fill=YELLOW); f.text(P(xx + 25, 10), str(coins), size=15, bold=True)
        xx += 50
    assert coins == 0
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
