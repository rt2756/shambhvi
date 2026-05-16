import { dayDiff, weekId } from "./dates";
import type { ProgressData } from "./schema";

/**
 * Record a study activity for `today` (YYYY-MM-DD) and update the streak.
 * Pure: mutates and returns the passed progress object so it is easy to test.
 *
 * Rules:
 *  - Same day as last activity → no streak change.
 *  - Exactly the next day → streak + 1.
 *  - Exactly one day skipped AND a weekly freeze is available → freeze is
 *    consumed, streak continues (+1). One grace skip per ISO week.
 *  - Otherwise (2+ days skipped, or 1 skipped with no freeze) → streak resets to 1.
 */
export function registerActivity(
  progress: ProgressData,
  today: string,
): ProgressData {
  const s = progress.streak;

  // Refill the weekly freeze when a new ISO week starts.
  const wk = weekId(today);
  if (s.freezeWeek !== wk) {
    s.freezeWeek = wk;
    s.freezesAvailable = 1;
  }

  if (s.lastActiveDate === today) {
    return progress; // already counted today
  }

  if (s.lastActiveDate === null) {
    s.current = 1;
  } else {
    const gap = dayDiff(s.lastActiveDate, today);
    if (gap === 1) {
      s.current += 1;
    } else if (gap === 2 && s.freezesAvailable > 0) {
      s.freezesAvailable -= 1;
      s.current += 1; // one missed day forgiven
    } else {
      s.current = 1; // streak broken
    }
  }

  s.lastActiveDate = today;
  if (!s.activeDates.includes(today)) {
    s.activeDates.push(today);
    s.activeDates.sort();
  }
  if (s.current > s.longest) s.longest = s.current;

  return progress;
}
