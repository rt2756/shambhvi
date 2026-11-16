#!/usr/bin/env python3
"""Check the chapter-test data files: structure + answer keys.

    python3 tools/check_tests.py            # every class
    python3 tools/check_tests.py 7          # one class

Structure: every file in the manifest exists, has 4 tests of 10 questions, each question is
either multiple choice ("o", right answer first, no duplicate options) or numeric ("n"), and
has an explanation ("e").

Answer keys: a question may carry "k" — a Python formula for its answer (F = Fraction).
The script works it out and compares it with "n", or with the number at the start of the
right option. So a wrong key, or a slip while editing, is caught here rather than in a test.
"""
import glob, json, math, os, re, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def lead_number(s):
    """'−3', '₹1,250', '2 3/4 m', '3/8', '12.5%' -> Fraction, else None."""
    s = re.sub(r"<[^>]+>", "", str(s)).replace("−", "-").replace("₹", "").replace(",", "").strip()
    m = re.match(r"^(-?\d+) (\d+)/(\d+)", s)
    if m:
        w = int(m.group(1)); f = F(int(m.group(2)), int(m.group(3)))
        return w - f if m.group(1).startswith("-") else w + f
    m = re.match(r"^(-?\d+(?:\.\d+)?)\s*/\s*(\d+)", s)
    if m:
        return F(m.group(1)) / int(m.group(2))
    m = re.match(r"^-?\d+(?:\.\d+)?", s) or re.search(r"\d+(?:\.\d+)?", s)   # else: first number in the text
    return F(m.group(0)) if m else None

def check_file(path, problems):
    name = os.path.relpath(path, ROOT)
    data = json.load(open(path, encoding="utf-8"))
    checked = 0
    if not data.get("title"): problems.append(f"{name}: no title")
    tests = data.get("tests", [])
    if len(tests) != 4: problems.append(f"{name}: {len(tests)} tests, want 4")
    for ti, test in enumerate(tests, 1):
        qs = test.get("q", [])
        if len(qs) != 10: problems.append(f"{name} T{ti}: {len(qs)} questions, want 10")
        for qi, q in enumerate(qs, 1):
            where = f"{name} T{ti} Q{qi}"
            if not q.get("t") or not q.get("e"): problems.append(f"{where}: missing t or e")
            if "o" in q:
                o = q["o"]
                if not 2 <= len(o) <= 4: problems.append(f"{where}: {len(o)} options")
                if len(set(o)) != len(o): problems.append(f"{where}: duplicate options {o}")
                target = lead_number(o[0])
            elif "n" in q:
                target = F(str(q["n"]))
            else:
                problems.append(f"{where}: needs o or n"); continue
            if "k" in q:
                try:
                    got = eval(q["k"], {"F": F, "math": math, "__builtins__": {"abs": abs, "round": round, "sum": sum, "min": min, "max": max, "sorted": sorted, "len": len, "pow": pow, "int": int, "range": range, "all": all}})
                except Exception as ex:
                    problems.append(f"{where}: k failed: {ex}"); continue
                if target is None:
                    problems.append(f"{where}: k given but option has no number: {q['o'][0]!r}")
                elif (F(str(round(got, 9))) if isinstance(got, float) else F(got)) != target:   # floats come from square roots
                    problems.append(f"{where}: key says {target}, formula gives {got}")
                checked += 1
    return sum(len(t.get("q", [])) for t in tests), checked

def main():
    classes = sys.argv[1:] or sorted(
        re.search(r"class(\d+)", d).group(1) for d in glob.glob(os.path.join(ROOT, "content/class*/tests")))
    problems, total, checked = [], 0, 0
    for c in classes:
        d = os.path.join(ROOT, f"content/class{c}/tests")
        manifest = json.load(open(os.path.join(d, "manifest.json")))
        on_disk = {os.path.basename(p) for p in glob.glob(os.path.join(d, "*.json"))} - {"manifest.json"}
        for extra in sorted(on_disk - set(manifest)): problems.append(f"class{c}: {extra} not in manifest")
        for f in manifest:
            p = os.path.join(d, f)
            if not os.path.exists(p): problems.append(f"class{c}: manifest lists missing {f}"); continue
            try:
                n, k = check_file(p, problems); total += n; checked += k
            except json.JSONDecodeError as ex:
                problems.append(f"class{c}/{f}: bad JSON: {ex}")
    for p in problems: print("✗", p)
    print(f"{total} questions, {checked} answer keys recomputed, {len(problems)} problems")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
