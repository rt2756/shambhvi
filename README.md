# Learning Hub — Class 5–10

CBSE / NCERT revision notes and practice questions, **bucketed by class (5–10)** for maths
and science, plus class-free vocabulary and a to-do list. The **content lives in plain
Markdown files**, one per chapter; the page fetches them and renders collapsible sections
in the browser. No build step, no Jekyll — published with **GitHub Pages**.

**Class 7 is the deep one** (full notes + ~448 maths questions + science). The other classes
currently hold a **syllabus map** — the full chapter list of the year, taken from the NCERT
book — ready to be filled in chapter by chapter.

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
| `content/class7/math-questions/*.md` · `science-questions/*.md` | Class 7 practice questions, same chapter numbering as its notes. |
| `content/class7/saved/` · `content/class7/links/` | The tricky-questions notebook and the reference links. |
| `content/vocab/` · `content/math-todo/` | Class-free: word power, and the tables/squares/cubes checklist. |
| `index.html` | **Home** — the class picker (5–10) plus the class-free sections. |
| `class<N>-math.html` · `class<N>-science.html` | One page per class per subject. |
| `class7-math-questions.html` · `class7-science-questions.html` · `class7-saved.html` · `class7-links.html` | The extra class-7 pages. |
| `questions.html` · `science.html` · `saved.html` · `links.html` | Redirect stubs kept so old bookmarks still work. |
| `assets/js/app.js` | Loads a manifest + `.md` files and builds the page; one engine drives every layout (chosen by `#app`'s `data-mode`). |
| `assets/js/marked.min.js` | The Markdown parser (vendored — `marked` v12.0.2). |
| `assets/css/style.css` | All the styling, in one commented stylesheet. |
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

## Questions

The **Questions** page (`class7-math-questions.html`) is a second layout that shares the same engine.
Questions live in `content/class7/math-questions/`, one Markdown file per topic — the **same
numbered chapters** as the notes (`1.numbers.md`, …). They render as **auto-numbered
cards**, each with a tap-to-reveal **“Show answer.”**

Write each question as a block, separated by a blank-line-padded `---`; put the answer in
a `> [!ANSWER]` block (optional). **Don't number the questions yourself** — the page
numbers them in order. A file with no questions shows a “coming soon” state.

```markdown
# 1. Numbers

What is the smallest whole number?

> [!ANSWER]
> 0

---

Find (−6) × 102 using the distributive shortcut.

> [!ANSWER]
> (−6) × 100 + (−6) × 2 = −612
```

### ⭐ Starring a question for revision

Put a **`<!-- star -->`** comment line at the top of a question block — followed by a blank
line — to mark it as one to revise (typically one she got wrong in a test):

```markdown
<!-- star -->

There are **45 students** in a class and **3/5** of them are boys. How many girls?

> [!ANSWER]
> …
```

On the page that question gets a **gold card with a ⭐**, and a **`⭐ Starred only (N)`**
button appears next to *Expand all*. Tapping it hides every unstarred question, hides the
chapters left with nothing (and their chips), and opens the ones that remain — the whole
revision list in one view. Tap again to go back to everything.

The button only appears on pages that actually have a star, and this works on **every**
questions page (class 5–10, maths and science, plus ⭐ Saved) because they share one engine.
Question numbers keep their real position in the chapter, so a starred question is easy to
find in the book. To unstar, delete the comment line.

### Adding a question chapter

1. Create `content/class7/math-questions/<topic>.md` starting with a `# Title` line.
2. Add `"<topic>.md"` to `content/class7/math-questions/manifest.json` (the order there is the page order).

## Local preview

The notes load from separate files, so you need a tiny local server — **double-clicking
`index.html` won't work** (browsers block reading local files over `file://`). From the
repo root:

    python3 -m http.server

then open <http://localhost:8000>.

## Published site

Served by GitHub Pages from `main` / root: <https://rt2756.github.io/shambhvi/>.
