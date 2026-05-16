export const PROGRESS_VERSION = 1;
export const PROGRESS_KEY = "shambhvi-progress-v1";

export interface QuizAttempt {
  completedAt: string; // ISO timestamp
  total: number;
  correct: number;
}

export interface ChapterProgress {
  notesFirstOpenedAt?: string;
  notesLastOpenedAt?: string;
  notesViewCount: number;
  quizAttempts: QuizAttempt[];
  bestScorePct: number;
}

export interface StreakState {
  current: number;
  longest: number;
  lastActiveDate: string | null; // YYYY-MM-DD (Asia/Kolkata)
  activeDates: string[]; // sorted unique YYYY-MM-DD
  freezesAvailable: number; // weekly grace skips remaining
  freezeWeek: string | null; // weekId when the freeze was last refilled
}

export interface ProgressData {
  version: number;
  streak: StreakState;
  chapters: Record<string, ChapterProgress>;
  tutor: { totalMessages: number; lastUsedAt: string | null };
}

export function defaultProgress(): ProgressData {
  return {
    version: PROGRESS_VERSION,
    streak: {
      current: 0,
      longest: 0,
      lastActiveDate: null,
      activeDates: [],
      freezesAvailable: 1,
      freezeWeek: null,
    },
    chapters: {},
    tutor: { totalMessages: 0, lastUsedAt: null },
  };
}

export function emptyChapter(): ChapterProgress {
  return {
    notesViewCount: 0,
    quizAttempts: [],
    bestScorePct: 0,
  };
}
