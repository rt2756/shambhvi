"use client";

import { useEffect, useState } from "react";
import { TutorChat } from "./TutorChat";

interface Props {
  chapterSlug: string;
  chapterTitle: string;
}

export function AskTutorButton({ chapterSlug, chapterTitle }: Props) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    if (open) {
      window.addEventListener("keydown", onKey);
      return () => window.removeEventListener("keydown", onKey);
    }
  }, [open]);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-30 flex items-center gap-2 rounded-full bg-brand-600 px-4 py-3 text-sm font-medium text-white shadow-lg hover:bg-brand-700"
        aria-label={`Ask tutor about ${chapterTitle}`}
      >
        <span aria-hidden>💬</span>
        Ask tutor
      </button>

      {open && (
        <>
          <div
            className="fixed inset-0 z-40 bg-slate-900/30"
            onClick={() => setOpen(false)}
            aria-hidden
          />
          <aside
            className="fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col border-l border-slate-200 bg-white shadow-xl"
            role="dialog"
            aria-label={`Tutor chat for ${chapterTitle}`}
          >
            <header className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
              <div>
                <p className="text-xs text-slate-500">Tutor</p>
                <p className="text-sm font-semibold text-slate-900">
                  {chapterTitle}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
                aria-label="Close tutor"
              >
                ✕
              </button>
            </header>
            <div className="flex-1 overflow-hidden">
              <TutorChat
                chapterSlug={chapterSlug}
                chapterTitle={chapterTitle}
                variant="panel"
              />
            </div>
          </aside>
        </>
      )}
    </>
  );
}
