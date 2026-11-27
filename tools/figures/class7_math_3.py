"""Figures for class 7 maths Ch 3, A Peek Beyond the Point. Number lines and rulers are drawn
from exact fractions; every marked value is checked against its tick position."""
import os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "3")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def dec(v):
    """Exact decimal string of a Fraction with denominator 10^k."""
    v = Fr(v); s = "-" if v < 0 else ""; v = abs(v)
    k = 0
    while (v * 10 ** k).denominator != 1: k += 1
    assert k <= 4, v
    n = int(v * 10 ** k); whole, frac = divmod(n, 10 ** k)
    return s + (f"{whole}.{frac:0{k}d}" if k else str(whole))

assert dec(Fr(4185, 1000)) == "4.185" and dec(Fr(7, 2)) == "3.5" and dec(Fr(3069, 1000)) == "3.069"

def numline(f, y, a, b, n, L=480, x0=0, labels=(), marks=(), boxes=(), sub=None, big=()):
    """Number line from a to b (Fractions) split into n equal steps. labels: values to print under
    their ticks; marks: (value, text, colour) arrows above; boxes: (value, text) boxes below.
    Every marked value must sit exactly on a tick (or sub-tick if sub is given)."""
    a, b = Fr(a), Fr(b); step = (b - a) / n
    X = lambda v: x0 + float((Fr(v) - a) / (b - a)) * L
    f.seg(P(x0 - 12, y), P(x0 + L + 12, y), w=1.8)
    ticks = [a + i * step for i in range(n + 1)]
    for t in ticks:
        h = 9 if (t in big or t in (a, b)) else 6
        f.seg(P(X(t), y - h), P(X(t), y + h), w=1.8 if h == 9 else 1.3)
    if sub:
        for i in range(n * sub + 1):
            t = a + i * step / sub
            if t not in ticks: f.seg(P(X(t), y - 3), P(X(t), y + 3), w=0.9)
    fine = step / (sub or 1)
    for v in labels:
        assert (Fr(v) - a) % step == 0, f"label {v} not on a tick"
        f.label(P(X(v), y - 22), dec(v), size=12)
    for v, t, col in marks:
        assert (Fr(v) - a) % fine == 0 and a <= Fr(v) <= b, f"{f.name}: mark {v} not on a tick"
        f.seg(P(X(v), y + 30), P(X(v), y + 4), color=col, w=2)
        f.seg(P(X(v) - 4, y + 11), P(X(v), y + 4), color=col, w=2); f.seg(P(X(v) + 4, y + 11), P(X(v), y + 4), color=col, w=2)
        f.label(P(X(v), y + 42), t, color=col, bold=True, size=13)
    for v, t in boxes:
        assert (Fr(v) - a) % fine == 0, f"{f.name}: box {v} not on a tick"
        f.seg(P(X(v), y - 8), P(X(v), y - 40), w=1.4)
        box(f, X(v) - 16, y - 66, 32, 26); f.label(P(X(v), y - 53), t, size=13, bold=True)
    return X

# ---------------------------------------------------------------- reading a ruler in tenths
@fig
def ruler_objects():
    f = Fig("ruler_objects"); k = 100        # 1 cm = 100 units
    items = [("eraser", Fr(24, 10), "#90caf9"), ("pencil", Fr(45, 10), "#ffcc80"), ("chalk", Fr(14, 10), "#eeeeee")]
    for i, (name, length, col) in enumerate(items):
        y = 30 + (2 - i) * 34
        box(f, 0, y, float(length) * k, 22, fill=col); f.label(P(-8, y + 11), name, anchor="end", size=13)
        f.seg(P(float(length) * k, y - 4), P(float(length) * k, 0), color=ASK, w=1, dash="3,3")
    for mm in range(0, 51):
        h = 14 if mm % 10 == 0 else (9 if mm % 5 == 0 else 5)
        f.seg(P(mm * k / 10, 0), P(mm * k / 10, -h), w=1.2 if h == 14 else 0.8)
        if mm % 10 == 0: f.label(P(mm * k / 10, -26), str(mm // 10), size=13)
    f.seg(P(0, 0), P(500, 0), w=1.4); f.label(P(510, -26), "cm", anchor="start", size=12)
    return f

# ---------------------------------------------------------------- 3.4 = 34 tenths
@fig
def tenths_pencil():
    f = Fig("tenths_pencil"); k = 110
    v = Fr(34, 10)
    box(f, 0, 20, float(v) * k, 20, fill="#a5d6a7")
    for t in range(0, 41):
        h = 12 if t % 10 == 0 else 5
        f.seg(P(t * k / 10, 0), P(t * k / 10, -h), w=1.2 if h == 12 else 0.8)
        if t % 10 == 0: f.label(P(t * k / 10, -24), str(t // 10), size=13)
    f.seg(P(0, 0), P(4 * k, 0), w=1.4)
    for t in range(0, 34):
        f.seg(P(t * k / 10, 20), P(t * k / 10, 40), color=INK, w=0.6)
    assert v == 3 + Fr(4, 10) == 34 * Fr(1, 10)
    f.label(P(float(v) * k + 8, 30), "3 units + 4 tenths = 34 tenths", anchor="start", size=13, color=GIVEN, bold=True)
    return f

# ---------------------------------------------------------------- hundredths: zooming into a tenth
@fig
def hundredths_zoom():
    f = Fig("hundredths_zoom")
    numline(f, 90, 4, 5, 10, labels=[4, 5, Fr(44, 10), Fr(45, 10)], marks=[(Fr(44, 10), "", HELP)])
    f.seg(P(4 * 48, 80), P(0, 18), color=HELP, w=1, dash="4,3"); f.seg(P(5 * 48, 80), P(480, 18), color=HELP, w=1, dash="4,3")
    numline(f, 0, Fr(44, 10), Fr(45, 10), 10, labels=[Fr(44, 10), Fr(45, 10)], marks=[(Fr(445, 100), "4.45", ASK)], big=[Fr(445, 100)])
    return f

# ---------------------------------------------------------------- one unit split in 10 or in 4
@fig
def quarters():
    f = Fig("quarters"); L = 360
    v = Fr(3, 2)
    for y, n, name in ((70, 10, "tenths"), (0, 4, "quarters")):
        f.seg(P(0, y), P(2 * L / 2 * 1, y), w=1.6)
        for i in range(2 * n + 1):
            t = Fr(i, n); h = 10 if t.denominator == 1 else 5
            f.seg(P(float(t) * L / 2 * 1, y - h), P(float(t) * L / 2, y + h), w=1.2)
            if t.denominator == 1: f.label(P(float(t) * L / 2, y - 22), str(int(t)), size=13)
        assert (v * n).denominator == 1
        f.seg(P(0, y + 16), P(float(v) * L / 2, y + 16), color=ASK, w=4)
        f.label(P(float(v) * L / 2 + 10, y + 16), f"1 and {int((v - 1) * n)} {name}", anchor="start", color=ASK, size=13, bold=True)
    return f

# ---------------------------------------------------------------- find the lengths in the boxes
@fig
def boxes_line():
    f = Fig("boxes_line")
    vals = [Fr(5, 100), Fr(47, 100), Fr(108, 100), Fr(16, 10), Fr(215, 100)]
    numline(f, 0, 0, Fr(22, 10), 22, L=640, labels=[0, 1, 2], sub=10,
            boxes=[(v, chr(ord("a") + i)) for i, v in enumerate(vals)])
    return f

# ---------------------------------------------------------------- wires on zoomed rulers
@fig
def wires():
    f = Fig("wires")
    for i, (lo, end) in enumerate(((Fr(49, 10), Fr(537, 100)), (Fr(144, 10), Fr(1503, 100)), (Fr(67, 10), Fr(752, 100)), (Fr(89, 10), Fr(98, 10)))):
        y = -i * 80
        X = numline(f, y, lo, lo + Fr(12, 10), 12, L=520, sub=10, labels=[lo + Fr(j, 10) for j in range(0, 13, 2)])
        assert lo < end < lo + Fr(12, 10) and (end * 100).denominator == 1
        f.seg(P(-12, y + 18), P(X(end), y + 18), color="#d32f2f", w=5)
        f.label(P(-20, y + 18), chr(ord("a") + i), anchor="end", bold=True, size=14)
    return f

# ---------------------------------------------------------------- zooming in to 4.185
def zoom(name, target, ask=False):
    f = Fig(name); t = Fr(target)
    lo, step, y = Fr(0), Fr(1), 0
    for level in range(4):
        hi = lo + 10 * step
        k = (t - lo) // step
        last = level == 3
        lab = [lo, hi] if level else [lo, hi]
        mark = [(t, "?" if ask else dec(t), ASK)] if last else [(lo + k * step, "", HELP)]
        if last: assert (t - lo) % step == 0
        X = numline(f, y, lo, hi, 10, labels=lab, marks=mark)
        if not last:
            f.seg(P(X(lo + k * step), y - 8), P(0, y - 92 + 12), color=HELP, w=1, dash="4,3")
            f.seg(P(X(lo + (k + 1) * step), y - 8), P(480, y - 92 + 12), color=HELP, w=1, dash="4,3")
            lo, step, y = lo + k * step, step / 10, y - 110
    return f

@fig
def zoom_4185():
    return zoom("zoom_4185", Fr(4185, 1000))

@fig
def zoom_9876():
    return zoom("zoom_9876", Fr(9876, 1000))

@fig
def zoom_0407():
    return zoom("zoom_0407", Fr(407, 1000))

# ---------------------------------------------------------------- reading number lines
@fig
def line_1_11():
    f = Fig("line_1_11")
    numline(f, 0, 1, Fr(13, 10), 3, L=420, labels=[1, Fr(11, 10), Fr(12, 10), Fr(13, 10)], sub=10, marks=[(Fr(104, 100), "1.04", ASK)])
    return f

@fig
def line_AD():
    f = Fig("line_AD")
    numline(f, 0, 5, Fr(54, 10), 4, L=560, labels=[5, Fr(51, 10), Fr(53, 10), Fr(54, 10)], sub=10,
            marks=[(Fr(509, 100), "A", ASK), (Fr(513, 100), "B", ASK), (Fr(52, 10), "C", ASK), (Fr(531, 100), "D", ASK)])
    return f

@fig
def line_abc():
    f = Fig("line_abc")
    numline(f, 0, 5, 10, 10, L=440, labels=[5, 10], boxes=[(6, "a"), (Fr(15, 2), "b"), (Fr(19, 2), "c")])
    return f

@fig
def line_dh():
    f = Fig("line_dh")
    numline(f, 0, 8, Fr(81, 10), 10, L=400, labels=[8, Fr(81, 10)], boxes=[(Fr(801, 100), "d"), (Fr(805, 100), "e")])
    numline(f, -120, Fr(43, 10), Fr(485, 100), 11, L=440, labels=[Fr(43, 10), Fr(48, 10)],
            boxes=[(Fr(435, 100), "f"), (Fr(45, 10), "g"), (Fr(485, 100), "h")])
    return f

@fig
def line_ex3():
    f = Fig("line_ex3")
    numline(f, 0, Fr(64, 10), Fr(66, 10), 8, L=440, labels=[Fr(64, 10), Fr(65, 10), Fr(66, 10)],
            boxes=[(Fr(645, 100), "a"), (Fr(6525, 1000), "c"), (Fr(655, 100), "b")])
    return f

# ---------------------------------------------------------------- ex 15: sum closest to 10.5
def sum_boxes(name, a=None, b=None):
    f = Fig(name); s = 40
    for row, num in ((1, a), (0, b)):
        y = row * 52
        xs = [0, 58, 100, 142]
        for j, x in enumerate(xs):
            box(f, x, y, 34, 40, fill="#fff59d")
            if num: f.label(P(x + 17, y + 20), num[0] if j == 0 else num[1 + j], bold=True, size=20)
        f.dot(P(46, y + 4))
    f.label(P(-18, 20), "+", size=22, bold=True)
    f.seg(P(-24, -10), P(190, -10), w=1.6)
    if a:
        tot = Fr(int(a.replace(".", "")), 1000) + Fr(int(b.replace(".", "")), 1000)
        assert tot == Fr(105, 10) and len(set((a + b).replace(".", ""))) == 8
        f.label(P(95, -32), "= 10.500", bold=True, size=18, color=ANS)
    return f

@fig
def sum_boxes_q():
    return sum_boxes("sum_boxes_q")

@fig
def sum_boxes_ans():
    return sum_boxes("sum_boxes_ans", "2.031", "8.469")

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
