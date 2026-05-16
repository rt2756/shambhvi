import Link from "next/link";
import { notFound } from "next/navigation";
import { AskTutorButton } from "@/components/AskTutorButton";
import { ViewTracker } from "@/components/ViewTracker";
import { getChapter, getMathChapters } from "@/lib/content";
import { Markdown } from "@/lib/markdown";

interface Props {
  params: Promise<{ chapter: string }>;
}

export async function generateStaticParams() {
  const chapters = await getMathChapters();
  return chapters
    .filter((c) => c.status === "ready")
    .map((c) => ({ chapter: c.slug }));
}

export default async function ChapterPage({ params }: Props) {
  const { chapter: slug } = await params;
  const chapter = await getChapter(slug);
  if (!chapter) notFound();

  return (
    <article className="space-y-6">
      <header className="border-b border-slate-200 pb-4">
        <Link
          href="/math"
          className="text-sm text-slate-500 hover:text-brand-600"
        >
          ← Back to Math
        </Link>
        {chapter.ncertChapter ? (
          <p className="mt-3 text-xs font-medium uppercase tracking-wide text-slate-500">
            NCERT Chapter {chapter.ncertChapter}
          </p>
        ) : null}
        <h1 className="mt-1 text-3xl font-bold text-slate-900">
          {chapter.title}
        </h1>
        {chapter.summary && (
          <p className="mt-2 text-slate-600">{chapter.summary}</p>
        )}
      </header>

      <div className="prose prose-slate max-w-none">
        <Markdown>{chapter.content}</Markdown>
      </div>

      <footer className="flex flex-wrap gap-3 border-t border-slate-200 pt-4">
        <Link
          href={`/math/${chapter.slug}/quiz`}
          className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
        >
          Take the quiz
        </Link>
        {chapter.nextChapter && (
          <Link
            href={`/math/${chapter.nextChapter}`}
            className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:border-brand-600 hover:text-brand-600"
          >
            Next chapter →
          </Link>
        )}
      </footer>

      <AskTutorButton chapterSlug={chapter.slug} chapterTitle={chapter.title} />
      <ViewTracker slug={chapter.slug} />
    </article>
  );
}
