import fs from "node:fs/promises";
import path from "node:path";
import matter from "gray-matter";

const MATH_DIR = path.join(process.cwd(), "content", "math");
const CHAPTERS_DIR = path.join(MATH_DIR, "chapters");
const FOUNDATIONS_DIR = path.join(MATH_DIR, "foundations");

export const NCERT_CHAPTER_ORDER = [
  "integers",
  "fractions-and-decimals",
  "data-handling",
  "simple-equations",
  "lines-and-angles",
  "triangle-and-its-properties",
  "comparing-quantities",
  "rational-numbers",
  "perimeter-and-area",
  "algebraic-expressions",
  "exponents-and-powers",
  "symmetry",
  "visualising-solid-shapes",
] as const;

export type ChapterStatus = "ready" | "coming-soon";

export interface ChapterMeta {
  slug: string;
  title: string;
  ncertChapter?: number;
  order?: number;
  estimatedMinutes?: number;
  summary?: string;
  prerequisites?: string[];
  nextChapter?: string;
}

export interface ChapterEntry extends ChapterMeta {
  status: ChapterStatus;
}

export interface Chapter extends ChapterMeta {
  content: string;
}

export async function getMathChapters(): Promise<ChapterEntry[]> {
  const files = new Set(await safeReadDir(CHAPTERS_DIR));
  return Promise.all(
    NCERT_CHAPTER_ORDER.map(async (slug, i) => {
      const filename = `${slug}.md`;
      if (files.has(filename)) {
        const meta = await readMeta(path.join(CHAPTERS_DIR, filename));
        return { ...meta, status: "ready" as const };
      }
      return {
        slug,
        title: titleFromSlug(slug),
        ncertChapter: i + 1,
        order: i + 1,
        status: "coming-soon" as const,
      };
    }),
  );
}

export async function getFoundationTopics(): Promise<ChapterEntry[]> {
  const files = await safeReadDir(FOUNDATIONS_DIR);
  const entries = await Promise.all(
    files
      .filter((f) => f.endsWith(".md"))
      .map(async (f) => {
        const meta = await readMeta(path.join(FOUNDATIONS_DIR, f));
        return { ...meta, status: "ready" as const };
      }),
  );
  return entries.sort((a, b) => {
    const ao = a.order ?? 99;
    const bo = b.order ?? 99;
    if (ao !== bo) return ao - bo;
    return a.title.localeCompare(b.title);
  });
}

export async function getChapter(slug: string): Promise<Chapter | null> {
  return readChapter(path.join(CHAPTERS_DIR, `${slug}.md`));
}

export async function getFoundation(topic: string): Promise<Chapter | null> {
  return readChapter(path.join(FOUNDATIONS_DIR, `${topic}.md`));
}

async function readChapter(filepath: string): Promise<Chapter | null> {
  try {
    const raw = await fs.readFile(filepath, "utf8");
    const { data, content } = matter(raw);
    const slug = (data.slug as string) ?? path.basename(filepath, ".md");
    return {
      slug,
      title: (data.title as string) ?? titleFromSlug(slug),
      ncertChapter: data.ncertChapter as number | undefined,
      order: data.order as number | undefined,
      estimatedMinutes: data.estimatedMinutes as number | undefined,
      summary: data.summary as string | undefined,
      prerequisites: data.prerequisites as string[] | undefined,
      nextChapter: data.nextChapter as string | undefined,
      content,
    };
  } catch {
    return null;
  }
}

async function readMeta(filepath: string): Promise<ChapterMeta> {
  const raw = await fs.readFile(filepath, "utf8");
  const { data } = matter(raw);
  const slug = (data.slug as string) ?? path.basename(filepath, ".md");
  return {
    slug,
    title: (data.title as string) ?? titleFromSlug(slug),
    ncertChapter: data.ncertChapter as number | undefined,
    order: data.order as number | undefined,
    estimatedMinutes: data.estimatedMinutes as number | undefined,
    summary: data.summary as string | undefined,
    prerequisites: data.prerequisites as string[] | undefined,
    nextChapter: data.nextChapter as string | undefined,
  };
}

async function safeReadDir(dir: string): Promise<string[]> {
  try {
    return await fs.readdir(dir);
  } catch {
    return [];
  }
}

function titleFromSlug(slug: string): string {
  return slug
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}
