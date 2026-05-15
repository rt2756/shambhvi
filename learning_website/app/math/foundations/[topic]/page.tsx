import Link from "next/link";
import { notFound } from "next/navigation";
import { AskTutorButton } from "@/components/AskTutorButton";
import { getFoundation, getFoundationTopics } from "@/lib/content";
import { Markdown } from "@/lib/markdown";

interface Props {
  params: Promise<{ topic: string }>;
}

export async function generateStaticParams() {
  const topics = await getFoundationTopics();
  return topics.map((t) => ({ topic: t.slug }));
}

export default async function FoundationPage({ params }: Props) {
  const { topic: slug } = await params;
  const topic = await getFoundation(slug);
  if (!topic) notFound();

  return (
    <article className="space-y-6">
      <header className="border-b border-slate-200 pb-4">
        <Link
          href="/math"
          className="text-sm text-slate-500 hover:text-brand-600"
        >
          ← Back to Math
        </Link>
        <p className="mt-3 text-xs font-medium uppercase tracking-wide text-slate-500">
          Foundations
        </p>
        <h1 className="mt-1 text-3xl font-bold text-slate-900">
          {topic.title}
        </h1>
        {topic.summary && (
          <p className="mt-2 text-slate-600">{topic.summary}</p>
        )}
      </header>

      <div className="prose prose-slate max-w-none">
        <Markdown>{topic.content}</Markdown>
      </div>

      <footer className="flex flex-wrap gap-3 border-t border-slate-200 pt-4">
        <Link
          href={`/math/foundations/${topic.slug}/quiz`}
          className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
        >
          Take the quiz
        </Link>
      </footer>

      <AskTutorButton chapterSlug={topic.slug} chapterTitle={topic.title} />
    </article>
  );
}
