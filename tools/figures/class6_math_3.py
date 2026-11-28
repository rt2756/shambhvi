"""Figures for class 6 maths Ch 3, Number Play. Every number on a picture is recomputed from what
is drawn: children's 'taller neighbours' counts come from the drawn heights, number lines place each
mark at its value, pattern pictures add up their own cells, dice count their pips, and the game line
marks exactly the numbers a winner must say."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class6", "math", "3")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, PURPLE, RED = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0", "#ce93d8", "#ef9a9a"

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK, n=24):
    f.poly([P(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)], fill=fill, color=color)

def fmt(n):
    """Indian commas for 5-digit numbers: 15077 -> 15,077."""
    s = str(n)
    return s if len(s) <= 4 else s[:-3] + "," + s[-3:]

# ---------------------------------------------------------------- 3.1 taller neighbours
def says(h):
    return [sum(1 for j in (i - 1, i + 1) if 0 <= j < len(h) and h[j] > h[i]) for i in range(len(h))]

def children(f, heights, x0=0, expect=None, title=None):
    s = says(heights)
    if expect is not None: assert s == expect, (heights, s)
    for i, (h, n) in enumerate(zip(heights, s)):
        x = x0 + i * 34
        box(f, x, 0, 24, h * 12, fill=[BLUE, ORANGE, GREEN, PINK, PURPLE, YELLOW, RED, GREY][i % 8])
        disc(f, P(x + 12, h * 12 + 22), 11, "#ffffff", color=ASK if n == 2 else INK)
        f.text(P(x + 12, h * 12 + 17), str(n), bold=True, size=14, color=ASK if n == 2 else INK)
    if title: f.label(P(x0, -20), title, anchor="start", size=12, color=HELP)
    return s

@fig
def heights_intro():
    f = Fig("heights_intro")
    children(f, [7, 4, 5, 6, 8, 3, 5, 7], expect=[0, 2, 1, 1, 0, 2, 1, 0],
             title="Each child says how many of their neighbours are taller.")
    return f

@fig
def heights_ascending():
    f = Fig("heights_ascending")
    children(f, [3, 4, 5, 6, 7], expect=[1, 1, 1, 1, 0], title="Shortest to tallest: 1, 1, 1, 1, 0")
    return f

@fig
def heights_01210():
    f = Fig("heights_01210")
    children(f, [7, 5, 3, 4, 6], expect=[0, 1, 2, 1, 0], title="Tall, shorter, shortest, taller, tall: 0, 1, 2, 1, 0")
    return f

@fig
def heights_two_2s():
    f = Fig("heights_two_2s")
    children(f, [5, 3, 7, 4, 6], expect=[0, 2, 0, 2, 0], title="Short children in places 2 and 4: two of them say 2")
    return f

# ---------------------------------------------------------------- 3.3 number lines
def numline(f, y, lo, step, n, k=48, labels=None, given=(), x0=0, fmtf=fmt):
    """n equally spaced ticks lo, lo + step, ...; labels: which indices to write (None = all)."""
    f.seg(P(x0 - 18, y), P(x0 + (n - 1) * k + 18, y), w=1.8)
    for d in (-1, 1):
        e = x0 - 18 if d < 0 else x0 + (n - 1) * k + 18
        f.seg(P(e, y), P(e - 7 * d, y + 5), w=1.8); f.seg(P(e, y), P(e - 7 * d, y - 5), w=1.8)
    vals = [lo + i * step for i in range(n)]
    for i, v in enumerate(vals):
        x = x0 + i * k
        f.seg(P(x, y - 7), P(x, y + 7), w=1.8)
        if labels is None or i in labels:
            f.label(P(x, y - 24), fmtf(v), size=11, bold=i in given, color=INK if (labels is not None or i in given) else ANS)
    return vals

LINES = [("a", 1990, 5, {4: 2010, 6: 2020}), ("b", 9993, 1, {3: 9996, 4: 9997}),
         ("c", 15077, 1, {0: 15077, 1: 15078, 6: 15083}), ("d", 83705, 1000, {3: 86705, 4: 87705})]

def check_lines():
    for name, lo, step, given in LINES:
        for i, v in given.items(): assert lo + i * step == v, (name, i, v)

@fig
def numlines_question():
    check_lines()
    f = Fig("numlines_question")
    for r, (name, lo, step, given) in enumerate(LINES):
        y = -r * 60
        f.label(P(-34, y - 5), name + ".", bold=True, size=14)
        numline(f, y, lo, step, 10, labels=set(given), given=set(given))
    return f

@fig
def numlines_answer():
    check_lines()
    f = Fig("numlines_answer")
    for r, (name, lo, step, given) in enumerate(LINES):
        y = -r * 60
        f.label(P(-34, y - 5), name + ".", bold=True, size=14)
        vals = numline(f, y, lo, step, 10, labels=None, given=set(given))
        # circle the smallest (first) and box the largest (last)
        ring = [P(30 * math.cos(2 * math.pi * t / 40), y - 20 + 12 * math.sin(2 * math.pi * t / 40)) for t in range(41)]
        for p, q in zip(ring, ring[1:]): f.seg(p, q, color=ASK, w=1.6)
        lx = 9 * 48
        f.seg(P(lx - 26, y - 33), P(lx + 26, y - 33), color=ASK, w=1.6); f.seg(P(lx - 26, y - 8), P(lx + 26, y - 8), color=ASK, w=1.6)
        f.seg(P(lx - 26, y - 33), P(lx - 26, y - 8), color=ASK, w=1.6); f.seg(P(lx + 26, y - 33), P(lx + 26, y - 8), color=ASK, w=1.6)
        assert vals[0] == min(vals) and vals[-1] == max(vals)
    f.label(P(-40, -4 * 60 + 10), "Green = filled in. Circle = smallest, box = largest.", anchor="start", size=12, color=HELP)
    return f

@fig
def numline_place():
    f = Fig("numline_place")
    k = 52                                    # pixels per 1000
    f.seg(P(1000 * k / 1000 - 30, 0), P(10000 * k / 1000 + 30, 0), w=1.8)
    for t in range(1000, 10001, 1000):
        x = t * k / 1000
        f.seg(P(x, -7), P(x, 7), w=1.8)
        f.label(P(x, -26), f"{t:,}" if t == 10000 else str(t), size=11)
    nums = sorted([2180, 2754, 1500, 3600, 9950, 9590, 1050, 3050, 5030, 5300, 8400])
    for i, v in enumerate(nums):
        x = v * k / 1000
        up = i % 2 == 0
        y = 30 if up else -46
        f.seg(P(x, 0), P(x, y - 4 if up else y + 14), color=GIVEN, w=1.2)
        disc(f, P(x, 0), 3.2, ASK, color=ASK)
        f.label(P(x, y), str(v), size=11, color=GIVEN, bold=True)
        assert 1000 <= v <= 10000
    return f

# ---------------------------------------------------------------- 3.8 mental maths
MIDS = [25000, 400, 13000, 1500, 60000]
LEFT = [38800, 28000, 61600, 31000]
RIGHT = [3400, 63000, 19500, 20900]

@fig
def mental_boxes():
    f = Fig("mental_boxes")
    def bx(x, y, n, fill):
        box(f, x - 42, y - 13, 84, 26, fill=fill); f.text(P(x, y - 5), f"{n:,}", size=13)
    ys = [0, -46, -92, -138, -184]
    for y, n in zip(ys, MIDS): bx(200, y, n, ORANGE)
    for y, n in zip([-10, -60, -110, -160], LEFT): bx(0, y, n, BLUE)
    for y, n in zip([-10, -60, -110, -160], RIGHT): bx(400, y, n, BLUE)
    # the two examples: 38,800 = 25,000 + 400 + 400 + 13,000 ; 3,400 = 1,500 + 1,500 + 400
    assert 25000 + 400 * 2 + 13000 == 38800 and 1500 * 2 + 400 == 3400
    for y, times in [(0, 1), (-46, 2), (-92, 1)]:
        for t in range(times):
            f.seg(P(158, y + 3 * t), P(42, -10), color=GIVEN, w=1.4)
    for y, times in [(-138, 2), (-46, 1)]:
        for t in range(times):
            f.seg(P(242, y + 3 * t), P(358, -10), color=GIVEN, w=1.4)
    f.label(P(200, 28), "use these as often as you like", size=11, color=HELP)
    return f

# ---------------------------------------------------------------- 3.9 number patterns (our own)
def cell(f, x, y, n, fill, w=34, h=24, size=12):
    box(f, x, y, w, h, fill=fill); f.text(P(x + w / 2, y + h / 2 - 5), str(n), size=size)
    return n

@fig
def pattern_a():
    f = Fig("pattern_a")
    tot = 0
    for r in range(5):
        if r % 2 == 0:
            for c in range(4): tot += cell(f, 30 + c * 60, -r * 34, 40, PINK)
        else:
            for c in range(5): tot += cell(f, c * 60, -r * 34, 50, BLUE)
    assert tot == 12 * 40 + 10 * 50 == 980
    return f

@fig
def pattern_b():
    f = Fig("pattern_b")
    tot = 0
    big = {(i, j) for (a, b) in [(1, 1), (1, 5), (5, 1), (5, 5)] for i in (a, a + 1) for j in (b, b + 1)}
    for i in range(8):
        for j in range(8):
            v = 5 if (i, j) in big else 1
            tot += cell(f, j * 28, -i * 24, v, YELLOW if v == 5 else GREY, w=28)
    assert tot == 48 * 1 + 16 * 5 == 128
    return f

@fig
def pattern_c():
    f = Fig("pattern_c")
    tot = 0
    for i in range(4):
        for j in range(8): tot += cell(f, j * 32, -i * 24, 32, PINK, w=32)
    for i in range(4, 8):
        for j in (0, 1, 2, 7): tot += cell(f, j * 32, -i * 24, 64, PURPLE, w=32)
    assert tot == 32 * 32 + 16 * 64 == 2048
    return f

PIPS = {2: [(-1, 1), (1, -1)], 6: [(-1, 1), (-1, 0), (-1, -1), (1, 1), (1, 0), (1, -1)]}

@fig
def pattern_d():
    f = Fig("pattern_d")
    tot, u = 0, 30
    for i in range(7):
        for j in range(5):
            border = i in (0, 6) or j in (0, 4)
            v = 2 if border else 6
            x, y = j * (u + 3), -i * (u + 3)
            box(f, x, y, u, u, fill=PURPLE if border else RED)
            for dx, dy in PIPS[v]:
                disc(f, P(x + u / 2 + dx * 8, y + u / 2 + dy * 8), 2.8, "#ffffff", color="#ffffff", n=12)
            tot += len(PIPS[v])
    assert tot == 20 * 2 + 15 * 6 == 130
    f.label(P(0, -7 * (u + 3) - 6), "count all the dots", anchor="start", size=12, color=HELP)
    return f

@fig
def pattern_e():
    """A hexagon of six triangles; each triangle holds 15, 35, 25 and 25."""
    f = Fig("pattern_e")
    R, tot = 120, 0
    C = P(0, 0)
    for k in range(6):
        a1, a2 = 90 + 60 * k, 150 + 60 * k
        p1, p2 = along(C, a1, R), along(C, a2, R)
        f.poly([C, p1, p2], fill=YELLOW if k % 2 else ORANGE)
        mid = a1 + 30
        spots = [(along(C, mid - 12, 0.8 * R), 15), (along(C, mid + 12, 0.8 * R), 35),
                 (along(C, mid - 15, 0.45 * R), 25), (along(C, mid + 15, 0.45 * R), 25)]
        for p, v in spots:
            f.text(P(p[0], p[1] - 5), str(v), size=12, bold=True); tot += v
    assert tot == 6 * (15 + 35 + 25 + 25) == 600
    return f

@fig
def pattern_f():
    """Rings of coins: 1000 in the middle, then 4 × 500, 8 × 250 and 16 × 125."""
    f = Fig("pattern_f")
    tot = 0
    rings = [(0, 1, 1000, 18), (52, 4, 500, 15), (100, 8, 250, 15), (150, 16, 125, 15)]
    for R, n, v, r in reversed(rings):
        if R: f.circle(P(0, 0), R + 24, color=HELP, w=1.2)
    for R, n, v, r in rings:
        for k in range(n):
            c = along(P(0, 0), 90 + 360 * k / n + (11.25 if n == 16 else 0), R)
            disc(f, c, r, GREEN)
            f.text(P(c[0], c[1] - 4), str(v), size=10 if v < 1000 else 11, bold=True, color=ASK)
            tot += v
    assert [n * v for _, n, v, _ in rings] == [1000, 2000, 2000, 2000] and tot == 7000
    return f

@fig
def pattern_own_300():
    f = Fig("pattern_own_300")
    tot = 0
    for i in range(4):
        for j in range(4):
            if i in (0, 3) or j in (0, 3): tot += cell(f, j * 36, -i * 26, 25, GREEN, w=36, h=26)
    assert tot == 12 * 25 == 300
    return f

# ---------------------------------------------------------------- 3.12 game of 21
@fig
def game21():
    f = Fig("game21")
    k = 26
    win = [n for n in range(1, 22) if (21 - n) % 4 == 0]
    assert win == [1, 5, 9, 13, 17, 21]
    f.seg(P(-10, 0), P(21 * k + 10, 0), w=1.6)
    for n in range(0, 22):
        x = n * k
        f.seg(P(x, -5), P(x, 5), w=1.4)
        if n in win:
            disc(f, P(x, -20), 11, GREEN)
        f.text(P(x, -25), str(n), size=11, bold=n in win)
    for a, b in zip(win, win[1:]):
        f.carc(P((a + b) / 2 * k, 2), 2 * k, 20, 160, color=GIVEN, w=1.6)
        f.label(P((a + b) / 2 * k, 2 * k + 8), "4", size=11, color=GIVEN)
    f.label(P(0, -52), "Say the green numbers: whatever your friend adds (1, 2 or 3), you add the rest of 4.", anchor="start", size=12, color=HELP)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
