"use client";

import { useEffect, useRef, useState } from "react";
import { todayInKolkata } from "@/lib/progress/dates";
import {
  exportProgressJSON,
  importProgressJSON,
  loadProgress,
  resetProgress,
} from "@/lib/progress/store";
import type { ProgressData } from "@/lib/progress/schema";

function titleFromSlug(slug: string): string {
  return slug
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

export default function ProgressPage() {
  const [data, setData] = useState<ProgressData | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  function refresh() {
    setData(loadProgress());
  }

  useEffect(() => {
    refresh();
    window.addEventListener("shambhvi-progress-change", refresh);
    return () =>
      window.removeEventListener("shambhvi-progress-change", refresh);
  }, []);

  if (!data) {
    return <p className="text-slate-500">Loading…</p>;
  }

  const chapters = Object.entries(data.chapters);
  const totalViews = chapters.reduce(
    (n, [, c]) => n + c.notesViewCount,
    0,
  );
  const totalQuizzes = chapters.reduce(
    (n, [, c]) => n + c.quizAttempts.length,
    0,
  );

  function handleExport() {
    const blob = new Blob([exportProgressJSON()], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `shambhvi-progress-${todayInKolkata()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    setMsg("Progress downloaded.");
  }

  function handleImportFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const ok = importProgressJSON(String(reader.result));
      setMsg(ok ? "Progress restored." : "That file could not be read.");
      if (ok) refresh();
    };
    reader.readAsText(file);
  }

  function handleReset() {
    if (
      window.confirm(
        "Erase all progress and streak data? This cannot be undone.",
      )
    ) {
      resetProgress();
      refresh();
      setMsg("Progress cleared.");
    }
  }

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Progress</h1>
        <p className="mt-2 text-slate-600">
          Your study streak, quiz scores, and activity.
        </p>
      </header>

      <section className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Stat label="Current streak" value={`${data.streak.current} 🔥`} />
        <Stat label="Longest streak" value={`${data.streak.longest} 🏆`} />
        <Stat label="Chapters opened" value={String(totalViews)} />
        <Stat label="Quizzes taken" value={String(totalQuizzes)} />
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold text-slate-900">
          Last 12 weeks
        </h2>
        <Heatmap activeDates={data.streak.activeDates} />
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold text-slate-900">
          By chapter
        </h2>
        {chapters.length === 0 ? (
          <p className="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-6 text-sm text-slate-500">
            No activity yet. Open a chapter or take a quiz to get started.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full border-collapse text-sm">
              <thead>
                <tr className="border-b border-slate-300 text-left">
                  <th className="py-2 pr-4 font-semibold">Topic</th>
                  <th className="py-2 pr-4 font-semibold">Views</th>
                  <th className="py-2 pr-4 font-semibold">Quizzes</th>
                  <th className="py-2 pr-4 font-semibold">Best score</th>
                </tr>
              </thead>
              <tbody>
                {chapters
                  .sort((a, b) => a[0].localeCompare(b[0]))
                  .map(([slug, c]) => (
                    <tr key={slug} className="border-b border-slate-200">
                      <td className="py-2 pr-4">{titleFromSlug(slug)}</td>
                      <td className="py-2 pr-4">{c.notesViewCount}</td>
                      <td className="py-2 pr-4">{c.quizAttempts.length}</td>
                      <td className="py-2 pr-4">
                        {c.quizAttempts.length > 0
                          ? `${c.bestScorePct}%`
                          : "—"}
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="text-lg font-semibold text-slate-900">
          Backup &amp; restore
        </h2>
        <p className="mt-1 text-sm text-slate-600">
          Progress is saved only in this browser. Export a backup now and
          then to keep it safe.
        </p>
        <div className="mt-4 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={handleExport}
            className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Export JSON
          </button>
          <button
            type="button"
            onClick={() => fileRef.current?.click()}
            className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:border-brand-600 hover:text-brand-600"
          >
            Import JSON
          </button>
          <input
            ref={fileRef}
            type="file"
            accept="application/json"
            className="hidden"
            onChange={handleImportFile}
          />
          <button
            type="button"
            onClick={handleReset}
            className="rounded-lg border border-rose-300 px-4 py-2 text-sm font-medium text-rose-600 hover:bg-rose-50"
          >
            Reset all
          </button>
        </div>
        {msg && <p className="mt-3 text-sm text-slate-600">{msg}</p>}
      </section>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <p className="text-xs uppercase tracking-wide text-slate-500">
        {label}
      </p>
      <p className="mt-1 text-2xl font-bold text-slate-900">{value}</p>
    </div>
  );
}

function Heatmap({ activeDates }: { activeDates: string[] }) {
  const active = new Set(activeDates);
  const today = new Date(`${todayInKolkata()}T00:00:00Z`);
  const days: { date: string; on: boolean }[] = [];
  for (let i = 83; i >= 0; i--) {
    const d = new Date(today);
    d.setUTCDate(d.getUTCDate() - i);
    const iso = d.toISOString().slice(0, 10);
    days.push({ date: iso, on: active.has(iso) });
  }
  const weeks: { date: string; on: boolean }[][] = [];
  for (let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7));
  }

  return (
    <div className="flex gap-1">
      {weeks.map((week, wi) => (
        <div key={wi} className="flex flex-col gap-1">
          {week.map((day) => (
            <div
              key={day.date}
              title={`${day.date}${day.on ? " — studied" : ""}`}
              className={`h-3 w-3 rounded-sm ${
                day.on ? "bg-brand-600" : "bg-slate-200"
              }`}
            />
          ))}
        </div>
      ))}
    </div>
  );
}
