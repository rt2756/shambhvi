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

Nothing left — every class 5–10 has notes and tests for Maths, Science and English. Ask the user
before starting anything under *Later*.

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
- If plain `rm` is blocked by permissions, `git rm` works for tracked files.
- After a rewrite, check that no old files remain: every `.md` / `.json` in the folder should be in
  its `manifest.json`.
- Class 10 maths rationalised book drops: Euclid's lemma + decimal expansions (Ch 1), division algorithm
  (Ch 2), cross-multiplication + equations reducible to linear (Ch 3), areas of similar triangles +
  Pythagoras proofs (Ch 6), area of a triangle + centroid (Ch 7), complementary-angle ratios (Ch 8),
  melting/recasting + frustums (Ch 12), ogives (Ch 13). Keep tests clear of these.
- The answer keys printed in NCERT books sometimes have slips (e.g. class 9 science Ch 2 Q11) —
  trust the chapter text and say so in the notes.
