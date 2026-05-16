import { describe, expect, it } from "vitest";
import { dayDiff, todayInKolkata, weekId } from "../lib/progress/dates";
import { defaultProgress } from "../lib/progress/schema";
import { registerActivity } from "../lib/progress/streak";

describe("date helpers", () => {
  it("todayInKolkata returns YYYY-MM-DD", () => {
    expect(todayInKolkata()).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });

  it("todayInKolkata uses the Kolkata day boundary", () => {
    // 2026-05-15 22:00 UTC = 2026-05-16 03:30 IST → Kolkata date is the 16th.
    const utcNight = new Date("2026-05-15T22:00:00Z");
    expect(todayInKolkata(utcNight)).toBe("2026-05-16");
  });

  it("dayDiff counts whole days", () => {
    expect(dayDiff("2026-05-01", "2026-05-01")).toBe(0);
    expect(dayDiff("2026-05-01", "2026-05-02")).toBe(1);
    expect(dayDiff("2026-05-01", "2026-05-10")).toBe(9);
  });

  it("weekId returns the Monday of the week", () => {
    // 2026-05-16 is a Saturday; its week's Monday is 2026-05-11.
    expect(weekId("2026-05-16")).toBe("2026-05-11");
    // Sunday belongs to the week that started the previous Monday.
    expect(weekId("2026-05-17")).toBe("2026-05-11");
    // Monday maps to itself.
    expect(weekId("2026-05-18")).toBe("2026-05-18");
  });
});

describe("registerActivity", () => {
  it("first activity starts the streak at 1", () => {
    const p = registerActivity(defaultProgress(), "2026-05-10");
    expect(p.streak.current).toBe(1);
    expect(p.streak.longest).toBe(1);
    expect(p.streak.lastActiveDate).toBe("2026-05-10");
  });

  it("same-day activity does not change the streak", () => {
    let p = registerActivity(defaultProgress(), "2026-05-10");
    p = registerActivity(p, "2026-05-10");
    expect(p.streak.current).toBe(1);
  });

  it("consecutive days increment the streak", () => {
    let p = registerActivity(defaultProgress(), "2026-05-10");
    p = registerActivity(p, "2026-05-11");
    p = registerActivity(p, "2026-05-12");
    expect(p.streak.current).toBe(3);
    expect(p.streak.longest).toBe(3);
  });

  it("one missed day is forgiven when a weekly freeze is available", () => {
    let p = registerActivity(defaultProgress(), "2026-05-11"); // Mon
    expect(p.streak.freezesAvailable).toBe(1);
    // Skip the 12th; return on the 13th (gap = 2).
    p = registerActivity(p, "2026-05-13");
    expect(p.streak.current).toBe(2);
    expect(p.streak.freezesAvailable).toBe(0);
  });

  it("one missed day breaks the streak when no freeze is left", () => {
    let p = registerActivity(defaultProgress(), "2026-05-11"); // Mon, freeze=1
    p = registerActivity(p, "2026-05-13"); // gap 2, uses the freeze → current 2
    // Skip the 14th; return on the 15th (gap 2) — freeze already spent this week.
    p = registerActivity(p, "2026-05-15");
    expect(p.streak.current).toBe(1);
    expect(p.streak.longest).toBe(2);
  });

  it("a gap of two or more missed days always breaks the streak", () => {
    let p = registerActivity(defaultProgress(), "2026-05-11");
    // Return three days later (gap = 3): a single freeze cannot cover 2 days.
    p = registerActivity(p, "2026-05-14");
    expect(p.streak.current).toBe(1);
  });

  it("longest streak is preserved after a reset", () => {
    let p = registerActivity(defaultProgress(), "2026-05-11");
    p = registerActivity(p, "2026-05-12");
    p = registerActivity(p, "2026-05-13"); // current 3, longest 3
    // Big gap → reset.
    p = registerActivity(p, "2026-05-25");
    expect(p.streak.current).toBe(1);
    expect(p.streak.longest).toBe(3);
  });

  it("a new ISO week refills the freeze", () => {
    let p = registerActivity(defaultProgress(), "2026-05-11"); // Mon (week A)
    p = registerActivity(p, "2026-05-13"); // gap 2, freeze used → 0
    expect(p.streak.freezesAvailable).toBe(0);
    // Jump to the next week (2026-05-18 is the next Monday) — freeze refills.
    p = registerActivity(p, "2026-05-18");
    expect(p.streak.freezesAvailable).toBe(1);
  });

  it("records every active date once, sorted", () => {
    let p = registerActivity(defaultProgress(), "2026-05-12");
    p = registerActivity(p, "2026-05-11");
    p = registerActivity(p, "2026-05-12"); // duplicate, ignored
    expect(p.streak.activeDates).toEqual(["2026-05-11", "2026-05-12"]);
  });
});
