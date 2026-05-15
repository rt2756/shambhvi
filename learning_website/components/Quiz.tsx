"use client";

import { useState } from "react";
import { Markdown } from "@/lib/markdown";
import type { Quiz as QuizData, QuizResult } from "@/lib/quiz/schema";

interface Props {
  quiz: QuizData;
  onComplete?: (result: QuizResult) => void;
}

export function Quiz({ quiz, onComplete }: Props) {
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [perQuestion, setPerQuestion] = useState<Record<string, boolean>>(
    {},
  );
  const [done, setDone] = useState(false);

  const q = quiz.questions[current];
  const isLast = current === quiz.questions.length - 1;
  const answered = selected !== null;

  function choose(i: number) {
    if (answered) return;
    setSelected(i);
    setPerQuestion((prev) => ({
      ...prev,
      [q.id]: i === q.correctIndex,
    }));
  }

  function next() {
    if (isLast) {
      setDone(true);
      const correct = Object.values(perQuestion).filter(Boolean).length;
      onComplete?.({
        slug: quiz.slug,
        total: quiz.questions.length,
        correct,
        perQuestion,
      });
      return;
    }
    setCurrent((c) => c + 1);
    setSelected(null);
  }

  function retake() {
    setCurrent(0);
    setSelected(null);
    setPerQuestion({});
    setDone(false);
  }

  if (done) {
    const correct = Object.values(perQuestion).filter(Boolean).length;
    const total = quiz.questions.length;
    const pct = Math.round((correct / total) * 100);
    const cheer =
      pct >= 80
        ? "Brilliant! 🎉"
        : pct >= 50
          ? "Good effort — review the misses and try again."
          : "Keep going — read the notes once more, then retry.";
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        <p className="text-sm font-medium uppercase tracking-wide text-slate-500">
          Score
        </p>
        <p className="mt-2 text-5xl font-bold text-brand-600">
          {correct}/{total}
        </p>
        <p className="mt-1 text-lg text-slate-700">{pct}%</p>
        <p className="mt-4 text-slate-600">{cheer}</p>
        <button
          type="button"
          onClick={retake}
          className="mt-6 rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-700"
        >
          Retake quiz
        </button>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between text-sm text-slate-500">
        <span>
          Question {current + 1} of {quiz.questions.length}
        </span>
        <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium capitalize">
          {q.difficulty}
        </span>
      </div>

      <div className="prose prose-slate max-w-none">
        <Markdown>{q.prompt}</Markdown>
      </div>

      <div className="mt-5 grid gap-3">
        {q.options.map((opt, i) => {
          const isCorrect = i === q.correctIndex;
          const isPicked = i === selected;
          let cls =
            "flex items-center gap-3 rounded-lg border px-4 py-3 text-left transition";
          if (!answered) {
            cls +=
              " border-slate-300 bg-white hover:border-brand-600 hover:bg-brand-50";
          } else if (isCorrect) {
            cls += " border-emerald-500 bg-emerald-50";
          } else if (isPicked) {
            cls += " border-rose-500 bg-rose-50";
          } else {
            cls += " border-slate-200 bg-white opacity-60";
          }
          return (
            <button
              key={i}
              type="button"
              onClick={() => choose(i)}
              disabled={answered}
              className={cls}
            >
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-slate-300 text-xs font-medium">
                {String.fromCharCode(65 + i)}
              </span>
              <span className="prose prose-sm max-w-none [&_p]:my-0">
                <Markdown>{opt}</Markdown>
              </span>
              {answered && isCorrect && (
                <span className="ml-auto text-emerald-600">✓</span>
              )}
              {answered && isPicked && !isCorrect && (
                <span className="ml-auto text-rose-600">✗</span>
              )}
            </button>
          );
        })}
      </div>

      {answered && (
        <div className="mt-5 rounded-lg border border-slate-200 bg-slate-50 p-4">
          <p className="mb-1 text-sm font-semibold text-slate-700">
            {selected === q.correctIndex ? "Correct ✓" : "Not quite ✗"}
          </p>
          <div className="prose prose-sm max-w-none text-slate-700">
            <Markdown>{q.explanation}</Markdown>
          </div>
        </div>
      )}

      <div className="mt-6 flex justify-end">
        <button
          type="button"
          onClick={next}
          disabled={!answered}
          className="rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isLast ? "Finish" : "Next question"}
        </button>
      </div>
    </div>
  );
}
