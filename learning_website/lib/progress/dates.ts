// Pure date helpers — no DOM, fully unit-testable.

// Today's date in Asia/Kolkata as YYYY-MM-DD (laptop-timezone independent).
export function todayInKolkata(now: Date = new Date()): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Kolkata",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(now);
}

// Whole-day difference (b - a) between two YYYY-MM-DD strings.
export function dayDiff(a: string, b: string): number {
  const da = Date.parse(`${a}T00:00:00Z`);
  const db = Date.parse(`${b}T00:00:00Z`);
  return Math.round((db - da) / 86_400_000);
}

// Monday (YYYY-MM-DD) of the ISO week containing the given date.
export function weekId(dateStr: string): string {
  const d = new Date(`${dateStr}T00:00:00Z`);
  const day = d.getUTCDay(); // 0=Sun … 6=Sat
  const shift = day === 0 ? -6 : 1 - day;
  d.setUTCDate(d.getUTCDate() + shift);
  return d.toISOString().slice(0, 10);
}
