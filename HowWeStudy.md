# How we study a chapter — the routine that works

A repeatable routine for studying one chapter, first used for **Class 7 · Algebraic
Expressions** (14 Nov 2026). For the next chapter, ask Claude to *"follow HowWeStudy.md for
&lt;chapter&gt;"*.

## The routine

### 1. Teach the chapter in chat
- Go **topic by topic, in order**. For each: a plain definition, then a **worked example**,
  then the general rule, then a **⚠️ common mistake** line.
  - For Algebraic Expressions the order was: what an expression is (variable, constant) →
    terms (the sign belongs to the term) → factors and coefficients → like and unlike terms →
    monomial, binomial and trinomial → adding and subtracting → finding values → patterns.
- Use small **tables** to compare things, such as terms or the types of expression.
- Say **why** each rule works, not just how (see `CLAUDE.md`).
- End with about **7 quick practice questions** in chat.

### 2. A practice worksheet in the browser (20 questions)
- Claude builds an HTML worksheet and opens it in **its own browser pane** (the in-app
  browser), not the user's Chrome.
- **Most questions are multiple choice, and the rest need a number answer**, so the page can
  mark itself. Cover every topic from step 1, from easy to medium.
- **No timer.** It's practice, not an exam. The first version had a 25-minute timer. It ran
  out midway and locked the answers, so we removed it.
- **Answers save as you go** (in the browser), so a reload doesn't lose work.
- You can answer over several sittings. If answers are lost, tell Claude which ones you'd
  done and it will fill them back in.
- **Submit** shows the **total score** at the top. Each question turns **green or red**, with
  the correct answer and a one-line reason.
- Afterwards, Claude reads the page and gives the score in chat as a table.

### 3. A challenge set (10 harder questions)
- Only after scoring well on step 2.
- **Multi-step** questions: several brackets, nested brackets, three expressions at once,
  values with negatives and powers, working a pattern backwards, writing the expression from
  a word problem, finding missing powers in like terms.
- Open it in a **new tab**, so the earlier result stays visible.

### 4. Wrap up
- Give the score and say what's next: a harder set, or the next chapter. For Algebraic
  Expressions, the next chapters were Simple Equations and Exponents & Powers.

## Worksheet tips (for Claude)
- The saved worksheets are in `worksheets/`. Copy one and swap the `Q` list for a new
  chapter. Also change the `KEY` used to save answers, so each worksheet keeps its own
  answers.
- **Serve over http, not `file://`.** The browser pane shows local files as static
  snapshots, so the scripts (marking and saving answers) don't run. From the repo root, run
  `python3 -m http.server`, then open `http://localhost:8000/worksheets/<file>.html`. The
  published site works too.
- **No `confirm()` or `alert()` pop-ups.** The pane doesn't show them, so Submit looked as if
  it did nothing.
- **Test Submit after any edit.** One fix left `onclick=()=>submit` (no brackets), which
  never runs.
- Each question needs a short **why** in its explanation (`e:`), not just the answer.

## Log

| Date | Chapter | Practice (20) | Challenge (10) |
|---|---|---|---|
| 14 Nov 2026 | Class 7 · Algebraic Expressions | 20 / 20 | 10 / 10 |
