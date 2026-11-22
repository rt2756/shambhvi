#!/usr/bin/env python3
"""Check the Little Learners data (content/little/*.json): structure + answer keys.

    python3 tools/check_little.py

Each topic: title, emoji, group (maths|words|world), "parent" notes that each carry a
"why", at least 5 "ask" questions, and 3 rounds of 5 questions. Each question has text,
2-4 distinct options (right one FIRST) and a hint. Answer keys are checked two ways:
  "k" - a Python formula; must equal the number at the start of the right option
  "c" - an emoji; the picture must contain exactly as many of it as the right option says
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "content", "little")

def lead(s):
    m = re.search(r"-?\d+", s.replace("₹", "").replace("−", "-"))
    return int(m.group()) if m else None

errors = 0
def bad(where, msg):
    global errors
    errors += 1
    print(f"  ✗ {where}: {msg}")

files = json.load(open(os.path.join(DIR, "manifest.json")))
total = 0
for name in files:
    d = json.load(open(os.path.join(DIR, name), encoding="utf-8"))
    for key in ("title", "emoji", "group", "parent", "ask", "rounds"):
        if key not in d: bad(name, f"missing {key}")
    if d.get("group") not in ("maths", "words", "world"): bad(name, "bad group")
    for p in d.get("parent", []):
        if not p.get("learn") or not p.get("why"): bad(name, "parent note without learn/why")
    if len(d.get("ask", [])) < 5: bad(name, "fewer than 5 ask questions")
    if len(d.get("rounds", [])) != 3: bad(name, "needs 3 rounds")
    for r, qs in enumerate(d.get("rounds", []), 1):
        if len(qs) != 5: bad(f"{name} r{r}", f"{len(qs)} questions, want 5")
        for i, q in enumerate(qs, 1):
            w = f"{name} r{r} q{i}"
            total += 1
            o = q.get("o", [])
            if not q.get("t") or not q.get("h"): bad(w, "missing text or hint")
            if not 2 <= len(o) <= 4: bad(w, f"{len(o)} options")
            if len(set(o)) != len(o): bad(w, "duplicate options")
            if "k" in q and eval(q["k"]) != lead(o[0]):
                bad(w, f"key {q['k']} = {eval(q['k'])} but right option is {o[0]!r}")
            if "c" in q and q["p"].count(q["c"]) != lead(o[0]):
                bad(w, f"picture has {q['p'].count(q['c'])} × {q['c']} but right option is {o[0]!r}")
print(f"{len(files)} topics, {total} questions — " + ("all good ✓" if not errors else f"{errors} problem(s)"))
sys.exit(1 if errors else 0)
