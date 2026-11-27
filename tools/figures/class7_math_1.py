"""Figures for class 7 maths Ch 1, Large Numbers Around Us. Every number drawn is computed
here and asserted, so a label can never disagree with the picture."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "1")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def indian(n):
    s = str(n); head, tail = s[:-3], s[-3:]
    groups = []
    while len(head) > 2: groups.insert(0, head[-2:]); head = head[:-2]
    if head: groups.insert(0, head)
    return ",".join(groups + [tail]) if groups else tail

def american(n):
    return f"{n:,}"

assert indian(9876501234) == "9,87,65,01,234" and american(9876501234) == "9,876,501,234"
assert indian(67285183) == "6,72,85,183" and indian(100000) == "1,00,000"

# ---------------------------------------------------------------- heights compared with Somu's building
@fig
def heights():
    f = Fig("heights"); k = 0.6                      # 1 metre = 0.6 units
    floors, floor_h = 10, 4                          # each floor is 4 times Somu's 1 m
    building = floors * floor_h
    assert building == 40
    for m in range(0, 501, 100):
        f.seg(P(-8, m * k), P(0, m * k), w=1.4); f.label(P(-14, m * k), str(m), anchor="end", size=12)
    f.seg(P(0, 0), P(0, 500 * k), w=1.4); f.seg(P(0, 0), P(470, 0), w=1.4)
    f.label(P(-40, 250 * k), "metres", size=12, anchor="end")
    items = [("Somu", 1, "#ffb74d"), ("building", building, "#90a4ae"), ("Statue of Unity", 180, "#81c784"), ("Kunchikal falls", 450, "#64b5f6")]
    for i, (name, h, col) in enumerate(items):
        x = 30 + i * 110
        box(f, x, 0, 70, max(h * k, 1.5), fill=col)
        f.label(P(x + 35, h * k + 12), f"{h} m", bold=True, size=13)
        f.label(P(x + 35, -16), name, size=13)
        if name == "building":
            for j in range(1, floors):
                f.seg(P(x, j * floor_h * k), P(x + 70, j * floor_h * k), w=0.8)
    assert 180 - building == 140 and 450 - building == 410
    return f

# ---------------------------------------------------------------- Indian and American comma groups
@fig
def comma_groups():
    f = Fig("comma_groups"); n = 9876501234; s = str(n); w = 38
    for i, d in enumerate(s):
        box(f, i * w, 0, w - 4, 40, fill="#fff8e1"); f.label(P(i * w + (w - 4) / 2, 20), d, bold=True, size=20)
    def brackets(groups, y, up, names, color):
        i = 0
        for g, name in zip(groups, names):
            x0, x1 = i * w + 2, (i + len(g)) * w - 6
            yy = y + (8 if up else -8)
            f.seg(P(x0, y), P(x0, yy), color=color, w=1.6); f.seg(P(x1, y), P(x1, yy), color=color, w=1.6)
            f.seg(P(x0, yy), P(x1, yy), color=color, w=1.6)
            f.label(P((x0 + x1) / 2, yy + (14 if up else -14)), name, color=color, size=13, bold=True)
            i += len(g)
        assert "".join(groups) == s
    ind = indian(n).split(","); ame = american(n).split(",")
    brackets(ind, 48, True, ["arab", "crore", "lakh", "thousand", "hundreds"], GIVEN)
    brackets(ame, -8, False, ["billion", "million", "thousand", "hundreds"], ANS)
    f.label(P(-12, 74), "Indian", color=GIVEN, anchor="end", size=13)
    f.label(P(-12, -34), "American", color=ANS, anchor="end", size=13)
    f.label(P(len(s) * w + 8, 74), indian(n), color=GIVEN, anchor="start", size=14)
    f.label(P(len(s) * w + 8, -34), american(n), color=ANS, anchor="start", size=14)
    return f

# ---------------------------------------------------------------- rounding on a number line
@fig
def rounding_line():
    f = Fig("rounding_line"); lo, hi, n = 6_72_00_000, 6_73_00_000, 6_72_85_183
    L = 520; X = lambda v: (v - lo) / (hi - lo) * L
    f.seg(P(0, 0), P(L, 0), w=2)
    for v in range(lo, hi + 1, 10_000):
        big = v in (lo, hi, (lo + hi) // 2)
        f.seg(P(X(v), -6 if not big else -10), P(X(v), 6 if not big else 10), w=1.4 if not big else 2.2)
    f.label(P(X(lo), -26), indian(lo), size=13); f.label(P(X(hi), -26), indian(hi), size=13)
    mid = (lo + hi) // 2
    f.label(P(X(mid), -26), indian(mid) + " (halfway)", size=12, color=HELP)
    f.dot(P(X(n), 0), color=ASK); f.label(P(X(n), 22), indian(n), color=ASK, bold=True, size=14)
    assert hi - n == 14_817 and n - lo == 85_183 and hi - n < n - lo
    f.seg(P(X(n), 40), P(X(hi), 40), color=ANS, w=2); f.label(P((X(n) + X(hi)) / 2, 52), "14,817", color=ANS, size=12)
    f.seg(P(X(lo), 40), P(X(n), 40), color=HELP, w=1.4, dash="5,4"); f.label(P((X(lo) + X(n)) / 2, 52), "85,183", color=HELP, size=12)
    return f

# ---------------------------------------------------------------- toothpick (seven-stick) digits
SEG = {0: "abcdef", 1: "bc", 2: "abged", 3: "abgcd", 4: "fgbc", 5: "afgcd", 6: "afgedc", 7: "abc", 8: "abcdefg", 9: "abcdfg"}
def sticks(s): return sum(len(SEG[int(c)]) for c in s)
assert sticks("7") == 3 and sticks("42019") == 23 and sticks("5108") == 20 and sticks("2008") == 24

def digit(f, x, d, col="#d32f2f", s=26):
    pts = {"a": (P(x, 2 * s), P(x + s, 2 * s)), "b": (P(x + s, 2 * s), P(x + s, s)), "c": (P(x + s, s), P(x + s, 0)),
           "d": (P(x, 0), P(x + s, 0)), "e": (P(x, s), P(x, 0)), "f": (P(x, 2 * s), P(x, s)), "g": (P(x, s), P(x + s, s))}
    for k in SEG[d]:
        p, q = pts[k]; f.seg(p, q, color=col, w=4.5)

@fig
def toothpick_digits():
    f = Fig("toothpick_digits")
    for d in range(10):
        x = d * 50; digit(f, x, d)
        f.label(P(x + 13, -18), f"{len(SEG[d])}", color=GIVEN, bold=True, size=14)
    f.label(P(-12, -18), "sticks:", anchor="end", size=13)
    return f

# ---------------------------------------------------------------- number cards (end-of-chapter Q9)
def cards(name, top=None, bot=None):
    f = Fig(name); w = 46
    for i in range(7):
        box(f, i * w, 60, w - 6, 44, fill="#ffe0b2")
        if top: f.label(P(i * w + (w - 6) / 2, 82), top[i], bold=True, size=20)
    for i in range(5):
        box(f, (i + 2) * w, 0, w - 6, 44, fill="#d1c4e9")
        if bot: f.label(P((i + 2) * w + (w - 6) / 2, 22), bot[i], bold=True, size=20)
    return f

@fig
def cards_q():
    return cards("cards_q")

@fig
def cards_sum():
    a, b = "9987654", "87654"
    assert sorted(a + b) == sorted("99887766554433"[:12]) and int(a) + int(b) == 1_00_75_308
    return cards("cards_sum", a, b)

@fig
def cards_diff():
    a, b = "1122334", "99887"
    assert int(a) - int(b) == 10_22_447
    return cards("cards_diff", a, b)

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
