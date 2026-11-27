"""Tiny geometry-to-SVG helper. World coords: y up. Every angle mark asserts that the
drawn angle equals the number written on it, so a label can never disagree with the picture."""
import math

INK, GIVEN, ASK, HELP, ANS = "#263238", "#1565c0", "#c62828", "#8a969c", "#2e7d32"

def d2r(a): return math.radians(a)
def P(x, y): return (float(x), float(y))
def add(p, q): return (p[0] + q[0], p[1] + q[1])
def mul(v, k): return (v[0] * k, v[1] * k)
def unit(a): return (math.cos(d2r(a)), math.sin(d2r(a)))
def along(p, a, t): return add(p, mul(unit(a), t))
def dirto(p, q): return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360
def dist(p, q): return math.hypot(q[0] - p[0], q[1] - p[1])

def meet(p1, a1, p2, a2):
    """Intersection of line through p1 at angle a1 and line through p2 at angle a2."""
    d1, d2 = unit(a1), unit(a2)
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-12: raise ValueError("parallel")
    t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / den
    return along(p1, a1, t)

def on_y(p, a, y):   # point on line (p, a) with the given y
    return meet(p, a, (0, y), 0)

def on_x(p, a, x):
    return meet(p, a, (x, 0), 90)

class Fig:
    def __init__(self, name):
        self.name, self.items, self.pts = name, [], []

    def _track(self, *ps):
        self.pts.extend(ps)

    def seg(self, p, q, color=INK, w=2.2, dash=None):
        self._track(p, q)
        self.items.append(("line", p, q, color, w, dash))

    def line(self, p, a, t0, t1, **kw):
        """Segment of the line through p at angle a, from parameter t0 to t1."""
        self.seg(along(p, a, t0), along(p, a, t1), **kw)

    def arrows(self, p, a, n=1, color=INK):
        """Parallel marks: n chevrons at p pointing along direction a."""
        for i in range(n):
            tip = along(p, a, 7 + 7 * i)
            for s in (+1, -1):
                self.seg(along(tip, a + 180 + 35 * s, 9), tip, color=color, w=2)

    def angle(self, v, a1, a2, label, expect=None, r=22, color=GIVEN, lr=None, bold=False):
        """Arc counter-clockwise from ray a1 to ray a2 at vertex v."""
        sweep = (a2 - a1) % 360
        if expect is not None:
            assert abs(sweep - expect) < 0.05, f"{self.name}: angle {label!r} drawn {sweep:.2f}, labelled {expect}"
        self.items.append(("arc", v, r, a1, sweep, color))
        mid = a1 + sweep / 2
        lr = lr or r + 15
        self._track(along(v, mid, lr + 10))
        self.items.append(("text", along(v, mid, lr), label, color, "middle", bold or color == ASK, 15))

    def right(self, v, a1, s=11, color=INK):
        """Right-angle square between rays a1 and a1 + 90."""
        p1, p3 = along(v, a1, s), along(v, a1 + 90, s)
        p2 = add(p1, mul(unit(a1 + 90), s))
        self.items.append(("poly", [p1, p2, p3], color))

    def dot(self, p, color=INK):
        self._track(p)
        self.items.append(("dot", p, color))

    def text(self, p, s, color=INK, anchor="middle", bold=False, size=15):
        self._track(add(p, (0, 12)), add(p, (0, -6)))
        self.items.append(("text", p, s, color, anchor, bold, size))

    def label(self, p, s, color=INK, anchor="middle", bold=False, size=15):
        """Like text(), but also keeps the text's estimated width inside the picture, so long
        labels anchored at one end are not clipped. (text() is kept as it was so existing
        figures are drawn exactly the same.)"""
        w = len(s) * size * (0.6 if bold else 0.56)
        x0 = {"start": p[0], "end": p[0] - w, "middle": p[0] - w / 2}[anchor]
        self._track(P(x0, p[1]), P(x0 + w, p[1]))
        self.text(p, s, color=color, anchor=anchor, bold=bold, size=size)

    def poly(self, ps, fill="#ffe0b2", color=INK):
        self._track(*ps)
        self.items.append(("fillpoly", ps, fill, color))

    def circle(self, c, r, color=HELP, w=1.6, dash=None):
        """A full circle (compass drawing)."""
        self._track(add(c, (-r, -r)), add(c, (r, r)))
        self.items.append(("circle", c, r, color, w, dash))

    def carc(self, c, r, a1, a2, color=HELP, w=1.6, dash=None):
        """A compass arc of radius r about c, counter-clockwise from angle a1 to a2 (degrees)."""
        sweep = (a2 - a1) % 360
        self._track(*[along(c, a1 + sweep * k / 8, r) for k in range(9)])
        self.items.append(("carc", c, r, a1, sweep, color, w, dash))

    def ticks(self, p, q, n=1, color=INK, size=7, gap=5):
        """n equal-length tick marks across the middle of segment pq (the 'equal sides' sign)."""
        a = dirto(p, q); m = mul(add(p, q), 0.5)
        for i in range(n):
            c = along(m, a, (i - (n - 1) / 2) * gap)
            self.seg(along(c, a + 90, size), along(c, a - 90, size), color=color, w=1.6)

    def svg(self, pad=14, scale=1.0):
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
        x0, x1, y0, y1 = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
        W, H = (x1 - x0), (y1 - y0)
        def T(p): return (round(p[0] - x0, 1), round(y1 - p[1], 1))
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W*scale:.0f}" height="{H*scale:.0f}" font-family="Helvetica, Arial, sans-serif">',
               f'<rect width="100%" height="100%" fill="#ffffff"/>']
        for it in self.items:
            k = it[0]
            if k == "line":
                _, p, q, c, w, dash = it; (a, b), (cc, d) = T(p), T(q)
                da = f' stroke-dasharray="{dash}"' if dash else ""
                out.append(f'<line x1="{a}" y1="{b}" x2="{cc}" y2="{d}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{da}/>')
            elif k == "fillpoly":
                _, ps, fill, c = it
                out.append('<polygon points="' + " ".join(f"{T(p)[0]},{T(p)[1]}" for p in ps) + f'" fill="{fill}" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>')
            elif k == "arc":
                _, v, r, a1, sw, c = it
                s, e = T(along(v, a1, r)), T(along(v, a1 + sw, r))
                large = 1 if sw > 180 else 0
                out.append(f'<path d="M{s[0]},{s[1]} A{r},{r} 0 {large} 0 {e[0]},{e[1]}" fill="none" stroke="{c}" stroke-width="1.8"/>')
            elif k == "circle":
                _, c, r, col, w, dash = it; a, b = T(c)
                da = f' stroke-dasharray="{dash}"' if dash else ""
                out.append(f'<circle cx="{a}" cy="{b}" r="{r:.1f}" fill="none" stroke="{col}" stroke-width="{w}"{da}/>')
            elif k == "carc":
                _, c, r, a1, sw, col, w, dash = it
                s, e = T(along(c, a1, r)), T(along(c, a1 + sw, r))
                da = f' stroke-dasharray="{dash}"' if dash else ""
                out.append(f'<path d="M{s[0]},{s[1]} A{r:.1f},{r:.1f} 0 {1 if sw > 180 else 0} 0 {e[0]},{e[1]}" fill="none" stroke="{col}" stroke-width="{w}"{da}/>')
            elif k == "poly":
                _, ps, c = it
                out.append('<polyline points="' + " ".join(f"{T(p)[0]},{T(p)[1]}" for p in ps) + f'" fill="none" stroke="{c}" stroke-width="1.6"/>')
            elif k == "dot":
                _, p, c = it; a, b = T(p)
                out.append(f'<circle cx="{a}" cy="{b}" r="3.6" fill="{c}"/>')
            elif k == "text":
                _, p, s, c, anc, bold, size = it; a, b = T(p)
                fw = ' font-weight="bold"' if bold else ""
                s = s.replace("&", "&amp;").replace("<", "&lt;")
                out.append(f'<text x="{a}" y="{b + size * 0.35:.1f}" font-size="{size}" fill="{c}" text-anchor="{anc}"{fw}>{s}</text>')
        out.append("</svg>")
        return "\n".join(out) + "\n"
