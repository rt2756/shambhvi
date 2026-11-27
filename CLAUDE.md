# CLAUDE.md

Guidance for AI assistants working in this repository.

## Start here

**Read `PLAN.md` first.** It holds the agreed plan, what's done, what's next, and learnings.
Do the next item, then update `PLAN.md` (tick it, add learnings). Work **one session at a time** —
don't start parallel or child sessions.

## What this repo is

CBSE / NCERT revision for a school student, **bucketed by class (5–10)**, published via
GitHub Pages. **Every class has three subjects — Maths, Science, English — and every subject
has exactly two things: detailed chapter NOTES and 4-level self-marking TESTS, on one chapter
list taken from the current NCERT book.** Don't add other page types (practice-question sets,
cheat sheets, extra tabs) — fold anything useful into the notes or the tests.

- Maths: `content/class<N>/math/*.md` + `content/class<N>/tests/*.json` (same file names).
- Science: `content/class<N>/science/*.md` + `content/class<N>/science-tests/*.json`. Science
  stays **one subject** up to class 10, as in the NCERT book (no physics/chemistry/biology split).
- English: the class-free grammar course — `content/grammar/notes/` (21 lessons, each saying
  which classes teach it) and `content/grammar/tests/`; each class's English tab shows only its
  lessons via `manifest-class<N>.json` in both folders. Run `python3 tools/check_tests.py grammar` after edits.

Pages per class: `class<N>-math.html`, `class<N>-tests.html`, `class<N>-science.html`,
`class<N>-science-tests.html`, `class<N>-english.html`, `class<N>-english-tests.html`. See
`README.md` for the full file map, callout syntax, and how rendering works.

**Notes are detailed teaching, not cheat sheets** — explain each chapter the way a patient
tutor would explain it to a child, and follow the **notes standard** below
(model chapter: `content/class7/math/5.parallel-and-intersecting-lines.md`).

**Music** is class-free too: `content/music/notes/` (theory lessons, written for a complete-beginner
electric guitarist), `content/music/practice/` (30-minute-a-day plan, one file per week, tick-off
checklists) and `content/music/tests/`, shown on `music.html`, `guitar-practice.html` and
`music-tests.html`. TAB and chord boxes go in fenced code blocks. Run `python3 tools/check_tests.py music` after edits.

Source books are local and gitignored: `ncert_books/class_<N>/*.pdf` (see its `INDEX.md`).
**Always verify a chapter list or fact against the actual book PDF** rather than recalling
it — the 2024–26 NCERT rewrites renamed and reordered many chapters.

## The rule that matters most: teach *why*, not just *how*

Every concept, rule, step, shortcut, or formula you write **must be explained** — the
student should understand *why it is true*, not just memorise *that it is*. A step with no
reason attached is a defect, even when it is correct.

- Pair each rule with a **`**Why it works:**`** (or **Why:**) explanation — see how
  `content/class7/math/5.parallel-and-intersecting-lines.md` proves vertically opposite,
  alternate and interior angles instead of just stating them.
- If the "why" is long, it can live nearby or in a linked section — but it must exist
  **somewhere** in the notes, not only in the student's memory.
- Before finishing any edit, apply the test: *would the student be able to re-derive this,
  or would they just have to remember it?* If it's the latter, the explanation is missing.

## The notes standard (agreed 2026-11-27 after the class 7 maths Ch 5 pilot)

A chapter's notes must be **complete on their own** — a student with only these notes gets everything.

1. **No pointers to the book.** Never write "the book", "NCERT", "Example 6", "Fig. 8.13",
   "Activity 10.9", "Exercise 5.2", "selected", or "the rest are similar". Write the content out.
2. **Own words, same facts.** The books are © NCERT ("not to be republished") and the site is
   public: restate questions in your own words, keeping every number, label and condition. No
   verbatim passages, no screenshots of the book. Check each question against the PDF.
3. **Teach concept by concept:** example → idea → rule with its *why* → worked examples, step by step.
4. **Activities become "Try this":** what you need, what to do, what you will see, and why.
5. **Draw a figure wherever one helps** (always for geometry, ray diagrams, circuits, graphs).
   Figures are SVG files drawn from exact coordinates by a script in `tools/figures/`
   (`geo.py` + one `class<N>_<subject>_<ch>.py` per chapter; extend `geo.py` when you need new shapes).
   Every labelled angle/length is asserted against the drawn geometry. Save to
   `assets/img/class<N>/<subject>/<ch>/<name>.svg`, embed with `![alt text](assets/img/...svg)`.
   Look at every figure in the browser pane and compare it with the book's figure before finishing.
6. **Every question is solved, step by step, with the reason for each step.** Worked examples in the
   teaching are shown openly. **Practice questions** ("Check yourself", mid-chapter) and **all
   end-of-chapter questions** ("Exercises — try first") hide their solution in a `> [!ANSWER]`
   block — the page shows it as a **Show answer** button. No end-of-chapter question may be skipped.
7. End with **"In a nutshell"** and a **"Top traps"** warning line.

**Enforced by `python3 tools/check_notes.py`** (all of the above that a script can check: book
pointers, one `[!ANSWER]` per question, question counts against `tools/notes_coverage.json`, images,
figure scripts re-drawing the committed SVGs exactly, nutshell/traps, length). The **pre-commit hook**
(`tools/hooks/pre-commit`) runs it, plus `tools/check_tests.py` for any staged test set, and refuses
the commit on any problem. **Never commit with `--no-verify`**; fix what it reports.

**Soft check against the pilot** (warnings only, never blocks a commit): the checker also measures
each rewritten chapter against the approved pilot for its subject (`PILOTS` in `tools/check_notes.py`;
maths = class 7 Ch 5) — why-explanations, worked examples, callouts, figures, "Try this" activities,
answer length, and how many answers give reasons and steps — and prints `⚠ soft (vs pilot)` when a
measure is under half the pilot's. `--compare <notes file>` shows the full table. Treat each warning as
a prompt to look again, not as a rule: improve the chapter, or record why it is fine in `PLAN.md`.
Science and grammar get their own pilots later. A script can't
judge whether an answer is right or a figure matches the book — check those against the PDF by hand,
and list any differences from the book's answer key in `PLAN.md`.

## Voice

Intuition first — **concrete example → the idea → the general rule** — then the compact
rule. Keep it short and plain, with lots of worked examples and `> [!TIP]` / `> [!NOTE]`
callouts, matching the existing style. Verify any numbers or factor lists before writing
them into the notes.

## Studying a chapter together

When asked to teach a chapter, follow **`HowWeStudy.md`**: teach the chapter in chat → a
self-marking 20-question worksheet (no timer, answers saved) opened in Claude's browser pane →
a 10-question challenge set → log the scores there. Reusable worksheets are in `worksheets/`.
