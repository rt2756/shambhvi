"""Figures for class 8 maths Ch 5, Number Play. Every number written on a picture is recomputed
from what is drawn: the sign tree evaluates each branch, dot pictures count their dots and rows,
place-value pictures add up to the number, and the Venn diagrams are checked against real lists
of multiples, so no label can disagree with its picture."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "5")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0"

def box(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, 30)], fill=fill, color=color)

def dots(f, x, y, n, cols, fill, u=16, r=6):
    """n dots in rows of `cols`, first row at height y, going down. Returns the dot centres."""
    cs = []
    for k in range(n):
        row, col = divmod(k, cols)
        c = P(x + col * u, y - row * u)
        disc(f, c, r, fill); cs.append(c)
    return cs

def indian(n):
    """Indian commas: 100000 -> 1,00,000."""
    s = str(n)
    if len(s) <= 3: return s
    head, tail, parts = s[:-3], s[-3:], []
    while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
    return ",".join(([head] if head else []) + parts + [tail])

def brace(f, x, ytop, ybot, text, side=1, color=GIVEN):
    """A thin bracket beside rows, with a label."""
    f.seg(P(x, ytop), P(x, ybot), color=color, w=1.6)
    f.seg(P(x - 4 * side, ytop), P(x, ytop), color=color, w=1.6)
    f.seg(P(x - 4 * side, ybot), P(x, ybot), color=color, w=1.6)
    f.label(P(x + 8 * side, (ytop + ybot) / 2 - 5), text, anchor="start" if side > 0 else "end", size=12, color=color)

# ---------------------------------------------------------------- 5.1 signs between four numbers
@fig
def sign_tree():
    f = Fig("sign_tree")
    a, b, c, d = 3, 4, 5, 6
    leaves = []
    def node(x, y, label, color=INK):
        disc(f, P(x, y + 5), 12, "#ffffff", color=HELP)
        f.text(P(x, y), label, bold=True, size=14, color=color)
    node(0, 0, str(a))
    ys = {1: 120, 2: 60, 3: 30}
    k = 0
    for s1 in "+−":
        y1 = ys[1] * (1 if s1 == "+" else -1)
        f.seg(P(14, 5), P(96, y1 + 5), color=HELP, w=1.4)
        f.label(P(52, (y1 + 5) / 2 + 8), s1, size=15, bold=True, color=GIVEN if s1 == "+" else ASK)
        node(110, y1, str(b))
        for s2 in "+−":
            y2 = y1 + ys[2] * (1 if s2 == "+" else -1)
            f.seg(P(124, y1 + 5), P(206, y2 + 5), color=HELP, w=1.4)
            f.label(P(162, (y1 + y2) / 2 + 12), s2, size=15, bold=True, color=GIVEN if s2 == "+" else ASK)
            node(220, y2, str(c))
            for s3 in "+−":
                y3 = y2 + ys[3] * (1 if s3 == "+" else -1)
                f.seg(P(234, y2 + 5), P(316, y3 + 5), color=HELP, w=1.4)
                f.label(P(272, (y2 + y3) / 2 + 12), s3, size=15, bold=True, color=GIVEN if s3 == "+" else ASK)
                node(330, y3, str(d))
                sgn = {"+": 1, "−": -1}
                val = a + sgn[s1] * b + sgn[s2] * c + sgn[s3] * d
                assert val % 2 == 0
                leaves.append(val)
                f.label(P(356, y3), f"{a} {s1} {b} {s2} {c} {s3} {d} = {val}".replace("-", "−"), anchor="start", size=13,
                        color=ANS)
    assert sorted(leaves) == sorted([18, 6, 8, -4, 10, -2, 0, -12])
    f.label(P(0, -200), "All eight answers are even.", anchor="start", size=13, bold=True, color=ANS)
    return f

# ---------------------------------------------------------------- 5.1 two even numbers and 4
def four_case(name, p, q, rem_p, rem_q):
    f = Fig(name)
    u = 16
    def block(x, y, rows, extra, fill, lab):
        cs = dots(f, x, y, 4 * rows + extra, 4, fill)
        assert len(cs) == 4 * rows + extra
        total_rows = rows + (1 if extra else 0)
        box_h = total_rows * u
        f.seg(P(x - 9, y + 9), P(x + 4 * u - 7, y + 9), color=HELP, w=1)
        brace(f, x + 4 * u, y + 8, y - box_h + 8, f"{lab} = {4 * rows + extra}")
        return total_rows
    block(0, 0, p, rem_p, BLUE, f"4×{p}" + (f" + {rem_p}" if rem_p else ""))
    f.text(P(150, -40), "+", size=22, bold=True)
    block(190, 0, q, rem_q, YELLOW, f"4×{q}" + (f" + {rem_q}" if rem_q else ""))
    total = 4 * p + rem_p + 4 * q + rem_q
    # the sum, packed into rows of 4: blue first, then yellow
    y0 = -(max(p + (rem_p > 0), q + (rem_q > 0)) + 1) * u - 20
    f.text(P(-30, y0 - 40), "=", size=22, bold=True)
    fills = [BLUE] * (4 * p + rem_p) + [YELLOW] * (4 * q + rem_q)
    for k, fl in enumerate(fills):
        row, col = divmod(k, 4)
        disc(f, P(col * u, y0 - row * u), 6, fl)
    full, left = divmod(total, 4)
    rows_drawn = full + (1 if left else 0)
    brace(f, 4 * u, y0 + 8, y0 - rows_drawn * u + 8,
          f"{total} = 4 × {full}" + (f" + {left}" if left else "") + ("  ✓ multiple of 4" if left == 0 else "  ✗ remainder 2"))
    return f, total, left

@fig
def fours_both():
    f, total, left = four_case("fours_both", 3, 4, 0, 0)
    assert (total, left) == (28, 0)
    return f

@fig
def fours_both_rem2():
    f, total, left = four_case("fours_both_rem2", 1, 2, 2, 2)
    assert (total, left) == (16, 0)            # 6 + 10 = 16: the two leftover 2s make a full row
    return f

@fig
def fours_mixed():
    f, total, left = four_case("fours_mixed", 2, 1, 0, 2)
    assert (total, left) == (14, 2)            # 8 + 6 = 14: a lonely 2 is left over
    return f

# ---------------------------------------------------------------- 72 split two ways
@fig
def eight_split():
    f = Fig("eight_split")
    u = 16
    for x0, first, title in [(0, 48, "72 = 48 + 24"), (230, 50, "72 = 50 + 22")]:
        for k in range(72):
            row, col = divmod(k, 8)
            disc(f, P(x0 + col * u, -row * u), 6, BLUE if k < first else YELLOW)
        f.label(P(x0 + 56, 22), title, size=14, bold=True)
        ok = first % 8 == 0 and (72 - first) % 8 == 0
        f.label(P(x0 + 56, -9 * u - 6), "both parts are whole rows of 8 ✓" if ok else "the cut goes through a row ✗",
                size=12, color=ANS if ok else ASK)
    return f

# ---------------------------------------------------------------- factors of 12 cover a row
@fig
def twelve_rows():
    f = Fig("twelve_rows")
    u = 16
    groupings = [2, 3, 4, 6]
    for i, g in enumerate(groupings):
        y = -i * 30
        for k in range(12):
            disc(f, P(k * u + (k // g) * 6, y), 6, [BLUE, YELLOW][(k // g) % 2])
        assert 12 % g == 0
        f.label(P(12 * u + (12 // g) * 6 + 4, y - 5), f"12 = {12 // g} groups of {g}", anchor="start", size=13)
    f.label(P(0, 22), "One row of 12 splits exactly into groups of 2, 3, 4 and 6,", anchor="start", size=13, color=GIVEN)
    f.label(P(0, -4 * 30 - 4), "so every row of every multiple of 12 does too.", anchor="start", size=13, color=GIVEN)
    return f

# ---------------------------------------------------------------- remainder 3 on division by 5
@fig
def five_k_plus_3():
    f = Fig("five_k_plus_3")
    u = 16
    x = 0
    for k in range(0, 4):
        n = 5 * k + 3
        cs = dots(f, x, 0, 5 * k, 5, BLUE)
        cs += [P(x + j * u, -k * u) for j in range(3)]
        for c in cs[5 * k:]:
            disc(f, c, 6, ORANGE)
        assert len(cs) == n and n % 5 == 3
        f.label(P(x + 2 * u, 24), f"k = {k}", size=13, color=GIVEN)
        f.label(P(x + 2 * u, -4 * u - 4), f"5×{k} + 3 = {n}", size=13, bold=True)
        x += 5 * u + 36
    f.label(P(0, -4 * u - 34), "Blue: k full rows of 5.  Orange: the 3 left over.", anchor="start", size=12, color=HELP)
    return f

# ---------------------------------------------------------------- remainders on division by 7 add up
@fig
def sevens_add():
    f = Fig("sevens_add")
    u = 16
    def lump(x, y, rows, extra, fill, lab):
        dots(f, x, y, 7 * rows, 7, fill)
        for j in range(extra):
            disc(f, P(x + j * u, y - rows * u), 6, ORANGE)
        f.label(P(x + 3 * u, y + 22), lab, size=13, bold=True)
    lump(0, 0, 2, 5, BLUE, "7p + 5")
    f.text(P(130, -22), "+", size=22, bold=True)
    lump(160, 0, 1, 3, YELLOW, "7q + 3")
    f.label(P(0, -3 * u - 18), "p rows (here 2)", anchor="start", size=12, color=HELP)
    f.label(P(160, -3 * u - 18), "q rows (here 1)", anchor="start", size=12, color=HELP)
    # the leftovers 5 + 3 = 8 = one more row of 7 and 1
    y = -6 * u - 10
    left = 5 + 3
    full, r = divmod(left, 7)
    assert (full, r) == (1, 1)
    for j in range(left):
        row, col = divmod(j, 7)
        disc(f, P(col * u, y - row * u), 6, ORANGE)
    f.label(P(7 * u + 6, y - 5), f"leftovers 5 + 3 = {left} = one more row of 7 + {r}", anchor="start", size=13, color=ANS)
    f.label(P(0, y - 2 * u - 16), "So (7p + 5) + (7q + 3) = 7(p + q + 1) + 1: remainder 1.", anchor="start", size=13, bold=True, color=ANS)
    return f

# ---------------------------------------------------------------- 5.2 why "add the digits" works for 9
@fig
def nines_427():
    f = Fig("nines_427")
    n = 427
    h, t, o = n // 100, n // 10 % 10, n % 10
    x = 0
    ones = 0
    for count, big, lab in [(h, 99, "hundreds"), (t, 9, "tens")]:
        for i in range(count):
            box(f, x, 0, 44, 26, fill=BLUE)
            f.text(P(x + 22, 8), str(big), size=13, bold=True)
            disc(f, P(x + 22, -20), 9, ORANGE)
            f.text(P(x + 22, -24), "1", size=11, bold=True)
            x += 52
            ones += 1
        f.label(P(x - count * 52 + (count * 52 - 8) / 2, 40), f"{count} {lab}", size=12, color=GIVEN)
        x += 16
    for i in range(o):
        disc(f, P(x + 12, -20), 9, ORANGE)
        f.text(P(x + 12, -24), "1", size=11, bold=True)
        x += 24
        ones += 1
    f.label(P(x - o * 24 / 2 - 6, 40), f"{o} ones", size=12, color=GIVEN)
    assert h * 100 + t * 10 + o == n and h * 99 + t * 9 + ones == n and ones == h + t + o == 13
    f.label(P(0, -52), "Blue blocks (99 and 9) are already multiples of 9.", anchor="start", size=13, color=GIVEN)
    f.label(P(0, -72), f"Orange ones left: {h} + {t} + {o} = {ones} = 9 + {ones - 9}, so 427 ÷ 9 leaves remainder {n % 9}.",
            anchor="start", size=13, bold=True, color=ANS)
    assert n % 9 == ones - 9 == 4
    return f

# ---------------------------------------------------------------- 5.2 place values and 11
@fig
def elevens_places():
    f = Fig("elevens_places")
    rows = []
    for k in range(6):
        pv = 10 ** k
        m = round(pv / 11)
        diff = pv - 11 * m
        assert diff in (1, -1) and diff == (1 if k % 2 == 0 else -1)
        rows.append((pv, m, diff))
    for i, (pv, m, diff) in enumerate(rows):
        y = -i * 30
        f.label(P(0, y), indian(pv), anchor="end", size=14, bold=True)
        f.label(P(12, y), f"= 11 × {indian(m)} {'+' if diff > 0 else '−'} 1", anchor="start", size=14)
        f.label(P(230, y), "one MORE than a multiple of 11" if diff > 0 else "one LESS than a multiple of 11",
                anchor="start", size=13, color=ANS if diff > 0 else ASK)
    f.label(P(-60, 30), "place value", anchor="start", size=12, color=HELP)
    return f

@fig
def elevens_signs():
    f = Fig("elevens_signs")
    n = 320185
    s = str(n)
    L = len(s)
    total = 0
    for i, ch in enumerate(s):
        k = L - 1 - i                           # power of ten of this digit
        sign = 1 if k % 2 == 0 else -1
        total += sign * int(ch)
        x = i * 44
        box(f, x, 0, 36, 36, fill=GREEN if sign > 0 else PINK)
        f.text(P(x + 18, 12), ch, size=18, bold=True)
        f.text(P(x + 18, -22), "+" if sign > 0 else "−", size=18, bold=True, color=ANS if sign > 0 else ASK)
        f.label(P(x + 18, 48), indian(10 ** k), size=11, color=HELP)
    assert total == -3 and n % 11 == 8
    f.label(P(0, -50), f"+5 − 8 + 1 − 0 + 2 − 3 = {total}", anchor="start", size=14, bold=True, color=ANS)
    f.label(P(0, -72), f"So 320185 is 3 short of a multiple of 11 (remainder 11 − 3 = {n % 11}).", anchor="start", size=13, color=ANS)
    return f

# ---------------------------------------------------------------- digital roots go round a 9-clock
def droot(n):
    while n > 9: n = sum(int(c) for c in str(n))
    return n

@fig
def root_clock():
    f = Fig("root_clock")
    R = 80
    for x0, step in [(0, 4), (250, 3)]:
        pos = {}
        for r in range(1, 10):
            a = 90 - (r % 9) * 40
            pos[r] = along(P(x0, 0), a, R)
        seq = [droot(step * m) for m in range(1, 10)]
        if step == 4: assert seq == [4, 8, 3, 7, 2, 6, 1, 5, 9]
        if step == 3: assert seq == [3, 6, 9] * 3
        for i in range(8):
            a1, a2 = pos[seq[i]], pos[seq[i + 1]]
            if a1 != a2: f.seg(a1, a2, color=GIVEN if step == 4 else ANS, w=1.4)
        for r in range(1, 10):
            hit = r in seq
            disc(f, pos[r], 13, YELLOW if hit else GREY)
            f.text(P(pos[r][0], pos[r][1] - 5), str(r), size=13, bold=hit, color=INK if hit else HELP)
        f.label(P(x0, -R - 34), f"multiples of {step}: " + ", ".join(map(str, seq[:9 if step == 4 else 3])) + ", …",
                size=12, color=GIVEN if step == 4 else ANS)
    return f

# ---------------------------------------------------------------- Venn diagrams for 4, 8, 32
@fig
def venn_options():
    f = Fig("venn_options")
    m4 = set(range(4, 2001, 4)); m8 = set(range(8, 2001, 8)); m32 = set(range(32, 2001, 32))
    assert m32 < m8 < m4                       # every multiple of 32 is a multiple of 8, and of 8 a multiple of 4
    def ell(c, rx, ry, fill):
        f.poly([P(c[0] + rx * math.cos(d2r(a)), c[1] + ry * math.sin(d2r(a))) for a in range(0, 360, 10)], fill=fill)
    # (i) three overlapping in a row
    ell(P(0, 0), 42, 28, BLUE); ell(P(56, 0), 42, 28, YELLOW); ell(P(112, 0), 42, 28, GREEN)
    for x, t in [(-14, "4"), (56, "8"), (126, "32")]: f.text(P(x, -5), t, size=13, bold=True)
    f.label(P(-50, 42), "(i)", anchor="start", bold=True, size=14)
    # (ii) two overlapping: 4 on the left, 8 in the overlap, 32 on the right
    x0 = 260
    ell(P(x0, 0), 44, 30, BLUE); ell(P(x0 + 60, 0), 44, 30, YELLOW)
    f.text(P(x0 - 20, -5), "4", size=13, bold=True); f.text(P(x0 + 30, -5), "8", size=13, bold=True); f.text(P(x0 + 80, -5), "32", size=13, bold=True)
    f.label(P(x0 - 54, 42), "(ii)", anchor="start", bold=True, size=14)
    # (iii) nested the wrong way: 32 outside, then 8, then 4
    y0 = -130
    ell(P(56, y0), 70, 56, GREEN); ell(P(56, y0 - 6), 46, 38, YELLOW); ell(P(56, y0 - 10), 20, 16, BLUE)
    f.text(P(56, y0 + 40), "32", size=13, bold=True); f.text(P(56, y0 + 14), "8", size=13, bold=True); f.text(P(56, y0 - 15), "4", size=13, bold=True)
    f.label(P(-50, y0 + 62), "(iii)", anchor="start", bold=True, size=14)
    # (iv) nested the right way: 4 outside, then 8, then 32
    ell(P(x0 + 30, y0), 70, 56, BLUE); ell(P(x0 + 30, y0 - 6), 46, 38, YELLOW); ell(P(x0 + 30, y0 - 10), 20, 16, GREEN)
    f.text(P(x0 + 30, y0 + 40), "4", size=13, bold=True); f.text(P(x0 + 30, y0 + 14), "8", size=13, bold=True); f.text(P(x0 + 30, y0 - 15), "32", size=12, bold=True)
    f.label(P(x0 - 54, y0 + 62), "(iv)", anchor="start", bold=True, size=14)
    f.label(P(-50, y0 - 80), "Each oval is 'multiples of' the number written in it.", anchor="start", size=12, color=HELP)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
