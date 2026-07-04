# Maths

CBSE / NCERT maths revision notes. The **content lives in plain Markdown files**, one per
topic; the page fetches them and renders collapsible sections in the browser. No build
step, no Jekyll — published with **GitHub Pages**.

## Writing principle — always explain *why*, never just *how*

These notes teach for **understanding, not memorisation**. Every rule, step, shortcut, or
formula must come with the **reason it works** — right beside it, or linked from it. The
test: *would the student be able to **re-derive** the step, or would they just have to
**remember** it?* If it's the latter, the "why" is missing and the note isn't finished.

- ✅ **Do:** state the rule, then a **`**Why it works:**`** line explaining the idea behind
  it (see the multiply/divide sign rule and the factor count-check in `content/math/1.numbers.md`).
- ❌ **Don't:** drop in a recipe like "add 1 to each power and multiply" with no reason —
  that's just one more thing to memorise.

Worked examples, `> [!TIP]` callouts, and "Why it works" lines exist for exactly this. A
concept with no explanation anywhere in the notes is treated as unfinished.

## Files

| Path | What it is |
|---|---|
| `content/math/*.md` | The notes — one Markdown file per topic. **Edit these.** |
| `content/math/manifest.json` | The ordered list of topic files to show. |
| `content/math-questions/*.md` | The practice questions — one file per topic, same chapters as the notes. |
| `content/math-questions/manifest.json` | The ordered list of question files to show. |
| `index.html` · `questions.html` | The two layouts — **Notes** and **Questions**. Each is a thin shell with a container the content renders into. |
| `assets/js/app.js` | Loads a manifest + `.md` files and builds the page; one engine drives both layouts (chosen by `#app`'s `data-mode`). |
| `assets/js/marked.min.js` | The Markdown parser (vendored — `marked` v12.0.2). |
| `assets/css/style.css` | All the styling, in one commented stylesheet. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is (no Jekyll). |

## Editing notes

Just edit the Markdown in `content/math/`. The first `#` heading in a file is the topic
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

1. Create `content/math/<topic>.md` starting with a `# Title` line.
2. Add `"<topic>.md"` to `content/math/manifest.json` (the order there is the page order).

## Questions

The **Questions** page (`questions.html`) is a second layout that shares the same engine.
Questions live in `content/math-questions/`, one Markdown file per topic — the **same
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

### Adding a question chapter

1. Create `content/math-questions/<topic>.md` starting with a `# Title` line.
2. Add `"<topic>.md"` to `content/math-questions/manifest.json` (the order there is the page order).

## Local preview

The notes load from separate files, so you need a tiny local server — **double-clicking
`index.html` won't work** (browsers block reading local files over `file://`). From the
repo root:

    python3 -m http.server

then open <http://localhost:8000>.

## Published site

Served by GitHub Pages from `main` / root: <https://rt2756.github.io/shambhvi/>.
