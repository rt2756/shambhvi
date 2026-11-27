# Learning Hub — Class 2–10

CBSE / NCERT revision, **bucketed by class (5–10)**. Every class has the same three subjects —
**Maths, Science and English** — and each subject has exactly **two tabs: 📘 Notes** (detailed,
chapter-by-chapter teaching that follows the NCERT book) **and 🎯 Tests** (four self-marking
levels per chapter, on the same chapter list). Plus class-free vocabulary, music and a to-do list. The **content lives in plain
Markdown files**, one per chapter; the page fetches them and renders collapsible sections
in the browser. No build step, no Jekyll — published with **GitHub Pages**.

Science follows the NCERT book as one subject up to class 10 (NCERT only splits it into
physics, chemistry and biology from class 11). English is the grammar course, filtered to the
lessons each class is taught.

## Writing principle — always explain *why*, never just *how*

These notes teach for **understanding, not memorisation**. Every rule, step, shortcut, or
formula must come with the **reason it works** — right beside it, or linked from it. The
test: *would the student be able to **re-derive** the step, or would they just have to
**remember** it?* If it's the latter, the "why" is missing and the note isn't finished.

- ✅ **Do:** state the rule, then a **`**Why it works:**`** line explaining the idea behind
  it (see the multiply/divide sign rule and the factor count-check in `content/class7/math/1.numbers.md`).
- ❌ **Don't:** drop in a recipe like "add 1 to each power and multiply" with no reason —
  that's just one more thing to memorise.

Worked examples, `> [!TIP]` callouts, and "Why it works" lines exist for exactly this. A
concept with no explanation anywhere in the notes is treated as unfinished.

## Files

Content is bucketed **by class** (5–10); vocabulary and the to-do list are class-free and live at the top level.

| Path | What it is |
|---|---|
| `content/class<N>/math/*.md` | Maths notes for class N — one Markdown file per chapter. **Edit these.** |
| `content/class<N>/science/*.md` | Science notes for class N (class 5's is *The World Around Us*). |
| `content/class<N>/<subject>/manifest.json` | The ordered list of files to show in that panel stack. |
| `content/class<N>/<subject>/0.syllabus.md` | The chapter map for the year — every class has one, written from the NCERT book. |
| `content/class<N>/tests/*.json` · `content/class<N>/science-tests/*.json` | Maths and science **tests** — one file per chapter, **same file names as the notes**. |
| `content/vocab/` · `content/math-todo/` | Class-free: word power, and the tables/squares/cubes checklist. |
| `content/grammar/notes/*.md` · `content/grammar/tests/*.json` | Class-free **English grammar**: 21 lessons (CBSE / NCERT classes 5–10, mapped in `0.syllabus.md`) + four tests per lesson. Each class's English tab shows only its lessons, listed in `manifest-class<N>.json` in both folders (pages `class<N>-english.html`, `class<N>-english-tests.html`, via `data-manifest`). The full set is on `grammar.html`, `grammar-tests.html`. |
| `content/music/notes/*.md` · `content/music/practice/*.md` · `content/music/tests/*.json` | Class-free **music theory + electric-guitar practice**: theory lessons (map in `0.syllabus.md`), a week-by-week 30-min practice plan with tick-off days (`data-mode="todo"`), and four tests per lesson. Pages: `music.html`, `guitar-practice.html`, `music-tests.html`. Check with `python3 tools/check_tests.py music`. |
| `little.html` · `assets/js/little.js` · `content/little/*.json` | **Little Learners** (ages 4–6, pre-school → Class 1): 24 topics × 3 rounds × 5 tap-the-picture questions, read aloud, plus grown-up notes (with the *why*) and spoken questions. Edit `tools/build_little.py`, then run it and `python3 tools/check_little.py`. |
| `say-along.html` · `assets/js/say-along.js` · `assets/js/words-data.js` | **Say-along** (part of Little Learners): one big item at a time, read aloud, then it flies to its place on a board (hundred chart, A–Z / वर्णमाला chart, tables side by side, week / year). Seven modes: counting (from / to / up or down / count by 1s 2s 5s 10s / digits-then-number / with the English number name), the alphabet (A for Apple…), times tables 1–20 (“six twos are twelve”), **वर्णमाला** and **गिनती 1–100** read in Hindi (needs a Hindi voice on the device), days & months, and **🖼️ Picture words** — 25 topics, 347 words a child should know before Class 1 (body, wild / farm / water animals, birds, insects, fruits, vegetables, food, plants, vehicles, shapes, colours, clothes, home, kitchen, school, weather, helpers, feelings, actions, good habits, festivals, Our India, instruments), each with a one-line “what it is” and an optional Hindi word; data in `assets/js/words-data.js`, cards on `little.html`. Each has 👩‍🏫 Teach me and 🙋 Ask me (👀 Show answer reveals). Slow → very fast; space = play/pause, ← → = step. All data is in the JS file. |
| `index.html` | **Home** — the class picker (2–10) plus the class-free sections. |
| `class<N>-math.html` · `class<N>-tests.html` | Maths **Notes** and **Tests** for class N (5–10). |
| `class<N>-science.html` · `class<N>-science-tests.html` | Science **Notes** and **Tests** for class N. |
| `class<N>-english.html` · `class<N>-english-tests.html` | English (grammar) **Notes** and **Tests** for class N. |
| `test.html` | The one page that runs any test (see *Chapter tests* below). |
| `class<N>-science-tests.html` · `content/class<N>/science-tests/*.json` | **Science chapter tests** (classes 3–10; classes 3–4 follow NCERT *Our Wondrous World*, classes 1–2 have no EVS book) — same four-level format, one file per science chapter. |
| `assets/js/tests.js` · `tools/check_tests.py` | The test engine, and the script that re-checks every answer key. |
| `questions.html` · `science.html` · `science-questions.html` · `saved.html` · `links.html` | Redirect stubs kept so old bookmarks still work. |
| `assets/js/app.js` | Loads a manifest + `.md` files and builds the page; one engine drives every layout (chosen by `#app`'s `data-mode`). |
| `assets/js/marked.min.js` | The Markdown parser (vendored — `marked` v12.0.2). |
| `assets/css/style.css` | All the styling, in one commented stylesheet. |
| `assets/js/theme.js` | Light / dark mode for every page: loaded in each page's `<head>`, follows the device setting until 🌙 / ☀️ (next to the page links) is pressed, then remembers it. Dark colours are the `html[data-theme="dark"]` block at the end of `style.css` — use the colour variables (`var(--card)` etc.), not `#fff`, so new styles get a dark version for free. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is (no Jekyll). |

### Adding a class page

Everything is driven by `data-content-dir` on the `#app` div — to add, say, class 6 maths notes, drop
`content/class6/math/1.patterns.md`, add it to that folder's `manifest.json`, and it appears on
`class6-math.html`. No new HTML needed.

## Editing notes

Just edit the Markdown in `content/class7/math/`. The first `#` heading in a file is the topic
title shown on the collapsible panel; use `##` for sub-topics, `-` for bullets, `**bold**`
for emphasis. Save and reload — the change shows up, and `git diff` shows a clean,
readable delta.

### Coloured callout boxes

Write them as GitHub-style alerts (these also render as proper boxes when you view the
`.md` on github.com):

```markdown
> [!TIP]
> A handy tip.

> [!WARNING]
> The ⚠️ common-mistakes line.
```

| You write | You get |
|---|---|
| `> [!TIP]` | 💡 green tip box |
| `> [!WARNING]` or `> [!CAUTION]` | ⚠️ red "common mistakes" box |
| `> [!NOTE]` | 📘 blue note box |
| `> [!IMPORTANT]` | 📝 purple example box |

### Adding a new topic

1. Create `content/class7/math/<topic>.md` starting with a `# Title` line.
2. Add `"<topic>.md"` to `content/class7/math/manifest.json` (the order there is the page order).

## Chapter tests

**Four tests per chapter — 🟢 Simple, 🟡 Hard, 🟠 Harder, 🔴 Hardest — 10 questions each, 1 mark
each.** The student answers, presses **Submit**, and only then sees the marks, the right answer
and a one-line *why* for every question. Answers save as she goes; the score is remembered and
shown on the hub.

How it is organised (the same three pieces for every class):

| Piece | File | What it does |
|---|---|---|
| Hub | `class<N>-tests.html` | One row per chapter, four level buttons, saved scores. |
| Runner | `test.html?c=<N>&f=<chapter>&t=<1–4>` | One shared page that runs any test. |
| Data | `content/class<N>/tests/<n>.<chapter>.json` + `manifest.json` | One file per chapter, holding its four tests. |

Every class from 2 to 10 has tests. For classes 5–10 the maths and science tests use **exactly
the same chapter list as the notes** (the current NCERT book), with the same file names. Classes
2–4 follow the current NCERT books (class 2: *Joyful Mathematics*; classes 3 and 4: *Maths Mela*)
and have tests only (no notes yet); their home cards open the tests page directly. The questions are our own, written in the
style of the source — not copied.

A question is multiple choice or a number answer:

```json
{"t": "Find (−7) × 6.", "o": ["−42", "42", "−13", "−1"], "e": "why…", "k": "-7*6"}
{"t": "Find 12 − (−5).", "n": 17, "u": "cm", "e": "why…", "k": "12-(-5)"}
```

- **`o`** — the options, with the **right answer always first**. The page shuffles them (the same
  way each visit), so there is no answer letter to keep in step.
- **`n`** — a number answer (`u` is an optional unit shown beside the box). `3/4` typed by the
  student is accepted for `0.75`.
- **`e`** — the explanation shown after Submit. Every question needs one (the *why* rule).
- **`k`** — optional: a formula for the answer. `python3 tools/check_tests.py` works out every
  `k` and compares it with the key, and also checks each file has 4 tests × 10 questions.
  **Run it after any edit.**

**Class-free test sets.** A set can also be a name instead of a class number: `content/grammar/tests/`
is run as `test.html?c=grammar&f=…`, its hub is `grammar-tests.html` (`data-class="grammar"`), and
`python3 tools/check_tests.py grammar` checks it. To add another set, give it a label in `SET_NAMES`
in `assets/js/tests.js`.

**Science test sets.** Each class's science tests are the set `<N>-science`: data in
`content/class<N>/science-tests/` (manifest lists the chapter files, matching the science notes'
file names), run as `test.html?c=<N>-science&f=…`, hub `class<N>-science-tests.html`
(`data-class="<N>-science"`, the 🧫 Sci Tests tab), checked with `python3 tools/check_tests.py <N>-science`.

To add a class: create `content/class<N>/tests/` with chapter files and a `manifest.json`, copy
`class7-tests.html` to `class<N>-tests.html`, and change `data-class`.

## Local preview

The notes load from separate files, so you need a tiny local server — **double-clicking
`index.html` won't work** (browsers block reading local files over `file://`). From the
repo root:

    python3 -m http.server

then open <http://localhost:8000>.

## Published site

Served by GitHub Pages from `main` / root: <https://rt2756.github.io/shambhvi/>.
