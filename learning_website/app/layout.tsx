import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Shambhvi — Class 7 Math",
  description: "Shambhvi's class 7 CBSE math learning site",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        <header className="border-b border-slate-200 bg-white">
          <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
            <Link
              href="/"
              className="text-lg font-semibold text-slate-900 hover:text-brand-600"
            >
              Shambhvi
            </Link>
            <nav className="flex items-center gap-6 text-sm text-slate-600">
              <Link href="/math" className="hover:text-brand-600">
                Math
              </Link>
              <Link href="/tutor" className="hover:text-brand-600">
                Tutor
              </Link>
              <Link href="/progress" className="hover:text-brand-600">
                Progress
              </Link>
            </nav>
          </div>
        </header>
        <main className="mx-auto w-full max-w-5xl flex-1 px-6 py-8">
          {children}
        </main>
        <footer className="border-t border-slate-200 bg-white">
          <div className="mx-auto max-w-5xl px-6 py-4 text-xs text-slate-500">
            Made with love for Shambhvi
          </div>
        </footer>
      </body>
    </html>
  );
}
