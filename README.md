# Shambhvi's Maths

A small static website of class-7 (CBSE / NCERT) maths revision notes, built for Shambhvi.
Plain HTML + CSS — no build step, no JavaScript — published with **GitHub Pages**.

## Structure

| Path | What it is |
|---|---|
| `index.html` | Home page — links to each subject. |
| `assets/css/style.css` | All the styling, in one commented stylesheet. |
| `topics/*.html` | One page per subject (Numbers, Algebra, Ratio &amp; %, Geometry, Mensuration, Data Handling). |
| `topics/_template.html` | Reference page showing every component (callout boxes, tables, prev/next pager). Copy it to start a new section. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is (no Jekyll processing). |

## Adding a topic's notes

1. Copy `topics/_template.html` (or an existing topic page) and give it a clear name.
2. Replace the placeholder content with the notes. The handy building blocks are:
   - `<div class="box eg">` — a worked example
   - `<div class="box tip">` — a handy tip
   - `<div class="box warn">` — the ⚠️ common-mistakes line
   - a normal `<table>` for tables (e.g. multiplication tables)
3. Save and reload in a browser — no build step.

## Viewing locally

Double-click `index.html`, or run a tiny local server from the repo root:

    python3 -m http.server

then open <http://localhost:8000>.

## Published site

Served by GitHub Pages from this repository. Once Pages is enabled, the site is live at
<https://rt2756.github.io/shambhvi/>.
