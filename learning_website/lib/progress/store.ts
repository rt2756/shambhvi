import {
  defaultProgress,
  PROGRESS_KEY,
  PROGRESS_VERSION,
  type ProgressData,
} from "./schema";

export function loadProgress(): ProgressData {
  if (typeof window === "undefined") return defaultProgress();
  try {
    const raw = window.localStorage.getItem(PROGRESS_KEY);
    if (!raw) return defaultProgress();
    const parsed = JSON.parse(raw) as Partial<ProgressData>;
    if (parsed?.version !== PROGRESS_VERSION) {
      // No migrations yet — start fresh on version mismatch.
      return defaultProgress();
    }
    const base = defaultProgress();
    return {
      ...base,
      ...parsed,
      streak: { ...base.streak, ...parsed.streak },
      tutor: { ...base.tutor, ...parsed.tutor },
      chapters: parsed.chapters ?? {},
    };
  } catch {
    return defaultProgress();
  }
}

export function saveProgress(progress: ProgressData): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
    window.dispatchEvent(new Event("shambhvi-progress-change"));
  } catch {
    // localStorage full or unavailable — ignore.
  }
}

export function resetProgress(): void {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(PROGRESS_KEY);
  window.dispatchEvent(new Event("shambhvi-progress-change"));
}

export function exportProgressJSON(): string {
  return JSON.stringify(loadProgress(), null, 2);
}

export function importProgressJSON(json: string): boolean {
  try {
    const parsed = JSON.parse(json) as Partial<ProgressData>;
    if (
      typeof parsed !== "object" ||
      parsed === null ||
      typeof parsed.streak !== "object" ||
      typeof parsed.chapters !== "object"
    ) {
      return false;
    }
    const base = defaultProgress();
    const merged: ProgressData = {
      ...base,
      ...parsed,
      version: PROGRESS_VERSION,
      streak: { ...base.streak, ...parsed.streak },
      tutor: { ...base.tutor, ...parsed.tutor },
      chapters: parsed.chapters ?? {},
    };
    saveProgress(merged);
    return true;
  } catch {
    return false;
  }
}
