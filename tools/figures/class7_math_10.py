"""Figures for class 7 maths Ch 10, Operations with Integers. Number-line jumps assert that the
coin really ends at a + b; token pictures count the drawn tokens and assert they match the value
written under them, so a picture can never disagree with its answer."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "10")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

GREENT, REDT, BAGC = "#66bb6a", "#ef5350", "#fff8e1"

# ---------------------------------------------------------------- helpers
def disc(f, c, r, fill, color=INK):
    f.poly([along(c, 360 * k / 24, r) for k in range(24)], fill=fill, color=color)

def token(f, c, sign, crossed=False, r=10):
    """A green (+1) or red (-1) token; crossed tokens are the ones taken out."""
    disc(f, c, r, GREENT if sign > 0 else REDT)
    f.text(add(c, (0, -1)), "+" if sign > 0 else "−", color="#ffffff", bold=True, size=15)
    if crossed:
        k = r * 0.8
        f.seg(add(c, (-k, -k)), add(c, (k, k)), color=INK, w=2.4)
        f.seg(add(c, (-k, k)), add(c, (k, -k)), color=INK, w=2.4)
    return sign

def head(f, tip, a, color=INK, s=9):
    for d in (+28, -28):
        f.seg(along(tip, a + 180 + d, s), tip, color=color, w=2)

def numline(f, lo, hi, u, y=0, labels=None, every=1):
    f.seg(P(lo * u - 18, y), P(hi * u + 18, y), w=1.8)
    head(f, P(hi * u + 18, y), 0); head(f, P(lo * u - 18, y), 180)
    for n in range(lo, hi + 1):
        f.seg(P(n * u, y - 5), P(n * u, y + 5), w=1.4)
        if labels is None or n in labels:
            if n % every == 0 or (labels and n in labels):
                f.label(P(n * u, y - 19), str(n).replace("-", "−"), size=12)

def jump(f, x0, x1, u, label, color, up=True, y=0, sweep=110):
    """A flat circular jump from x0 to x1 (in units), above (up) or below the line, arrow at x1."""
    half = abs(x1 - x0) * u / 2
    r = half / math.sin(math.radians(sweep / 2))
    drop = r * math.cos(math.radians(sweep / 2))
    mx = (x0 + x1) / 2 * u
    if up:
        c = P(mx, y - drop); f.carc(c, r, 90 - sweep / 2, 90 + sweep / 2, color=color, w=2.2)
    else:
        c = P(mx, y + drop); f.carc(c, r, 270 - sweep / 2, 270 + sweep / 2, color=color, w=2.2)
    h = r - drop
    tip = P(x1 * u, y + (3 if up else -3))
    head(f, tip, 270 if up else 90, color=color)
    f.label(P(mx, y + (h + 12 if up else -h - 14)), label, color=color, bold=True, size=14)

# ---------------------------------------------------------------- number-line moves
@fig
def carrom_ab():
    f = Fig("carrom_ab"); u = 30; a, b = 4, 3
    numline(f, 0, 12, u)
    jump(f, 0, a, u, "a", GIVEN)
    jump(f, a, a + b, u, "b", GIVEN)
    f.dot(P((a + b) * u, 0), color=ANS)
    f.label(P((a + b) * u, -40), "P = a + b", color=ANS, bold=True, size=14)
    assert a + b == 7
    return f

@fig
def carrom_5_m7():
    f = Fig("carrom_5_m7"); u = 34; a, b = 5, -7
    numline(f, -4, 7, u)
    jump(f, 0, a, u, "+5", GIVEN, up=True)
    jump(f, a, a + b, u, "−7", ASK, up=False)
    f.dot(P((a + b) * u, 0), color=ANS)
    f.label(P((a + b) * u - 6, 16), "P = −2", color=ANS, bold=True, size=14, anchor="end")
    assert a + b == -2
    return f

@fig
def try_magnitudes():
    f = Fig("try_magnitudes"); u = 26
    cases = [("(i)", 3, -5, 0), ("(ii)", 5, -2, -150), ("(iii)", -4, 4, -300)]
    for name, a, b, y in cases:
        numline(f, -6, 6, u, y=y, labels=[0])
        jump(f, 0, a, u, "a", GIVEN, up=True, y=y)
        jump(f, a, a + b, u, "b", ASK, up=False, y=y)
        p = a + b
        f.dot(P(p * u, y), color=ANS)
        f.label(P(p * u + (14 if p != 0 else 0), y + 14 if p != 0 else y - 34), "P", color=ANS, bold=True, size=14)
        f.label(P(-6 * u - 40, y), name, bold=True, size=15, anchor="end")
    assert [a + b for _, a, b, _ in cases] == [-2, 3, 0]
    return f

@fig
def elevator():
    f = Fig("elevator"); s = 1.2   # pixels per metre
    f.seg(P(0, 30 * s), P(0, -140 * s), w=1.8)
    for m in range(30, -141, -15):
        f.seg(P(-5, m * s), P(5, m * s), w=1.3)
        f.label(P(-12, m * s), str(m).replace("-", "−"), size=11, anchor="end")
    f.seg(P(-4, 0), P(70, 0), color="#6d4c41", w=3)
    f.label(P(75, 6), "ground (0)", size=12, anchor="start", color="#6d4c41")
    start, rate, t = 15, -3, 45
    end = start + t * rate
    assert end == -120
    f.dot(P(0, start * s), color=GIVEN)
    f.label(P(14, start * s + 4), "start: +15 m", size=13, anchor="start", color=GIVEN, bold=True)
    f.seg(P(34, (start - 6) * s), P(34, (end + 4) * s), color=ASK, w=2.4)
    head(f, P(34, (end + 4) * s), 270, color=ASK)
    f.label(P(44, (start + end) / 2 * s), "45 × (−3) = −135", size=13, anchor="start", color=ASK, bold=True)
    f.dot(P(0, end * s), color=ANS)
    f.label(P(14, end * s - 12), "end: −120 m", size=13, anchor="start", color=ANS, bold=True)
    return f

# ---------------------------------------------------------------- tokens
@fig
def tokens_7_minus_18():
    f = Fig("tokens_7_minus_18"); g = 27
    have, take = 7, 18
    pairs = take - have
    greens = 0
    for i in range(take):                       # top row: every green, all removed
        greens += token(f, P(i * g, 40), +1, crossed=True)
    reds = 0
    for i in range(have, take):                 # the reds of the zero pairs stay
        reds += -token(f, P(i * g, 0), -1)
    assert greens == take and reds == pairs == 11
    f.seg(P(-10, 64), P((have - 1) * g + 10, 64), color=GIVEN, w=1.6)
    f.label(P((have - 1) * g / 2, 76), "7 greens to start", color=GIVEN, size=13, bold=True)
    f.seg(P(have * g - 10, 64), P((take - 1) * g + 10, 64), color=HELP, w=1.6)
    f.label(P((have + take - 1) * g / 2, 76), "11 zero pairs put in", color=HELP, size=13, bold=True)
    f.label(P((have + take - 1) * g / 2, -26), "11 reds left: 7 − 18 = −11", color=ANS, size=14, bold=True)
    f.label(P(-16, 40), "remove 18 greens", size=12, anchor="end", color=ASK)
    return f

def bag(f, x, y, w, h, title):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=BAGC)
    f.label(P(x + w / 2, y + h + 12), title, size=12, color=HELP, bold=True)

def rounds_fig(name, mult, cand, caption):
    """mult × cand with the bag: positive mult puts tokens in, negative mult adds zero pairs
    and takes the multiplicand's tokens out. Asserts the tokens left equal mult × cand."""
    f = Fig(name); g = 25; bw = 2 * g + 16
    n, k = abs(mult), abs(cand); s = 1 if cand > 0 else -1
    value = 0
    for r in range(n):
        x0 = r * (bw + 14)
        extra = g if mult < 0 else 0
        bag(f, x0, -extra - 16, bw, extra + 32, f"round {r + 1}")
        for j in range(k):
            c_top = P(x0 + 18 + j * g, 0)
            if mult > 0:
                value += token(f, c_top, s)
            else:
                token(f, c_top, s, crossed=True)               # taken out
                value += token(f, P(c_top[0], -g), -s)          # its partner stays
    assert value == mult * cand, (name, value)
    f.label(P((n * (bw + 14) - 14) / 2, -(g if mult < 0 else 0) - 34), caption, color=ANS, size=14, bold=True)
    return f

@fig
def bag_4_times_m2():
    return rounds_fig("bag_4_times_m2", 4, -2, "8 reds: 4 × (−2) = −8")

@fig
def bag_m4_times_2():
    return rounds_fig("bag_m4_times_2", -4, 2, "8 reds left: (−4) × 2 = −8")

@fig
def bag_m4_times_m2():
    return rounds_fig("bag_m4_times_m2", -4, -2, "8 greens left: (−4) × (−2) = 8")

@fig
def sets_minus_2():
    f = Fig("sets_minus_2"); g = 25
    sets = [("Set 1", 2, 0), ("Set 2", 4, 2), ("Set 3", 6, 4)]
    for i, (name, nred, ngreen) in enumerate(sets):
        y = -i * 40
        f.label(P(-20, y), name, size=13, anchor="end", bold=True)
        v = 0
        for j in range(nred): v += token(f, P(j * g, y), -1)
        for j in range(ngreen): v += token(f, P((nred + j) * g + 8, y), +1)
        assert v == -2
        f.label(P(10 * g + 24, y), "= −2", size=14, anchor="start", color=ANS, bold=True)
    return f

def rect_fig(name, rows, left, right, ltxt, rtxt, wtxt):
    """rows × (left + right) as a token rectangle: left block then right block in every row."""
    f = Fig(name); g = 25; gap = 50
    tot = 0; lsum = rsum = 0
    for r in range(rows):
        y = -r * g
        for j in range(abs(left)):
            lsum += token(f, P(j * g, y), 1 if left > 0 else -1)
        for j in range(abs(right)):
            rsum += token(f, P(abs(left) * g + gap + j * g, y), 1 if right > 0 else -1)
    assert lsum == rows * left and rsum == rows * right
    xl1 = (abs(left) - 1) * g; xr0 = abs(left) * g + gap; xr1 = xr0 + (abs(right) - 1) * g
    f.seg(P(-12, 22), P(xr1 + 12, 22), color=GIVEN, w=1.6)
    f.label(P((xr1) / 2, 36), wtxt, color=GIVEN, size=13, bold=True)
    yb = -(rows - 1) * g - 22
    f.seg(P(-12, yb), P(xl1 + 12, yb), color=ANS, w=1.6)
    f.label(P(xl1 / 2, yb - 14), ltxt, color=ANS, size=13, bold=True)
    f.seg(P(xr0 - 12, yb), P(xr1 + 12, yb), color=ANS, w=1.6)
    f.label(P((xr0 + xr1) / 2, yb - 14), rtxt, color=ANS, size=13, bold=True)
    return f, lsum, rsum

@fig
def distributive():
    f, l, r = rect_fig("distributive", 4, 2, -3, "4 × 2 = 8", "4 × (−3) = −12", "4 × (2 + (−3)) = −4")
    assert l + r == 4 * (2 + (-3))
    return f

@fig
def distributive_neg():
    # (−4) × (2 + (−3)): add the inverse (−2 and +3) four times
    f, l, r = rect_fig("distributive_neg", 4, -2, 3, "(−4) × 2 = −8", "(−4) × (−3) = 12", "(−4) × (2 + (−3)) = 4")
    assert l == -4 * 2 and r == -4 * -3 and l + r == -4 * (2 + (-3))
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
