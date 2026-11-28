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

- **Notes** follow **the notes standard in `CLAUDE.md`**: standalone (no pointers to the book),
  teach the *why*, drawn figures, every question solved step by step, practice and end-of-chapter
  answers behind **Show answer**. Model chapter: `content/class7/math/5.parallel-and-intersecting-lines.md`.
- **Tests**: four levels (Simple, Hard, Harder, Hardest) × 10 questions per chapter, **same file
  names as the notes**. Format at the top of `assets/js/tests.js`. Check with
  `python3 tools/check_tests.py <N>` (or `<N>-science`, `grammar`).
- Science stays **one subject** up to class 10, as in the NCERT book (no physics/chemistry/biology split).
- No other page types (no practice-question sets, cheat sheets, RD Sharma, saved/links tabs).

## To do — rewrite every chapter's notes to the new standard (agreed 2026-11-27)

The class 7 maths Ch 5 pilot was approved, so every other chapter (147 of them) gets the same treatment.
**Each box below is one session.** Do the first unticked box, nothing more.

### How to do one batch (every session)

1. Read `CLAUDE.md` (the notes standard) and the model chapter
   `content/class7/math/5.parallel-and-intersecting-lines.md`. Skim `tools/figures/class7_math_5.py`
   to see how figures are drawn.
2. For each chapter in the batch, extract it from the book PDF (`pdftotext -layout`, see *Learnings*
   for the page offset) **including the answer key at the back**, and render the pages with figures
   (`pdftoppm -r 80 -png`) to look at them.
3. Rewrite the notes file in place (same file name, so manifests and tests stay as they are):
   - keep what is already good in the current notes; remove every pointer to the book;
   - turn activities into "Try this"; draw every needed figure with a new
     `tools/figures/class<N>_<subject>_<ch>.py`;
   - put each in-chapter "Figure it out / Think and answer / Check yourself" set under
     **Check yourself** with `> [!ANSWER]` blocks, and **every** end-of-chapter question under
     **Exercises — try first** with `> [!ANSWER]` blocks; answers step by step with reasons, matching
     the book's answer key (where the key has a slip, trust the text and say so).
4. Add each chapter to `tools/notes_coverage.json` with the book's counts: `check` = in-chapter
   practice questions, `exercises` = end-of-chapter questions (count every lettered part), and a
   `book` note listing them. Then `python3 tools/check_notes.py class<N>/<subject>` must pass (no ✗).
   Read every `⚠ soft (vs pilot)` warning and run `--compare` on the chapter: fix what is genuinely
   thin, and note the rest in the *Done* entry. Open
   `class<N>-<subject>.html` in the browser pane, confirm every figure loads and every Show answer
   opens, and compare each figure with the book's.
5. Tick the box, add learnings, and ask the user before committing.

### Batches

- [x] **Setup: notes checker + pre-commit hook** (2026-11-27). `tools/check_notes.py`,
  `tools/notes_coverage.json`, `tools/hooks/pre-commit`. Starting point (`--survey`): **513 book
  pointers** in 147 old-style chapters — class 5 maths 23, 5 sci 1, 6 maths 31, 6 sci 60, 7 maths 25,
  7 sci 68, 8 maths 6, 8 sci 65, 9 maths 32, 9 sci 97, 10 maths 62, 10 sci 43. (A low count does not mean
  a chapter is done: most old chapters also lack hidden answers and figures.)

### Phase 1 — all maths first (agreed 2026-11-27)

Order: class 7, 8, 6, 9, 10, 5. Besides the hard checks, every maths chapter gets a **soft check against
the pilot**: `python3 tools/check_notes.py` prints `⚠ soft (vs pilot)` warnings, and
`python3 tools/check_notes.py --compare content/class<N>/math/<file>.md` shows the full comparison.
Warnings never block a commit, but look at each one: improve the chapter, or write one line in the
batch's *Done* entry saying why it is fine (e.g. "no figures: a chapter on number patterns").

**Class 7 maths** (*Ganita Prakash* Part 1 + Part 2)
- [x] Ch 5 Parallel and Intersecting Lines — pilot, commit `29069e5`
- [x] Ch 1 Large Numbers Around Us · Ch 2 Arithmetic Expressions · Ch 3 A Peek Beyond the Point (2026-11-27)
- [x] Ch 4 Expressions using Letter-Numbers · Ch 6 Number Play · Ch 8 Working with Fractions (2026-11-27)
- [x] Ch 7 A Tale of Three Intersecting Lines · Ch 9 Geometric Twins (2026-11-27)
- [x] Ch 10 Operations with Integers · Ch 11 Finding Common Ground · Ch 12 Another Peek Beyond the Point (2026-11-27)
- [x] Ch 13 Connecting the Dots… · Ch 15 Finding the Unknown (2026-11-28)
- [x] Ch 14 Constructions and Tilings (2026-11-28)

**Class 8 maths** (*Ganita Prakash* I + II)
- [x] Ch 1 A square and a cube · Ch 2 Power play · Ch 3 A story of numbers (2026-11-28)
- [ ] Ch 4 Quadrilaterals · Ch 9 The Baudhāyana–Pythagoras theorem (figure-heavy)
- [ ] Ch 5 Number play · Ch 6 We distribute, yet things multiply · Ch 7 Proportional reasoning — 1
- [ ] Ch 8 Fractions in disguise · Ch 10 Proportional reasoning — 2 · Ch 13 Algebra play
- [ ] Ch 11 Exploring some geometric themes · Ch 12 Tales by dots and lines · Ch 14 Area

**Class 6 maths** (*Ganita Prakash*)
- [ ] Ch 1 Patterns in mathematics · Ch 3 Number play · Ch 5 Prime time
- [ ] Ch 2 Lines and angles · Ch 8 Playing with constructions (figure-heavy)
- [ ] Ch 4 Data handling and presentation · Ch 6 Perimeter and area · Ch 7 Fractions
- [ ] Ch 9 Symmetry · Ch 10 The other side of zero

**Class 9 maths** (new 8-chapter book; long chapters, two per session)
- [ ] Ch 1 Coordinates · Ch 2 Linear polynomials
- [ ] Ch 3 The world of numbers · Ch 4 Algebraic identities
- [ ] Ch 5 Circles · Ch 6 Perimeter and area (figure-heavy)
- [ ] Ch 7 Probability · Ch 8 Sequences and progressions

**Class 10 maths** (rationalised book — see *Learnings* for dropped topics)
- [ ] Ch 1 Real numbers · Ch 2 Polynomials · Ch 3 Pair of linear equations
- [ ] Ch 4 Quadratic equations · Ch 5 Arithmetic progressions
- [ ] Ch 6 Triangles · Ch 7 Coordinate geometry (figure-heavy)
- [ ] Ch 8 Introduction to trigonometry · Ch 9 Applications of trigonometry (figure-heavy)
- [ ] Ch 10 Circles · Ch 11 Areas related to circles (figure-heavy)
- [ ] Ch 12 Surface areas and volumes · Ch 13 Statistics · Ch 14 Probability

**Class 5 maths** (*Maths Mela*)
- [ ] Ch 1 We the Travellers — I · Ch 2 Fractions · Ch 3 Angles as turns
- [ ] Ch 4 We the Travellers — II · Ch 5 Far and Near · Ch 6 The Dairy Farm
- [ ] Ch 7 Shapes and patterns · Ch 10 Symmetrical designs · Ch 11 Grandmother's quilt (figure-heavy)
- [ ] Ch 8 Weight and capacity · Ch 9 Coconut farm
- [ ] Ch 12 Racing seconds · Ch 13 Animal jumps
- [ ] Ch 14 Maps and locations · Ch 15 Data through pictures

### Phase 2 — science and English (later; plan the details when Phase 1 is done)

Do **not** start these until all maths boxes are ticked. Then, as for maths, first rewrite **one
pilot chapter** per subject, get the user's approval, and add it to `PILOTS` in `tools/check_notes.py`
so the soft check compares against it.

- [ ] **Science pilot:** pick one class 7 science chapter with diagrams (e.g. Ch 11 Light: shadows &
  reflections), rewrite it to the standard, user reviews, then set it as the science pilot.
- [ ] **English grammar pilot:** one grammar lesson rewritten with a Check yourself set; user reviews.

**Class 7 science** (*Curiosity*) — Ch 1 *The Ever-Evolving World of Science* is in the book but
**missing from both the notes and the tests**: write `1.<name>.md` and its 4-level test file and add
both to their manifests (run `python3 tools/check_tests.py 7-science`).
- [ ] Ch 1 The Ever-Evolving World of Science (new notes + test) · Ch 2 Acidic, basic & neutral · Ch 3 Electricity: circuits & components
- [ ] Ch 4 Metals & non-metals · Ch 5 Physical & chemical changes · Ch 6 Adolescence
- [ ] Ch 7 Heat transfer in nature · Ch 8 Measurement of time & motion · Ch 9 Life processes in animals
- [ ] Ch 10 Life processes in plants · Ch 11 Light: shadows & reflections · Ch 12 Earth, Moon & the Sun

**Class 8 science** (*Curiosity*)
- [ ] Ch 1 Investigative world of science · Ch 2 The invisible living world · Ch 3 Health · Ch 4 Electricity — magnetic and heating effects
- [ ] Ch 5 Exploring forces · Ch 6 Pressure, winds, storms and cyclones · Ch 7 Particulate nature of matter
- [ ] Ch 8 Elements, compounds and mixtures · Ch 9 Solutes, solvents and solutions · Ch 10 Light — mirrors and lenses
- [ ] Ch 11 Keeping time with the skies · Ch 12 How nature works in harmony · Ch 13 Our home — Earth

**Class 6 science** (*Curiosity*)
- [ ] Ch 1 The wonderful world of science · Ch 2 Diversity in the living world · Ch 3 Mindful eating
- [ ] Ch 4 Exploring magnets · Ch 5 Measurement of length & motion · Ch 6 Materials around us
- [ ] Ch 7 Temperature & its measurement · Ch 8 States of water · Ch 9 Methods of separation
- [ ] Ch 10 Living creatures · Ch 11 Nature's treasures · Ch 12 Beyond Earth

**Class 9 science** (long chapters, two per session)
- [ ] Ch 1 Exploration · Ch 2 Cell
- [ ] Ch 3 Tissues in action · Ch 4 Describing motion
- [ ] Ch 5 Mixtures and separation · Ch 6 How forces affect motion
- [ ] Ch 7 Work, energy and simple machines · Ch 8 Journey inside the atom
- [ ] Ch 9 Atomic foundations of matter · Ch 10 Sound waves
- [ ] Ch 11 Reproduction · Ch 12 Diversity and classification
- [ ] Ch 13 Earth as a system

**Class 10 science** (long chapters, two per session)
- [ ] Ch 1 Chemical reactions and equations · Ch 2 Acids, bases and salts
- [ ] Ch 3 Metals and non-metals · Ch 4 Carbon and its compounds
- [ ] Ch 5 Life processes · Ch 6 Control and coordination
- [ ] Ch 7 How do organisms reproduce? · Ch 8 Heredity
- [ ] Ch 9 Light — reflection and refraction · Ch 10 The human eye (figure-heavy: ray diagrams)
- [ ] Ch 11 Electricity · Ch 12 Magnetic effects of electric current (circuit and field diagrams)
- [ ] Ch 13 Our environment

**Class 5 science** (*Our Wondrous World*) — this also covers the old *Later* idea of adding the
book's activities and questions.
- [ ] Ch 1 Water · Ch 2 Journey of a river · Ch 3 The mystery of food
- [ ] Ch 4 Our school · Ch 5 Our vibrant country · Ch 6 Some unique places
- [ ] Ch 7 Energy · Ch 8 Clothes
- [ ] Ch 9 Rhythms of nature · Ch 10 Earth — our shared home

**English grammar** (class-free, 21 lessons)
- [ ] Check all lessons against the standard: remove the few pointers to "the book" / NCERT, and add a
  short **Check yourself** set with `[!ANSWER]` blocks to each lesson.

## Later (not agreed yet — ask the user before starting)

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
- 2026-11-27 — Class 7 maths Ch 1, 2, 3 rewritten to the notes standard (99 + 98 + 102 Check-yourself
  answers, 26 + 17 + 35 exercises; 7 + 6 + 16 figures from `tools/figures/class7_math_{1,2,3}.py`).
  Checker passes. Soft warnings looked at and left: no other warnings for Ch 1; Ch 2 and Ch 3 have many
  one-line fill-in answers (blanks, conversions, single sums), so "% answers with steps" (19%, 15%) and
  Ch 3's "avg words per answer" (29) are low; the longer answers do have steps. Answer-key differences
  (trust these notes): Ch 1 Q3 key's 987654312 is wrong (only 123456789 works); Ch 1 Q6(c) the 5000th
  "5" is in 13,495, not 13,995; Ch 1 Q9(a) the largest sum is 99,87,654 + 87,654 = 1,00,75,308 (key
  1,00,54,320); Ch 1 Q10 (c) and (e) key uses cards that don't exist (×4, ×14) — exact answers found
  for (a)–(d), 20,91,000 for (e); Ch 1 Q2 is 61 letters with "lakhs" as in the question's example (key
  60); Ch 1 fact 52,00,00,00,000 ÷ 130 = 4 crore (old notes said 40 crore); Ch 1 Q5 (no two consecutive
  names without a shared letter) has no key answer: none exist. Ch 2 Q2 of "remove brackets" key is
  garbled; Ch 2 end Q4(a) and Figure it Out Q4(b) print the same expression more than once (kept, and
  said so). Ch 3 end Q10 prints 6.18, 6.17 but the pattern and key give 8.18, 8.17. Picture-only
  questions the key doesn't answer (Ch 3 objects measured "two ways", fill-the-boxes line) became a
  Try this / a redrawn figure with our own values; the wire picture uses the key's values.
- 2026-11-27 — Class 7 maths Ch 4, 6, 8 rewritten to the notes standard (59 + 58 + 30 Check-yourself
  answers, 36 + 17 + 23 exercises; 12 + 6 + 21 figures from `tools/figures/class7_math_{4,6,8}.py`).
  Checker passes with no warnings for Ch 4 and Ch 6; Ch 8 keeps "avg words per answer" (33): many
  answers are one-line divisions in the Evaluate table and unit-square products whose figure does the
  explaining. Figures stay below the pilot's rate (number chapters; grids, magic squares and calendars
  are Markdown tables instead). Answer-key differences (trust these notes): Ch 4 Mind-the-Mistake item 4
  key prints the wrong form as "x + 5" (question shows x + y); Ch 4 Q14 vertices: key's 16n + 4 counts each
  square's own corners — notes also give 12n + 4 for touching corners counted once; Ch 6 key's "3779"
  should be 377; Ch 6 end Q2 (50 sheets, sum 6000): key says possible by parity, but each sheet sums to
  4k − 1, so 50 sheets sum to 2 more than a multiple of 4 and 6000 is impossible — notes give both steps;
  Ch 6 Q10(c) is False only because 2p + 1 misses 1 when p starts at 1 (said so); Ch 8 Moon answer is
  2 1/2 hours after 10 pm, i.e. 12:30 am (key garbled); Ch 8 water tank (b) 14/30 = 7/15. The height
  pictures, grids and cryptarithms were solved by trying every case in a script (each has one answer;
  Grid B has two). Ch 6's height arrangements and Ch 8's shaded-square puzzles are our own drawings
  with values matching the key (3/32, 3/8, 1/16; ants 29/32 and 3/32).
- 2026-11-27 — Class 7 maths Ch 7 and Ch 9 rewritten to the notes standard (67 + 19 Check-yourself
  answers, 6 + 19 exercises; 40 + 35 figures from `tools/figures/class7_math_{7,9}.py`). Checker passes
  with no soft warnings for either (Ch 7's construction and third-angle answers were turned into numbered
  steps to get there; its many one-line "longest < sum of the other two" checks stay short). Ch 7 has no
  separate end-of-chapter set: the last Figure it Out (altitudes, right triangles, special triangles) plus
  the shortest-path-in-a-box puzzle are its Exercises. Ch 7 answer key matches; no slips found. Ch 9 is
  Part 2 Ch 1 and **Part 2 prints no answer key**, so every answer was worked out here (the 6-congruent-
  regions puzzle by trying all tetrominoes in a script: only the L-shape works). Picture-only questions
  (bent figures, look-alike pairs, branch figures) are redrawn with our own shapes and values; the big
  "find the missing angles" figure became six small figures (a)-(f) using the same angles (68°, 34°, 90°,
  60°, 44°, 34°/56°). Ch 9's "Are ∆DFE and ∆GED congruent?": the triangles are, but the naming must be
  ∆DFE ≅ ∆DGE — the notes say both.
- 2026-11-27 — Class 7 maths Ch 10, 11, 12 rewritten to the notes standard (40 + 67 + 73 Check-yourself
  answers, 41 + 19 + 27 exercises; 11 + 6 + 6 figures from `tools/figures/class7_math_{10,11,12}.py`:
  number-line jumps, token bags, factor tree, Venn of primes, star rows, 1 ÷ 7 remainder cycle, leap-year
  rule). Checker passes; the only soft warning is Ch 12 "avg words per answer" (36): many one-line
  conversions (× 10 tables, unit blanks, decimal-place counts), as in Ch 3 and Ch 8. Figures stay below the
  pilot's rate (number chapters; ladders and long divisions are code blocks). Part 2 has **no answer key**, so
  every answer was worked out here and checked by script. Slips in the old notes, now fixed: Ch 10 Q15 minimum
  is −60 ((−6) × (5 + (3 − (−2)))), not −55; Machine 2 (never solved before) is −(a × b) − c → −111; the Q7
  machine is a − b × c → −70. Book quirks (said so in the notes): Ch 10 Q11 (b), (c) are fractions (4/81,
  20/81), not integers; Ch 10 the "play the same game with the grid below" grid is the same grid; Ch 10 Q6(b)
  assumes Anil sat Anita's 25-question test (5 unanswered); Ch 12 FIO Q2(b) prints options (i) and (iv) the
  same; Ch 12 end Q8 (f) repeats (b); Ch 12 Q10 "nearest to 5" is 9.16 because no product is smaller.
  Answers that never end (24.86 ÷ 1.2, 5.728 ÷ 1.52, 234.45 ÷ 12.6, 60 1/4 ÷ 3 1/2) are given to a few places
  with the reason. Ch 11's Mystery Colours page became a Try this; Ch 12's Hidato puzzle page is left out.
- 2026-11-28 — Class 7 maths Ch 13 and Ch 15 rewritten to the notes standard (58 + 58 Check-yourself
  answers, 25 + 37 exercises; 22 + 27 figures from `tools/figures/class7_math_{13,15}.py`). Checker passes;
  no soft warnings for Ch 15. Ch 13 keeps "figures /1000 words" (1.5): a long data chapter whose data lives in
  tables (onion prices, the 15-row height survey) rather than pictures; it still has 22 dot plots and bar
  graphs. Part 2 has **no answer key**, so every answer was worked out and checked by script. Slips and quirks
  (said so where they matter): Ch 13 Shubman's mean is 110 ÷ 5 = 22, not 21; the Grade 5 class mean is
  4046 ÷ 28 = 144.5 (printed 144.4); the runs-per-over graph's bars don't add up to a finished match (Red stops
  at over 18 with 152 against Blue's 163), so it is redrawn with our own consistent match; Ex Q5 (17 heights):
  five students are exactly 115 cm, so "shorter/taller than one height" cannot split 8/8 (old notes said it
  could). Graphs from published charts (rockets, animal speeds, skyscrapers, EVs) are redrawn with values read
  off them and labelled approximate; the "1 minute" and School A/B dot plots became tables of their printed
  summaries. Lock puzzle checked by brute force (only 415). Ch 15 Example 3 prints 135 in the question and 132
  in the working (135 is right: the answer 7024 needs it); window grill (Ex Q8) assumes the bottom frame is 3 cm
  like the top (as drawn), giving 6 gaps of 3 cm; the maze path visits 11 of 12 boxes (−7 = 11 − 3x is a
  decoy) and ends in 30 = 4 − 50n, n = −13/25; staircase sticks are 9n + 4 (counted from the drawing).
  Mobiles and sack balances are redrawn with our own shapes and the same numbers.
- 2026-11-28 — Class 7 maths Ch 14 rewritten to the notes standard (38 Check-yourself answers, 10 exercises;
  46 figures from `tools/figures/class7_math_14.py`). Checker passes with **no soft warnings**. Every
  construction in the script is done with exact circle meeting points and its result asserted (90°, halves,
  copied angles, parallels); tilings come from a search. Part 2 has **no answer key**. Choices made: the tangram
  silhouettes (picture-only, many answers) are a Try this with tips; the 8-pointed star (p148) is read as eight
  rhombuses round the centre, so it is built with the parallel-line construction its section teaches; the
  compass-only flower uses petals centred on the six circle points (the half-circle look needs a ruler for
  midpoints); 65.5° is shown impossible because every constructible angle, doubled enough, is a multiple of 15.
  Brute force: removing any of the 7 "black" squares of a 5 × 3 grid makes it untileable, any of the 8 "white"
  squares leaves it tileable. The old notes' book-pointer lines ("Book Figure it Out") are gone.
- 2026-11-28 — Class 8 maths Ch 1, 2, 3 rewritten to the notes standard (44 + 101 + 77 Check-yourself
  answers, 11 + 34 + 4 exercises; 15 + 10 + 27 figures from `tools/figures/class8_math_{1,2,3}.py`). Checker
  passes; no soft warnings for Ch 1. Ch 2 keeps "avg words per answer" (33) and "% answers with steps" (18%), Ch 3
  keeps "% answers with steps" (26%): both have many one-line drills (write in exponential form, read a power line,
  name a product of two landmark symbols) where a list of steps would be padding; the longer answers have steps.
  Ch 1 and Ch 3 have no separate end set: Ch 1's last Figure it Out + the Square Pairs puzzle are its Exercises,
  Ch 3's last Figure it Out (4 questions) is. Answer-key differences and quirks (trust these notes): Ch 1 key has no
  answer for Q9 (tiny squares): the picture is 9 × 9 tiles of 5 × 5, so 2025 = 3⁴ × 5² = 45²; Square Pairs checked
  by brute force (1-17 in a row: only one order and its reverse; 1-32 in a circle: exactly one). Ch 2 key Q12 gives
  only (vi) 10⁹ + 10⁹, but (v) 2 × 10⁹ is the same number, so both are right; the old notes had 70,04,00,00,000 =
  7.004 × 10⁹ (it has 11 digits: 10¹⁰, as the key says); key's 172 expansion has a "+" for "×" typo. Ch 2's
  estimation questions are answered with stated assumptions (coin 4 g, walking 5 km/h, etc.); the age and
  billion-seconds answers count back from 28 November 2026 and say so. Ch 3 text writes 2367 as MMCCCLXII, which is
  2362 (its own sum gives MMCCCLXVII). Ch 3's picture numerals (Egyptian 276, 4322, 9608 + 507, 1080 + 46, 522 × 10,
  1010 × 10; the base-5 sum 182 + 412) are redrawn with our own simplified symbols and the same values; our base-5
  symbols are ▲ ■ ◆ ● ★ ✚ (the base-4 example uses · ✦ ⬟ so the two systems don't share symbols).

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
- `geo.py` `Fig.text()` only keeps the anchor point inside the picture, so long labels get clipped;
  new scripts use `Fig.label()` (same look, width-aware). `text()` is unchanged so the pilot's SVGs still match.
- Class 7 Part 1 PDF: book page = PDF page − 18 for Ch 1 (Ch 1 text PDF 19–41, its answers 42–56;
  Ch 2 text 57–78, answers 79–96; Ch 3 text 97–131, answers 132–151; Ch 4 starts at 152). Each chapter's
  answer key sits right after the chapter, not at the back of the book.
- `pdftotext -layout` scrambles stacked fractions (Ch 3); read the answer key and zoom on the page
  image (`pdftoppm -r 150 -x … -y … -W … -H …`) for number lines and pictures.
- A `> [!ANSWER]` outside a `### Check yourself` / `## Exercises` section is not counted by the checker;
  after writing, list answers outside sections (see how Ch 1's estimates were caught) before setting counts.
- Python's `http.server` (the `static` preview) sometimes drops parallel fetches; reload the page if it
  says "Couldn't load this page".
- The answer keys printed in NCERT books sometimes have slips (e.g. class 9 science Ch 2 Q11) —
  trust the chapter text and say so in the notes.
- Class 7 Part 1 PDF pages: Ch 4 text 152–176, answers 177–192; Ch 6 text 227–245, answers 246–258;
  Ch 8 text 293–319, answers 323–331 (book page = PDF page − 120 for Ch 8).
- The checker ends a Check-yourself section at the next `###` heading: a sub-heading such as "Mind the
  mistake" must itself be called `### Check yourself: …`, or its answers are not counted.
- "for example 5" trips the book-example check; write "for instance" or "say" before a number.
- A quick way to look at a new script's figures: write a throwaway HTML page listing the SVGs, open it
  in the `static` preview, then delete it (plain `rm` may be blocked; `python3 -c "import os; os.remove(…)"` works).
- `geo.py` now has `circle()`, `carc()` (compass arcs) and `ticks()` (equal-side marks); the older chapters'
  SVGs are unchanged. `class7_math_7.py` / `_9.py` have `sss()`, `asa()`, `side()` (width-aware length
  labels) and `eq_ticks()` (asserts ticked sides really are equal) — copy them for later geometry chapters.
- Class 7 Part 1 PDF: Ch 7 text 259–285, answers 286–292. Part 2 PDF: Ch 1 (site Ch 9) text 19–41; Part 2
  has **no answer key**, so solve and double-check everything for site Ch 9–15.
- In a Check-yourself section, a question stem followed by parts (a), (b) must not start with `**4.**`
  (the checker then wants its own answer); write `**Question 4.**` instead.
- Class 7 Part 2 PDF: book page = PDF page − 18. Ch 2 (site Ch 10) text 42–64, Ch 3 (site 11) 65–84,
  Ch 4 (site 12) 85–114 (the Hidato page is 113–114). Picture-only data (pattern machines, star rows, arrow
  number lines) needs `pdftoppm` — `pdftotext` drops it.
- Token figures: `class7_math_10.py` has `token()` (green/red, crossed = taken out), `rounds_fig()` (bag
  pictures that assert tokens left = product) and `jump()` (flat number-line arcs) — reuse for integers in
  other classes. A figure can sit inside a `> [!ANSWER]` block (`> ![alt](…)`); it renders and is counted.
- Class 7 Part 2 PDF: Ch 5 (site Ch 13) text PDF 115–152, lock puzzle 153; Ch 7 (site Ch 15) text 182–208.
  Ch 13's data is mostly in pictures (dot plots, graphs, the stories cards): render with `pdftoppm` and read
  values off the zoomed image; redraw charts with our own figures rather than copying them.
- `class7_math_13.py` has reusable `dotplot()` (stacked dots + mean/median lines), `vbars()` (clustered
  vertical bars with legend) and `hbars()` (clustered horizontal bars) — copy them for any data chapter.
  `class7_math_15.py` has `mobile()` / `balance()` (assert the drawn puzzle balances with the solved weights)
  and edge-counting for stick patterns (`cell_edges`), so a stick-count formula is checked against the drawing.
- A question in a section without a `### Check yourself…` heading (e.g. under "### Doing the same to both
  sides") is not counted: add a `### Check yourself: …` heading right before it.
- `**Worked example 7**` trips the book-example check; number our own as `**Example 7: title.**`.
- Class 7 Part 2 PDF: Ch 6 (site Ch 14) text PDF 154–181 (book page = PDF page − 18). `class7_math_14.py` has
  `inter()` (two circles' meeting points), `tick_arc()` (a short compass mark through a point), `bisect()`,
  `tile()` (finds a tiling of a cell set by a list of tile shapes) and `draw_tiles()` — reuse for class 6 Ch 8
  constructions and any tiling questions.

- Class 8 Part 1 PDF: book page = PDF page − 16. Ch 1 text PDF 17–34, answers 35–38; Ch 2 text 39–67, answers
  68–76; Ch 3 text 77–110, answers 111–122; Ch 4 starts at 123. Each answer key sits right after its chapter.
- `tools/notes_coverage.json` keeps one entry per line (and already has a few duplicate class 7 keys). Never
  rewrite it with `json.dump` (it reflows the file and drops the duplicates); insert or replace the one line.
- Unicode shapes render at very different sizes in the site font (△ ⬡ ∿ come out tiny next to ○); the filled
  ▲ ■ ◆ ● ★ ✚ look even. Check any symbol-heavy text in the browser pane.
- Reusable drawers: `class8_math_1.py` `cube()` (oblique n × n × n cube with grid lines) and `tri_sq()` (square of
  dots cut by a staircase); `class8_math_2.py` `power_line()` (exact fractions) and `indian()` (Indian commas);
  `class8_math_3.py` `eg_number()` (Egyptian), `meso_number()` (base 60, blanks or placeholder), `maya_number()`,
  `rod_number()`, `abacus()`, each asserting the drawn symbols add up to the value, and `shift()` to place a
  sub-figure inside a bigger one.
- A Check-yourself question line can carry its picture: `**(i)** ![alt](…)` is still counted as a question.
