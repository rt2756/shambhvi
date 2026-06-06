# Maths

CBSE / NCERT maths revision notes. The **content lives in plain Markdown files**, one per
topic; the page fetches them and renders collapsible sections in the browser. No build
step, no Jekyll — published with **GitHub Pages**.

## Files

| Path | What it is |
|---|---|
| `content/math/*.md` | The notes — one Markdown file per topic. **Edit these.** |
| `content/math/manifest.json` | The ordered list of topic files to show. |
| `index.html` | Thin shell: header + an empty container the notes render into. |
| `assets/js/app.js` | Loads the manifest + `.md` files and builds the page. |
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

## Local preview

The notes load from separate files, so you need a tiny local server — **double-clicking
`index.html` won't work** (browsers block reading local files over `file://`). From the
repo root:

    python3 -m http.server

then open <http://localhost:8000>.

## Published site

Served by GitHub Pages from `main` / root: <https://rt2756.github.io/shambhvi/>.
