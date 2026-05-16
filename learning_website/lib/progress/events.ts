import { todayInKolkata } from "./dates";
import { emptyChapter } from "./schema";
import { loadProgress, saveProgress } from "./store";
import { registerActivity } from "./streak";

// A study activity counts toward the streak: opening a chapter for >=30s,
// answering a quiz, or sending a tutor message.
function withActivity(mutate: (p: ReturnType<typeof loadProgress>) => void) {
  const p = loadProgress();
  mutate(p);
  registerActivity(p, todayInKolkata());
  saveProgress(p);
}

export function recordChapterView(slug: string): void {
  withActivity((p) => {
    const ch = p.chapters[slug] ?? emptyChapter();
    const nowIso = new Date().toISOString();
    if (!ch.notesFirstOpenedAt) ch.notesFirstOpenedAt = nowIso;
    ch.notesLastOpenedAt = nowIso;
    ch.notesViewCount += 1;
    p.chapters[slug] = ch;
  });
}

export function recordQuizAttempt(
  slug: string,
  total: number,
  correct: number,
): void {
  withActivity((p) => {
    const ch = p.chapters[slug] ?? emptyChapter();
    ch.quizAttempts.push({
      completedAt: new Date().toISOString(),
      total,
      correct,
    });
    const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
    if (pct > ch.bestScorePct) ch.bestScorePct = pct;
    p.chapters[slug] = ch;
  });
}

export function recordTutorMessage(): void {
  withActivity((p) => {
    p.tutor.totalMessages += 1;
    p.tutor.lastUsedAt = new Date().toISOString();
  });
}
