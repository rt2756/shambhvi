#!/usr/bin/env python3
"""Check chapter notes against the notes standard in CLAUDE.md.

    python3 tools/check_notes.py               # strict check of every rewritten chapter
    python3 tools/check_notes.py class7/math   # only chapters under content/class7/math
    python3 tools/check_notes.py --survey      # count book pointers in EVERY notes file (no failure)
    python3 tools/check_notes.py --compare class8/math/4.quadrilaterals.md   # measure a chapter against its pilot

A chapter counts as "rewritten" once it has a "## Exercises — try first" section. Every rewritten
chapter must be listed in tools/notes_coverage.json with the number of practice questions
("check") and end-of-chapter questions ("exercises") the book has; the checker makes sure the
notes answer exactly that many. Strict checks:

  1. no pointers to the book ("the book", NCERT, Example 6, Fig. 5.3, Activity 2, Exercise 5.2,
     "selected", "the rest are similar", ...) outside HTML comments;
  2. in "Check yourself" and "Exercises — try first" sections, every question has exactly one
     > [!ANSWER] block, and the counts match tools/notes_coverage.json;
  3. every image has alt text and points to a file that exists;
  4. the chapter's figure script (tools/figures/class<N>_<subject>_<ch>.py) runs — its angle checks
     pass — and reproduces the committed SVGs exactly (so nobody hand-edits a figure);
  5. "In a nutshell" and a "Top traps" line are present, and the chapter is not too short.

Soft check (warnings only, never blocks): each rewritten chapter is measured against the approved
pilot for its subject (PILOTS below) — why-explanations, worked examples, callouts, figures, "Try
this" activities, answer length and how many answers give reasons and steps. A measure under half the
pilot's value prints a "⚠ soft" warning: look at it and either improve the chapter or note in PLAN.md
why it is fine (a chapter on numbers needs fewer figures than one on angles).

Exit status 1 if any strict check fails (the pre-commit hook relies on this).
"""
import glob, json, os, re, subprocess, sys, tempfile, filecmp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
COVERAGE = os.path.join(ROOT, "tools", "notes_coverage.json")
NOTES_DIRS = ["class*/math", "class*/science"]
MIN_WORDS = 2000

BANNED = [
    (r"\bthe book\b", "says 'the book'"),
    (r"\bbook['’]s\b", "says 'book's'"),
    (r"\bNCERT\b", "mentions NCERT"),
    (r"\btextbook\b", "mentions the textbook"),
    (r"(?<!\*\*)\bExample \d+\b(?!\.\*\*)", "refers to a numbered book example (our own worked examples are fine as '**Example 1.**')"),
    (r"\bFig(?:\.|ure)\s*\d+\.\d+", "refers to a book figure number"),
    (r"\bActivity \d+(?:\.\d+)?\b", "refers to a numbered book activity"),
    (r"\bExercise \d+\.\d+", "refers to a numbered book exercise"),
    (r"\bselected\b", "says 'selected' (every question must be solved)"),
    (r"\b(?:the )?rest (?:are|is) (?:similar|done the same way)", "skips questions as 'similar'"),
    (r"\bsimilar(?:ly)? to (?:Q|question|the above|part)", "skips a question as 'similar'"),
    (r"\bpage \d+\b", "refers to a book page"),
]

QMARK = re.compile(r"^\s*\*\*\(?(?:\d+|[a-z]|[ivx]+)[.)]\*\*")   # **1.**  **(a)**  **(iv)**
ANSWER = re.compile(r"^\s*>\s*\[!ANSWER\]")
IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


def strip_comments(text):
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def notes_files(filters):
    files = []
    for pat in NOTES_DIRS:
        for d in sorted(glob.glob(os.path.join(CONTENT, pat))):
            for f in sorted(glob.glob(os.path.join(d, "*.md"))):
                rel = os.path.relpath(f, CONTENT).replace(os.sep, "/")
                if os.path.basename(f).startswith("0."): continue
                if filters and not any(rel.startswith(x.rstrip("/")) for x in filters): continue
                files.append(rel)
    return files


def banned_hits(text):
    hits = []
    for i, line in enumerate(strip_comments(text).splitlines(), 1):
        for pat, why in BANNED:
            for m in re.finditer(pat, line, flags=re.I):
                hits.append((i, why, m.group(0)))
    return hits


def sections(lines):
    """Yield (kind, start, end) for every Check yourself (H3) and Exercises (H2) section."""
    out = []
    for i, line in enumerate(lines):
        if re.match(r"^###\s+Check yourself", line, re.I):
            j = next((k for k in range(i + 1, len(lines)) if re.match(r"^#{2,3}\s", lines[k])), len(lines))
            out.append(("check", i, j))
        elif re.match(r"^##\s+Exercises\b", line, re.I):
            j = next((k for k in range(i + 1, len(lines)) if re.match(r"^##\s", lines[k])), len(lines))
            out.append(("exercises", i, j))
    return out


def count_questions(lines, start, end, problems, where):
    """Each question (a **1.** / **(a)** marker, a numbered ### heading with no parts, or plain
    text before an answer) must be followed by exactly one [!ANSWER] block."""
    answers, pending, pending_line, text_since = 0, False, None, False
    i = start + 1
    while i < end:
        line = lines[i]
        if ANSWER.match(line):
            if not pending and not text_since:
                problems.append(f"{where}:{i+1}: answer block with no question before it")
            answers += 1; pending = False; text_since = False
            while i + 1 < end and lines[i + 1].startswith(">"): i += 1   # skip the rest of the block
        elif QMARK.match(line):
            if pending:
                problems.append(f"{where}:{pending_line}: question has no [!ANSWER] block")
            pending, pending_line, text_since = True, i + 1, True
        elif re.match(r"^###\s+\d+\.", line):
            # a numbered exercise heading: a question itself, unless parts (a), (b)... follow
            if pending:
                problems.append(f"{where}:{pending_line}: question has no [!ANSWER] block")
            nxt = next((k for k in range(i + 1, end) if QMARK.match(lines[k]) or ANSWER.match(lines[k])
                        or re.match(r"^###\s", lines[k])), end)
            has_parts = nxt < end and QMARK.match(lines[nxt])
            pending, pending_line, text_since = (not has_parts), i + 1, (not has_parts)
        elif line.strip() and not line.startswith("#") and not line.startswith("!["):
            text_since = True
        i += 1
    if pending:
        problems.append(f"{where}:{pending_line}: question has no [!ANSWER] block")
    return answers


def figure_script_for(rel):
    m = re.match(r"class(\d+)/(math|science)/(\d+)\.", rel)
    return (m and os.path.join(ROOT, "tools", "figures", f"class{m.group(1)}_{m.group(2)}_{m.group(3)}.py"),
            m and os.path.join(ROOT, "assets", "img", f"class{m.group(1)}", m.group(2), m.group(3)))


def check_figures(rel, problems):
    script, imgdir = figure_script_for(rel)
    if not script or not os.path.isdir(imgdir):
        return
    if not os.path.exists(script):
        problems.append(f"{rel}: figures in {os.path.relpath(imgdir, ROOT)} but no script {os.path.relpath(script, ROOT)}")
        return
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, script], env=dict(os.environ, FIG_OUT=tmp),
                           capture_output=True, text=True)
        if r.returncode:
            last = (r.stderr.strip().splitlines() or ["(no output)"])[-1]
            problems.append(f"{rel}: figure script failed: {last}")
            return
        made, kept = set(os.listdir(tmp)), set(os.listdir(imgdir))
        for f in sorted(kept - made): problems.append(f"{rel}: figure {f} is not made by the script")
        for f in sorted(made - kept): problems.append(f"{rel}: script makes {f} but it is not committed (run the script)")
        for f in sorted(made & kept):
            if not filecmp.cmp(os.path.join(tmp, f), os.path.join(imgdir, f), shallow=False):
                problems.append(f"{rel}: figure {f} differs from what the script draws (re-run the script)")


def check_file(rel, coverage, problems):
    path = os.path.join(CONTENT, rel)
    text = open(path, encoding="utf-8").read()
    lines = strip_comments(text).splitlines()
    for ln, why, s in banned_hits(text):
        problems.append(f"{rel}:{ln}: {why}: {s!r}")
    counts = {"check": 0, "exercises": 0}
    for kind, a, b in sections(lines):
        counts[kind] += count_questions(lines, a, b, problems, rel)
    want = coverage.get(rel)
    if want is None:
        problems.append(f"{rel}: not listed in tools/notes_coverage.json (add the book's question counts)")
    else:
        for kind in ("check", "exercises"):
            if counts[kind] != want.get(kind, 0):
                problems.append(f"{rel}: {counts[kind]} answered {kind} questions, the book has {want.get(kind, 0)}")
    for m in IMG.finditer(text):
        alt, src = m.group(1).strip(), m.group(2)
        if not alt: problems.append(f"{rel}: image {src} has no alt text")
        if not src.startswith("http") and not os.path.exists(os.path.join(ROOT, src)):
            problems.append(f"{rel}: image {src} does not exist")
    check_figures(rel, problems)
    if not re.search(r"^##\s+In a nutshell", text, re.M | re.I): problems.append(f"{rel}: no '## In a nutshell' section")
    if not re.search(r"Top traps", text): problems.append(f"{rel}: no 'Top traps' line")
    words = len(re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text).split())
    if words < MIN_WORDS: problems.append(f"{rel}: only {words} words (under {MIN_WORDS})")
    return counts


# ---------------------------------------------------------------- soft check against the pilot
# Not rules: warnings when a rewritten chapter is much thinner than the approved pilot for its
# subject. They never fail the check or block a commit. Science and grammar get a pilot later.
PILOTS = {"math": "class7/math/5.parallel-and-intersecting-lines.md"}
SOFT_RATIO = 0.5          # warn below half the pilot's value


def profile(text):
    """Measures of how a chapter teaches, per 1000 words where that makes sense."""
    body = strip_comments(text)
    words = max(1, len(re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body).split()))
    k = 1000 / words
    answers = re.findall(r"^>\s*\[!ANSWER\][^\n]*\n((?:>.*\n?)*)", body, re.M)
    ans_words = [len(re.sub(r"^>\s?", "", a, flags=re.M).split()) for a in answers]
    reasoned = [a for a in answers if re.search(r"\bbecause\b|\bso\b|\bsince\b|\bwhy\b|\(.*(?:angles?|pair|rule|parallel|equal|formula|property).*\)|=", a, re.I)]
    stepped = [a for a in answers if re.search(r"^>\s*(?:\d+\.|-)\s", a, re.M)]
    return {
        "words": words,
        "why explanations /1000 words": len(re.findall(r"\*\*Why\b|\bWhy it works\b|\bWhy:|^\*\*Why", body, re.M)) * k,
        "worked examples /1000 words": len(re.findall(r"\*\*(?:Worked example|Example \d+)", body)) * k,
        "callouts /1000 words": len(re.findall(r"^>\s*\[!(?:TIP|NOTE|IMPORTANT|WARNING|CAUTION)\]", body, re.M)) * k,
        "figures /1000 words": len(IMG.findall(body)) * k,
        "'Try this' activities": len(re.findall(r"\*\*Try this", body)),
        "sections (##)": len(re.findall(r"^##\s", body, re.M)),
        "avg words per answer": sum(ans_words) / len(ans_words) if ans_words else 0,
        "% answers giving reasons": 100 * len(reasoned) / len(answers) if answers else 0,
        "% answers with steps or lists": 100 * len(stepped) / len(answers) if answers else 0,
        "has 'What this chapter is about'": 1 if re.search(r"^##\s+What this chapter is about", body, re.M) else 0,
    }


def subject_of(rel):
    m = re.match(r"class\d+/(math|science)/", rel)
    return m and m.group(1)


def pilot_profile(subject):
    rel = PILOTS.get(subject)
    return rel and profile(open(os.path.join(CONTENT, rel), encoding="utf-8").read())


def soft_compare(rel):
    """Return warnings comparing rel with its subject's pilot (empty if no pilot or rel is the pilot)."""
    subject = subject_of(rel)
    if not subject or PILOTS.get(subject) in (None, rel): return []
    ref, me = pilot_profile(subject), profile(open(os.path.join(CONTENT, rel), encoding="utf-8").read())
    warns = []
    for key, want in ref.items():
        if key == "words": continue
        if key == "figures /1000 words":
            if me[key] == 0: warns.append(f"{rel}: no figures at all (the pilot has {want:.1f} per 1000 words; most maths chapters need some)")
            continue
        if want and me[key] < SOFT_RATIO * want:
            warns.append(f"{rel}: {key} = {me[key]:.1f}, pilot {want:.1f}")
    return warns


def print_compare(rel):
    subject = subject_of(rel)
    ref = pilot_profile(subject)
    if not ref:
        print(f"No pilot for {subject} yet."); return
    me = profile(open(os.path.join(CONTENT, rel), encoding="utf-8").read())
    print(f"{'measure':36s} {'this chapter':>13s} {'pilot':>8s}")
    for key in ref:
        flag = "  ⚠" if key != "words" and ref[key] and me[key] < SOFT_RATIO * ref[key] else ""
        print(f"{key:36s} {me[key]:13.1f} {ref[key]:8.1f}{flag}")


def is_rewritten(rel):
    return bool(re.search(r"^##\s+Exercises\b", open(os.path.join(CONTENT, rel), encoding="utf-8").read(), re.M))


def main():
    args = sys.argv[1:]
    survey = "--survey" in args
    if "--compare" in args:
        for rel in [a for a in args if not a.startswith("--")]:
            rel = rel.replace("content/", "", 1); print(f"\n{rel}"); print_compare(rel)
        return 0
    filters = [a for a in args if not a.startswith("--")]
    files = notes_files(filters)
    coverage = json.load(open(COVERAGE, encoding="utf-8")) if os.path.exists(COVERAGE) else {}

    if survey:
        total = 0
        for rel in files:
            n = len(banned_hits(open(os.path.join(CONTENT, rel), encoding="utf-8").read()))
            total += n
            print(f"{'✓' if is_rewritten(rel) else ' '} {n:4d}  {rel}")
        print(f"\n{total} book pointers in {len(files)} notes files (✓ = rewritten to the new standard)")
        return 0

    problems, done, soft = [], 0, []
    for rel in coverage:
        if (not filters or any(rel.startswith(x.rstrip("/")) for x in filters)) and not os.path.exists(os.path.join(CONTENT, rel)):
            problems.append(f"tools/notes_coverage.json lists {rel}, which does not exist")
    for rel in files:
        if not is_rewritten(rel) and rel not in coverage: continue
        done += 1
        check_file(rel, coverage, problems)
        soft += soft_compare(rel)
    for p in problems: print("✗", p)
    for w in soft: print("⚠ soft (vs pilot):", w)
    print(f"{done} rewritten chapters checked, {len(problems)} problems, {len(soft)} soft warnings "
          f"({len(files) - done} chapters still in the old style; see --survey)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
