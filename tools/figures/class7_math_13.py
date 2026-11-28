"""Figures for class 7 maths Ch 13, Connecting the Dots (data). Every dot plot and bar graph is
drawn from the data lists below, and the mean / median lines are computed from the same lists and
asserted against the values written in the notes, so a picture can never disagree with the text.
Graphs from published charts (rockets, animal speeds, skyscrapers, electric vehicles) are redrawn
with values read off those charts, rounded."""
import os, sys, math
from statistics import mean, median
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "13")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

BLUE, ORANGE, GREEN, PURPLE, GREY = "#1e88e5", "#fb8c00", "#43a047", "#8e24aa", "#b0bec5"
GRID = "#cfd8dc"

def close(a, b, tol=0.01): return abs(a - b) < tol

def blob(f, c, r, fill):
    f.poly([along(c, 30 * k, r) for k in range(12)], fill=fill, color=fill)

def rect(f, x, y, w, h, fill, color=None):
    f.poly([P(x, y), P(x + w, y), P(x + w, y + h), P(x, y + h)], fill=fill, color=color or fill)

# ---------------------------------------------------------------- dot plots
def axis(f, y0, lo, hi, step, k, label_every=1, fmt=str):
    f.seg(P(0, y0), P((hi - lo) * k, y0), w=1.6)
    n = round((hi - lo) / step)
    for i in range(n + 1):
        v = lo + i * step
        x = (v - lo) * k
        f.seg(P(x, y0 - 4), P(x, y0 + 4), w=1.2)
        if i % label_every == 0:
            f.label(P(x, y0 - 16), fmt(round(v, 2)), size=12)

def dotplot(f, y0, values, lo, hi, step, k, color, title=None, r=5.5, gap=12, label_every=1,
            fmt=str, marks=(), round_to=None):
    """Stack one dot per value above a number line at height y0. marks = [(value, name, dash)]."""
    axis(f, y0, lo, hi, step, k, label_every, fmt)
    counts = {}
    top = 0
    for v in values:
        key = round(v, 6)
        counts[key] = counts.get(key, 0) + 1
        h = counts[key]
        blob(f, P((v - lo) * k, y0 + 4 + h * gap - gap / 2 + r), r, color)
        top = max(top, h)
    ytop = y0 + 10 + top * gap + 6
    for v, name, dash in marks:
        x = (v - lo) * k
        f.seg(P(x, y0 - 2), P(x, ytop), color=INK, w=1.6, dash="6,4" if dash else None)
    if title:
        f.label(P(-10, y0 + 10), title, anchor="end", bold=True, size=13)
    return ytop

def legend_line(f, x, y, text, dash):
    f.seg(P(x, y), P(x + 26, y), color=INK, w=1.6, dash="6,4" if dash else None)
    f.label(P(x + 34, y), text, anchor="start", size=12)

# ---------------------------------------------------------------- bar graphs
def vbars(f, cats, series, colors, names, top, step, k=3.0, bw=12, gap=10, ylabel=None,
          xlabel=None, unit_fmt=str, cat_size=11, rotate_hint=False, base=0):
    """Clustered vertical bars. series = list of lists (one per name). k = px per unit."""
    ns = len(series)
    cw = ns * bw + gap
    W = len(cats) * cw
    for v in range(base, top + 1, step):
        y = (v - base) * k
        f.seg(P(0, y), P(W, y), color=GRID, w=1)
        f.label(P(-6, y), unit_fmt(v), anchor="end", size=11)
    f.seg(P(0, 0), P(W, 0), w=1.6)
    f.seg(P(0, 0), P(0, (top - base) * k), w=1.6)
    for i, c in enumerate(cats):
        x0 = i * cw + gap / 2
        for j, s in enumerate(series):
            v = s[i]
            if v is None: continue
            rect(f, x0 + j * bw, 0, bw - 1, (v - base) * k, colors[j])
        f.label(P(x0 + ns * bw / 2, -14), c, size=cat_size)
    lx = 0
    for j, nm in enumerate(names):
        rect(f, lx, (top - base) * k + 18, 12, 12, colors[j])
        f.label(P(lx + 18, (top - base) * k + 24), nm, anchor="start", size=12)
        lx += 24 + len(nm) * 7.5
    if ylabel:
        f.label(P(0, (top - base) * k + 46), ylabel, anchor="start", size=12, bold=True)
    if xlabel:
        f.label(P(W / 2, -34), xlabel, size=12, bold=True)
    return W

def hbars(f, cats, series, colors, names, top, step, k=1.0, bh=7, gap=8, show_values=None,
          val_fmt=str, name_w=0):
    """Clustered horizontal bars, first category at the top."""
    ns = len(series)
    ch = ns * bh + gap
    H = len(cats) * ch
    for v in range(0, top + 1, step):
        x = v * k
        f.seg(P(x, 0), P(x, H), color=GRID, w=1)
        f.label(P(x, -12), str(v), size=11)
    f.seg(P(0, 0), P(0, H), w=1.6)
    for i, c in enumerate(cats):
        ytop = H - i * ch - gap / 2
        for j, s in enumerate(series):
            v = s[i]
            y = ytop - (j + 1) * bh
            rect(f, 0, y, v * k, bh - 1, colors[j])
            if show_values and show_values[j][i] is not None:
                f.label(P(v * k + 4, y + bh / 2), val_fmt(show_values[j][i]), anchor="start", size=11)
        f.label(P(-8, ytop - ns * bh / 2), c, anchor="end", size=12)
    if names:
        lx = 0
        for j, nm in enumerate(names):
            rect(f, lx, H + 12, 12, 12, colors[j])
            f.label(P(lx + 18, H + 18), nm, anchor="start", size=12)
            lx += 26 + len(nm) * 7.5
    return H

# ================================================================ data (same as in the notes)
SHREYAS, PARAG = [3, 8, 10, 5, 4], [5, 4, 6, 3, 4, 8]
YAHA = [25, 24, 26, 28, 30, 35, 39, 43, 49, 56, 59, 44]
WAHA = [19, 17, 23, 30, 38, 35, 42, 39, 53, 60, 52, 42]
YAANGBA = [169, 173, 155, 165, 160, 164]
POOVIZHI = [170, 173, 165, 118, 175]
STORIES = [6, 8, 5, 15, 3, 0, 2, 7, 12, 40, 10, 5, 0, 1, 8]
NEWS = [16, 18, 20, 22, 26, 16, 10]
BOYS = [147, 135, 130, 154, 128, 135, 134, 158, 155, 146, 146, 142, 140, 141, 144, 145, 150]
GIRLS = [143, 136, 150, 144, 154, 140, 145, 148, 156, 150, 150]
PALMS = [50, 45, 43, 52, 61, 63, 46, 55, 60, 55, 59, 56, 56, 49, 54, 65, 66, 51, 44, 58, 60, 54, 52,
         57, 61, 62, 60, 60, 67]
NB_BOYS, NB_GIRLS = [3.5, 4.1, 2.6, 3.2, 3.4, 3.8], [4.0, 3.1, 3.4, 3.7, 2.5, 3.4]
PETS = [0, 1, 0, 4, 8, 0, 0, 2, 1, 1, 5, 3, 4, 0, 0, 10, 25, 2, 2, 4]
POCKETS_B = [3] + [4] * 4 + [5] * 5 + [6] * 2
POCKETS_G = [0, 2] + [3] * 4 + [4] * 5 + [5, 6]
SUDOKU = [410, 400, 370, 340, 360, 400, 320, 330, 310, 320, 290, 380, 280, 270, 230, 220, 240]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ================================================================ figures
@fig
def fair_share():
    """Guavas: uneven piles levelled to the mean."""
    f = Fig("fair_share"); s = 16
    def piles(x0, vals, color):
        for i, v in enumerate(vals):
            for h in range(v):
                rect(f, x0 + i * (s + 6), h * s, s, s - 2, color, color=INK)
        return x0 + len(vals) * (s + 6)
    m = mean(SHREYAS); assert m == 6 and sum(SHREYAS) == 30
    xe = piles(0, SHREYAS, "#c5e1a5")
    for i, v in enumerate(SHREYAS):
        f.label(P(i * (s + 6) + s / 2, -12), str(v), size=12, bold=True)
    f.label(P(xe / 2, -32), "3 + 8 + 10 + 5 + 4 = 30", size=12)
    f.seg(P(xe + 12, 5 * s), P(xe + 52, 5 * s), color=ANS, w=2.5)
    f.seg(P(xe + 44, 5 * s + 6), P(xe + 52, 5 * s), color=ANS, w=2.5)
    f.seg(P(xe + 44, 5 * s - 6), P(xe + 52, 5 * s), color=ANS, w=2.5)
    f.label(P(xe + 32, 5 * s + 16), "share", size=12, color=ANS, bold=True)
    x2 = xe + 64
    xe2 = piles(x2, [int(m)] * 5, "#a5d6a7")
    for i in range(5):
        f.label(P(x2 + i * (s + 6) + s / 2, -12), "6", size=12, bold=True, color=ANS)
    f.label(P((x2 + xe2) / 2, -32), "30 ÷ 5 = 6 each", size=12, color=ANS, bold=True)
    f.seg(P(-4, m * s), P(xe2 + 4, m * s), color=ASK, w=1.6, dash="6,4")
    f.label(P(xe2 + 8, m * s), "mean = 6", anchor="start", size=12, color=ASK, bold=True)
    return f

@fig
def onion_dotplot():
    f = Fig("onion_dotplot"); k = 9
    dotplot(f, 0, WAHA, 10, 60, 5, k, PURPLE, "Wahapur")
    dotplot(f, 70, YAHA, 10, 60, 5, k, GREEN, "Yahapur")
    f.label(P(25 * k, -36), "price of onions (₹ per kg)", size=12, bold=True)
    assert sum(YAHA) == 458 and sum(WAHA) == 450
    return f

@fig
def family_heights():
    f = Fig("family_heights"); k = 5
    my, dy = mean(YAANGBA), median(YAANGBA)
    mp, dp = mean(POOVIZHI), median(POOVIZHI)
    assert close(my, 164.33) and dy == 164.5 and close(mp, 160.2) and dp == 170
    dotplot(f, 0, POOVIZHI, 115, 175, 10, k, ORANGE, "Poovizhi", marks=[(mp, "", False), (dp, "", True)])
    dotplot(f, 70, YAANGBA, 115, 175, 10, k, BLUE, "Yaangba", marks=[(my, "", False), (dy, "", True)])
    legend_line(f, 0, 140, "mean (solid)", False); legend_line(f, 150, 140, "median (dashed)", True)
    f.label(P(60 * k / 2, -36), "height (cm)", size=12, bold=True)
    f.label(P(0, 36), "118: far from the rest", anchor="start", size=11, color=ASK, bold=True)
    return f

@fig
def stories_dotplot():
    f = Fig("stories_dotplot"); k = 11
    m, d = mean(STORIES), median(STORIES)
    assert sum(STORIES) == 122 and len(STORIES) == 15 and close(m, 8.13) and d == 6
    dotplot(f, 0, STORIES, 0, 40, 5, k, BLUE, marks=[(m, "", False), (d, "", True)])
    legend_line(f, 0, 70, "mean ≈ 8.1", False); legend_line(f, 130, 70, "median = 6", True)
    f.label(P(40 * k, 38), "40: outlier", anchor="end", size=11, color=ASK, bold=True)
    f.label(P(20 * k, -36), "number of stories read", size=12, bold=True)
    return f

@fig
def news_dotplot():
    f = Fig("news_dotplot"); k = 14
    m, d = mean(NEWS), median(NEWS)
    assert sum(NEWS) == 128 and close(m, 18.29) and d == 18
    dotplot(f, 0, NEWS, 0, 30, 5, k, BLUE, marks=[(m, "", False), (d, "", True)])
    legend_line(f, 0, 60, "mean ≈ 18.3", False); legend_line(f, 130, 60, "median = 18", True)
    f.label(P(15 * k, -36), "pages", size=12, bold=True)
    return f

@fig
def class_heights():
    f = Fig("class_heights"); k = 9
    mb, db = mean(BOYS), median(BOYS); mg, dg = mean(GIRLS), median(GIRLS)
    mc, dc = mean(BOYS + GIRLS), median(BOYS + GIRLS)
    assert close(mb, 142.94) and db == 144 and close(mg, 146.91) and dg == 148
    assert mc == 144.5 and dc == 145
    dotplot(f, 0, GIRLS, 125, 160, 5, k, ORANGE, "Girls", marks=[(mg, "", False), (dg, "", True)])
    dotplot(f, 70, BOYS, 125, 160, 5, k, BLUE, "Boys", marks=[(mb, "", False), (db, "", True)])
    dotplot(f, 140, BOYS + GIRLS, 125, 160, 5, k, GREEN, "Whole class", marks=[(mc, "", False), (dc, "", True)])
    legend_line(f, 0, 225, "mean (solid)", False); legend_line(f, 150, 225, "median (dashed)", True)
    f.label(P(35 * k / 2, -36), "height (cm)", size=12, bold=True)
    return f

@fig
def palm_dotplot():
    f = Fig("palm_dotplot"); k = 12
    m, d = mean(PALMS), median(PALMS)
    assert len(PALMS) == 29 and sum(PALMS) == 1621 and close(m, 55.90) and d == 56
    assert sum(p < m for p in PALMS) == 13
    dotplot(f, 0, PALMS, 40, 70, 5, k, GREEN, marks=[(m, "", False), (d, "", True)], r=5, gap=11)
    legend_line(f, 0, 70, "mean ≈ 55.9", False); legend_line(f, 130, 70, "median = 56", True)
    f.label(P(15 * k, -36), "height of tree (feet)", size=12, bold=True)
    return f

@fig
def newborn_dotplot():
    f = Fig("newborn_dotplot"); k = 120
    mb, db, mg, dg = mean(NB_BOYS), median(NB_BOYS), mean(NB_GIRLS), median(NB_GIRLS)
    assert close(mb, 3.43) and close(db, 3.45) and close(mg, 3.35) and close(dg, 3.4)
    fmt = lambda v: f"{v:.1f}"
    dotplot(f, 0, NB_GIRLS, 2.4, 4.2, 0.2, k, ORANGE, "Girls", marks=[(mg, "", False), (dg, "", True)], fmt=fmt)
    dotplot(f, 60, NB_BOYS, 2.4, 4.2, 0.2, k, BLUE, "Boys", marks=[(mb, "", False), (db, "", True)], fmt=fmt)
    legend_line(f, 0, 115, "mean (solid)", False); legend_line(f, 150, 115, "median (dashed)", True)
    f.label(P(0.9 * k, -36), "weight at birth (kg)", size=12, bold=True)
    return f

@fig
def pets_dotplot():
    f = Fig("pets_dotplot"); k = 16
    m, d = mean(PETS), median(PETS)
    assert len(PETS) == 20 and sum(PETS) == 72 and m == 3.6 and d == 2
    dotplot(f, 0, PETS, 0, 25, 1, k, BLUE, marks=[(m, "", False), (d, "", True)], label_every=5)
    legend_line(f, 0, 100, "mean = 3.6", False); legend_line(f, 130, 100, "median = 2", True)
    f.label(P(12.5 * k, -36), "animals at home", size=12, bold=True)
    return f

@fig
def pockets_dotplot():
    f = Fig("pockets_dotplot"); k = 26
    assert len(POCKETS_B) == 12 and len(POCKETS_G) == 13
    dotplot(f, 0, POCKETS_G, 0, 7, 1, k, "#00897b", "Girls")
    dotplot(f, 90, POCKETS_B, 0, 7, 1, k, ORANGE, "Boys")
    f.label(P(3.5 * k, -36), "number of pockets", size=12, bold=True)
    return f

@fig
def sudoku_dotplot():
    f = Fig("sudoku_dotplot"); k = 1.6
    w1, w2 = SUDOKU[:9], SUDOKU[9:]
    assert mean(w1) == 360 and median(w1) == 360 and mean(w2) == 278.75 and median(w2) == 275
    dotplot(f, 0, w2, 200, 420, 20, k, ORANGE, "Week 2", marks=[(mean(w2), "", False), (median(w2), "", True)])
    dotplot(f, 70, w1, 200, 420, 20, k, BLUE, "Week 1", marks=[(mean(w1), "", False), (median(w1), "", True)])
    legend_line(f, 0, 130, "mean (solid)", False); legend_line(f, 150, 130, "median (dashed)", True)
    f.label(P(110 * k, -36), "time to solve (seconds)", size=12, bold=True)
    return f

@fig
def onion_bars():
    f = Fig("onion_bars")
    vbars(f, MONTHS, [YAHA, WAHA], [GREEN, PURPLE], ["Yahapur", "Wahapur"], 60, 10, k=3.2,
          bw=13, gap=12, ylabel="price (₹ per kg)")
    return f

ROCKET_ORGS = ["SpaceX", "CASC", "Roscosmos", "Arianespace", "Rocket Lab", "United Launch Alliance",
               "ISRO", "Galactic Energy", "Expace", "Others"]
ROCKETS = {2021: [31, 48, 16, 15, 6, 5, 2, 1, 4, 18], 2022: [61, 35, 21, 6, 6, 8, 5, 2, 4, 17],
           2023: [96, 45, 18, 3, 9, 3, 7, 7, 6, 26]}

@fig
def rockets():
    f = Fig("rockets")
    assert sum(ROCKETS[2023]) == 220 and ROCKETS[2022][0] - ROCKETS[2021][0] == 30
    hbars(f, ROCKET_ORGS, [ROCKETS[2021], ROCKETS[2022], ROCKETS[2023]], ["#1a237e", "#64b5f6", "#90a4ae"],
          ["2021", "2022", "2023"], 100, 20, k=3.2, bh=7, gap=9)
    f.label(P(160, -32), "number of rocket launches (approximate)", size=12, bold=True)
    return f

C1 = [210, 257, 372, 441, 536, 564, 555, 465, 394, 310, 222, 186]
C2 = [459, 384, 381, 327, 304, 276, 295, 318, 369, 409, 435, 468]
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

@fig
def daylight():
    f = Fig("daylight")
    a = [h / d for h, d in zip(C1, DAYS)]; b = [h / d for h, d in zip(C2, DAYS)]
    assert max(a) == a[5] and min(b) == b[5] and close(a[5], 18.8) and close(a[11], 6.0)
    vbars(f, MONTHS, [a, b], [BLUE, ORANGE], ["City 1", "City 2"], 20, 5, k=8, bw=13, gap=12,
          ylabel="average hours of daylight per day")
    return f

# Our own T20 match (not from any real game). Blue bats first for all 20 overs; Red chases.
RUNS_BLUE = [4, 9, 6, 8, 12, 3, 7, 5, 10, 6, 8, 14, 5, 9, 7, 11, 6, 12, 15, 9]
WK_BLUE = [3, 6, 10, 14, 17, 19]
RUNS_RED = [8, 11, 2, 7, 9, 10, 4, 6, 13, 8, 5, 9, 12, 7, 12, 16, 15, 14]
WK_RED = [3, 7, 11, 15]

@fig
def runs_per_over():
    f = Fig("runs_per_over")
    target = sum(RUNS_BLUE) + 1
    assert sum(RUNS_BLUE) == 166 and target == 167
    assert sum(RUNS_RED[:17]) < target <= sum(RUNS_RED) and len(RUNS_RED) == 18
    assert min(RUNS_RED) == 2 and RUNS_RED.index(2) == 2 and RUNS_BLUE[11] == 14
    red = RUNS_RED + [None, None]
    cats = [str(i) for i in range(1, 21)]
    k, bw, gap = 9, 9, 7
    vbars(f, cats, [RUNS_BLUE, red], [BLUE, "#e53935"], ["Blue team", "Red team"], 20, 5, k=k, bw=bw,
          gap=gap, ylabel="runs in the over", xlabel="over", cat_size=10)
    cw = 2 * bw + gap
    for team, runs, wk in ((0, RUNS_BLUE, WK_BLUE), (1, RUNS_RED, WK_RED)):
        for o in wk:
            x = (o - 1) * cw + gap / 2 + team * bw + bw / 2 - 0.5
            f.circle(P(x, runs[o - 1] * k + 7), 3.5, color=INK, w=1.6)
    return f

@fig
def animal_speeds():
    f = Fig("animal_speeds")
    names = ["peregrine falcon", "spine-tailed swift", "free-tailed bat", "green darner dragonfly",
             "flying fish", "cheetah", "pronghorn antelope", "ostrich", "human", "Australian tiger beetle",
             "sailfish", "dolphin", "California sea lion", "Gentoo penguin", "humpback whale"]
    sp = [322, 170, 96, 64, 56, 103, 88, 64, 37, 8, 109, 40, 40, 35, 26]
    col = ["#64b5f6"] * 5 + ["#d84315"] * 5 + ["#1565c0"] * 5
    k, bh, gap = 1.25, 12, 5
    H = len(names) * (bh + gap)
    for v in range(0, 336, 16):
        f.seg(P(v * k, 0), P(v * k, H), color=GRID, w=1)
        if v % 48 == 0: f.label(P(v * k, -12), str(v), size=11)
    f.seg(P(0, 0), P(0, H), w=1.6)
    for i, (n, s, c) in enumerate(zip(names, sp, col)):
        y = H - (i + 1) * (bh + gap) + gap / 2
        rect(f, 0, y, s * k, bh, c)
        f.label(P(s * k + 4, y + bh / 2), f"{s} km/h", anchor="start", size=11)
        f.label(P(-8, y + bh / 2), n, anchor="end", size=12)
    for j, (nm, c) in enumerate((("in air", "#64b5f6"), ("on land", "#d84315"), ("in water", "#1565c0"))):
        rect(f, j * 110, H + 12, 12, 12, c); f.label(P(j * 110 + 18, H + 18), nm, anchor="start", size=12)
    f.label(P(160, -32), "top speed (km per hour); one grid step = 16 km/h", size=12, bold=True)
    return f

SKY = [("Hong Kong", 553), ("Shenzhen", 367), ("New York", None), ("Dubai", 251), ("Guangzhou", 188),
       ("Shanghai", 183), ("Tokyo", None), ("Kuala Lumpur", 154), ("Chongqing", 144), ("Jakarta", 112),
       ("Bangkok", 110), ("Singapore", 95), ("Mumbai", 86), ("Seoul", 82), ("Toronto", 81),
       ("Melbourne", 69), ("Miami", 58), ("Istanbul", 48), ("Moscow", 46), ("London", None)]
SKY_HIDDEN = {"New York": 315, "Tokyo": 165, "London": 30}

@fig
def skyscrapers():
    f = Fig("skyscrapers")
    vals = [v if v is not None else SKY_HIDDEN[n] for n, v in SKY]
    assert vals == sorted(vals, reverse=True)
    mi = [n for n, _ in SKY].index("Mumbai")
    assert mi == 12 and len(SKY) - mi - 1 == 7
    hbars(f, [n for n, _ in SKY], [vals], ["#c9a227"], None, 600, 100, k=0.55, bh=11, gap=4,
          show_values=[[v for _, v in SKY]])
    f.label(P(160, -32), "number of buildings taller than 150 m", size=12, bold=True)
    return f

def two_bar_answer(name, cats, a, b, na, nb, top, step, k, ylabel, colors=(BLUE, ORANGE), **kw):
    f = Fig(name)
    vbars(f, cats, [a, b], list(colors), [na, nb], top, step, k=k, ylabel=ylabel, **kw)
    return f

G5 = "w a a a w n s a n w a a a a a w w s a a n w a a n".split()
G9 = "n w s a s w s s a a w s s a s a n w s s a w a w a".split()

@fig
def superpower():
    cats = ["water", "air", "space", "none"]
    a = [G5.count(c) for c in "wasn"]; b = [G9.count(c) for c in "wasn"]
    assert a == [6, 13, 2, 4] and b == [6, 8, 9, 2] and sum(a) == sum(b) == 25
    return two_bar_answer("superpower", cats, a, b, "Grade 5", "Grade 9", 14, 2, k=12,
                          ylabel="number of students", bw=24, gap=26, cat_size=12)

@fig
def jodhpur():
    cats = ["12 am", "3 am", "6 am", "9 am", "12 pm", "3 pm", "6 pm", "9 pm"]
    d1 = [20, 18, 16, 20, 26, 34, 30, 24]; d2 = [37, 34, 30, 33, 37, 43, 42, 39]
    return two_bar_answer("jodhpur", cats, d1, d2, "Day 1", "Day 2", 44, 4, k=4.5,
                          ylabel="temperature (°C); 1 unit = 4 °C", bw=16, gap=16, cat_size=11)

EV_STATES = ["Uttarakhand", "West Bengal", "Andhra Pr.", "Odisha", "Assam", "Gujarat", "Delhi"]
EV = {2022: [15, 10, 29, 27, 40, 69, 62], 2023: [16, 21, 34, 44, 60, 89, 74], 2024: [19, 43, 55, 62, 64, 78, 81]}

def ev(name, n):
    f = Fig(name)
    s = [[v if i < n else None for i, v in enumerate(EV[y])] for y in (2022, 2023, 2024)]
    vbars(f, EV_STATES, s, [BLUE, "#e53935", "#fbc02d"], ["2022", "2023", "2024"], 100, 25, k=1.9,
          bw=14, gap=20, ylabel="registrations (thousands)", cat_size=11)
    return f

@fig
def ev_question(): return ev("ev_question", 5)

@fig
def ev_answer():
    assert EV[2023][4] - EV[2022][4] == 20 and round(EV[2024][1] / EV[2022][1], 1) == 4.3
    return ev("ev_answer", 7)

@fig
def sports():
    cats = ["Cricket", "Basketball", "Swimming", "Hockey", "Athletics"]
    watch = [1240, 470, 510, 430, 250]; play = [620, 320, 320, 250, 105]
    assert all(2 * p <= w * 1.4 for p, w in zip(play, watch))
    f = Fig("sports")
    vbars(f, cats, [[w / 100 for w in watch], [p / 100 for p in play]], [BLUE, GREEN],
          ["Watching", "Participating"], 14, 2, k=12, bw=22, gap=26, cat_size=12,
          ylabel="number of people; 1 unit = 200 people", unit_fmt=lambda v: str(v * 100))
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
