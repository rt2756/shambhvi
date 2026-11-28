"""Figures for class 6 maths Ch 5, Prime Time. Every number on a picture is checked: Venn diagrams
place each number by testing which multiples it belongs to, the sieve circles exactly the primes,
fig arrangements are the factor pairs, factor trees multiply back to their top number, and thread-art
pictures count the pegs the thread really reaches."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class6", "math", "5")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, PURPLE, RED = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0", "#ce93d8", "#ef9a9a"
C30 = math.cos(math.radians(30))

def isprime(n): return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK, n=24):
    f.poly([P(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)], fill=fill, color=color)

def ring(f, c, rx, ry, color, w=2.2):
    pts = [P(c[0] + rx * math.cos(2 * math.pi * k / 72), c[1] + ry * math.sin(2 * math.pi * k / 72)) for k in range(73)]
    for p, q in zip(pts, pts[1:]): f.seg(p, q, color=color, w=w)

# ---------------------------------------------------------------- Venn diagrams of multiples
def venn(name, a, b, upto, show=None, la=None, lb=None, blanks=False):
    """Two circles: multiples of a (left) and of b (right) up to `upto`. Each number is written in
    the region it belongs to; show = which numbers to write (default: all)."""
    f = Fig(name)
    R, d = 120, 150
    cl, cr = P(0, 0), P(d, 0)
    ring(f, cl, R, R, ASK); ring(f, cr, R, R, GIVEN)
    nums = [n for n in range(1, upto + 1) if n % a == 0 or n % b == 0]
    if show is not None: nums = [n for n in nums if n in show]
    left = [n for n in nums if n % a == 0 and n % b]
    mid = [n for n in nums if n % a == 0 and n % b == 0]
    right = [n for n in nums if n % b == 0 and n % a]
    def place(ns, x0, x1, y0, y1, cols):
        rows = max(1, math.ceil(len(ns) / cols))
        for k, n in enumerate(ns):
            r, c = divmod(k, cols)
            x = x0 + (c + 0.5) * (x1 - x0) / cols
            y = y1 - (r + 0.5) * (y1 - y0) / rows
            pt = P(x, y)
            # the place really is in the right region
            inl, inr = dist(pt, cl) < R - 8, dist(pt, cr) < R - 8
            assert (inl, inr) == (n % a == 0, n % b == 0), (name, n, inl, inr)
            f.text(P(x, y - 5), str(n), size=13 if len(ns) < 14 else 11, bold=n in mid)
    place(left, -95, 20, -80, 80, 3 if len(left) > 8 else 2)
    place(mid, 38, 112, -78, 78, 1 if len(mid) <= 6 else 2)
    place(right, 132, 245, -80, 80, 3 if len(right) > 8 else 2)
    f.label(P(-60, R + 18), la or f"Multiples of {a}", size=13, bold=True, color=ASK)
    f.label(P(d + 60, R + 18), lb or f"Multiples of {b}", size=13, bold=True, color=GIVEN)
    f.label(P(d / 2, -R - 22), "Common multiples (middle)", size=12, color=HELP)
    return f

@fig
def venn_3_5_30(): return venn("venn_3_5_30", 3, 5, 30)
@fig
def venn_3_5_60(): return venn("venn_3_5_60", 3, 5, 60)
@fig
def venn_2_5(): return venn("venn_2_5", 2, 5, 60)
@fig
def venn_3_7(): return venn("venn_3_7", 3, 7, 60)
@fig
def venn_4_6(): return venn("venn_4_6", 4, 6, 60)

@fig
def venn_q8():
    f = venn("venn_q8", 3, 8, 80, show={24, 48, 72}, la="Multiples of ___", lb="Multiples of ___")
    return f
@fig
def venn_q8_answer(): return venn("venn_q8_answer", 3, 8, 80)

# ---------------------------------------------------------------- jumps
@fig
def jumps_24():
    f = Fig("jumps_24")
    k = 22
    f.seg(P(-8, 0), P(25 * k, 0), w=1.6)
    for n in range(0, 25):
        f.seg(P(n * k, -5), P(n * k, 5), w=1.2)
        f.text(P(n * k, -22), str(n), size=10, bold=n == 24, color=ASK if n == 24 else INK)
    for size, col, up in [(4, GIVEN, 1), (6, ANS, -1)]:
        lands = list(range(0, 25, size))
        assert 24 in lands
        for a in lands[:-1]:
            if up > 0: f.carc(P((a + size / 2) * k, 4), size * k / 2, 0, 180, color=col, w=1.8)
            else: f.carc(P((a + size / 2) * k, -30), size * k / 2, 180, 360, color=col, w=1.8)
    f.label(P(0, 64), "jumps of 4: 4, 8, 12, 16, 20, 24", anchor="start", size=12, color=GIVEN)
    f.label(P(0, -100), "jumps of 6: 6, 12, 18, 24", anchor="start", size=12, color=ANS)
    disc(f, P(24 * k, 14), 6, YELLOW)
    return f

@fig
def table_31_70():
    """31 to 70: multiples of 3 shaded green, multiples of 4 circled."""
    f = Fig("table_31_70")
    u = 34
    for r in range(4):
        for c in range(10):
            n = 31 + 10 * r + c
            x, y = c * u, -r * u
            box(f, x, y, u, u, fill=GREEN if n % 3 == 0 else "#ffffff")
            if n % 4 == 0: f.circle(P(x + u / 2, y + u / 2), 13, color=GIVEN, w=1.8)
            f.text(P(x + u / 2, y + u / 2 - 5), str(n), size=13, bold=n % 12 == 0)
    assert [n for n in range(31, 71) if n % 3 == 0 and n % 4 == 0] == [36, 48, 60]
    return f

# ---------------------------------------------------------------- 5.2 primes
def dot_rect(f, x0, rows, cols, g=14, fill=GREEN):
    for i in range(rows):
        for j in range(cols):
            disc(f, P(x0 + j * g, -i * g), 5, fill, n=16)
    f.label(P(x0 + (cols - 1) * g / 2, -rows * g - 8), f"{rows} × {cols}", size=12, bold=True)
    return x0 + cols * g + 26

@fig
def figs_12_7():
    f = Fig("figs_12_7")
    pairs = [(r, 12 // r) for r in range(1, 13) if 12 % r == 0]
    assert pairs == [(1, 12), (2, 6), (3, 4), (4, 3), (6, 2), (12, 1)]
    x = 0
    for r, c in pairs: x = dot_rect(f, x, r, c)
    f.label(P(0, 40), "12 figs: 6 rectangles (rows × columns)", anchor="start", size=12, color=HELP)
    x += 30
    sevens = [(r, 7 // r) for r in range(1, 8) if 7 % r == 0]
    assert sevens == [(1, 7), (7, 1)]
    x0 = x
    for r, c in sevens: x = dot_rect(f, x, r, c, fill=ORANGE)
    f.label(P(x0, 40), "7 figs: only 1 × 7 and 7 × 1", anchor="start", size=12, color=HELP)
    return f

@fig
def sieve():
    f = Fig("sieve")
    u = 30
    primes = 0
    for n in range(1, 101):
        r, c = divmod(n - 1, 10)
        x, y = c * u, -r * u
        p = isprime(n)
        box(f, x, y, u, u, fill=YELLOW if p else "#ffffff")
        f.text(P(x + u / 2, y + u / 2 - 5), str(n), size=11, bold=p, color=INK if p else HELP)
        if p:
            f.circle(P(x + u / 2, y + u / 2), 12, color=ANS, w=1.6); primes += 1
        else:
            f.seg(P(x + 5, y + 5), P(x + u - 5, y + u - 5), color=RED, w=1.2)
    assert primes == 25
    f.label(P(0, -10 * u - 12), "25 primes up to 100 (circled); 1 and the composites are crossed out.", anchor="start", size=12, color=HELP)
    return f

# ---------------------------------------------------------------- 5.4 factor trees and the 2 × 3 × 5 block
def tree(f, x, y, n, split, dx=44, dy=46):
    """split: dict n -> (a, b). Draws the tree and returns the prime leaves."""
    if n not in split:
        assert isprime(n)
        disc(f, P(x, y + 5), 13, GREEN, n=20)
        f.text(P(x, y), str(n), size=13, bold=True)
        return [n]
    a, b = split[n]
    assert a * b == n
    f.text(P(x, y), str(n), size=13, bold=True)
    f.seg(P(x - 4, y - 6), P(x - dx + 6, y - dy + 16), w=1.4, color=HELP)
    f.seg(P(x + 4, y - 6), P(x + dx - 6, y - dy + 16), w=1.4, color=HELP)
    return tree(f, x - dx, y - dy, a, split, dx * 0.62, dy) + tree(f, x + dx, y - dy, b, split, dx * 0.62, dy)

@fig
def tree_56():
    f = Fig("tree_56")
    leaves = tree(f, 0, 0, 56, {56: (4, 14), 4: (2, 2), 14: (2, 7)}, dx=60)
    assert sorted(leaves) == [2, 2, 2, 7] and math.prod(leaves) == 56
    f.label(P(150, -60), "56 = 2 × 2 × 2 × 7", anchor="start", size=14, bold=True)
    return f

@fig
def trees_36():
    f = Fig("trees_36")
    x = 0
    for first in [(2, 18), (3, 12), (4, 9), (6, 6)]:
        split = {36: first, 18: (2, 9), 12: (3, 4), 9: (3, 3), 6: (2, 3), 4: (2, 2)}
        leaves = tree(f, x, 0, 36, split, dx=54, dy=44)
        assert sorted(leaves) == [2, 2, 3, 3]
        x += 215
    f.label(P(-40, -150), "Four ways to start, always two 2s and two 3s: 36 = 2 × 2 × 3 × 3", anchor="start", size=13, bold=True)
    return f

def iso(x, y, z, u):
    return P((x + y) * C30 * u, (z + (y - x) / 2) * u)

def draw_cubes(f, cubes, x0=0, u=14, cols=("#fff9c4", "#ffe082", "#ffb300")):
    S = set(cubes)
    def Q(x, y, z): q = iso(x, y, z, u); return P(q[0] + x0, q[1])
    for (x, y, z) in sorted(S, key=lambda c: (c[0] - c[1] + c[2], c[2])):
        if (x, y, z + 1) not in S:
            f.poly([Q(x, y, z + 1), Q(x + 1, y, z + 1), Q(x + 1, y + 1, z + 1), Q(x, y + 1, z + 1)], fill=cols[0])
        if (x, y - 1, z) not in S:
            f.poly([Q(x, y, z), Q(x + 1, y, z), Q(x + 1, y, z + 1), Q(x, y, z + 1)], fill=cols[1])
        if (x + 1, y, z) not in S:
            f.poly([Q(x + 1, y, z), Q(x + 1, y + 1, z), Q(x + 1, y + 1, z + 1), Q(x + 1, y, z + 1)], fill=cols[2])

@fig
def block_30():
    f = Fig("block_30")
    cubes = {(x, y, z) for x in range(5) for y in range(3) for z in range(2)}
    assert len(cubes) == 2 * 3 * 5 == 30
    draw_cubes(f, cubes, u=22)
    f.label(P(60, -80), "5 long, 3 deep, 2 high: 30 little cubes", size=13, bold=True)
    f.label(P(60, -100), "(5 × 3) × 2 = 15 × 2 = 30; (2 × 3) × 5 = 6 × 5 = 30; (2 × 5) × 3 = 10 × 3 = 30", size=11, color=HELP)
    return f

# ---------------------------------------------------------------- 5.3 thread art
def thread(f, c, n, gap, R=62):
    pts = [along(c, 90 - 360 * k / n, R) for k in range(n)]
    for k, p in enumerate(pts):
        disc(f, p, 3, INK, n=12)
        f.text(add(along(c, 90 - 360 * k / n, R + 13), (0, -4)), str(k if k else n), size=9, color=HELP)
    seen, k = [0], gap % n
    while k != 0:
        seen.append(k); k = (k + gap) % n
    seen.append(0)
    for a, b in zip(seen, seen[1:]):
        f.seg(pts[a], pts[b], color=ASK, w=1.6)
    reached = len(set(seen))
    assert reached == n // math.gcd(n, gap)
    f.label(P(c[0], c[1] - R - 30), f"{n} pegs, gap {gap}: reaches {reached}", size=12, bold=True)
    return reached

def thread_fig(name, cases):
    f = Fig(name)
    for i, (n, g) in enumerate(cases):
        thread(f, P(i * 175, 0), n, g)
    return f

@fig
def thread_art():
    return thread_fig("thread_art", [(12, 4), (13, 3), (16, 5), (24, 6)])

@fig
def thread_art_answers():
    return thread_fig("thread_art_answers", [(15, 10), (10, 7), (14, 6), (8, 3)])


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
