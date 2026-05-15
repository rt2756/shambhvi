#!/usr/bin/env tsx
/**
 * One-off migration: split the legacy mathematics.md into the per-topic
 * foundation files. Applies only safe KaTeX conversions (Unicode fractions,
 * "N power K", "N degrees") and leaves everything else for the parent to
 * KaTeX-ify during review. Idempotent — re-running overwrites the outputs.
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP_ROOT = path.resolve(HERE, "..");
const REPO_ROOT = path.resolve(APP_ROOT, "..");
const SOURCE = path.join(REPO_ROOT, "mathematics.md");
const TARGET_DIR = path.join(APP_ROOT, "content", "math", "foundations");

interface Section {
  slug: string;
  title: string;
  order: number;
  summary: string;
  startLine: number; // 1-indexed inclusive
  endLine: number;
  stripFirstHeading?: boolean;
}

const SECTIONS: Section[] = [
  {
    slug: "multiplication-tables",
    title: "Multiplication Tables (1–20)",
    order: 1,
    summary: "Times-table grid from 1×1 through 20×20.",
    startLine: 4,
    endLine: 16,
  },
  {
    slug: "angles-basics",
    title: "Angles: The Basics",
    order: 2,
    summary:
      "Acute, obtuse, reflex, straight, right angles, and clock angle math.",
    startLine: 20,
    endLine: 33,
    stripFirstHeading: true,
  },
  {
    slug: "polygons",
    title: "Polygons and Shapes",
    order: 3,
    summary:
      "Triangles, quadrilaterals, pentagons, and other regular polygons.",
    startLine: 35,
    endLine: 69,
    stripFirstHeading: true,
  },
  {
    slug: "measurements",
    title: "Measurements",
    order: 4,
    summary: "Length, weight, and capacity units and conversions.",
    startLine: 71,
    endLine: 102,
    stripFirstHeading: true,
  },
  {
    slug: "place-value",
    title: "Place Value and Large Numbers",
    order: 5,
    summary:
      "Hundred, thousand, million, billion, trillion as powers of 10.",
    startLine: 104,
    endLine: 110,
    stripFirstHeading: true,
  },
  {
    slug: "number-types",
    title: "Types of Numbers",
    order: 6,
    summary:
      "Natural, whole, integers, positive/negative, prime, composite, even, odd.",
    startLine: 112,
    endLine: 162,
    stripFirstHeading: true,
  },
  {
    slug: "factors-and-multiples",
    title: "Factors and Multiples",
    order: 7,
    summary:
      "Factors, multiples, primes, divisibility tests, prime factorisation, co-prime numbers.",
    startLine: 164,
    endLine: 401,
    stripFirstHeading: true,
  },
  {
    slug: "fractions-basics",
    title: "Fractions: The Basics",
    order: 8,
    summary:
      "Types of fractions, conversions, comparison, addition, multiplication, and division.",
    startLine: 403,
    endLine: 500,
    stripFirstHeading: true,
  },
];

function applySafeKatex(text: string): string {
  return (
    text
      // Unicode fractions
      .replace(/¼/g, "$\\frac{1}{4}$")
      .replace(/½/g, "$\\frac{1}{2}$")
      .replace(/¾/g, "$\\frac{3}{4}$")
      .replace(/⅓/g, "$\\frac{1}{3}$")
      .replace(/⅔/g, "$\\frac{2}{3}$")
      .replace(/⅕/g, "$\\frac{1}{5}$")
      .replace(/⅖/g, "$\\frac{2}{5}$")
      .replace(/⅗/g, "$\\frac{3}{5}$")
      .replace(/⅘/g, "$\\frac{4}{5}$")
      .replace(/⅙/g, "$\\frac{1}{6}$")
      .replace(/⅛/g, "$\\frac{1}{8}$")
      // "10 power 2" → "$10^{2}$"
      .replace(/(\d+)\s+power\s+(\d+)/g, "$$$1^{$2}$$")
      // "90 degrees" → "90°" (no LaTeX needed)
      .replace(/(\d+)\s+degrees?\b/g, "$1°")
      // Relative "images/..." → absolute "/images/..." for Next.js public/
      .replace(/\]\(images\//g, "](/images/")
  );
}

function buildFrontmatter(s: Section): string {
  return [
    "---",
    `slug: ${s.slug}`,
    `title: ${JSON.stringify(s.title)}`,
    `order: ${s.order}`,
    `summary: ${JSON.stringify(s.summary)}`,
    "---",
    "",
    '<!-- Migrated from mathematics.md. Math expressions like "2 / 3" or "2 * 3" should be converted to KaTeX ($\\frac{2}{3}$, $2 \\times 3$) during review. -->',
    "",
    `# ${s.title}`,
    "",
  ].join("\n");
}

async function main() {
  const raw = await fs.readFile(SOURCE, "utf8");
  const lines = raw.split("\n");
  await fs.mkdir(TARGET_DIR, { recursive: true });

  for (const section of SECTIONS) {
    let body = lines.slice(section.startLine - 1, section.endLine).join("\n");
    if (section.stripFirstHeading) {
      // Strip leading H1 or H2 so the frontmatter-derived title doesn't duplicate.
      body = body.replace(/^#{1,2}\s.*\n+/, "");
    }
    body = applySafeKatex(body);
    const out = buildFrontmatter(section) + body.trim() + "\n";
    const outPath = path.join(TARGET_DIR, `${section.slug}.md`);
    await fs.writeFile(outPath, out, "utf8");
    const rel = path.relative(APP_ROOT, outPath);
    console.log(
      `wrote ${rel}  (lines ${section.startLine}-${section.endLine})`,
    );
  }

  console.log(
    `\nDone. ${SECTIONS.length} foundation files written to ${path.relative(APP_ROOT, TARGET_DIR)}/`,
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
