"""Figures for class 8 maths Ch 2, Power Play. Every number written on a picture is computed
from the drawing's own data (layers are 2^n, tree levels are counted, power lines are exact
fractions, the Earth's mark is placed by dividing the two distances), so no label can disagree
with its picture."""
import math, os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "2")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, ORANGE, GREEN, PINK, PURPLE, GREY = "#90caf9", "#ffcc80", "#a5d6a7", "#f48fb1", "#ce93d8", "#eceff1"
COLS = ["#ef9a9a", "#90caf9", "#ffcc80", "#a5d6a7", "#ce93d8", "#80cbc4"]
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
def sup(n): return str(n).translate(SUP)

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK, steps=30):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, steps)], fill=fill, color=color)

def frac_str(q):
    q = Fr(q)
    return str(q.numerator) if q.denominator == 1 else f"1/{q.denominator}" if q.numerator == 1 else f"{q.numerator}/{q.denominator}"

# ---------------------------------------------------------------- folding paper
@fig
def fold_layers():
    f = Fig("fold_layers")
    x = 0
    for n in range(5):
        layers = 2 ** n
        h, w = 5, 70 - 12 * n            # each fold halves the sheet, so draw it a little narrower
        for k in range(layers):
            box(f, x, k * h, w, h, fill=BLUE if k % 2 == 0 else "#bbdefb", color="#1565c0")
        f.label(P(x + w / 2, -16), f"{n} fold{'s' if n != 1 else ''}", size=13, bold=True)
        f.label(P(x + w / 2, -34), f"{layers} layer{'s' if layers > 1 else ''} = 2{sup(n)}", size=12, color=GIVEN)
        x += max(w, 80) + 24
    return f

def thickness_cm(n): return 0.001 * 2 ** n

def indian(n):
    s = str(int(round(n))); head, tail = s[:-3], s[-3:]
    groups = []
    while len(head) > 2: groups.insert(0, head[-2:]); head = head[:-2]
    return ",".join(([head] if head else []) + groups + [tail])

def nice(cm):
    if cm < 100: return f"{cm:.3g} cm"
    if cm < 1e5: return f"{cm/100:.3g} m"
    if cm < 1e8: return f"{cm/1e5:.3g} km"
    return f"{indian(cm/1e5)} km"

@fig
def fold_ladder():
    """Folds 0 to 46 on a line: equal steps of folds are equal 'times 2' steps of thickness."""
    f = Fig("fold_ladder")
    k = 15
    f.seg(P(0, 0), P(46 * k, 0))
    marks = {10: "just over 1 cm", 17: "taller than a child", 26: "most of the way up the Burj Khalifa (830 m)",
             30: "where planes fly", 40: "nearly the Earth's width", 46: "past the Moon (3,84,400 km)"}
    for n in range(47):
        big = n in marks or n == 0
        f.seg(P(n * k, -4 if not big else -8), P(n * k, 4 if not big else 8), w=1.2 if not big else 2.2)
    f.label(P(0, -24), "0", size=12); f.label(P(0, -40), "0.001 cm", size=11, color=HELP)
    assert nice(thickness_cm(10)) == "1.02 cm" and nice(thickness_cm(26)) == "671 m" and nice(thickness_cm(46)) == "7,03,687 km"
    assert 3.844e10 < thickness_cm(46) and thickness_cm(45) < 3.844e10       # 46 folds pass the Moon, 45 do not
    for i, (n, what) in enumerate(sorted(marks.items())):
        y = 22 + 34 * i
        f.seg(P(n * k, 8), P(n * k, y - 4), color=HELP, w=1, dash="3 3")
        f.label(P(n * k - 4, y), f"{n} folds: {nice(thickness_cm(n))}", anchor="end", size=12, bold=True, color=GIVEN)
        f.label(P(n * k - 4, y + 15), what, anchor="end", size=11, color=INK)
    f.label(P(23 * k, -26), "folds (each step = thickness × 2)", size=12, color=HELP)
    return f

# ---------------------------------------------------------------- the stones that shine
@fig
def stones_tree():
    f = Fig("stones_tree")
    W = 640
    levels = [("king", 1), ("daughters", 3), ("baskets", 9), ("keys", 27), ("rooms", 81)]
    prev = None
    for lv, (name, count) in enumerate(levels):
        assert count == 3 ** lv
        y = -lv * 62
        xs = [W * (i + 0.5) / count for i in range(count)]
        if prev:
            for i, x in enumerate(xs):
                f.seg(prev[i // 3], P(x, y), color=HELP, w=1)
        r = [12, 9, 7, 4, 2.4][lv]
        for x in xs:
            disc(f, P(x, y), r, COLS[lv], color=INK if r > 3 else COLS[lv], steps=30 if r > 3 else 60)
        f.label(P(-12, y - 5), f"{name}: {count} = 3{sup(lv)}" if lv else "king: 1", anchor="end", size=13, bold=True)
        prev = [P(x, y) for x in xs]
    return f

# ---------------------------------------------------------------- combinations
@fig
def outfits():
    f = Fig("outfits")
    caps = [(70, "#81c784"), (230, "#e57373"), (390, "#64b5f6")]
    dresses = [(0, "#fff176"), (155, "#aed581"), (310, "#7986cb"), (465, "#ef5350")]
    lines = 0
    for cx, _ in caps:
        for dx, _ in dresses:
            f.seg(P(cx + 30, 100), P(dx + 30, 46), color=HELP, w=1.1); lines += 1
    assert lines == len(caps) * len(dresses) == 12
    for cx, col in caps:      # a cap: half disc with a brim
        f.poly([P(cx + 30 + 24 * math.cos(d2r(a)), 104 + 20 * math.sin(d2r(a))) for a in range(0, 181, 15)], fill=col)
        f.seg(P(cx + 2, 104), P(cx + 66, 104), w=3)
    for dx, col in dresses:   # a T-shirt shape
        f.poly([P(dx + 12, 40), P(dx + 48, 40), P(dx + 60, 28), P(dx + 50, 20), P(dx + 46, 26), P(dx + 46, -10),
                P(dx + 14, -10), P(dx + 14, 26), P(dx + 10, 20), P(dx + 0, 28)], fill=col)
    f.label(P(270, -34), "3 caps × 4 dresses = 12 outfits (one line for each)", size=14, bold=True, color=ANS)
    return f

@fig
def lock_dials():
    f = Fig("lock_dials")
    n, u = 5, 22
    for c in range(n):
        for d in range(10):
            box(f, c * 44, -d * u, 34, u - 2, fill=GREEN if d == 0 else "#ffffff")
            f.text(P(c * 44 + 17, -d * u + 4), str(d), size=13)
    total = 10 ** n
    assert total == 100000
    f.label(P(n * 44 / 2 - 5, 30), "5 dials, 10 choices on each", size=13, bold=True)
    f.label(P(n * 44 / 2 - 5, -10 * u - 12), "10 × 10 × 10 × 10 × 10 = 10⁵ = 1,00,000 passwords", size=13, color=ANS, bold=True)
    return f

# ---------------------------------------------------------------- halving a line
@fig
def halving():
    f = Fig("halving")
    k = 40
    length = Fr(16)
    for i in range(6):
        y = -i * 34
        f.seg(P(0, y), P(float(length) * k, y), color=GIVEN, w=4)
        f.seg(P(0, y - 6), P(0, y + 6)); f.seg(P(float(length) * k, y - 6), P(float(length) * k, y + 6))
        e = 4 - i
        assert length == Fr(2) ** e
        lab = "2⁴ = 16 units" if i == 0 else f"2⁴ ÷ 2{sup(i) if i > 1 else ''} = 2{sup(e)} = {frac_str(length)} unit{'s' if length > 1 else ''}"
        f.label(P(float(length) * k + 12, y - 5), lab, anchor="start", size=13, bold=(e < 0), color=ANS if e < 0 else INK)
        length /= 2
    return f

# ---------------------------------------------------------------- power lines
def power_line(f, base, lo, hi, asks=None):
    g = 30
    f.seg(P(0, (lo - 0.4) * g), P(0, (hi + 0.4) * g), w=2.4)
    for e in range(lo, hi + 1):
        y = e * g
        v = Fr(base) ** e
        f.seg(P(-8, y), P(8, y))
        f.label(P(-16, y - 5), f"{base}{sup(e)}", anchor="end", size=14, bold=True)
        f.label(P(16, y - 5), indian(v.numerator) if v.denominator == 1 else f"1/{indian(v.denominator)}", anchor="start", size=13, color=GIVEN)
    f.label(P(150, (hi - 0.5) * g), f"up one step: × {base}", anchor="start", size=12, color=ANS)
    f.label(P(150, (lo + 0.5) * g), f"down one step: ÷ {base}", anchor="start", size=12, color=ASK)
    f.seg(P(140, (lo + 1.2) * g), P(140, (hi - 1.2) * g), color=HELP, w=1.4)
    f.arrows(P(140, (hi - 1.2) * g + 8), 90, color=HELP)

@fig
def power_line_4():
    f = Fig("power_line_4")
    power_line(f, 4, -2, 8)
    assert 4 ** 8 == 65536 and Fr(4) ** -2 == Fr(1, 16)
    return f

@fig
def power_line_7():
    f = Fig("power_line_7")
    power_line(f, 7, -4, 7)
    assert 7 ** 7 == 823543 and Fr(7) ** -4 == Fr(1, 2401)
    return f

# ---------------------------------------------------------------- lotus pond
@fig
def pond():
    f = Fig("pond")
    s = 90
    for i, day in enumerate(range(26, 31)):
        x = i * (s + 26)
        covered = Fr(2) ** (day - 30)                    # doubles every day, full on day 30
        box(f, x, 0, s, s, fill="#b3e5fc", color="#0277bd")
        w, h = float(s), float(s)          # covered part: halve the width, then the height, ...
        for j in range(30 - day):
            if j % 2 == 0: w /= 2
            else: h /= 2
        assert abs(w * h - float(covered) * s * s) < 1e-9
        box(f, x, 0, w, h, fill=PINK, color="#0277bd")
        f.label(P(x + s / 2, -18), f"day {day}", size=13, bold=True)
        f.label(P(x + s / 2, -36), "full" if covered == 1 else f"{frac_str(covered)} full", size=13, color=ANS if day == 29 else INK, bold=day == 29)
    return f

# ---------------------------------------------------------------- Sun, Earth, Saturn
@fig
def sun_earth_saturn():
    f = Fig("sun_earth_saturn")
    L = 600
    saturn, earth = 1.4335e12, 1.496e11
    t = earth / saturn
    assert abs(t - 0.1044) < 0.0005                      # Earth is about a tenth of the way
    f.seg(P(0, 0), P(L + 40, 0))
    for x, name, col in [(0, "Sun", INK), (t * L, "Earth", ANS), (L, "Saturn", INK)]:
        f.seg(P(x, -8), P(x, 8), color=col, w=2.4)
        f.label(P(x, 16), name, size=14, bold=True, color=col)
    f.label(P(t * L, -24), "1.496 × 10¹¹ m", size=12, color=ANS)
    f.label(P(L, -24), "1.4335 × 10¹² m", size=12)
    f.label(P(t * L + 8, 40), "about 1/10 of the way to Saturn", anchor="start", size=12, color=HELP)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
