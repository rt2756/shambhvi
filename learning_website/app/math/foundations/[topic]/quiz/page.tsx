import Link from "next/link";
import { notFound } from "next/navigation";
import { Quiz } from "@/components/Quiz";
import { getFoundation, getFoundationTopics } from "@/lib/content";
import { getQuiz } from "@/lib/quiz/load";

interface Props {
  params: Promise<{ topic: string }>;
}

export async function generateStaticParams() {
  const topics = await getFoundationTopics();
  return topics.map((t) => ({ topic: t.slug }));
}

export default async function FoundationQuizPage({ params }: Props) {
  const { topic: slug } = await params;
  const topic = await getFoundation(slug);
  if (!topic) notFound();

  const quiz = await getQuiz(slug);

  return (
    <div className="space-y-6">
      <header className="border-b border-slate-200 pb-4">
        <Link
          href={`/math/foundations/${slug}`}
          className="text-sm text-slate-500 hover:text-brand-600"
        >
          ← Back to {topic.title}
        </Link>
        <h1 className="mt-3 text-3xl font-bold text-slate-900">
          {topic.title} — Quiz
        </h1>
      </header>

      {quiz ? (
        <Quiz quiz={quiz} />
      ) : (
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center text-slate-500">
          <p className="text-sm">
            Quiz for this topic is coming soon. Read the notes meanwhile.
          </p>
        </div>
      )}
    </div>
  );
}
