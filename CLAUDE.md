# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this repo is

CBSE / NCERT maths **revision notes** for a school student — plain Markdown in
`content/math/*.md` (notes) and `content/math-questions/*.md` (practice questions),
rendered in the browser and published via GitHub Pages. See `README.md` for the full file
map, callout syntax, and how rendering works.

## The rule that matters most: teach *why*, not just *how*

Every concept, rule, step, shortcut, or formula you write **must be explained** — the
student should understand *why it is true*, not just memorise *that it is*. A step with no
reason attached is a defect, even when it is correct.

- Pair each rule with a **`**Why it works:**`** explanation. This repo already uses that
  pattern — see the multiply/divide sign rule and the factor **count-check** in
  `content/math/1.numbers.md`.
- If the "why" is long, it can live nearby or in a linked section — but it must exist
  **somewhere** in the notes, not only in the student's memory.
- Before finishing any edit, apply the test: *would the student be able to re-derive this,
  or would they just have to remember it?* If it's the latter, the explanation is missing.

## Voice

Intuition first — **concrete example → the idea → the general rule** — then the compact
rule. Keep it short and plain, with lots of worked examples and `> [!TIP]` / `> [!NOTE]`
callouts, matching the existing style. Verify any numbers or factor lists before writing
them into the notes.
