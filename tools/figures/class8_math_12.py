"""Figures for class 8 maths Ch 12, Tales by Dots and Lines. Dot plots are drawn from their data
and every mean or median written on them is recomputed; line graphs are drawn from the tables
in this script (values read off published charts are marked approximate in the notes); the
activity strips are our own and are checked to cover all 48 half-hours; so no label can disagree
with its picture."""
import math, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class8", "math", "12")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

COLS = ["#1e88e5", "#e53935", "#43a047", "#fb8c00", "#8e24aa", "#00897b"]
LIGHT = "#cfd8dc"

def rect(f, x, y, w, h, fill="#ffffff", color=INK):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color)

def disc(f, c, r, fill, color=None):
    f.poly([P(c[0] + r * math.cos(d2r(a)), c[1] + r * math.sin(d2r(a))) for a in range(0, 360, 30)], fill=fill, color=color or fill)

def mean(v): return F(sum(F(x) for x in v), len(v))

def median(v):
    s = sorted(F(x) for x in v); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

def fmt(q):
    q = float(q)
    return str(int(q)) if q == int(q) else f"{q:.2f}".rstrip("0").rstrip(".")

def dotplot(f, x0, y0, data, lo, hi, step=1, k=24, colour="#f4511e", show_mean=True, label_every=1, new=None, title=None):
    """Axis from lo to hi; stacked dots; a vertical line at the mean."""
    W = (hi - lo) * k
    f.seg(P(x0, y0), P(x0 + W, y0), w=1.4)
    t = lo
    i = 0
    while t <= hi + 1e-9:
        x = x0 + (t - lo) * k
        f.seg(P(x, y0), P(x, y0 - 4), w=1)
        if i % label_every == 0: f.label(P(x, y0 - 18), fmt(t), size=11, color=HELP)
        t += step; i += 1
    count = {}
    for v in data:
        n = count.get(v, 0); count[v] = n + 1
        col = "#43a047" if (new is not None and v in new and n == count[v] - 1 and count[v] > data.count(v) - new.count(v)) else colour
        disc(f, P(x0 + (v - lo) * k, y0 + 9 + n * 13), 5.5, col)
    if show_mean:
        m = mean(data)
        xm = x0 + float(m - lo) * k
        top = y0 + 14 + max(count.values()) * 13
        f.seg(P(xm, y0 - 2), P(xm, top), color=GIVEN, w=1.6, dash="4,3")
        f.label(P(xm + 4, top + 4), f"mean = {fmt(m)}", anchor="start", size=11, color=GIVEN)
    if title: f.label(P(x0 - 12, y0 + 12), title, anchor="end", size=13, bold=True)
    return W

# ---------------------------------------------------------------- 12.1 the mean as a balance point
@fig
def balance():
    f = Fig("balance")
    for i, data in enumerate([[6, 7, 8], [10, 10, 11, 17]]):
        y0 = -i * 110
        lo, hi = (4, 10) if i == 0 else (8, 18)
        dotplot(f, 0, y0, data, lo, hi, k=28)
        m = mean(data)
        lhs = sum(m - v for v in data if v < m); rhs = sum(v - m for v in data if v > m)
        assert lhs == rhs
        f.label(P(0, y0 - 40), f"distances below the mean: {' + '.join(fmt(m - v) for v in data if v < m)} = {fmt(lhs)};   above: {' + '.join(fmt(v - m) for v in data if v > m)} = {fmt(rhs)}",
                anchor="start", size=11, color=ANS)
    return f

@fig
def new_value():
    f = Fig("new_value")
    old = [5, 5, 10, 24]
    assert mean(old) == 11
    dotplot(f, 0, 0, old, 4, 24, k=18, label_every=2, title="before")
    new = old + [17]
    assert mean(new) == F(61, 5)
    dotplot(f, 0, -80, new, 4, 24, k=18, label_every=2, new=[17], title="after")
    f.label(P(0, -126), "the new value 17 (green) is above the old mean 11, so the mean moves up to 12.2", anchor="start", size=11, color=ANS)
    return f

SHIFT = [8, 3, 10, 13, 4, 6, 7, 7, 8, 8, 5]

@fig
def shift_plots():
    f = Fig("shift_plots")
    assert mean(SHIFT) == F(79, 11)
    dotplot(f, 0, 0, SHIFT, 0, 14, k=20, label_every=2, colour="#8e24aa")
    up = [v + 10 for v in SHIFT]
    assert mean(up) == mean(SHIFT) + 10
    dotplot(f, 0, -90, up, 10, 24, k=20, label_every=2, colour="#8e24aa")
    f.label(P(0, -136), "every value + 10: the same picture slid along, so the mean is 7.18 + 10 = 17.18", anchor="start", size=11, color=ANS)
    return f

@fig
def median_shift():
    f = Fig("median_shift")
    d = [3, 5, 8, 11, 14]
    assert median(d) == 8
    dotplot(f, 0, 0, d, 2, 15, k=22, show_mean=False)
    f.label(P(0, 40), f"median = {fmt(median(d))}", anchor="start", size=12, color=GIVEN)
    d2 = d + [11]
    assert median(d2) == F(19, 2)
    dotplot(f, 0, -80, d2, 2, 15, k=22, show_mean=False, new=[11])
    f.label(P(0, -40), f"include 11: median = (8 + 11) ÷ 2 = {fmt(median(d2))}", anchor="start", size=12, color=ANS)
    return f

# ---------------------------------------------------------------- Figure it out dot plots
ALBUMS = {"A": [5, 5, 5.25, 5.5, 5.75, 6, 6.5], "B": [0.5, 0.75, 1.5, 1.5, 2, 3.75, 4.25, 5], "C": [3.5, 3.5, 3.5, 4, 4, 4, 4.25, 4.5]}

@fig
def albums():
    f = Fig("albums")
    for i, (k_, v) in enumerate(ALBUMS.items()):
        dotplot(f, 0, -i * 70, v, 0, 7.5, step=0.5, k=40, colour=INK, show_mean=False, title=k_)
    assert round(float(mean(ALBUMS["A"])), 2) == 5.57
    assert round(float(mean(ALBUMS["B"])), 2) != 5.57 and round(float(mean(ALBUMS["C"])), 2) != 5.57
    return f

MISSING = [6, 7, 7, 9, 10, 12]               # plus one missing dot; mean must be 9

@fig
def missing_dot():
    f = Fig("missing_dot")
    dotplot(f, 0, 0, MISSING, 4, 14, k=28, show_mean=False)
    x = (9 - 4) * 28
    f.seg(P(x, -2), P(x, 50), color=GIVEN, w=1.6, dash="4,3")
    f.label(P(x + 4, 54), "mean = 9", anchor="start", size=11, color=GIVEN)
    missing = 9 * 7 - sum(MISSING)
    assert missing == 12
    return f

CYCLE = {0: 3, 1: 1, 2: 4, 3: 7, 4: 7, 5: 5, 6: 4, 7: 6, 8: 3, 10: 2}

@fig
def cycles():
    f = Fig("cycles")
    data = [v for v, c in CYCLE.items() for _ in range(c)]
    assert len(data) == 42 and CYCLE[2] == 4
    dotplot(f, 0, 0, data, 0, 10, k=30, colour="#26a69a", show_mean=False)
    f.label(P(150, -40), "number of times each student rode a cycle in one week", size=11, color=HELP)
    return f

CROSS = {14: 2, 15: 2, 16: 3, 18: 5, 19: 4, 20: 4, 21: 3, 22: 1, 23: 1}

@fig
def cross_plot():
    f = Fig("cross_plot")
    k = 30
    f.seg(P(0, 0), P(9 * k, 0), w=1.4)
    for v in range(14, 24):
        f.label(P((v - 14) * k, -18), str(v), size=11, color=HELP)
        for n in range(CROSS.get(v, 0)):
            f.text(P((v - 14) * k, 6 + n * 14), "×", size=15, bold=True)
    data = [v for v, c in CROSS.items() for _ in range(c)]
    assert mean(data) > 17
    return f

# ---------------------------------------------------------------- line graphs
def line_graph(f, series, xs_labels, ymin, ymax, ystep, W=420, H=200, ylab="", legend=True, every=1, markers=True):
    n = len(xs_labels)
    dx = W / (n - 1)
    sy = H / (ymax - ymin)
    y = ymin
    while y <= ymax + 1e-9:
        f.seg(P(0, (y - ymin) * sy), P(W, (y - ymin) * sy), color=LIGHT, w=1)
        f.label(P(-8, (y - ymin) * sy - 5), fmt(y), anchor="end", size=10, color=HELP)
        y += ystep
    for i, lab in enumerate(xs_labels):
        if i % every == 0: f.label(P(i * dx, -18), lab, size=10, color=HELP)
    for j, (name, vals) in enumerate(series):
        col = COLS[j % len(COLS)]
        pts = [P(i * dx, (v - ymin) * sy) for i, v in enumerate(vals) if v is not None]
        for p, q in zip(pts, pts[1:]): f.seg(p, q, color=col, w=2)
        if markers:
            for p in pts: disc(f, p, 3.2, col)
        if legend:
            f.poly([P(W + 14, H - j * 20), P(W + 26, H - j * 20), P(W + 26, H - j * 20 + 10), P(W + 14, H - j * 20 + 10)], fill=col, color=col)
            f.label(P(W + 32, H - j * 20), name, anchor="start", size=11)
    if ylab: f.label(P(0, H + 16), ylab, anchor="start", size=11, color=HELP)

MONTHS = "J F M A M J J A S O N D".split()
KERALA = [30.5, 31.5, 32.5, 33, 32, 30.5, 29, 29, 29.5, 30, 31, 31]
PUNJAB = [18.5, 26, 29, 34, 37, 38, 34.5, 35, 35.5, 33, 28, 23]

@fig
def temperature():
    f = Fig("temperature")
    line_graph(f, [("Kerala", KERALA), ("Punjab", PUNJAB)], MONTHS, 0, 40, 10, ylab="monthly maximum temperature (°C), 2023 (approximate)")
    assert max(PUNJAB) - min(PUNJAB) > max(KERALA) - min(KERALA)
    return f

YEARS = [str(y) for y in range(2012, 2025)]
WORLD = [150, 240, 260, 250, 230, 470, 460, 590, 1270, 1800, 2480, 2900, 2850]
USA = [60, 100, 110, 110, 100, 300, 230, 380, 1000, 1230, 1950, 2230, 2260]
CHINA = [20, 20, 30, 50, 60, 70, 110, 90, 90, 120, 200, 220, 280]
RUSSIA = [30, 30, 40, 30, 20, 20, 30, 30, 20, 40, 30, 60, 100]

@fig
def space():
    f = Fig("space")
    line_graph(f, [("World", WORLD), ("USA", USA), ("China", CHINA), ("Russia", RUSSIA)], [y[2:] for y in YEARS], 0, 3000, 500,
               ylab="objects launched into space each year (approximate)")
    doubles = [YEARS[i] + "→" + YEARS[i + 1] for i in range(12) if WORLD[i + 1] >= 2 * WORLD[i]]
    assert doubles == ["2016→2017", "2019→2020"]
    return f

BIRTHS = [1.43, 1.58, 1.63, 1.77, 1.95, 1.99, 1.98, 1.85, 1.76, 1.68, 1.55, 1.69, 1.46, 1.59, 1.55, 1.69, 1.90, 1.97, 1.96,
          1.91, 1.77, 1.75, 1.56, 1.79, 1.50, 1.64, 1.64, 1.79, 1.99, 1.96, 1.99, 1.93, 1.86, 1.77, 1.62, 1.60]   # Apr 2017 - Mar 2020

@fig
def births():
    f = Fig("births")
    labels = []
    for i in range(len(BIRTHS)):
        m = (3 + i) % 12; y = 2017 + (3 + i) // 12
        labels.append(f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m]} {str(y)[2:]}" if m in (0, 6) else "")
    line_graph(f, [("births", BIRTHS)], labels, 0.5, 2.0, 0.5, W=520, legend=False, ylab="live births each month in India (millions, approximate)")
    year2019 = BIRTHS[21:33]
    assert len(year2019) == 12 and abs(sum(year2019) - 21.40) < 0.01
    return f

RAIN_DAYS = {"Mangaluru": [0.1, 0, 0.1, 1.8, 6.2, 24.1, 27.7, 24.5, 14, 8.8, 3.9, 0.9],
             "New Delhi": [1.2, 1.5, 1.5, 1.1, 1.5, 4, 10, 10, 4, 1, 0.3, 1],
             "Port Blair": [2.4, 1.3, 0.9, 3.3, 15.5, 18.7, 17.3, 18.8, 16.8, 14.1, 11.3, 5.4],
             "Rameswaram": [2.6, 1.3, 1.9, 3.4, 2.5, 0.4, 1, 1, 1.9, 8.1, 10.4, 7.8]}

@fig
def delhi_rain():
    f = Fig("delhi_rain")
    line_graph(f, [("New Delhi", RAIN_DAYS["New Delhi"])], MONTHS, 0, 30, 5, ylab="average number of rainy days in each month")
    return f

@fig
def rain_days_all():
    f = Fig("rain_days_all")
    line_graph(f, [(k, [round(v) for v in vals]) for k, vals in RAIN_DAYS.items()], MONTHS, 0, 30, 5, ylab="average rainy days per month (rounded)")
    tot = {k: sum(v) for k, v in RAIN_DAYS.items()}
    assert max(tot, key=tot.get) == "Port Blair" and min(tot, key=tot.get) == "New Delhi"
    return f

@fig
def shop():
    f = Fig("shop")
    days = "Mon Tue Wed Thu Fri Sat Sun".split()
    line_graph(f, [("visiting", [16, 19, 10, 14, 20, 22, 35]), ("purchasing", [10, 8, 7, 11, 12, 16, 26])], days, 0, 40, 5,
               ylab="average number of customers")
    return f

SALT = {"Andaman and Nicobar": [16, 12, 12, 12, 13.88, 18.22, 18.73, 20.63, 19.73, 20.99],
        "Assam": [6, 12, 12, 12, 12, 15, 14, 12.02, 13.72, 12.35],
        "Gujarat": [16.5, 14.75, 14.75, 14.75, 13, 14.45, 14.28, 14.54, 14.8, 19.2],
        "Mizoram": [20, 20, 22, 22, 20, 22, 25, 27.65, 29.03, 29.8],
        "Uttar Pradesh": [16.15, 16.97, 16.18, 18.24, 18.96, 20.63, 21.3, 25.39, 26.9, 24.81],
        "West Bengal": [9.47, 11.65, 11.63, 11.43, 11.11, 12.79, 16.14, 18.43, 21.66, 23.99]}
RISE = {k: round(v[-1] - v[0], 2) for k, v in SALT.items()}
assert max(RISE, key=RISE.get) == "West Bengal" and RISE["West Bengal"] == 14.52

@fig
def salt():
    f = Fig("salt")
    yrs = [str(y)[2:] for y in range(2016, 2026)]
    line_graph(f, [(k, [round(x) for x in SALT[k]]) for k in ("Gujarat", "Mizoram", "Uttar Pradesh")], yrs, 0, 35, 5,
               ylab="retail price of 1 kg iodised salt in January (₹, rounded)")
    return f

LIGHT_YEARS = ["1983", "1990", "2000", "2010", "2023"]
RURAL_E = [15, 35, 50, 72, 99]; RURAL_K = [83, 63, 48, 26, 1]
URBAN_E = [64, 80, 91, 96, 99]; URBAN_K = [34, 19, 9, 3, 0.5]

@fig
def lighting():
    f = Fig("lighting")
    line_graph(f, [("electricity", RURAL_E), ("kerosene", RURAL_K)], LIGHT_YEARS, 0, 100, 20, W=200, H=160, legend=False, ylab="rural (% of households)")
    # urban panel, shifted right
    W = 200; H = 160; x0 = 290
    for y in range(0, 101, 20):
        f.seg(P(x0, y * H / 100), P(x0 + W, y * H / 100), color=LIGHT, w=1)
        f.label(P(x0 - 8, y * H / 100 - 5), str(y), anchor="end", size=10, color=HELP)
    for i, lab in enumerate(LIGHT_YEARS): f.label(P(x0 + i * W / 4, -18), lab, size=10, color=HELP)
    for j, vals in enumerate([URBAN_E, URBAN_K]):
        pts = [P(x0 + i * W / 4, v * H / 100) for i, v in enumerate(vals)]
        for p, q in zip(pts, pts[1:]): f.seg(p, q, color=COLS[j], w=2)
        for p in pts: disc(f, p, 3.2, COLS[j])
    f.label(P(x0, H + 16), "urban (% of households)", anchor="start", size=11, color=HELP)
    f.label(P(0, -40), "blue: electricity   red: kerosene   (main source of light at home, approximate)", anchor="start", size=11)
    assert RURAL_K[0] > 50 and URBAN_E[0] > 50 and URBAN_E[2] > 80
    return f

URBAN_H = [(6, 2.6), (8, 2.35), (10, 2.1), (12, 1.75), (14, 1.3), (15, 1.1), (17, 0.7), (20, 0.35), (22, 0.2), (24, 0.15)]
RURAL_H = [(6, 2.85), (8, 2.65), (10, 2.4), (12, 2.0), (14, 1.6), (15, 1.35), (17, 0.85), (20, 0.35), (22, 0.2), (24, 0.17)]

def hobby(age, rural):
    """Hours per day on hobbies and games, read off the published chart (approximate), joined by straight lines."""
    pts = RURAL_H if rural else URBAN_H
    for (a1, h1), (a2, h2) in zip(pts, pts[1:]):
        if a1 <= age <= a2:
            return h1 + (h2 - h1) * (age - a1) / (a2 - a1)
    raise ValueError(age)

@fig
def hobbies():
    f = Fig("hobbies")
    W, H = 360, 180
    sx, sy = W / 18, H / 3
    for h in range(0, 4):
        f.seg(P(0, h * sy), P(W, h * sy), color=LIGHT, w=1)
        f.label(P(-8, h * sy - 5), f"{h} h", anchor="end", size=10, color=HELP)
    for a in (6, 10, 15, 20, 24):
        f.label(P((a - 6) * sx, -18), str(a), size=10, color=HELP)
    for j, rural in enumerate([False, True]):
        pts = [P((a / 4 - 6) * sx, hobby(a / 4, rural) * sy) for a in range(24, 97)]
        for p, q in zip(pts, pts[1:]): f.seg(p, q, color=COLS[j], w=2.2)
    f.label(P(W / 2, -40), "age (years)   blue: urban   red: rural   (approximate)", size=11)
    assert hobby(10, False) == 2.1 and 14 < [a / 10 for a in range(60, 241) if hobby(a / 10, True) <= 1.5][0] < 15
    return f

# ---------------------------------------------------------------- activity strips (our own)
ACTS = [("sleeping", "#90caf9"), ("eating", "#ffcc80"), ("friends, hobbies, family", "#ef5350"),
        ("classes and study", "#fff176"), ("bath, dressing, exercise", "#a5d6a7"), ("travelling", "#9575cd")]
def strip(spec):
    out = []
    for act, n in spec: out += [act] * n
    assert len(out) == 48
    return out
DAYS = {
    "Strip 1": strip([(0, 12), (4, 2), (1, 1), (5, 1), (3, 8), (1, 1), (3, 6), (5, 1), (2, 6), (1, 1), (3, 4), (0, 5)]),
    "Strip 2": strip([(0, 14), (4, 2), (1, 1), (2, 8), (1, 1), (2, 2), (5, 1), (2, 8), (5, 1), (1, 1), (2, 4), (0, 5)]),
    "Strip 3": strip([(0, 16), (4, 1), (1, 1), (2, 4), (3, 4), (1, 1), (2, 6), (4, 2), (2, 6), (1, 1), (3, 2), (0, 4)]),
}

@fig
def strips():
    f = Fig("strips")
    bw, bh = 26, 9
    for j, (name, s) in enumerate(DAYS.items()):
        x0 = j * 60
        for i, a in enumerate(s):
            rect(f, x0, -i * bh, bw, bh, fill=ACTS[a][1], color="#78909c")
        f.label(P(x0 + bw / 2, 16), name, size=11, bold=True)
    for h in range(0, 25, 3):
        f.label(P(-8, -h * 2 * bh - 4), f"{h:02d}:00", anchor="end", size=10, color=HELP)
    for i, (a, c) in enumerate(ACTS):
        rect(f, 200, -i * 22, 14, 14, fill=c, color="#78909c")
    f.label(P(222, 30), "colours (match them!)", anchor="start", size=11, color=HELP)
    return f


if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
