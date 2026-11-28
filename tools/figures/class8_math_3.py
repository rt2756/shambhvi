"""Figures for class 8 maths Ch 3, A Story of Numbers. Numerals in old number systems are drawn
by functions that take an ordinary number, split it into landmark numbers and draw the right
symbols; each function reads its own drawing back (counts the symbols it placed) and asserts that
they add up to the number, so a picture can never show a different value from its caption.
The Egyptian, Mesopotamian, Mayan and rod symbols are our own simplified drawings."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "3")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, ORANGE, GREEN, RED, GREY = "#90caf9", "#ffcc80", "#a5d6a7", "#e57373", "#eceff1"
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
def sup(n): return str(n).translate(SUP)

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK, step=30):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, step)], fill=fill, color=color)

def curve(f, pts, color=INK, w=2.2):
    for p, q in zip(pts, pts[1:]):
        f.seg(p, q, color=color, w=w)

# ================================================================ Egyptian numerals
H = 24   # symbol height

def eg_symbol(f, power, x, y, color=INK):
    """Draw the Egyptian symbol for 10^power with its bottom centre at (x, y)."""
    if power == 0:                                   # a stroke
        f.seg(P(x, y), P(x, y + H), color=color)
    elif power == 1:                                 # a heel bone / arch
        f.seg(P(x - 7, y), P(x - 7, y + H - 7), color=color); f.seg(P(x + 7, y), P(x + 7, y + H - 7), color=color)
        f.carc(P(x, y + H - 7), 7, 0, 180, color=color, w=2.2)
    elif power == 2:                                 # a coil of rope
        c = P(x + 1, y + H - 9)
        pts = [along(c, 90 + t * 57.3, 1.5 + 6.5 * t / (3 * math.pi)) for t in [i * 0.3 for i in range(int(3 * math.pi / 0.3) + 1)]]
        curve(f, pts, color=color); f.seg(pts[-1], P(x - 3, y), color=color)
    elif power == 3:                                 # a lotus plant
        f.seg(P(x - 4, y + 5), P(x - 4, y + H - 2), color=color); f.seg(P(x - 4, y + H - 2), P(x + 6, y + H - 2), color=color)
        disc(f, P(x + 9, y + H - 2), 3, "#ffffff", color=color, step=45)
        f.poly([P(x - 10, y), P(x + 2, y), P(x - 4, y + 6)], fill="#ffffff", color=color)
    elif power == 4:                                 # a bent finger
        f.seg(P(x - 6, y), P(x + 3, y + H - 2), color=color); f.seg(P(x - 1, y), P(x + 8, y + H - 6), color=color)
        f.seg(P(x + 3, y + H - 2), P(x + 8, y + H - 6), color=color); f.seg(P(x - 6, y), P(x - 1, y), color=color)
    elif power == 5:                                 # a tadpole
        c = P(x + 3, y + H - 8)
        f.poly([P(c[0] + 6 * math.cos(d2r(a)), c[1] + 4.5 * math.sin(d2r(a))) for a in range(0, 360, 30)], fill="#ffffff", color=color)
        curve(f, [P(x - 3, y + H - 10), P(x - 6, y + 8), P(x - 3, y + 3), P(x - 6, y)], color=color)
    elif power == 6:                                 # a kneeling person with raised arms
        disc(f, P(x, y + H - 3), 3.5, "#ffffff", color=color, step=45)
        f.seg(P(x, y + H - 7), P(x, y + 7), color=color)
        f.seg(P(x, y + H - 10), P(x - 9, y + H - 1), color=color); f.seg(P(x, y + H - 10), P(x + 9, y + H - 1), color=color)
        f.seg(P(x, y + 7), P(x - 7, y), color=color); f.seg(P(x, y + 7), P(x + 6, y + 4), color=color); f.seg(P(x + 6, y + 4), P(x + 6, y), color=color)
    elif power == 7:                                 # the sun
        c = P(x, y + H / 2)
        disc(f, c, 5, "#ffffff", color=color, step=30)
        for a in range(0, 360, 45):
            f.seg(along(c, a, 8), along(c, a, 12), color=color, w=1.8)

def eg_number(f, n, x, y, per_row=3, gap=22):
    """Write n in Egyptian numerals from (x, y) (bottom-left), largest symbols first.
    Returns the x where the numeral ends. Asserts the symbols drawn add up to n."""
    drawn = 0
    for p in range(7, -1, -1):
        c = (n // 10 ** p) % 10 if p < 7 else n // 10 ** 7
        if not c: continue
        rows = math.ceil(c / per_row)
        for k in range(c):
            r, col = divmod(k, per_row)
            eg_symbol(f, p, x + 10 + col * gap, y + (rows - 1 - r) * (H + 6))
            drawn += 10 ** p
        x += min(c, per_row) * gap + 12
    assert drawn == n, (drawn, n)
    return x

def eg_row(f, label, n, y, x0=90, show=None):
    f.label(P(x0 - 14, y + 6), label, anchor="end", size=13, bold=True)
    end = eg_number(f, n, x0, y)
    if show: f.label(P(end + 10, y + 6), show, anchor="start", size=13, color=ANS, bold=True)
    return end

@fig
def egyptian_symbols():
    f = Fig("egyptian_symbols")
    for i in range(8):
        x = i * 62
        eg_symbol(f, i, x + 20, 0)
        f.label(P(x + 20, -18), "1" if i == 0 else "10" if i == 1 else f"10{sup(i)}", size=13, bold=True)
    return f

@fig
def egyptian_324():
    f = Fig("egyptian_324")
    eg_row(f, "324 =", 324, 0, show="3 hundreds, 2 tens, 4 ones")
    return f

@fig
def egyptian_read():
    f = Fig("egyptian_read")
    eg_row(f, "(i)", 276, 110)
    eg_row(f, "(ii)", 4322, 0)
    return f

@fig
def egyptian_answers():
    f = Fig("egyptian_answers")
    for i, n in enumerate([10458, 1023, 2660, 784, 1111, 70707]):
        eg_row(f, f"{n:,} =".replace(",", ""), n, -i * 100, x0=80)
    return f

def eg_sum(name, a, b, show_sum):
    f = Fig(name)
    end = eg_number(f, a, 0, 0)
    f.label(P(end + 6, 20), "and", size=14, anchor="start")
    eg_number(f, b, end + 46, 0)
    if show_sum:
        f.label(P(-6, -84), "Sum:", size=14, anchor="end", bold=True, color=ANS)
        e = eg_number(f, a + b, 0, -100)
        f.label(P(e + 8, -94), f"= {a + b}", size=14, anchor="start", bold=True, color=ANS)
    return f

@fig
def egyptian_add_example():
    f = Fig("egyptian_add_example")
    e = eg_number(f, 87, 0, 0)
    f.label(P(e + 6, 20), "+", size=18, anchor="start", bold=True)
    e2 = eg_number(f, 78, e + 30, 0)
    f.label(P(e2 + 8, 20), "=", size=18, anchor="start", bold=True)
    e3 = eg_number(f, 165, e2 + 36, 0)
    assert 87 + 78 == 165
    f.label(P(0, -40), "15 tens and 15 ones → 10 tens make a hundred, 10 ones make a ten → 1 hundred, 6 tens, 5 ones", anchor="start", size=12, color=HELP)
    return f

@fig
def egyptian_add_q1():
    return eg_sum("egyptian_add_q1", 9608, 507, False)

@fig
def egyptian_add_q2():
    return eg_sum("egyptian_add_q2", 1080, 46, False)

@fig
def egyptian_add_a1():
    return eg_sum("egyptian_add_a1", 9608, 507, True)

@fig
def egyptian_add_a2():
    return eg_sum("egyptian_add_a2", 1080, 46, True)

@fig
def egyptian_products():
    """The landmark-number products to work out (pictures only, no answers)."""
    f = Fig("egyptian_products")
    sets = [("× ten", [(1, 1), (2, 1), (3, 1), (4, 1)]),
            ("× hundred", [(1, 2), (2, 2), (3, 2), (4, 2)]),
            ("other products", [(1, 5), (2, 3), (3, 3), (4, 6)])]
    for r, (name, pairs) in enumerate(sets):
        y = -r * 60
        f.label(P(-10, y + 6), f"{chr(65 + r)}.", anchor="end", size=14, bold=True)
        for i, (a, b) in enumerate(pairs):
            x = i * 130
            f.label(P(x + 4, y + 6), f"({'i ii iii iv'.split()[i]})", anchor="start", size=12)
            eg_symbol(f, a, x + 44, y)
            f.label(P(x + 66, y + 6), "×", size=15)
            eg_symbol(f, b, x + 88, y)
    return f

@fig
def egyptian_times_ten_q():
    f = Fig("egyptian_times_ten_q")
    f.label(P(-8, 6), "(i)", anchor="end", size=13, bold=True)
    e = eg_number(f, 522, 0, 0)
    f.label(P(e + 4, 6), "× ten", anchor="start", size=14)
    f.label(P(e + 90, 6), "(ii)", anchor="end", size=13, bold=True)
    e2 = eg_number(f, 1010, e + 96, 0)
    f.label(P(e2 + 4, 6), "× ten", anchor="start", size=14)
    return f

@fig
def egyptian_times_ten_a():
    f = Fig("egyptian_times_ten_a")
    for i, n in enumerate([522, 1010]):
        y = -i * 70
        f.label(P(-8, y + 6), ["(i)", "(ii)"][i], anchor="end", size=13, bold=True)
        e = eg_number(f, n * 10, 0, y)
        f.label(P(e + 6, y + 6), f"= {n * 10}", anchor="start", size=14, bold=True, color=ANS)
    return f

# ================================================================ abacus
def abacus(f, x0, value, w=120, show_lines=True, label=None):
    """Lines for 1, 10, 100, 1000; counters on a line count 1 each, a counter just above a line
    counts 5. Asserts the counters add up to value."""
    total = 0
    for k in range(4):
        y = k * 46
        if show_lines:
            f.seg(P(x0, y), P(x0 + w, y), color="#1565c0", w=1.6)
        d = (value // 10 ** k) % 10
        fives, ones = divmod(d, 5)
        for j in range(ones):
            disc(f, P(x0 + 18 + j * 18, y), 6.5, RED, step=30); total += 10 ** k
        for j in range(fives):
            disc(f, P(x0 + 27, y + 22), 6.5, RED, step=30); total += 5 * 10 ** k
    assert total == value, (total, value)
    if label: f.label(P(x0 + w / 2, -26), label, size=13, bold=True)

def line_names(f, x):
    for k in range(4):
        f.label(P(x, k * 46 - 5), str(10 ** k), anchor="start", size=12, color=GIVEN, bold=True)

@fig
def abacus_3426():
    f = Fig("abacus_3426")
    abacus(f, 0, 3426, w=170, label="3426")
    line_names(f, 176)
    return f

@fig
def abacus_add():
    f = Fig("abacus_add")
    abacus(f, 0, 2907, w=120, label="2907")
    abacus(f, 130, 43, w=120, label="43", show_lines=False)
    for k in range(4): f.seg(P(120, k * 46), P(250, k * 46), color="#1565c0", w=1.6)
    f.seg(P(125, -12), P(125, 170), color=INK, w=2.4)
    line_names(f, 256)
    return f

@fig
def abacus_sum():
    f = Fig("abacus_sum")
    abacus(f, 0, 2950, w=170, label="2907 + 43 = 2950")
    line_names(f, 176)
    return f

# ================================================================ Mesopotamian numerals
def nail(f, x, y, color=INK):       # the wedge for 1: a small triangle head on a stem (14 tall)
    f.poly([P(x - 4, y + 14), P(x + 4, y + 14), P(x, y + 8)], fill=color, color=color)
    f.seg(P(x, y + 9), P(x, y), color=color, w=1.8)

def corner(f, x, y, color=INK):     # the wedge for 10: an angle opening to the right
    f.poly([P(x - 7, y + 10), P(x + 1, y + 14), P(x + 1, y + 6)], fill=color, color=color)
    f.seg(P(x - 7, y + 10), P(x + 6, y + 18), color=color, w=1.8); f.seg(P(x - 7, y + 10), P(x + 6, y + 2), color=color, w=1.8)

def placeholder(f, x, y, color=ASK):
    for dx in (-4, 4):
        f.seg(P(x + dx - 4, y + 4), P(x + dx + 4, y + 16), color=color, w=2.4)

def meso_digit(f, d, x):
    """Draw one base-60 digit (1-59) starting at x: corner wedges for the tens, then nails for the
    ones in rows of 3 (stacked). Returns the x after it. Asserts the wedges count to d."""
    tens, ones = divmod(d, 10)
    count = 0
    for i in range(tens):
        corner(f, x + 8 + i * 13, 0); count += 10
    x += tens * 13 + (4 if tens else 0)
    rows = math.ceil(ones / 3)
    for i in range(ones):
        r, c = divmod(i, 3)
        nail(f, x + 6 + c * 9, (rows - 1 - r) * 12); count += 1
    assert count == d
    return x + min(ones, 3) * 9 + 4

def meso_number(f, n, x0=0, gap=26, zero=None):
    """Base-60 place value numeral, largest place on the left; an empty place is a blank gap,
    or the placeholder sign if zero='sign'. Asserts the digits read back to n."""
    digits = []
    m = n
    while m: digits.insert(0, m % 60); m //= 60
    assert sum(d * 60 ** (len(digits) - 1 - i) for i, d in enumerate(digits)) == n
    x = x0
    for i, d in enumerate(digits):
        if d == 0:
            if zero == "sign": placeholder(f, x + 10, 0); x += 26
            else: x += 26
        else:
            x = meso_digit(f, d, x)
        x += gap
    return x, digits

@fig
def meso_digits():
    f = Fig("meso_digits")
    x = 0
    for d in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 20, 30, 40, 50, 59]:
        xs = x
        x = meso_digit(f, d, x)
        f.label(P((xs + x) / 2, -14), str(d), size=12, bold=True, color=GIVEN)
        x += 18
        if d == 9: x_break = x
    return f

@fig
def meso_examples():
    f = Fig("meso_examples")
    _, dg = meso_number(f, 640, 90); assert dg == [10, 40]
    f.label(P(80, 4), "640 =", anchor="end", size=14, bold=True)
    f.label(P(240, 4), "ten 60s and forty 1s", anchor="start", size=12, color=HELP)
    # second row: 7530 = 2 x 3600 + 5 x 60 + 30
    y = -60
    f.label(P(80, y + 4), "7530 =", anchor="end", size=14, bold=True)
    sub = Fig("sub")
    _, dg2 = meso_number(sub, 7530, 90); assert dg2 == [2, 5, 30]
    for it in sub.items:
        f.items.append(shift(it, 0, y))
    f.pts += [(p[0], p[1] + y) for p in sub.pts]
    f.label(P(300, y + 4), "two 3600s, five 60s and thirty 1s", anchor="start", size=12, color=HELP)
    return f

def shift(it, dx, dy):
    k = it[0]
    S = lambda p: (p[0] + dx, p[1] + dy)
    if k == "line": return (k, S(it[1]), S(it[2])) + it[3:]
    if k == "fillpoly": return (k, [S(p) for p in it[1]]) + it[2:]
    if k == "text": return (k, S(it[1])) + it[2:]
    if k in ("circle", "carc"): return (k, S(it[1])) + it[2:]
    if k == "arc": return (k, S(it[1])) + it[2:]
    if k == "dot": return (k, S(it[1])) + it[2:]
    if k == "poly": return (k, [S(p) for p in it[1]]) + it[2:]
    raise ValueError(k)

def rows_fig(name, items, draw, x0=110, dy=56):
    f = Fig(name)
    for i, (label, n) in enumerate(items):
        y = -i * dy
        sub = Fig("sub")
        end = draw(sub, n, x0)
        for it in sub.items: f.items.append(shift(it, 0, y))
        f.pts += [(p[0], p[1] + y) for p in sub.pts]
        f.label(P(x0 - 16, y + 4), label, anchor="end", size=13, bold=True)
    return f

@fig
def meso_answers():
    def draw(sub, n, x0):
        e, dg = meso_number(sub, n, x0)
        place = {1: "1s", 2: "60s, 1s", 3: "3600s, 60s, 1s"}[len(dg)]
        sub.label(P(330, 4), " + ".join(f"{d} × {60 ** (len(dg) - 1 - i)}" for i, d in enumerate(dg)), anchor="start", size=12, color=HELP)
        return e
    return rows_fig("meso_answers", [("63 =", 63), ("132 =", 132), ("200 =", 200), ("60 =", 60), ("3605 =", 3605)], draw)

@fig
def meso_ambiguity():
    """1, 60 and 3600 all look like one nail; 12, 602 and 36002 look alike too."""
    f = Fig("meso_ambiguity")
    xs = 0
    for n in [1, 60, 3600]:
        sub = Fig("sub")
        # written without spaces: only the non-zero digits
        e, dg = meso_number(sub, n, 0, gap=0)
        for it in sub.items: f.items.append(shift(it, xs, 0))
        f.pts += [(p[0] + xs, p[1]) for p in sub.pts]
        f.label(P(xs + 10, -16), str(n), size=13, bold=True, color=GIVEN)
        xs += 80
    f.label(P(xs - 10, 6), "all look the same when the blanks are lost", anchor="start", size=12, color=ASK)
    return f

@fig
def meso_placeholder():
    f = Fig("meso_placeholder")
    _, dg = meso_number(f, 3602, 90, zero="sign"); assert dg == [1, 0, 2]
    f.label(P(80, 4), "3602 =", anchor="end", size=14, bold=True)
    f.label(P(230, 4), "one 3600, no 60s (placeholder), two 1s", anchor="start", size=12, color=HELP)
    return f

# ================================================================ Mayan numerals
def shell(f, x, y):
    f.poly([P(x + 12 * math.cos(d2r(a)), y + 6 * math.sin(d2r(a))) for a in range(0, 360, 30)], fill="#fff8e1", color=INK)
    for dx in (-5, 0, 5): f.seg(P(x + dx, y - 4), P(x + dx, y + 4), w=1.2)

def maya_digit(f, d, x, y):
    """Digit 0-19 centred at x, bottom at y: shell for 0, bars (5) under dots (1). Returns height."""
    if d == 0:
        shell(f, x, y + 6); return 14
    bars, dots = divmod(d, 5)
    h = 0
    for b in range(bars):
        box(f, x - 18, y + h, 36, 6, fill=INK); h += 10
    for i in range(dots):
        disc(f, P(x - (dots - 1) * 6 + i * 12, y + h + 5), 4, INK, step=45)
    return h + (12 if dots else 0)

MAYA_PLACES = [1, 20, 360, 7200]

def maya_number(f, n, x):
    digits = []
    for p in reversed(MAYA_PLACES):
        digits.append(n // p); n %= p
    while len(digits) > 1 and digits[0] == 0: digits.pop(0)
    places = MAYA_PLACES[:len(digits)][::-1]
    assert all(0 <= d < 20 for d in digits[1:])
    y = 0
    for d, p in reversed(list(zip(digits, places))):       # bottom place first
        h = maya_digit(f, d, x, y)
        assert h <= 46
        f.label(P(x + 30, y + 2), f"{d} × {p}", anchor="start", size=12, color=HELP)
        if p != places[0]:
            f.seg(P(x - 24, y + 52), P(x + 24, y + 52), color=HELP, w=1, dash="3 3")
        y += 58
    return digits, places

@fig
def maya_digits():
    f = Fig("maya_digits")
    for i, d in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 10, 13, 15, 19]):
        x = i * 52
        maya_digit(f, d, x, 0)
        f.label(P(x, -18), str(d), size=13, bold=True, color=GIVEN)
    return f

@fig
def maya_answers():
    f = Fig("maya_answers")
    for i, n in enumerate([77, 100, 361, 721]):
        x = i * 150
        sub = Fig("sub")
        digits, places = maya_number(sub, n, 0)
        assert sum(d * p for d, p in zip(digits, places)) == n
        for it in sub.items: f.items.append(shift(it, x, 0))
        f.pts += [(p[0] + x, p[1]) for p in sub.pts]
        f.label(P(x, -22), f"({'i ii iii iv'.split()[i]}) {n}", size=13, bold=True)
    return f

# ================================================================ Chinese rod numerals
def rod_digit(f, d, x, upright, color=INK):
    """zong (upright) or heng (lying) rod digit 1-9 in a 22 x 26 cell, bottom-left (x, 0)."""
    if d == 0: return
    fives, ones = divmod(d, 5) if d != 5 else (0, 5)
    if upright:
        for i in range(ones): f.seg(P(x + 3 + i * 4, 0), P(x + 3 + i * 4, 18), color=color, w=2.4)
        if fives: f.seg(P(x, 22), P(x + 20, 22), color=color, w=2.4)
    else:
        for i in range(ones): f.seg(P(x, 2 + i * 4), P(x + 20, 2 + i * 4), color=color, w=2.4)
        if fives: f.seg(P(x + 10, 2 + ones * 4), P(x + 10, 14 + ones * 4), color=color, w=2.4)

@fig
def rod_digits():
    f = Fig("rod_digits")
    f.label(P(-10, 6), "zong", anchor="end", size=13, bold=True)
    f.label(P(-10, -44), "heng", anchor="end", size=13, bold=True)
    for d in range(1, 10):
        x = (d - 1) * 40
        rod_digit(f, d, x, True)
        rod_digit(f, d, x, False) if False else None
        sub = Fig("sub"); rod_digit(sub, d, x, False)
        for it in sub.items: f.items.append(shift(it, 0, -50))
        f.pts += [(p[0], p[1] - 50) for p in sub.pts]
        f.label(P(x + 10, -64), str(d), size=12, bold=True, color=GIVEN)
    return f

def rod_number(f, n, x0=0, only_zong=False, gap=34):
    digits = [int(c) for c in str(n)]
    for i, d in enumerate(digits):
        place = len(digits) - 1 - i
        upright = True if only_zong else (place % 2 == 0)      # units, hundreds, ... upright
        rod_digit(f, d, x0 + i * gap, upright)
    return digits

@fig
def rod_2634():
    f = Fig("rod_2634")
    dg = rod_number(f, 2634)
    assert dg == [2, 6, 3, 4]
    for i, (d, p) in enumerate(zip(dg, ["10³", "10²", "10", "1"])):
        f.label(P(i * 34 + 10, -16), p, size=12, color=GIVEN)
    f.label(P(150, 6), "= 2 × 10³ + 6 × 10² + 3 × 10 + 4 = 2634", anchor="start", size=13, bold=True)
    return f

@fig
def rod_41_zong():
    f = Fig("rod_41_zong")
    rod_number(f, 41, only_zong=True, gap=24)
    f.label(P(60, 6), "41 in zong rods only: 4 rods then 1 rod, five rods in a row", anchor="start", size=12, color=ASK)
    return f

# ================================================================ counting ideas
@fig
def cows_sticks():
    f = Fig("cows_sticks")
    n = 6
    for i in range(n):
        x = i * 58
        f.poly([P(x - 16, 60), P(x + 16, 60), P(x + 18, 74), P(x - 18, 74)], fill="#d7ccc8")       # cow body
        disc(f, P(x + 22, 76), 6, "#d7ccc8", step=45)                                                # head
        for dx in (-12, 12): f.seg(P(x + dx, 60), P(x + dx, 50), w=2)
        f.seg(P(x, 46), P(x, 12), color=HELP, w=1.2, dash="4 3")
        f.seg(P(x, 0), P(x, -22), color="#795548", w=4)                                             # a stick
    f.label(P((n - 1) * 29, -42), "one stick for each cow: a one-to-one mapping", size=13, color=GIVEN, bold=True)
    return f

QUICK = [3, 5, 2, 7, 4, 6, 1]

@fig
def quick_count():
    f = Fig("quick_count")
    import random
    rnd = random.Random(8)
    for i, n in enumerate(QUICK):
        x = i * 86
        box(f, x, 0, 74, 74, fill="#fffde7")
        placed = []
        while len(placed) < n:
            p = P(x + 10 + rnd.random() * 54, 10 + rnd.random() * 54)
            if all(dist(p, q) > 17 for q in placed): placed.append(p)
        for p in placed: disc(f, p, 6, "#ef6c00", step=30)
        assert len(placed) == n
        f.label(P(x + 37, -16), "ABCDEFG"[i], size=13, bold=True)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
