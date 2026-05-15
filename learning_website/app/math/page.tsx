import Link from "next/link";
import {
  getFoundationTopics,
  getMathChapters,
  type ChapterEntry,
} from "@/lib/content";

export default async function MathIndex() {
  const [chapters, foundations] = await Promise.all([
    getMathChapters(),
    getFoundationTopics(),
  ]);

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">Math</h1>
        <p className="mt-2 text-slate-600">
          Foundations first, then the 13 NCERT chapters for class 7.
        </p>
      </header>

      <section>
        <h2 className="mb-3 text-lg font-semibold text-slate-900">
          Foundations
        </h2>
        {foundations.length === 0 ? (
          <EmptyHint message="Run the migration script to populate foundations." />
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {foundations.map((topic) => (
              <ChapterCard
                key={topic.slug}
                entry={topic}
                href={`/math/foundations/${topic.slug}`}
              />
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold text-slate-900">
          NCERT Class 7
        </h2>
        <div className="grid gap-3 sm:grid-cols-2">
          {chapters.map((chapter) => (
            <ChapterCard
              key={chapter.slug}
              entry={chapter}
              href={`/math/${chapter.slug}`}
            />
          ))}
        </div>
      </section>
    </div>
  );
}

function ChapterCard({
  entry,
  href,
}: {
  entry: ChapterEntry;
  href: string;
}) {
  const ready = entry.status === "ready";
  const baseClasses =
    "block rounded-xl border p-4 transition shadow-sm";
  const stateClasses = ready
    ? "border-slate-200 bg-white hover:border-brand-600 hover:shadow"
    : "border-dashed border-slate-300 bg-slate-50 text-slate-500 cursor-not-allowed";

  const inner = (
    <>
      <div className="flex items-baseline justify-between">
        <div>
          {entry.ncertChapter ? (
            <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
              Chapter {entry.ncertChapter}
            </p>
          ) : null}
          <h3 className="text-base font-semibold">{entry.title}</h3>
        </div>
        {!ready && (
          <span className="rounded-full bg-slate-200 px-2 py-0.5 text-xs font-medium text-slate-600">
            Coming soon
          </span>
        )}
      </div>
      {entry.summary && (
        <p className="mt-2 line-clamp-2 text-sm text-slate-600">
          {entry.summary}
        </p>
      )}
    </>
  );

  if (!ready) {
    return <div className={`${baseClasses} ${stateClasses}`}>{inner}</div>;
  }

  return (
    <Link href={href} className={`${baseClasses} ${stateClasses}`}>
      {inner}
    </Link>
  );
}

function EmptyHint({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-6 text-sm text-slate-500">
      {message}
    </div>
  );
}
