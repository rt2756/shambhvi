"""Figures for class 7 maths Ch 12, Another Peek Beyond the Point. Areas, shaded-square counts,
arrow positions and long-division remainders are computed with exact decimals/fractions and
asserted against the values written in the notes."""
import os, sys
from decimal import Decimal as D
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "12")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, ORANGE, GREY = "#bbdefb", "#fff176", "#a5d6a7", "#ffcc80", "#eeeeee"

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def head(f, tip, a, color=INK, s=9):
    for d in (+28, -28):
        f.seg(along(tip, a + 180 + d, s), tip, color=color, w=2)

@fig
def rect_area():
    f = Fig("rect_area"); k = 18
    w, h = D("13.3"), D("5.7")
    box(f, 0, 0, float(w) * k, float(h) * k, fill=BLUE)
    f.label(P(float(w) * k / 2, -16), "13.3 cm", bold=True)
    f.label(P(float(w) * k + 10, float(h) * k / 2), "5.7 cm", bold=True, anchor="start")
    assert w * h == D("75.81")
    f.label(P(float(w) * k / 2, float(h) * k / 2), "area = 5.7 × 13.3 = 75.81 sq cm", color=ANS, bold=True, size=14)
    return f

@fig
def grid_07x04():
    f = Fig("grid_07x04"); c = 22; cols, rows = 7, 4
    both = 0
    for i in range(10):
        for j in range(10):
            inc, inr = i < cols, j < rows
            fill = GREEN if (inc and inr) else BLUE if inc else "#ffffff"
            both += inc and inr
            box(f, i * c, j * c, c, c, fill=fill, color="#90a4ae")
    box(f, 0, 0, 10 * c, 10 * c, fill="none")
    assert F(both, 100) == F(7, 10) * F(4, 10) == F(28, 100)
    f.label(P(cols * c / 2, 10 * c + 14), "0.7 (7 columns)", color=GIVEN, bold=True, size=13)
    f.label(P(10 * c + 10, rows * c / 2), "0.4 of it (4 rows)", anchor="start", color=ANS, bold=True, size=13)
    f.label(P(5 * c, -18), "28 of 100 squares: 0.7 × 0.4 = 0.28", color=ANS, bold=True, size=14)
    return f

@fig
def ribbon():
    f = Fig("ribbon"); L = 390   # px for 3.9 m
    n = 10; piece = D("3.9") / n
    assert piece == D("0.39")
    for i in range(n):
        box(f, i * L / n, 0, L / n, 24, fill=ORANGE if i % 2 == 0 else YELLOW)
    f.label(P(L / 20, -16), "0.39 m", size=12, color=ANS, bold=True)
    f.seg(P(0, 40), P(L, 40), color=GIVEN, w=1.6)
    f.seg(P(0, 34), P(0, 46), color=GIVEN, w=1.6); f.seg(P(L, 34), P(L, 46), color=GIVEN, w=1.6)
    f.label(P(L / 2, 54), "3.9 m in 10 equal pieces", color=GIVEN, bold=True, size=13)
    return f

@fig
def arrows():
    f = Fig("arrows"); L = 380
    for (a, b, labels, y, k) in [(D("3.1"), D("3.2"), ("3.1", "3.2"), 0, 6), (D("2.15"), D("2.17"), ("2.15", "2.17"), -110, 6)]:
        f.seg(P(-10, y), P(L + 10, y), w=2)
        for i in range(11):
            x = L * i / 10
            t = 16 if i in (0, 10) else 10 if i == 5 else 7
            f.seg(P(x, y), P(x, y - t), w=1.6)
        f.label(P(0, y - 30), labels[0], size=13, bold=True)
        f.label(P(L, y - 30), labels[1], size=13, bold=True)
        x = L * k / 10
        f.seg(P(x, y + 34), P(x, y + 6), color=ASK, w=2.2); head(f, P(x, y + 4), 270, color=ASK)
        val = a + (b - a) / 10 * k
        assert val in (D("3.16"), D("2.162"))
    return f

@fig
def cycle_7():
    f = Fig("cycle_7"); R = 90
    rems, digits, r = [], [], 1
    while True:
        rems.append(r); digits.append(r * 10 // 7); r = r * 10 % 7
        if r == 1: break
    assert rems == [1, 3, 2, 6, 4, 5] and "".join(map(str, digits)) == "142857"
    n = len(rems)
    for i, (rm, dg) in enumerate(zip(rems, digits)):
        a = 90 - 360 * i / n
        p = along(P(0, 0), a, R)
        f.circle(p, 18, color=GIVEN, w=2)
        f.label(p, str(rm), bold=True, size=16, color=GIVEN)
        a2 = a - 360 / n
        q = along(P(0, 0), a2, R)
        m = along(P(0, 0), (a + a2) / 2, R + 6)
        f.carc(P(0, 0), R, a2 + 13, a - 13, color=HELP, w=1.8)
        head(f, along(P(0, 0), a2 + 13, R), a2 + 13 - 90, color=HELP, s=8)
        f.label(along(P(0, 0), (a + a2) / 2, R + 26), f"digit {dg}", size=12, color=ANS, bold=True)
    f.label(P(0, 8), "remainders", size=12, color=GIVEN, bold=True)
    f.label(P(0, -10), "of 1 ÷ 7", size=12, color=GIVEN, bold=True)
    return f

@fig
def leap_rule():
    f = Fig("leap_rule"); w, h, gap = 230, 34, 62
    qs = ["divisible by 400?", "divisible by 100?", "divisible by 4?"]
    yes = ["366 days (leap)", "365 days", "366 days (leap)"]
    def leap(y):
        return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)
    assert [leap(y) for y in (2000, 1900, 2024, 2023)] == [True, False, True, False]
    for i, q in enumerate(qs):
        y = -i * gap
        box(f, 0, y, w, h, fill=BLUE)
        f.label(P(w / 2, y + h / 2), "Is the year " + q, size=13, bold=True)
        f.seg(P(w, y + h / 2), P(w + 50, y + h / 2), color=ANS, w=2); head(f, P(w + 50, y + h / 2), 0, color=ANS)
        f.label(P(w + 25, y + h / 2 + 12), "yes", size=12, color=ANS, bold=True)
        f.label(P(w + 58, y + h / 2), yes[i], size=13, anchor="start", color=ANS, bold=True)
        f.seg(P(w / 2, y), P(w / 2, y - gap + h + 4), color=ASK, w=2); head(f, P(w / 2, y - gap + h + 2), 270, color=ASK)
        f.label(P(w / 2 + 16, y - (gap - h) / 2), "no", size=12, color=ASK, bold=True)
    yb = -3 * gap + h
    f.label(P(w / 2, yb - 8), "365 days", size=13, bold=True, color=ASK)
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
