"use client";

import { useEffect, useState } from "react";
import { loadProgress } from "@/lib/progress/store";

export function StreakBadge() {
  const [streak, setStreak] = useState<number | null>(null);

  useEffect(() => {
    const refresh = () => setStreak(loadProgress().streak.current);
    refresh();
    window.addEventListener("shambhvi-progress-change", refresh);
    window.addEventListener("focus", refresh);
    return () => {
      window.removeEventListener("shambhvi-progress-change", refresh);
      window.removeEventListener("focus", refresh);
    };
  }, []);

  // Avoid SSR/hydration mismatch: render nothing until mounted.
  if (streak === null || streak === 0) return null;

  return (
    <span
      className="flex items-center gap-1 rounded-full bg-orange-100 px-2.5 py-1 text-xs font-semibold text-orange-700"
      title={`${streak}-day study streak — keep it going!`}
    >
      <span aria-hidden>🔥</span>
      {streak} day{streak === 1 ? "" : "s"}
    </span>
  );
}
