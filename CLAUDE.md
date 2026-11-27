# CLAUDE.md

Guidance for AI assistants working in this repository.

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
tutor would explain it to a child (style model: `content/class6/science/*.md`).

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

- Pair each rule with a **`**Why it works:**`** explanation. This repo already uses that
  pattern — see the multiply/divide sign rule and the factor **count-check** in
  `content/class7/math/1.numbers.md`.
- If the "why" is long, it can live nearby or in a linked section — but it must exist
  **somewhere** in the notes, not only in the student's memory.
- Before finishing any edit, apply the test: *would the student be able to re-derive this,
  or would they just have to remember it?* If it's the latter, the explanation is missing.

## Voice

Intuition first — **concrete example → the idea → the general rule** — then the compact
rule. Keep it short and plain, with lots of worked examples and `> [!TIP]` / `> [!NOTE]`
callouts, matching the existing style. Verify any numbers or factor lists before writing
them into the notes.

## Studying a chapter together

When asked to teach a chapter, follow **`HowWeStudy.md`**: teach the chapter in chat → a
self-marking 20-question worksheet (no timer, answers saved) opened in Claude's browser pane →
a 10-question challenge set → log the scores there. Reusable worksheets are in `worksheets/`.
