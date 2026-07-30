# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this repo is

CBSE / NCERT **revision notes and practice questions** for a school student — maths and
science, **bucketed by class (5–10)**. Plain Markdown in `content/class<N>/math/*.md` and
`content/class<N>/science/*.md` (notes), `content/class7/*-questions/*.md` (practice
questions), rendered in the browser and published via GitHub Pages. See `README.md` for the
full file map, callout syntax, and how rendering works.

**Class 7 is the live one** — it has full notes plus a question set for every chapter.
Classes 5, 6, 8, 9 and 10 currently hold only `0.syllabus.md`, a verified chapter map of
the year; fill them in one chapter at a time, matching the class-7 depth.

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
