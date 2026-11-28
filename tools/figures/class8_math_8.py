"""Figures for class 8 maths Ch 8, Fractions in Disguise (percentages). Bar models and double
number lines place every mark from the percentage it shows, money and amount labels are computed
from the same numbers, the area grid counts its own squares, and the knights board checks that no
knight attacks another, so no label can disagree with its picture."""
import math, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "8")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, YELLOW, GREEN, GREY, ORANGE, PINK, RED = "#90caf9", "#fff59d", "#a5d6a7", "#eceff1", "#ffcc80", "#f8bbd0", "#e57373"
NAVY, GOLD = "#37587a", "#f2a531"

def rect(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=INK):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, 20)], fill=fill, color=color)

def fmt(v):
    v = float(v)
    return f"{v:,.2f}".rstrip("0").rstrip(".") if v != int(v) else f"{int(v):,}"

def double_line(f, y, W, total, pcts, top_fmt, filled=None, unit=""):
    """A bar of length W standing for `total`; ticks at each percentage, amounts above, % below."""
    if filled is not None:
        rect(f, 0, y, W * filled / 100, 18, fill=BLUE)
    rect(f, 0, y, W, 18, fill="none", color=INK)
    for p in pcts:
        x = W * p / 100
        f.seg(P(x, y - 6), P(x, y + 24), color=INK, w=1.4)
        amount = F(total) * F(p) / 100
        f.label(P(x, y + 30), top_fmt(amount), size=12, color=GIVEN)
        f.label(P(x, y - 22), f"{fmt(p)}%", size=12, color=ANS)

# ---------------------------------------------------------------- 1.1 fractions as percentages
@fig
def three_quarters():
    f = Fig("three_quarters")
    W = 400
    for q in range(4):
        rect(f, q * W / 4, 0, W / 4, 22, fill=ORANGE if q < 3 else YELLOW)
    for q in range(5):
        x = q * W / 4
        f.seg(P(x, -6), P(x, 28), w=1.4)
        fr = F(q, 4)
        f.label(P(x, 34), f"{fr.numerator}/{fr.denominator}" if 0 < q < 4 else str(int(fr)), size=12, color=GIVEN)
        assert fr * 100 == 25 * q
        f.label(P(x, -22), f"{25 * q}%", size=12, color=ANS)
    f.label(P(W / 2, -46), "3/4 of the bar = 75 out of every 100 = 75%", size=13, bold=True)
    return f

@fig
def two_fifths():
    f = Fig("two_fifths")
    W = 400
    for q in range(5):
        rect(f, q * W / 5, 0, W / 5, 22, fill=BLUE if q < 2 else "#ffffff")
    for q in range(6):
        x = q * W / 5
        f.seg(P(x, -6), P(x, 28), w=1.4)
        f.label(P(x, 34), "0" if q == 0 else ("1" if q == 5 else f"{q}/5"), size=12, color=GIVEN)
        assert F(q, 5) * 100 == 20 * q
        f.label(P(x, -22), f"{20 * q}%", size=12, color=ANS)
    f.label(P(W * 0.2, 6), "savings", size=12, bold=True)
    f.label(P(W / 2, -46), "2/5 of the prize = 40%", size=13, bold=True)
    return f

@fig
def runners():
    f = Fig("runners")
    W = 420
    f.seg(P(0, 0), P(W, 0), w=2.4)
    for x in (0, W): f.seg(P(x, -8), P(x, 8), w=2.4)
    f.label(P(0, -24), "Start", size=12); f.label(P(W, -24), "Finish", size=12)
    for name, p in [("A", 38), ("B", 55), ("C", 72), ("D", 93)]:
        disc(f, P(W * p / 100, 0), 7, BLUE)
        f.label(P(W * p / 100, 14), name, size=13, bold=True)
    return f

@fig
def runners_answer():
    f = Fig("runners_answer")
    W = 420
    f.seg(P(0, 0), P(W, 0), w=2.4)
    for p in range(0, 101, 10):
        f.seg(P(W * p / 100, -5), P(W * p / 100, 5), w=1.2, color=HELP)
        f.label(P(W * p / 100, -22), f"{p}%", size=10, color=HELP)
    for name, p in [("A", 38), ("B", 55), ("C", 72), ("D", 93)]:
        disc(f, P(W * p / 100, 0), 7, BLUE)
        f.label(P(W * p / 100, 14), f"{name} ≈ {p}%", size=12, bold=True, color=ANS)
    return f

# ---------------------------------------------------------------- 1.2 percentage of a quantity
@fig
def sugar_120():
    f = Fig("sugar_120")
    double_line(f, 0, 400, 120, [0, 25, 50, 75, 100], lambda a: f"{fmt(a)} g", filled=25)
    assert F(120) * 25 / 100 == 30
    f.label(P(200, -46), "25% of 120 g of biscuits = 30 g of sugar", size=13, bold=True)
    return f

@fig
def marks_75():
    f = Fig("marks_75")
    double_line(f, 0, 400, 75, [0, 20, 40, 60, 80, 100], lambda a: fmt(a), filled=80)
    assert F(75) * 80 / 100 == 60
    f.label(P(200, -46), "80% of 75 marks = 60 marks", size=13, bold=True)
    return f

@fig
def cyclist():
    f = Fig("cyclist")
    W, total = 400, 230
    assert F(92) / F(40, 100) == total
    rect(f, 0, 0, W * 0.4, 22, fill=GREEN); rect(f, W * 0.4, 0, W * 0.6, 22, fill="#ffffff")
    f.label(P(W * 0.2, 6), "92 km done", size=12, bold=True)
    f.label(P(W * 0.7, 6), f"{fmt(total - 92)} km to go", size=12, bold=True, color=ASK)
    for p in range(0, 101, 20):
        f.seg(P(W * p / 100, -6), P(W * p / 100, 0), w=1.4)
        f.label(P(W * p / 100, -22), f"{p}%", size=11, color=ANS)
        f.label(P(W * p / 100, 30), fmt(F(total) * p / 100), size=11, color=GIVEN)
    f.label(P(0, 48), "Delhi", anchor="start", size=12); f.label(P(W, 48), "Agra", anchor="end", size=12)
    return f

@fig
def millet():
    f = Fig("millet")
    u = 40
    for i in range(9):
        rect(f, i * u, 0, u, 24, fill=ORANGE if i < 2 else BLUE)
    f.label(P(u, 32), "millet 2", size=12, bold=True)
    f.label(P(2 * u + 3.5 * u, 32), "water 7", size=12, bold=True)
    pct = F(2, 9) * 100
    assert round(float(pct), 2) == 22.22
    f.label(P(0, -18), f"millet = 2/9 of the mixture ≈ {float(pct):.2f}%", anchor="start", size=13, bold=True, color=ANS)
    return f

@fig
def sales_target():
    f = Fig("sales_target")
    k, target = 0.04, 5000
    days = [(1, 2000), (2, 3500), (3, 5000), (4, 6000), (5, 7800), (6, 9550)]
    for i, (d, s) in enumerate(days):
        y = -i * 30
        rect(f, 0, y, s * k, 18, fill=GREEN if s >= target else ORANGE)
        f.label(P(-8, y + 4), f"Day {d}", anchor="end", size=12)
        pct = F(s, target) * 100
        f.label(P(s * k + 8, y + 4), f"₹{s:,} = {fmt(pct)}%", anchor="start", size=12, color=ANS)
    for m in (0, 5000, 10000):
        x = m * k
        f.seg(P(x, 26), P(x, -6 * 30 + 12), color=ASK if m == target else HELP, w=1.4, dash="5,4")
        f.label(P(x, 32), f"{m // 50}%" + (" (target)" if m == target else ""), size=12, color=ASK if m == target else HELP)
    return f

@fig
def percent_line():
    f = Fig("percent_line")
    W = 520
    f.seg(P(0, 0), P(W, 0), w=2)
    for p in range(0, 401, 100):
        f.seg(P(W * p / 400, -8), P(W * p / 400, 8), w=2)
        f.label(P(W * p / 400, -26), f"{p}% ({p // 100})", size=12, color=HELP)
    marks = [90, 110, 200, 250, 15, 173, 358, 28.9, 305]
    for i, p in enumerate(sorted(marks)):
        x = W * p / 400
        h = 18 + (i % 3) * 18
        f.seg(P(x, 0), P(x, h), color=GIVEN, w=1.2)
        f.label(P(x, h + 4), f"{fmt(p)}%", size=11, color=GIVEN)
    return f

@fig
def missing_bars():
    f = Fig("missing_bars")
    rows = [("(i)", 5, 1, "20%", 75, 4, "60"), ("(ii)", 10, 1, "?", 90, 6, "?"), ("(iii)", 4, 1, "?", 140, 3, "?")]
    for r, (lab, n, k1, l1, tot, k2, l2) in enumerate(rows):
        y = -r * 78
        f.label(P(-14, y + 4), lab, anchor="end", size=13, bold=True)
        for x0, kk, ll, total in [(0, k1, l1, None), (260, k2, l2, tot)]:
            w = 200 / n
            for i in range(n):
                rect(f, x0 + i * w, y, w, 20, fill=BLUE if i < kk else "#ffffff", color="#e64a19")
            f.label(P(x0 + 100, y + 30), "100%", size=11, color=HELP)
            f.seg(P(x0, y - 8), P(x0 + kk * w, y - 8), color=GIVEN, w=1.4)
            f.label(P(x0 + kk * w / 2, y - 24), ll, size=12, color=GIVEN)
            if total: f.label(P(x0 + 200, y - 24), str(total), size=12, color=INK)
        assert F(tot) * k2 / n in (60, 54, 105)
    return f

# ---------------------------------------------------------------- 1.3 using percentages
@fig
def sweater_chain():
    f = Fig("sweater_chain")
    stages = [("Maker", 230, 255, 253), ("Wholesaler", 253, 310, 300), ("Shop", 300, 480, 430)]
    for i, (who, cp, mp, sp) in enumerate(stages):
        x = i * 170
        rect(f, x, -8, 140, 100, fill="#f5f5f5")
        f.label(P(x + 70, 70), who, size=14, bold=True)
        f.label(P(x + 10, 46), f"cost ₹{cp}", anchor="start", size=12)
        f.label(P(x + 10, 26), f"marked ₹{mp}", anchor="start", size=12)
        f.label(P(x + 10, 6), f"sold ₹{sp}", anchor="start", size=12)
        pr = F(sp - cp, cp) * 100
        f.label(P(x + 70, -26), f"profit ₹{sp - cp} = {float(pr):.1f}%", size=12, color=ANS, bold=True)
        if i < 2:
            f.text(P(x + 155, 38), "→", size=20, bold=True, color=GIVEN)
            assert stages[i + 1][1] == sp         # one stage's selling price is the next one's cost price
    return f

@fig
def compounding():
    f = Fig("compounding")
    k = 0.035
    simple, comp = 6000, 6000
    for t in range(0, 4):
        x = t * 120
        s = 6000 + 600 * t
        c = round(6000 * 1.1 ** t, 2)
        rect(f, x, 0, 40, s * k, fill=BLUE)
        rect(f, x + 46, 0, 40, c * k, fill=ORANGE)
        f.label(P(x + 20, s * k + 6), f"{s:,}", size=11, color=GIVEN)
        f.label(P(x + 66, c * k + 20 if t else c * k + 6), f"{fmt(c)}", size=11, color=ANS)
        f.label(P(x + 43, -18), f"year {t}", size=12)
    assert round(6000 * 1.1 ** 3, 2) == 7986
    rect(f, 0, -54, 14, 12, fill=BLUE); f.label(P(20, -54), "no compounding: + ₹600 every year", anchor="start", size=12)
    rect(f, 0, -74, 14, 12, fill=ORANGE); f.label(P(20, -74), "compounding: × 1.1 every year", anchor="start", size=12)
    return f

@fig
def area_grid():
    f = Fig("area_grid")
    u = 22
    for i in range(10):
        for j in range(10):
            f.dot(P((i - 1) * u, (j - 1) * u), color=HELP)
    def poly(pts, fill, lab, at):
        f.poly([P(x * u, y * u) for x, y in pts], fill=fill)
        f.text(P(at[0] * u, at[1] * u - 6), lab, size=15, bold=True)
    poly([(0, 4), (4, 4), (4, 8), (0, 8)], BLUE, "A", (2, 6))
    poly([(4, 2), (8, 2), (8, 8), (4, 8)], GREEN, "B", (6, 5))
    poly([(4, 0), (8, 0), (8, 2), (4, 2)], YELLOW, "C", (6, 1))
    poly([(0, 0), (4, 4), (0, 4)], PINK, "D", (1.2, 2.8))
    poly([(0, 0), (4, 0), (4, 4)], ORANGE, "E", (2.8, 1.2))
    areas = {"A": 16, "B": 24, "C": 8, "D": 8, "E": 8}
    assert sum(areas.values()) == 64 and F(areas["E"], 64) * 100 == F(25, 2)
    return f

@fig
def computer_use():
    f = Fig("computer_use")
    data = [("Children", 4, 5), ("Teenage", 24, 29), ("Twenties", 26, 37), ("Thirties", 14, 25),
            ("Forties", 7, 14), ("Fifties", 4, 9), ("Seniors", 2, 4)]
    k = 10
    for i, (grp, fem, male) in enumerate(data):
        y = -i * 40
        rect(f, 0, y, fem * k, 14, fill=NAVY)
        rect(f, 0, y - 15, male * k, 14, fill=GOLD)
        f.label(P(-8, y - 6), grp, anchor="end", size=12)
        f.label(P(fem * k + 4, y + 1), f"{fem}%", anchor="start", size=10, color=NAVY)
        f.label(P(male * k + 4, y - 14), f"{male}%", anchor="start", size=10, color="#8a5a00")
        assert fem < male
    for p in range(0, 41, 10):
        f.seg(P(p * k, 22), P(p * k, -7 * 40 + 18), color=GREY, w=1)
        f.label(P(p * k, -7 * 40 + 2), f"{p}%", size=11, color=HELP)
    rect(f, 0, 36, 12, 10, fill=NAVY); f.label(P(16, 36), "female", anchor="start", size=12)
    rect(f, 80, 36, 12, 10, fill=GOLD); f.label(P(96, 36), "male", anchor="start", size=12)
    f.label(P(0, -7 * 40 - 18), "Share of each group able to use a computer (survey, 2023; children's male value read off the chart, about 5%)", anchor="start", size=10, color=HELP)
    return f

@fig
def knights():
    f = Fig("knights")
    u = 34
    for r in range(8):
        for c in range(8):
            rect(f, c * u, r * u, u, u, fill="#8d2b2b" if (r + c) % 2 == 0 else "#ffffff", color="#8d2b2b")
    placed = [(0, c) for c in range(8)]                  # every square of the bottom row
    moves = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
    S = set(placed)
    assert all((r + dr, c + dc) not in S for r, c in placed for dr, dc in moves)
    for r, c in placed:
        disc(f, P(c * u + u / 2, r * u + u / 2), 11, YELLOW)
        f.text(P(c * u + u / 2, r * u + u / 2 - 6), "N", size=13, bold=True)
    f.label(P(4 * u, -18), "8 knights on one row: a knight always changes row by 1 or 2, so none attacks another", size=11, color=ANS)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
