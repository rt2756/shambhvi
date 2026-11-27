import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from geo import *

OUT = os.environ.get("FIG_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "class7", "math", "5")
os.makedirs(OUT, exist_ok=True)
FIGS = []
def fig(fn):
    FIGS.append(fn); return fn

def pair(f, alpha, gap=90, L=130, marks=1, labels=None, through=(0, 0)):
    """Two parallel lines at direction alpha, `gap` apart vertically; returns a point on each."""
    top, bot = add(through, (0, gap)), through
    for p, lab in zip((top, bot), labels or (None, None)):
        f.line(p, alpha, -L, L)
        if marks: f.arrows(along(p, alpha, L - 30), alpha, marks)
        if lab: f.text(along(p, alpha, L + 12), lab, anchor="start")
    return top, bot

def cross(f, top, bot, alpha, T, u, ext=45, label=None):
    """Transversal through point T on the top line at direction u; returns (T, B)."""
    B = meet(T, u, bot, alpha)
    f.seg(along(T, u, ext), along(B, u + 180, ext))
    if label: f.text(along(B, u + 180, ext + 12), label)
    return T, B

# ---------------------------------------------------------------- teaching figures
@fig
def crossing():
    f = Fig("crossing"); O = P(0, 0)
    f.line(O, 0, -120, 120); f.text(P(132, 0), "l", anchor="start")
    f.line(O, 60, -95, 95); f.text(along(O, 60, 108), "m")
    f.angle(O, 60, 180, "a", 120, r=20); f.angle(O, 0, 60, "b", 60, r=26)
    f.angle(O, 240, 360, "c", 120, r=20); f.angle(O, 180, 240, "d", 60, r=26)
    return f

@fig
def crossing_120():
    f = Fig("crossing_120"); O = P(0, 0)
    f.line(O, 0, -120, 120); f.text(P(132, 0), "l", anchor="start")
    f.line(O, 60, -95, 95); f.text(along(O, 60, 108), "m")
    f.angle(O, 60, 180, "a = 120°", 120, r=20, lr=48); f.angle(O, 0, 60, "b", 60, r=26, color=ASK)
    f.angle(O, 240, 360, "c", 120, r=20, color=ASK); f.angle(O, 180, 240, "d", 60, r=26, color=ASK)
    return f

@fig
def crossing_check():
    f = Fig("crossing_check"); O = P(0, 0)
    f.line(O, 20, -110, 110); f.text(along(O, 20, 122), "l")
    f.line(O, 105, -95, 95); f.text(along(O, 105, 108), "m")
    f.angle(O, 20, 105, "p", 85, r=24); f.angle(O, 105, 200, "q", 95, r=20)
    f.angle(O, 200, 285, "r", 85, r=24); f.angle(O, 285, 380, "s", 95, r=20)
    return f

@fig
def perpendicular():
    f = Fig("perpendicular"); O = P(0, 0)
    f.line(O, 0, -110, 110); f.text(P(122, 0), "l", anchor="start")
    f.line(O, 90, -80, 80); f.text(P(0, 94), "m")
    for a in (0, 90, 180, 270): f.right(O, a)
    f.text(P(30, 26), "90°", color=GIVEN, size=13)
    return f

@fig
def segments():
    f = Fig("segments")
    # FG and FH meet at the endpoint F
    F = P(0, 0); G = along(F, 200, 90); H = along(F, 85, 80)
    f.seg(F, G); f.seg(F, H); [f.dot(p) for p in (F, G, H)]
    f.text(add(F, (12, -8)), "F"); f.text(add(G, (-10, -6)), "G"); f.text(add(H, (0, 13)), "H")
    f.angle(F, 85, 200, "115°", 115, r=18, lr=34)
    # AB and CD cross at X, the midpoint of both
    X = P(190, 10); A, B = along(X, 150, 60), along(X, 330, 60); C, D = along(X, 40, 55), along(X, 220, 55)
    f.seg(A, B); f.seg(C, D); [f.dot(p) for p in (A, B, C, D, X)]
    for p, s, o in ((A, "A", (-8, 10)), (B, "B", (8, -10)), (C, "C", (8, 10)), (D, "D", (-8, -10)), (X, "X", (0, -16))):
        f.text(add(p, o), s)
    f.angle(X, 40, 150, "110°", 110, r=16, lr=32)
    # IJ meets KL at its midpoint I (a T-junction)
    K, L = P(300, -40), P(420, -40); I = P(360, -40); J = P(360, 50)
    f.seg(K, L); f.seg(I, J); [f.dot(p) for p in (K, L, I, J)]
    f.right(I, 0)
    f.text(add(K, (0, -15)), "K"); f.text(add(L, (0, -15)), "L"); f.text(add(I, (0, -15)), "I"); f.text(add(J, (0, 13)), "J")
    return f

@fig
def which_parallel():
    f = Fig("which_parallel")
    segs = {"a": (P(0, 120), 25, 80), "b": (P(110, 165), -50, 70), "c": (P(240, 160), 100, 70),
            "d": (P(20, 40), 5, 70), "e": (P(130, 60), 25, 90), "f": (P(260, 40), 60, 70),
            "g": (P(60, -40), -50, 80), "h": (P(200, -50), 100, 70)}
    for lab, (p, a, L) in segs.items():
        q = along(p, a, L); f.seg(p, q); f.text(add(along(p, a, L / 2), mul(unit(a + 90), 13)), lab, bold=True)
    return f

@fig
def notation():
    f = Fig("notation")
    for y in (60, 30):
        f.line(P(0, y), 0, 0, 130); f.arrows(P(80, y), 0, 1)
    for x in (190, 225):
        f.line(P(x, 70), -60, 0, 110); f.arrows(along(P(x, 70), -60, 70), -60, 2)
    V = P(40, -80); f.seg(V, P(40, -10)); f.seg(V, P(150, -80)); f.right(V, 0, s=13)
    f.text(P(70, -58), "90°", color=GIVEN, size=13)
    return f

@fig
def folds():
    f = Fig("folds"); S = 110
    for k, n in enumerate((1, 2, 3)):
        x = k * (S + 40)
        f.seg(P(x, 0), P(x + S, 0)); f.seg(P(x + S, 0), P(x + S, S)); f.seg(P(x + S, S), P(x, S)); f.seg(P(x, S), P(x, 0))
        strips = 2 ** n
        for i in range(1, strips):
            y = S * i / strips; f.seg(P(x, y), P(x + S, y), color=HELP, w=1.6, dash="5,4")
        f.text(P(x + S / 2, -18), f"{n} fold{'s' if n > 1 else ''}: {strips + 1} lines", size=13)
    return f

@fig
def corner_folds():
    f = Fig("corner_folds"); S = 160
    f.seg(P(0, 0), P(S, 0)); f.seg(P(S, 0), P(S, S)); f.seg(P(S, S), P(0, S)); f.seg(P(0, S), P(0, 0))
    for x in (S / 4, S / 2, 3 * S / 4): f.seg(P(x, 0), P(x, S), color=HELP, w=1.6, dash="5,4")
    f.poly([P(3 * S / 4, S - S / 4), P(3 * S / 4, S), P(S, S)], fill="#ffe0b2")
    f.poly([P(0, 0), P(S / 4, 0), P(S / 4, S / 4)], fill="#ffe0b2")
    f.text(P(7 * S / 8, S + 12), "a", bold=True); f.text(P(3 * S / 4 - 10, 7 * S / 8), "b", bold=True); f.text(P(7 * S / 8 + 8, 7 * S / 8 - 12), "c", bold=True)
    f.text(P(S / 8, -14), "p", bold=True); f.text(P(S / 4 + 10, S / 8), "q", bold=True); f.text(P(S / 8 - 8, S / 8 + 12), "r", bold=True)
    return f

def dotgrid(f, nx, ny, s=30):
    for i in range(nx):
        for j in range(ny): f.dot(P(i * s, j * s), color="#5c6bc0")

def dseg(f, a, b, lab=None, s=30, color=INK, w=3):
    p, q = P(a[0] * s, a[1] * s), P(b[0] * s, b[1] * s); f.seg(p, q, color=color, w=w)
    if lab:
        a_ = dirto(p, q); f.text(add(along(p, a_, dist(p, q) / 2), mul(unit(a_ + 90), 13)), lab, bold=True, color=color)

DP1 = [((0, 3), (2, 3), "a"), ((0, 0), (2, 2), "b"), ((4, 0), (4, 2), "c"), ((5, 3), (7, 0), "d")]
@fig
def dots_perp_q():
    f = Fig("dots_perp_q"); dotgrid(f, 8, 4)
    for a, b, l in DP1: dseg(f, a, b, l)
    return f

@fig
def dots_perp_a():
    f = Fig("dots_perp_a"); dotgrid(f, 8, 4)
    for a, b, l in DP1: dseg(f, a, b, l)
    dseg(f, (1, 3), (1, 2), color=ANS); dseg(f, (0, 2), (2, 0), color=ANS)
    dseg(f, (3, 1), (5, 1), color=ANS); dseg(f, (5, 3), (2, 1), color=ANS)
    f.right(P(30, 90), 270, s=8, color=ANS); f.right(P(30, 30), 45, s=8, color=ANS)
    f.right(P(120, 30), 0, s=8, color=ANS); f.right(P(150, 90), dirto(P(5, 3), P(2, 1)), s=8, color=ANS)
    return f

SHAPES = [[(1, 1), (5, 1), (7, 4), (3, 4)],          # parallelogram
          [(9, 0), (12, 0), (12, 5), (9, 2)],         # right trapezium
          [(1, 6), (1, 9), (4, 9), (4, 8), (2, 8), (2, 6)]]  # L-shape
@fig
def grid_shapes_q():
    f = Fig("grid_shapes_q"); s = 24
    for i in range(14): f.seg(P(i * s, -s), P(i * s, 10 * s), color="#cfd8dc", w=1)
    for j in range(-1, 11): f.seg(P(0, j * s), P(13 * s, j * s), color="#cfd8dc", w=1)
    for sh in SHAPES: f.poly([P(x * s, y * s) for x, y in sh], fill="#ffccbc", color="#c62828")
    return f

@fig
def grid_shapes_a():
    f = grid_shapes_q(); f.name = "grid_shapes_a"; s = 24
    f.arrows(P(3 * s, s), 0, 1, ANS); f.arrows(P(5 * s, 4 * s), 0, 1, ANS)
    f.arrows(along(P(5 * s, s), dirto(P(5, 1), P(7, 4)), 1.8 * s), dirto(P(5, 1), P(7, 4)), 2, ANS)
    f.arrows(along(P(s, s), dirto(P(1, 1), P(3, 4)), 1.8 * s), dirto(P(1, 1), P(3, 4)), 2, ANS)
    f.arrows(P(9 * s, 0.8 * s), 90, 1, ANS); f.arrows(P(12 * s, 2.2 * s), 90, 1, ANS)
    f.right(P(12 * s, 0), 90, s=9, color=ANS); f.right(P(9 * s, 0), 0, s=9, color=ANS)
    for c, a in (((1, 6), 0), ((1, 9), 270), ((4, 9), 180), ((4, 8), 90), ((2, 8), 270), ((2, 6), 90)):
        f.right(P(c[0] * s, c[1] * s), a, s=8, color=ANS)
    return f

DP4 = [((0, 11), (1, 10), "a"), ((3, 11), (5, 9), "b"), ((6, 8), (9, 11), "c"), ((7, 7), (11, 11), "d"),
       ((1, 9), (2, 6), "e"), ((3, 9), (4, 4), "f"), ((6, 4), (11, 6), "g"), ((1, 3), (11, 0), "h")]
@fig
def dots_par_q():
    f = Fig("dots_par_q"); dotgrid(f, 12, 12, 22)
    for a, b, l in DP4: dseg(f, a, b, l, s=22)
    return f

@fig
def dots_par_a():
    f = Fig("dots_par_a"); dotgrid(f, 12, 12, 22)
    for a, b, l in DP4:
        dseg(f, a, b, l, s=22)
    for (a, b, l), sh in zip(DP4, [(1, 0), (1, 0), (0, -1), (1, 0), (1, 0), (1, 0), (0, -1), (-1, 1)]):
        dseg(f, (a[0] + sh[0], a[1] + sh[1]), (b[0] + sh[0], b[1] + sh[1]), s=22, color=ANS)
    return f

@fig
def dots_which():
    f = Fig("dots_which"); dotgrid(f, 8, 5)
    dseg(f, (0, 2), (4, 0), "a"); dseg(f, (1, 4), (7, 1), "c"); dseg(f, (1, 4), (4, 0), "b")
    return f

@fig
def transversal_8():
    f = Fig("transversal_8")
    T, B = P(0, 90), P(0, 0)
    f.line(T, 0, -130, 130); f.text(P(142, 90), "l", anchor="start")
    f.line(B, -8, -130, 130); f.text(along(B, -8, 142), "m", anchor="start")
    u = 70; Bx = meet(T, u, B, -8)
    f.seg(along(T, u, 50), along(Bx, u + 180, 50)); f.text(along(Bx, u + 180, 62), "t")
    for V, a, nums in ((T, 0, "1234"), (Bx, -8, "5678")):
        f.text(along(V, (u + a + 180) / 2, 22), nums[0]); f.text(along(V, (a + u) / 2, 24), nums[1])
        f.text(along(V, (u + 180 + a + 360) / 2, 24), nums[2])
        f.text(along(V, (a + 180 + u + 180) / 2, 22), nums[3])
    return f

@fig
def make_parallel():
    f = Fig("make_parallel")
    u = 60
    X = P(0, 90); Y = along(X, u + 180, 100)
    f.line(X, 0, -120, 120); f.text(P(132, 90), "l", anchor="start")
    f.line(Y, 0, -120, 120, color=ANS); f.text(add(Y, (132, 0)), "m", anchor="start", color=ANS)
    f.seg(along(X, u, 45), along(Y, u + 180, 45)); f.text(along(Y, u + 180, 58), "t")
    f.dot(X); f.dot(Y); f.text(add(X, (-12, 12)), "X"); f.text(add(Y, (-12, 12)), "Y")
    f.angle(X, 0, u, "60°", 60, r=20, lr=36)
    f.angle(Y, 0, u, "60°", 60, r=20, lr=36, color=ANS)
    return f

@fig
def corresponding_par():
    f = Fig("corresponding_par"); top, bot = pair(f, 0, labels=("l", "m"))
    T, B = cross(f, top, bot, 0, top, 62, label="t")
    f.angle(T, 0, 62, "a", 62, r=22); f.angle(B, 0, 62, "b", 62, r=22)
    return f

@fig
def not_parallel():
    f = Fig("not_parallel")
    f.line(P(0, 90), 0, -130, 130); f.text(P(142, 90), "l", anchor="start")
    f.line(P(0, 0), 14, -130, 130); f.text(along(P(0, 0), 14, 142), "m", anchor="start")
    return f

@fig
def parallel_through_A():
    f = Fig("parallel_through_A"); A = P(40, 80)
    f.line(P(0, 0), 0, -110, 150); f.text(P(162, 0), "l", anchor="start")
    f.dot(A); f.text(add(A, (8, 14)), "A")
    return f

@fig
def parallel_through_A_ans():
    f = Fig("parallel_through_A_ans"); A = P(40, 80); F = P(40, 0)
    f.line(P(0, 0), 0, -110, 150); f.text(P(162, 0), "l", anchor="start")
    f.seg(P(40, -30), P(40, 115), color=HELP, dash="6,4"); f.text(P(40, 128), "t", color=HELP)
    f.line(A, 0, -110, 150, color=ANS); f.text(P(162, 80), "m", anchor="start", color=ANS)
    f.right(F, 0); f.right(A, 0, color=ANS); f.dot(A); f.text(add(A, (-12, 13)), "A")
    return f

@fig
def alternate():
    f = Fig("alternate"); top, bot = pair(f, 0, labels=("l", "m"))
    u = 65; T, B = cross(f, top, bot, 0, top, u, label="t")
    for V, labs in ((T, "abdc"), (B, "efhg")):
        f.text(along(V, (u + 180) / 2, 22), labs[0]); f.text(along(V, u / 2, 24), labs[1])
        f.text(along(V, (180 + u + 180) / 2, 22), labs[2]); f.text(along(V, (u + 180 + 360) / 2, 24), labs[3])
    return f

@fig
def ex1():
    f = Fig("ex1"); top, bot = pair(f, 0, labels=("l", "m"))
    u = 135; T, B = cross(f, top, bot, 0, P(-20, 90), u, label="t")
    for V, nums in ((T, "1234"), (B, "5678")):
        f.text(along(V, (u + 180) / 2, 26), nums[0]); f.text(along(V, u / 2 + 10, 22), nums[1])
        f.text(along(V, (180 + u + 180) / 2 + 10, 22), nums[3]); f.text(along(V, (u + 180 + 360) / 2, 26), nums[2])
    f.items = [it for it in f.items if not (it[0] == "text" and it[2] == "6")]
    f.angle(B, 0, u, "6 = 135°", 135, r=14, lr=50)
    return f

@fig
def ex2():
    f = Fig("ex2"); T = P(0, 90); Bp = P(0, 0)
    f.line(T, 0, -130, 130); f.text(P(142, 90), "l", anchor="start")
    f.line(Bp, -10, -130, 130); f.text(along(Bp, -10, 142), "m", anchor="start")
    u = 60; B = meet(T, u, Bp, -10); f.seg(along(T, u, 45), along(B, u + 180, 45)); f.text(along(B, u + 180, 57), "t")
    f.angle(T, u, 180, "a = 120°", 120, r=18, lr=46)
    f.angle(B, -10, u, "f = 70°", 70, r=24, lr=50)
    f.angle(T, 0, u, "b", 60, r=24, color=ASK)
    return f

@fig
def ex3():
    f = Fig("ex3"); top, bot = pair(f, 0, labels=("l", "m"))
    u = 130; T, B = cross(f, top, bot, 0, P(30, 90), u, label="t")
    f.angle(T, u + 180, 360, "3 = 50°", 50, r=22, lr=50)
    f.angle(B, 0, u, "6", 130, r=18, lr=30, color=ASK)
    return f

@fig
def ex4():
    f = Fig("ex4"); D = P(0, 0); C = P(180, 0)
    s = 180 * math.sin(d2r(55)) / math.sin(d2r(65)); A = along(D, 60, s); B = add(A, (180, 0))
    for p, q in ((A, B), (B, C), (C, D), (D, A)): f.seg(p, q)
    f.seg(A, C)
    f.arrows(along(D, 0, 80), 0, 1); f.arrows(along(A, 0, 80), 0, 1)
    f.arrows(along(D, 60, s / 2 - 8), 60, 2); f.arrows(along(C, 60, s / 2 - 8), 60, 2)
    for p, l, o in ((A, "A", (-10, 10)), (B, "B", (10, 10)), (C, "C", (10, -10)), (D, "D", (-10, -10))):
        f.text(add(p, o), l)
    f.angle(A, 240, dirto(A, C), "65°", 65, r=24, lr=40)
    f.angle(D, 0, 60, "60°", 60, r=22, lr=38)
    return f

@fig
def bend():
    f = Fig("bend"); top, bot = pair(f, 0, gap=120, L=150)
    A = P(-110, 120); C = P(-90, 0)
    O = meet(A, -35, C, 50)
    f.seg(A, O); f.seg(O, C); f.dot(O); f.text(add(O, (14, 0)), "O", anchor="start")
    f.line(O, 0, -150, 150, color=HELP, dash="6,4")
    f.angle(A, 325, 360, "35°", 35, r=26, lr=42)
    f.angle(C, 0, 50, "50°", 50, r=24, lr=40)
    f.angle(O, 145, 180, "35°", 35, r=26, lr=44, color=ANS)
    f.angle(O, 180, 230, "50°", 50, r=26, lr=44, color=ANS)
    return f

@fig
def illusion():
    f = Fig("illusion"); C = P(0, 0)
    for k in range(0, 180, 10):
        f.line(C, k, -150, 150, color="#90a4ae", w=1.4)
    f.line(P(0, 40), 0, -150, 150, w=3.4, color="#c62828"); f.line(P(0, -40), 0, -150, 150, w=3.4, color="#c62828")
    return f

# ---------------------------------------------------------------- exercise figures (Q1)
def q1(name, alpha, u, givens, asks, other=None, Tshift=0):
    f = Fig(name); top, bot = pair(f, alpha, L=110)
    T, B = cross(f, top, bot, alpha, along(top, alpha, Tshift), u, ext=40)
    V = {"T": T, "B": B}
    if other:
        u2, s2, marks2 = other
        T2, B2 = cross(f, top, bot, alpha, along(top, alpha, s2), u2, ext=40)
        V.update({"T2": T2, "B2": B2})
    for v, a1, a2, val in givens: f.angle(V[v], a1, a2, f"{val}°", val, r=20, lr=36)
    for v, a1, a2, lab, val in asks: f.angle(V[v], a1, a2, lab, val, r=18, lr=32, color=ASK)
    return f

@fig
def q1a(): return q1("q1a", 20, 152, [("T", -28, 20, 48)], [("B", 152, 200, "a", 48)], Tshift=-60)
@fig
def q1b(): return q1("q1b", -5, 123, [("T", -57, -5, 52)], [("B", 123, 175, "b", 52)], Tshift=-10)
@fig
def q1c(): return q1("q1c", -10, 71, [("T", 71, 170, 99), ("T", -10, 71, 81)], [("B", -10, 71, "c", 81)])
@fig
def q1d(): return q1("q1d", -9, 90, [("B", 90, 171, 81), ("B", -9, 90, 99)], [("T", 171, 270, "d", 99)])
@fig
def q1e(): return q1("q1e", 12, 95, [("B", 95, 192, 97), ("B", 12, 95, 83), ("B2", 123, 192, 69)],
                    [("T2", 303, 372, "e", 69)], other=(123, 55, 1), Tshift=-60)
@fig
def q1f(): return q1("q1f", 0, 48, [("B", 48, 180, 132)], [("T", 0, 48, "f", 48)])
@fig
def q1g():
    f = Fig("q1g"); L, R = P(0, 0), P(70, 0)
    for p in (L, R): f.line(p, 90, -100, 100); f.arrows(along(p, 90, 70), 90, 1)
    X = P(70, 10); Y = meet(X, 148, L, 90)
    f.seg(along(X, -32, 55), along(Y, 148, 45))
    f.angle(X, 90, 148, "58°", 58, r=16, lr=30); f.angle(X, -32, 90, "122°", 122, r=16, lr=34)
    f.angle(X, 148, 270, "122°", 122, r=16, lr=34); f.angle(X, 270, 328, "58°", 58, r=16, lr=30)
    f.angle(Y, 148, 270, "g", 122, r=16, lr=30, color=ASK)
    return f
@fig
def q1h(): return q1("q1h", 0, 60, [("B", 60, 180, 120), ("T2", 285, 360, 75)], [("B2", 105, 180, "h", 75)],
                    other=(105, 40, 1), Tshift=-60)
@fig
def q1i():
    f = Fig("q1i"); Pp = P(0, 0); Q = P(-130, 0)
    f.line(Pp, 0, -175, 70)
    R = meet(Q, 56, Pp, 110)
    f.line(Pp, 56, 0, 120); f.arrows(along(Pp, 56, 90), 56, 1)
    f.line(Q, 56, 0, dist(Q, R) + 40); f.arrows(along(Q, 56, 70), 56, 1)
    f.seg(Pp, along(R, 110, 30))
    f.angle(Pp, 110, 180, "70°", 70, r=18, lr=34); f.angle(Pp, 56, 110, "54°", 54, r=26, lr=42)
    f.angle(Pp, 0, 56, "56°", 56, r=18, lr=34)
    f.angle(R, 236, 290, "i", 54, r=20, lr=34, color=ASK)
    return f
@fig
def q1j():
    f = Fig("q1j"); V = P(-120, 60)
    A, Bd = -37, -64
    xs = [-60, 30, 120]
    hitsA = [meet(V, A, P(x, -40), 60) for x in xs]
    hitsB = [meet(V, Bd, P(x, -40), 60) for x in xs]
    for x, ha in zip(xs, hitsA):
        base = P(x, -40); t = ((ha[0] - x) * 0.5 + (ha[1] + 40) * 0.866)
        f.line(base, 60, min(-50, t - 40), 170); f.arrows(along(base, 60, 140), 60, 1)
    f.seg(along(V, A + 180, 15), along(hitsA[2], A, 30)); f.seg(along(V, Bd + 180, 15), along(hitsB[0], Bd, 30))
    f.angle(V, Bd, A, "27°", 27, r=34, lr=50)
    f.angle(hitsA[0], 143, 240, "97°", 97, r=16, lr=32)
    f.angle(hitsB[0], 116, 240, "124°", 124, r=14, lr=30)
    f.angle(hitsA[2], 143, 240, "j", 97, r=16, lr=30, color=ASK)
    return f

# ---------------------------------------------------------------- Q2, Q3
@fig
def q2i(): return q1("q2i", 0, 42, [("T", 0, 42, 42), ("B2", 80, 180, 100)], [("B", 42, 180, "a", 138)],
                     other=(80, 75, 1), Tshift=-40)
@fig
def q2ii():
    f = Fig("q2ii"); h, s = -6, 112
    H1, H2 = P(0, 90), P(0, 0)
    for p in (H1, H2): f.line(p, h, -120, 120); f.arrows(along(p, h, 90), h, 2)
    for x in (-40, 40):
        p = P(x, 45); f.line(p, s, -90, 90); f.arrows(along(p, s, 60), s, 1)
    TR = meet(P(40, 45), s, H1, h); BL = meet(P(-40, 45), s, H2, h)
    f.angle(TR, s + 180, h + 360, "62°", 62, r=18, lr=34)
    f.angle(BL, h + 180, s + 180, "a", 118, r=16, lr=30, color=ASK)
    return f
@fig
def q2iii():
    f = Fig("q2iii")
    for y in (100, 50, 0): f.line(P(0, y), 0, -110, 110); f.arrows(P(80, y), 0, 1)
    X = P(0, 50)
    f.line(X, 75, -60, 75); f.line(X, 110, 0, 80)
    T = meet(X, 110, P(0, 100), 0); B = meet(X, 75, P(0, 0), 0)
    f.angle(T, 0, 110, "110°", 110, r=16, lr=32)
    f.angle(X, 75, 110, "35°", 35, r=30, lr=44)
    f.angle(B, 75, 180, "a", 105, r=16, lr=30, color=ASK)
    return f
@fig
def q2iv():
    f = Fig("q2iv"); Pp = P(0, 0); Q = P(55, 0)
    f.line(Pp, 0, -60, 110); f.line(Pp, 90, 0, 165); f.right(Pp, 0)
    R = meet(Q, 113, Pp, 90)
    f.line(Pp, 113, 0, 120); f.arrows(along(Pp, 113, 80), 113, 1)
    f.line(Q, 113, 0, dist(Q, R) + 35); f.arrows(along(Q, 113, 40), 113, 1)
    f.angle(Pp, 113, 180, "67°", 67, r=20, lr=36)
    f.angle(R, 270, 293, "a", 23, r=30, lr=44, color=ASK)
    return f
@fig
def q3i():
    f = Fig("q3i"); top, bot = pair(f, 0, gap=80, L=120)
    f.line(P(0, 0), 90, -40, 120); f.right(P(0, 80), 270, s=10)
    Bp = P(0, 0); T = meet(Bp, 25, top, 0)
    f.seg(along(Bp, 205, 45), along(T, 25, 40))
    f.angle(Bp, 25, 90, "65°", 65, r=24, lr=40)
    f.angle(Bp, 180, 205, "x", 25, r=30, lr=44, color=ASK)
    f.angle(T, 205, 360, "y", 155, r=16, lr=30, color=ASK)
    return f
@fig
def q3ii():
    f = Fig("q3ii"); top, bot = pair(f, 0, gap=80, L=120, through=(-20, 0))
    X = P(0, 80); R = meet(X, 53, bot, 0); S = meet(X, 78, bot, 0)
    f.seg(along(R, 233, 40), along(X, 53, 50)); f.seg(along(S, 258, 40), along(X, 78, 50))
    f.angle(R, 0, 53, "53°", 53, r=20, lr=36); f.angle(S, 0, 78, "78°", 78, r=20, lr=36)
    f.angle(X, 53, 78, "x", 25, r=34, lr=48, color=ASK)
    return f

# ---------------------------------------------------------------- Q4, Q5, Q6
@fig
def q4():
    f = Fig("q4"); E = P(0, 0); top = P(0, 90)
    f.line(top, 0, -150, 140); f.arrows(P(-120, 90), 0, 1)
    f.line(E, 0, -150, 140); f.arrows(P(-120, 0), 0, 1)
    K = meet(E, 102, top, 0); B = meet(E, 45, top, 0)
    J = along(K, 102, 55); F = along(E, 282, 50); C = along(B, 45, 45); H = along(E, 225, 50)
    f.seg(J, F); f.seg(C, H)
    I = add(K, (-70, 0)); A = add(B, (60, 0)); G = P(-70, 0); D = P(90, 0)
    for p, l, o in ((J, "J", (-12, 0)), (K, "K", (-12, -14)), (I, "I", (0, -15)), (B, "B", (-12, 12)), (A, "A", (0, -15)),
                    (C, "C", (12, 4)), (G, "G", (0, -15)), (E, "E", (14, -12)), (D, "D", (0, -15)), (H, "H", (-12, -4)), (F, "F", (12, 0))):
        f.dot(p); f.text(add(p, o), l)
    f.angle(K, 102, 180, "78°", 78, r=18, lr=34); f.angle(B, 0, 45, "45°", 45, r=20, lr=36)
    return f
@fig
def q5():
    f = Fig("q5"); s = 70; top = 150
    Ae, Ce, Ee = P(0, top), P(s, top), P(2 * s, top)
    f.seg(add(Ae, (-25, 0)), add(Ee, (25, 0)))
    for p in (Ae, Ce, Ee): f.line(p, 90, -175, 30); f.arrows(along(p, 90, 18), 90, 1)
    D = meet(Ee, 215, Ce, 90); B = meet(Ee, 215, Ae, 90)
    f.seg(Ee, along(B, 215, 30)); f.right(Ae, 270, s=10)
    Fp = add(Ee, (0, -165))
    for p, l, o in ((Ae, "A", (-12, 12)), (Ce, "C", (-12, 12)), (Ee, "E", (12, 12)), (D, "D", (-12, 8)), (B, "B", (-12, 8)), (Fp, "F", (12, 0))):
        f.dot(p); f.text(add(p, o), l)
    f.angle(Ee, 215, 270, "55°", 55, r=24, lr=40)
    f.angle(D, 270, 395, "y", 125, r=16, lr=28, color=ASK)
    f.angle(B, 270, 395, "x", 125, r=16, lr=28, color=ASK)
    return f
@fig
def q6():
    f = Fig("q6"); M = P(0, 0)
    L = along(M, 95, 150); N = along(M, 55, 140); O = along(N, 331, 120)
    Pp = along(O, 43, 110); Q = along(Pp, 275, 140)
    for a, b in ((M, L), (M, N), (N, O), (O, Pp), (Pp, Q)): f.seg(a, b)
    f.arrows(along(M, 95, 100), 95, 1); f.arrows(along(Q, 95, 100), 95, 1)
    for p, l, o in ((L, "L", (12, 0)), (M, "M", (0, -15)), (N, "N", (0, 14)), (O, "O", (0, -16)), (Pp, "P", (12, 6)), (Q, "Q", (12, 0))):
        f.dot(p); f.text(add(p, o), l)
    f.angle(M, 55, 95, "40°", 40, r=30, lr=46)
    f.angle(N, 235, 331, "96°", 96, r=18, lr=34)
    f.angle(Pp, 223, 275, "52°", 52, r=22, lr=38)
    f.angle(O, 43, 151, "?", 108, r=18, lr=32, color=ASK)
    return f
@fig
def q6_ans():
    f = q6(); f.name = "q6_ans"
    M = P(0, 0); N = along(M, 55, 140); O = along(N, 331, 120)
    f.line(N, 95, -70, 50, color=HELP, dash="6,4"); f.line(O, 95, -60, 60, color=HELP, dash="6,4")
    f.items = [it for it in f.items if not (it[0] == "text" and it[2] in ("?", "96°"))]
    f.angle(N, 235, 275, "40°", 40, r=44, lr=64, color=ANS); f.angle(N, 275, 331, "56°", 56, r=44, lr=64, color=ANS)
    f.text(along(N, 283, 30), "96°", color=GIVEN, size=12)
    f.angle(O, 95, 151, "56°", 56, r=40, lr=60, color=ANS); f.angle(O, 43, 95, "52°", 52, r=40, lr=60, color=ANS)
    f.text(along(O, 97, 28), "108°", color=ASK, bold=True, size=13)
    return f

if __name__ == "__main__":
    for fn in FIGS:
        f = fn()
        open(os.path.join(OUT, f.name + ".svg"), "w").write(f.svg())
    print(len(FIGS), "figures written")
