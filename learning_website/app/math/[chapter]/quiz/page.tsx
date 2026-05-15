import Link from "next/link";
import { notFound } from "next/navigation";
import { Quiz } from "@/components/Quiz";
import { getChapter, getMathChapters } from "@/lib/content";
import { getQuiz } from "@/lib/quiz/load";

interface Props {
  params: Promise<{ chapter: string }>;
}

export async function generateStaticParams() {
  const chapters = await getMathChapters();
  return chapters
    .filter((c) => c.status === "ready")
    .map((c) => ({ chapter: c.slug }));
}

export default async function ChapterQuizPage({ params }: Props) {
  const { chapter: slug } = await params;
  const chapter = await getChapter(slug);
  if (!chapter) notFound();

  const quiz = await getQuiz(slug);

  return (
    <div className="space-y-6">
      <header className="border-b border-slate-200 pb-4">
        <Link
          href={`/math/${slug}`}
          className="text-sm text-slate-500 hover:text-brand-600"
        >
          ← Back to {chapter.title}
        </Link>
        <h1 className="mt-3 text-3xl font-bold text-slate-900">
          {chapter.title} — Quiz
        </h1>
      </header>

      {quiz ? (
        <Quiz quiz={quiz} />
      ) : (
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center text-slate-500">
          <p className="text-sm">
            Quiz for this chapter is coming soon. Read the notes meanwhile.
          </p>
        </div>
      )}
    </div>
  );
}
