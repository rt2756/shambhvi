# Plan — Notes + Tests for classes 5–10

**Read this first in every new session.** Pick the first item under *To do*, do it, then update this
file: tick the item, move it to *Done* with the date and commit, and add anything a later session
must know to *Learnings* (short — only what isn't obvious from the code).

## How we work

- **One session, one item, one at a time.** Don't start parallel or child sessions — running several
  at once burns the usage limit fast and they all stop half-way.
- Keep the session small: read this file, `CLAUDE.md`, and only the files for your item.
- Commit only when the user says so (see the global rule). Never touch another class's files.

## The goal (agreed 2026-11-26)

Every class 5–10 has three subjects — **Maths, Science, English** — and each subject has exactly two
things on **one chapter list taken from the current NCERT book**:

| | Notes | Tests |
|---|---|---|
| Maths | `content/class<N>/math/*.md` | `content/class<N>/tests/*.json` |
| Science | `content/class<N>/science/*.md` | `content/class<N>/science-tests/*.json` |
| English | `content/grammar/notes/` via `manifest-class<N>.json` | `content/grammar/tests/` via `manifest-class<N>.json` |

- **Notes** teach like a patient tutor explaining to a child: example → idea → rule, the *why* for
  every rule, the book's activities and questions worked, callouts, "In a nutshell", a final
  "Top traps" line. About 2,000–3,500 words per chapter. Style model: `content/class6/science/*.md`.
- **Tests**: four levels (Simple, Hard, Harder, Hardest) × 10 questions per chapter, **same file
  names as the notes**. Format at the top of `assets/js/tests.js`. Check with
  `python3 tools/check_tests.py <N>` (or `<N>-science`, `grammar`).
- Science stays **one subject** up to class 10, as in the NCERT book (no physics/chemistry/biology split).
- No other page types (no practice-question sets, cheat sheets, RD Sharma, saved/links tabs).

## To do

- [ ] **User reviews the pilot:** class 7 maths Ch 5 (*Parallel and Intersecting Lines*), rewritten to
  the new notes standard below, with 49 drawn figures. Wait for approval or changes before rolling out.
- [ ] **After approval:** write the standard into `CLAUDE.md`, add a notes checker (flags "the book",
  "Fig. 5.3", "Activity 2", "selected", "similar", and exercise questions with no hidden answer), then
  roll out one subject per session: class 7 maths, 7 science, then 8, 6, 9, 10, 5.

### New notes standard (pilot, agreed in principle 2026-11-27)

1. **Standalone.** No "the book", "Example 6", "Fig. 8.13", "Activity 10.9". Anything from the book is
   written out in full, in our own words (same numbers and facts; the book is © NCERT, so no verbatim
   copying or screenshots on the public site).
2. **Teach concept by concept:** concrete example → idea → rule with its *why* → worked examples, step by step.
3. **Activities become "Try this":** what you need, what to do, what you see, why it happens.
4. **Draw a figure wherever one is needed** (always for geometry). Figures are SVGs drawn from exact
   coordinates by a script in `tools/figures/` (see `class7_math_5.py`); every angle label is
   asserted against the drawn geometry. Compare each with the book's figure before finishing.
5. **Every question is solved, step by step, with reasons.** Teaching examples are shown openly; every
   practice question ("Check yourself") and every end-of-chapter question ("Exercises — try first")
   hides its solution in a `> [!ANSWER]` block, which the notes page shows as a **Show answer** button.
6. Ends with "In a nutshell" and a "Top traps" line, as before.

## Later (not agreed yet — ask the user before starting)

- Class 5 science: add the book's activities and worked questions, like classes 6–10.
- Classes 2–4: notes to go with the existing tests.

## Done

- 2026-11-26 — Page layout: six tabs per class 5–10 (Maths, Maths Tests, Science, Science Tests,
  English, English Tests); extra pages removed. Commit `1dda33d`.
- 2026-11-26 — Science notes deepened from the book: class 6 (`7e11681`), 7 (`dfcae04`), 8 (`02c1639`),
  9 (`1e9fbba`), 10 (`e3c653f`). Science tests for 3–10: `c36aaea`.
- 2026-11-27 — Class 6 maths (10 chapters, 400 Qs) and class 7 maths (15 chapters, 600 Qs) from
  *Ganita Prakash*. Commit `7c66921`.
- 2026-11-27 — Class 8 maths (14 chapters, 560 Qs, *Ganita Prakash* I + II) and class 9 maths
  (8 chapters, 320 Qs, new book). Commit `8f2157a`.
- 2026-11-27 — Class 5 maths (15 chapters of *Maths Mela*, 600 Qs, checker passes). Commit `6598e0e`.
- 2026-11-27 — Class 10 maths **notes** (14 chapters, 2,300–4,000 words each; cheat-sheet link removed). Commit `6598e0e`.
- 2026-11-27 — Class 10 maths **tests** (14 chapters, 560 Qs, checker passes; ~75% reused from the old
  19 files, out-of-syllabus ones replaced). Old test files and `content/class10/math-questions/` removed.
  Commit `9062054`, merged to `main`.

## Learnings

- Always check the chapter list against the PDF in `ncert_books/class_<N>/` — books changed a lot.
  Class 9 maths is the **new 8-chapter book** (not the old 12); classes 6–8 maths are *Ganita Prakash*.
- `pdftotext -f A -l B book.pdf -` extracts pages; contents pages list book page numbers, so find the
  PDF offset first (book page 1 is usually PDF page 13–21).
- Notes pages turn `> [!ANSWER]` blocks into Show answer buttons (`assets/js/app.js`, notes mode).
  Images go in as `![alt](assets/img/class<N>/<subject>/<chapter>/<name>.svg)`; the page gives them a
  white card, so they read fine in dark mode.
- If plain `rm` is blocked by permissions, `git rm` works for tracked files.
- After a rewrite, check that no old files remain: every `.md` / `.json` in the folder should be in
  its `manifest.json`.
- Class 10 maths rationalised book drops: Euclid's lemma + decimal expansions (Ch 1), division algorithm
  (Ch 2), cross-multiplication + equations reducible to linear (Ch 3), areas of similar triangles +
  Pythagoras proofs (Ch 6), area of a triangle + centroid (Ch 7), complementary-angle ratios (Ch 8),
  melting/recasting + frustums (Ch 12), ogives (Ch 13). Keep tests clear of these.
- The answer keys printed in NCERT books sometimes have slips (e.g. class 9 science Ch 2 Q11) —
  trust the chapter text and say so in the notes.
