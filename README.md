# Class 7 Maths

A single-page website of class-7 (CBSE / NCERT) maths revision notes — one running document.
Plain HTML + CSS, no build step, no JavaScript — published with **GitHub Pages**.

## Files

| Path | What it is |
|---|---|
| `index.html` | The notes — one running document, every topic on this page. |
| `assets/css/style.css` | All the styling, in one commented stylesheet. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is (no Jekyll processing). |

## Writing notes

Add topics straight into `index.html`. The pre-styled building blocks are:

- `<h2>Topic</h2>` and `<h3>Sub-topic</h3>` for headings
- `<div class="box eg">` — a worked example
- `<div class="box tip">` — a handy tip
- `<div class="box warn">` — the ⚠️ common-mistakes line
- a normal `<table>` for tables

No build step — save and reload the page.

## Local preview

Double-click `index.html`, or run a tiny server from the repo root:

    python3 -m http.server

then open <http://localhost:8000>.

## Published site

Served by GitHub Pages from `main` / root: <https://rt2756.github.io/shambhvi/>.
