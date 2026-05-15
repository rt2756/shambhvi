import Link from "next/link";

export default function NotFound() {
  return (
    <div className="space-y-4 text-center">
      <h1 className="text-3xl font-bold text-slate-900">Page not found</h1>
      <p className="text-slate-600">
        This page hasn't been added yet, or the link is wrong.
      </p>
      <Link
        href="/"
        className="inline-block rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
      >
        Go home
      </Link>
    </div>
  );
}
