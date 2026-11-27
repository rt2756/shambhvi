"""Figures for class 7 maths Ch 6, Number Play. The numbers the children call out are
computed from the drawn heights, dot pictures are counted, and the rhythm list is generated
and checked against the Virahanka numbers, so no label can disagree with its picture."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "6")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def circle(f, c, r, fill, color=INK):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, 20)], fill=fill, color=color)

COLS = ["#e57373", "#64b5f6", "#ffb74d", "#81c784", "#ba68c8", "#4db6ac", "#f06292"]

def calls(heights):
    """Each child says how many children in front (to the left) are taller."""
    return [sum(1 for j in range(i) if heights[j] > heights[i]) for i in range(len(heights))]

def people(f, heights, said, show):
    k = 0.9
    for i, h in enumerate(heights):
        x = i * 46; top = (h - 100) * k * 1.6
        col = COLS[i % len(COLS)]
        f.seg(P(x, 0), P(x, top - 18), color=col, w=3)                       # body
        f.seg(P(x - 9, 0), P(x, 22), color=col, w=2.4); f.seg(P(x + 9, 0), P(x, 22), color=col, w=2.4)
        circle(f, P(x, top - 9), 9, "#ffffff", color=col)                  # head
        f.label(P(x, top + 14), said[i] if show else "?", size=15, bold=True, color=ANS if show else ASK)
        f.label(P(x, -14), f"{h}", size=11, color=HELP)
    f.label(P(-30, -14), "cm", size=11, color=HELP, anchor="end")
    f.label(P(-30, 30), "front", size=12, anchor="end", color=GIVEN, bold=True)

@fig
def heights_example():
    f = Fig("heights_example")
    h = [140, 155, 125, 160, 150, 135, 165]
    said = calls(h); assert said == [0, 0, 2, 0, 2, 4, 0]
    people(f, h, [str(s) for s in said], True)
    return f

@fig
def heights_practice():
    f = Fig("heights_practice")
    h = [130, 150, 140, 160, 135, 165, 145]
    assert calls(h) == [0, 0, 1, 0, 3, 0, 3]
    people(f, h, None, False)
    return f

# ---------------------------------------------------------------- even and odd as pairs of dots
def dots(f, x0, n, color, extra_color=ASK):
    for i in range(n):
        col, row = divmod(i, 2)
        f.dot(P(x0 + col * 14, row * 14), color=extra_color if (n % 2 and i == n - 1) else color)
    return x0 + ((n + 1) // 2) * 14

@fig
def pairs():
    f = Fig("pairs"); x = 0
    for n in (4, 6, 8, 5, 7, 9):
        end = dots(f, x, n, GIVEN)
        f.label(P((x + end - 14) / 2, -18), str(n), size=13, bold=True, color=GIVEN if n % 2 == 0 else ASK)
        x = end + 24
    f.label(P(70, 40), "even: all in pairs", size=13, color=GIVEN)
    f.label(P(x - 120, 40), "odd: one left over", size=13, color=ASK)
    return f

@fig
def odd_plus_odd():
    f = Fig("odd_plus_odd")
    a, b = 5, 7
    end = dots(f, 0, a, GIVEN)
    f.label(P(end + 2, 7), "+", size=18, bold=True)
    end2 = dots(f, end + 20, b, ANS)
    f.label(P(end2 + 4, 7), "=", size=18, bold=True)
    # the two leftovers join into one new pair
    x0 = end2 + 26
    for i in range((a - 1) // 2 + (b - 1) // 2):
        f.dot(P(x0 + i * 14, 0), color=INK); f.dot(P(x0 + i * 14, 14), color=INK)
    xl = x0 + ((a - 1) // 2 + (b - 1) // 2) * 14
    f.dot(P(xl, 0), color=ASK); f.dot(P(xl, 14), color=ASK)
    assert (a + b) % 2 == 0 and (a - 1) // 2 + (b - 1) // 2 + 1 == (a + b) // 2
    f.label(P(xl + 10, -18), "the two leftovers make a pair: 12 is even", size=13, color=ASK, anchor="end")
    return f

# ---------------------------------------------------------------- small squares in grids
@fig
def grids():
    f = Fig("grids"); s = 16; x0 = 0
    for r, c in ((3, 3), (3, 4)):
        for i in range(c):
            for j in range(r):
                box(f, x0 + i * s, j * s, s, s, fill="#c8e6c9" if (r * c) % 2 == 0 else "#ffe0b2")
        n = r * c
        f.label(P(x0 + c * s / 2, -16), f"{r} × {c} = {n}, {'even' if n % 2 == 0 else 'odd'}", size=13, bold=True)
        x0 += c * s + 70
    return f

# ---------------------------------------------------------------- rhythms of short and long syllables
def rhythms(n):
    if n == 0: return [[]]
    if n < 0: return []
    return [[1] + r for r in rhythms(n - 1)] + [[2] + r for r in rhythms(n - 2)]

@fig
def rhythms_4():
    f = Fig("rhythms_4"); u = 44; h = 18
    rs = rhythms(4); assert len(rs) == 5
    for k, r in enumerate(rs):
        y = -k * (h + 10); x = 0
        for b in r:
            box(f, x, y, b * u - 4, h, fill="#bbdefb" if b == 1 else "#ffcc80")
            f.label(P(x + (b * u - 4) / 2, y + h / 2), "short" if b == 1 else "long", size=11)
            x += b * u
        f.label(P(4 * u + 12, y + h / 2), " + ".join(map(str, r)), anchor="start", size=13)
    vir = [len(rhythms(n)) for n in range(1, 9)]
    assert vir == [1, 2, 3, 5, 8, 13, 21, 34]
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
