# Shambhvi Learning Website

Local-only Next.js learning site for Shambhvi (class 7, CBSE, India). Math only in v1.

## Quick start

```bash
cd learning_website
npm install
npm run dev
```

Open `http://localhost:3000`.

## What's here

- **Foundation notes** under `content/math/foundations/` — migrated from `../mathematics.md` (one level up) via `npm run migrate:math`.
- **NCERT class 7 chapter notes** under `content/math/<slug>.md` — drafted in-session and reviewed by Ranjeet.
- **MCQ quizzes** per chapter under `content/math/quizzes/<slug>.json` (parent-reviewed for correctness).
- **AI tutor chat** at `/tutor` and as a floating side panel on chapter pages. Powered by Google Gemini via `@google/genai`. Falls back to a friendly "set up your key" message when `GEMINI_API_KEY` isn't set.
- **Progress + streak tracking** in localStorage (coming in Chunk 4).

## Scripts

| Command | What it does |
|---|---|
| `npm run dev` | Next.js dev server at `localhost:3000` |
| `npm run build` | Production build |
| `npm run typecheck` | TypeScript check, no emit |
| `npm run migrate:math` | Carve `../mathematics.md` into `content/math/foundations/*.md` |
| `npm run draft:chapter -- --slug <name>` | Draft one NCERT chapter via Gemini 2.5 Pro to `content/math/_drafts/<slug>.md` (needs `GEMINI_API_KEY`) |
| `npm run draft:chapter -- --all` | Draft all 13 NCERT chapters (~$10 in API cost) |

## AI tutor setup (optional)

1. Get a free Gemini key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Copy `.env.local.example` to `.env.local`.
3. Paste the key into `GEMINI_API_KEY=`.
4. Restart `npm run dev` if it was already running.

Safety: layered guardrails — input denylist, Gemini `safetySettings` set to `BLOCK_LOW_AND_ABOVE`, output blocking on `BLOCKED` finish reason, rate limit (30 messages / 5 min, 200 / day), math output normalizer for Unicode glyphs.

## Status

- ✅ Chunk 1 — scaffold + foundations migration
- ✅ Chunk 2 — AI tutor (server route, chat UI, floating button) + chapter drafting infrastructure
- ⏳ Chunk 3 — quizzes (infra + drafted quizzes for every chapter)
- ⏳ Chunk 4 — progress + streak + JSON export/import

Full plan: `/Users/ranjeet/.claude/plans/note-about-shambhvi-in-serene-galaxy.md`.
