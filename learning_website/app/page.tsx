import Link from "next/link";
import { getMathChapters, getFoundationTopics } from "@/lib/content";

export default async function Home() {
  const chapters = await getMathChapters();
  const foundations = await getFoundationTopics();
  const readyChapters = chapters.filter((c) => c.status === "ready").length;
  const totalReady = readyChapters + foundations.length;

  return (
    <div className="space-y-10">
      <section className="rounded-2xl bg-gradient-to-br from-brand-50 to-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-slate-900">
          Hi Shambhvi! 👋
        </h1>
        <p className="mt-3 max-w-2xl text-slate-700">
          This is your math practice space. Pick a chapter to read, take a
          quiz to test what you remember, or ask the tutor anything you don't
          understand.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/math"
            className="rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-700"
          >
            Start learning
          </Link>
          <Link
            href="/tutor"
            className="rounded-lg border border-slate-300 bg-white px-5 py-2.5 text-sm font-medium text-slate-700 hover:border-brand-600 hover:text-brand-600"
          >
            Ask the tutor
          </Link>
        </div>
      </section>

      <section>
        <div className="mb-4 flex items-baseline justify-between">
          <h2 className="text-xl font-semibold text-slate-900">
            What's inside
          </h2>
          <span className="text-sm text-slate-500">
            {totalReady} topics ready
          </span>
        </div>
        <div className="grid gap-4 sm:grid-cols-3">
          <FeatureCard
            title="Foundations"
            count={foundations.length}
            href="/math"
            description="Tables, factors, fractions basics — the building blocks."
          />
          <FeatureCard
            title="NCERT Class 7"
            count={readyChapters}
            href="/math"
            description={`${readyChapters} of ${chapters.length} chapters drafted so far.`}
          />
          <FeatureCard
            title="AI Tutor"
            href="/tutor"
            description="Stuck on a problem? Ask in plain English."
          />
        </div>
      </section>
    </div>
  );
}

function FeatureCard({
  title,
  count,
  href,
  description,
}: {
  title: string;
  count?: number;
  href: string;
  description: string;
}) {
  return (
    <Link
      href={href}
      className="block rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-brand-600 hover:shadow"
    >
      <div className="flex items-baseline justify-between">
        <h3 className="text-base font-semibold text-slate-900">{title}</h3>
        {count !== undefined && (
          <span className="text-xs font-medium text-slate-500">
            {count}
          </span>
        )}
      </div>
      <p className="mt-2 text-sm text-slate-600">{description}</p>
    </Link>
  );
}
