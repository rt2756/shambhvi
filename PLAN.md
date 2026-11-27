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

- [ ] **Class 10 maths tests.** The notes are **done** (14 chapters in `content/class10/math/`, listed in
  its `manifest.json`; uncommitted). Write `content/class10/tests/<same name>.json` for each of the
  14 chapters (`1.real-numbers.json` … `14.probability.json`) plus `manifest.json` in the same order.
  Reuse good questions from the old 19 test files and `content/class10/math-questions/*.md`
  (the book's answer key at the back of `ncert_books/class_10/maths.pdf` helps), then delete the old
  test files not in the new manifest and the whole `content/class10/math-questions/` folder.
  Run `python3 tools/check_tests.py 10` until it passes; check `class10-tests.html` loads.
- [ ] **Commit class 5 and class 10 maths** together with `PLAN.md` and the `CLAUDE.md` change
  (ask the user first).

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
- 2026-11-27 — Class 5 maths (15 chapters of *Maths Mela*, 600 Qs, checker passes). **Not committed yet.**
- 2026-11-27 — Class 10 maths **notes** (14 chapters, 2,300–4,000 words each; cheat-sheet link removed).
  **Not committed yet**; tests still to do (see *To do*).

## Learnings

- Always check the chapter list against the PDF in `ncert_books/class_<N>/` — books changed a lot.
  Class 9 maths is the **new 8-chapter book** (not the old 12); classes 6–8 maths are *Ganita Prakash*.
- `pdftotext -f A -l B book.pdf -` extracts pages; contents pages list book page numbers, so find the
  PDF offset first (book page 1 is usually PDF page 13–21).
- If plain `rm` is blocked by permissions, `git rm` works for tracked files.
- After a rewrite, check that no old files remain: every `.md` / `.json` in the folder should be in
  its `manifest.json`.
- The answer keys printed in NCERT books sometimes have slips (e.g. class 9 science Ch 2 Q11) —
  trust the chapter text and say so in the notes.
