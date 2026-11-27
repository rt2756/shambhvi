"""Figures for class 7 maths Ch 11, Finding Common Ground. Tile counts, jump landings, strip
lengths, star colours and the primes in the Venn picture are all computed and asserted, so a
picture can never disagree with the notes."""
import os, sys, math
from math import gcd
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "11")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

TILE, STRIP1, STRIP2 = "#ffe0b2", "#bbdefb", "#c8e6c9"

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def head(f, tip, a, color=INK, s=9):
    for d in (+28, -28):
        f.seg(along(tip, a + 180 + d, s), tip, color=color, w=2)

def pf(n):
    out, d = [], 2
    while d * d <= n:
        while n % d == 0: out.append(d); n //= d
        d += 1
    if n > 1: out.append(n)
    return out

@fig
def room_tiles():
    f = Fig("room_tiles"); L, B, s, k = 16, 12, 4, 14     # feet, tile side, px per foot
    assert s == gcd(L, B)
    n = 0
    for i in range(L // s):
        for j in range(B // s):
            box(f, i * s * k, j * s * k, s * k, s * k, fill=TILE); n += 1
    assert n == 12
    f.label(P(L * k / 2, B * k + 16), "16 ft", bold=True)
    f.label(P(L * k + 12, B * k / 2), "12 ft", bold=True, anchor="start")
    f.label(P(s * k / 2, s * k / 2), "4 ft", size=12, color=GIVEN, bold=True)
    f.label(P(L * k / 2, -18), "4 tiles across × 3 down = 12 tiles", color=ANS, bold=True, size=14)
    return f

@fig
def jumps():
    f = Fig("jumps"); u = 8; lo, hi, j = 0, 45, 14
    f.seg(P(-6, 0), P(hi * u + 10, 0), w=1.8); head(f, P(hi * u + 10, 0), 0)
    for n in range(lo, hi + 1):
        big = n % 7 == 0
        f.seg(P(n * u, -4 - 2 * big), P(n * u, 4 + 2 * big), w=1.2)
        if big: f.label(P(n * u, -18), str(n), size=12)
    landings = list(range(j, hi + 1, j))
    assert 28 in landings and 42 in landings and gcd(28, 42) == j
    x = 0
    for t in landings:
        c, r = P((x + t) / 2 * u, 0), (t - x) * u / 2
        f.carc(c, r, 0, 180, color=GIVEN, w=2.2)
        head(f, P(t * u, 3), 270, color=GIVEN)
        f.label(P((x + t) / 2 * u, r + 12), "+14", color=GIVEN, bold=True, size=13)
        x = t
    for t in (28, 42):
        f.label(P(t * u, -38), "treasure", color=ASK, bold=True, size=12)
    return f

@fig
def factor_tree_90():
    f = Fig("factor_tree_90"); dx, dy = 52, 50
    nodes = [(90, 2, 45)]
    x, y, n = 0, 0, 90
    primes = []
    while True:
        p = pf(n)[0]; q = n // p
        f.seg(P(x - 6, y - 12), P(x - dx + 10, y - dy + 12), w=1.6)
        f.seg(P(x + 6, y - 12), P(x + dx - 10, y - dy + 12), w=1.6)
        f.label(P(x, y), str(n), bold=True, size=16)
        f.label(P(x - dx, y - dy), str(p), color=ANS, bold=True, size=16)
        primes.append(p)
        x, y, n = x + dx, y - dy, q
        if len(pf(n)) == 1:
            f.label(P(x, y), str(n), color=ANS, bold=True, size=16); primes.append(n); break
    assert primes == [2, 3, 3, 5] and math.prod(primes) == 90
    f.label(P(-dx, y - 34), "90 = 2 × 3 × 3 × 5", color=ANS, bold=True, size=15, anchor="start")
    return f

@fig
def torans():
    f = Fig("torans"); k = 12; L = 24
    assert L == 6 * 8 // gcd(6, 8)
    for i in range(L // 6):
        box(f, i * 6 * k, 30, 6 * k, 22, fill=STRIP1)
        f.label(P((i + 0.5) * 6 * k, 41), "6", size=12, bold=True)
    for i in range(L // 8):
        box(f, i * 8 * k, 0, 8 * k, 22, fill=STRIP2)
        f.label(P((i + 0.5) * 8 * k, 11), "8", size=12, bold=True)
    f.label(P(-8, 41), "Anshu", anchor="end", size=13, bold=True)
    f.label(P(-8, 11), "Guna", anchor="end", size=13, bold=True)
    f.seg(P(L * k, -10), P(L * k, 64), color=ASK, w=2, dash="5,4")
    f.label(P(L * k, -22), "both reach 24 cm", color=ASK, bold=True, size=13)
    return f

STAR_COL = {"yellow": "#fdd835", "green": "#7cb342", "orange": "#fb8c00", "blue": "#3f51b5",
            "pink": "#d81b9a", "grey": "#9e9e9e"}

def star(f, c, r, fill):
    pts = [along(c, 90 + 36 * k, r if k % 2 == 0 else r * 0.45) for k in range(10)]
    f.poly(pts, fill=fill, color=fill)

@fig
def stars():
    f = Fig("stars"); g = 30; N = 18
    row1 = ["yellow", "green", "orange", "blue", "pink", "grey"]
    row2 = ["green", "orange", "yellow", "blue"]
    meet = [i for i in range(1, N + 1) if row1[(i - 1) % 6] == "blue" and row2[(i - 1) % 4] == "blue"]
    assert meet == [4, 16]
    for i in range(1, N + 1):
        x = (i - 1) * g
        star(f, P(x, 40), 12, STAR_COL[row1[(i - 1) % 6]])
        star(f, P(x, 0), 12, STAR_COL[row2[(i - 1) % 4]])
        f.label(P(x, -24), str(i), size=11, color=HELP)
    for i in meet:
        x = (i - 1) * g
        f.seg(P(x - 15, -12), P(x + 15, -12), color=ASK, w=2)
        f.seg(P(x - 15, -12), P(x - 15, 56), color=ASK, w=2)
        f.seg(P(x + 15, -12), P(x + 15, 56), color=ASK, w=2)
        f.seg(P(x - 15, 56), P(x + 15, 56), color=ASK, w=2)
    f.label(P(-24, 40), "Row 1", anchor="end", size=13, bold=True)
    f.label(P(-24, 0), "Row 2", anchor="end", size=13, bold=True)
    f.label(P(N * g - 10, 20), "…", size=18, anchor="start")
    return f

@fig
def venn_84_180():
    f = Fig("venn_84_180"); a, b = 84, 180
    pa, pb = pf(a), pf(b)
    common = []
    rb = list(pb)
    for p in pa:
        if p in rb: common.append(p); rb.remove(p)
    only_a = list(pa)
    for p in common: only_a.remove(p)
    only_b = rb
    assert math.prod(common) == gcd(a, b) == 12
    assert math.prod(common + only_a + only_b) == a * b // gcd(a, b) == 1260
    r = 85; ca, cb = P(0, 0), P(110, 0)
    f.circle(ca, r, color=GIVEN, w=2.2); f.circle(cb, r, color=ANS, w=2.2)
    f.label(P(-30, r + 14), "84 = 2 × 2 × 3 × 7", color=GIVEN, bold=True, size=13)
    f.label(P(140, r + 14), "180 = 2 × 2 × 3 × 3 × 5", color=ANS, bold=True, size=13)
    f.label(P(-40, 0), " ".join(map(str, only_a)), bold=True, size=18)
    f.label(P(55, 14), "2  2", bold=True, size=18, color=ASK)
    f.label(P(55, -12), "3", bold=True, size=18, color=ASK)
    f.label(P(150, 0), "  ".join(map(str, only_b)), bold=True, size=18)
    assert only_a == [7] and sorted(only_b) == [3, 5] and common == [2, 2, 3]
    f.label(P(55, -r - 18), "overlap = HCF = 2 × 2 × 3 = 12", color=ASK, bold=True, size=13)
    f.label(P(55, -r - 38), "everything = LCM = 2 × 2 × 3 × 7 × 3 × 5 = 1260", bold=True, size=13)
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
