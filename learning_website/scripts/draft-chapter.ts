#!/usr/bin/env tsx
/**
 * Draft a class-7 NCERT math chapter using Gemini 2.5 Pro.
 *
 * Examples:
 *   tsx scripts/draft-chapter.ts --slug integers
 *   tsx scripts/draft-chapter.ts --all
 *   tsx scripts/draft-chapter.ts --slug integers --force
 *
 * Output lands in content/math/_drafts/<slug>.md (gitignored).
 * Parent reviews, edits, then mv to content/math/<slug>.md.
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { config as loadEnv } from "dotenv";
import {
  getGeminiClient,
  MissingApiKeyError,
  SAFETY_SETTINGS,
  DRAFTING_MODEL,
} from "../lib/tutor/gemini.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
loadEnv({ path: path.join(ROOT, ".env.local") });

interface ChapterSpec {
  slug: string;
  title: string;
  ncertChapter: number;
  order: number;
  topics: string[];
  referenceImages?: string[];
}

const CHAPTERS: ChapterSpec[] = [
  {
    slug: "integers",
    title: "Integers",
    ncertChapter: 1,
    order: 1,
    topics: [
      "Introduction to integers (positive, negative, zero)",
      "Representation on the number line",
      "Addition of integers",
      "Subtraction of integers",
      "Properties of addition and subtraction (closure, commutative, associative, identity)",
      "Multiplication of integers (sign rules)",
      "Properties of multiplication",
      "Division of integers",
      "Word problems and real-life applications",
    ],
  },
  {
    slug: "fractions-and-decimals",
    title: "Fractions and Decimals",
    ncertChapter: 2,
    order: 2,
    topics: [
      "Review of fractions: proper, improper, mixed",
      "Multiplication of a fraction by a whole number",
      "Multiplication of a fraction by a fraction",
      "Division of fractions",
      "Decimals: place value, comparing, converting",
      "Multiplication of decimals (by 10, 100, 1000 and by another decimal)",
      "Division of decimals",
      "Word problems mixing fractions and decimals",
    ],
  },
  {
    slug: "data-handling",
    title: "Data Handling",
    ncertChapter: 3,
    order: 3,
    topics: [
      "Collecting and organising data",
      "Representative values: mean, mode, median",
      "Bar graphs and double bar graphs",
      "Chance and probability (intuitive introduction)",
    ],
  },
  {
    slug: "simple-equations",
    title: "Simple Equations",
    ncertChapter: 4,
    order: 4,
    topics: [
      "What is an equation? Variables vs constants",
      "Setting up equations from word statements",
      "Solving equations by trial and error",
      "Systematic methods: adding/subtracting/multiplying/dividing both sides",
      "Transposition",
      "Word problems leading to one-variable equations",
    ],
  },
  {
    slug: "lines-and-angles",
    title: "Lines and Angles",
    ncertChapter: 5,
    order: 5,
    topics: [
      "Recap: types of angles",
      "Complementary and supplementary angles",
      "Adjacent angles, linear pair, vertically opposite angles",
      "Parallel lines and a transversal",
      "Corresponding angles, alternate interior angles, co-interior angles",
      "Checking whether two lines are parallel",
    ],
    referenceImages: ["/images/angles.png", "/images/angles-diagram.png"],
  },
  {
    slug: "triangle-and-its-properties",
    title: "The Triangle and Its Properties",
    ncertChapter: 6,
    order: 6,
    topics: [
      "Triangle terminology: vertices, sides, angles",
      "Medians and altitudes",
      "Exterior angle and its property",
      "Angle sum property (interior angles add to 180°)",
      "Two special triangles: equilateral and isosceles",
      "Sum of two sides > third side (triangle inequality)",
      "Right-angled triangles and the Pythagoras property (introduction)",
    ],
  },
  {
    slug: "comparing-quantities",
    title: "Comparing Quantities",
    ncertChapter: 7,
    order: 7,
    topics: [
      "Equivalent ratios and proportion",
      "Unitary method",
      "Percentage: meaning, converting to/from fractions and decimals",
      "Use of percentage (everyday situations)",
      "Profit and loss (cost price, selling price, profit/loss %)",
      "Simple interest",
    ],
  },
  {
    slug: "rational-numbers",
    title: "Rational Numbers",
    ncertChapter: 8,
    order: 8,
    topics: [
      "What is a rational number? Positive and negative rationals",
      "Representation on the number line",
      "Rational numbers in standard form",
      "Comparing rational numbers",
      "Operations: addition, subtraction, multiplication, division of rationals",
    ],
  },
  {
    slug: "perimeter-and-area",
    title: "Perimeter and Area",
    ncertChapter: 9,
    order: 9,
    topics: [
      "Squares and rectangles (recap)",
      "Area of a parallelogram",
      "Area of a triangle",
      "Circumference of a circle",
      "Area of a circle",
      "Applications and conversion of units (cm² ↔ m²)",
    ],
  },
  {
    slug: "algebraic-expressions",
    title: "Algebraic Expressions",
    ncertChapter: 10,
    order: 10,
    topics: [
      "Variables, constants, terms, coefficients",
      "Like and unlike terms",
      "Monomials, binomials, polynomials",
      "Addition and subtraction of algebraic expressions",
      "Finding the value of an expression by substitution",
      "Using algebraic expressions to describe number patterns",
    ],
  },
  {
    slug: "exponents-and-powers",
    title: "Exponents and Powers",
    ncertChapter: 11,
    order: 11,
    topics: [
      "Meaning of exponent: base and power",
      "Laws of exponents (product, quotient, power of a power, zero exponent)",
      "Numbers in standard form (scientific notation)",
      "Comparing very large and very small numbers",
    ],
  },
  {
    slug: "symmetry",
    title: "Symmetry",
    ncertChapter: 12,
    order: 12,
    topics: [
      "Lines of symmetry for regular polygons",
      "Rotational symmetry: centre, angle, order",
      "Lines of symmetry AND rotational symmetry together",
    ],
  },
  {
    slug: "visualising-solid-shapes",
    title: "Visualising Solid Shapes",
    ncertChapter: 13,
    order: 13,
    topics: [
      "Plane shapes vs solid shapes (2D vs 3D)",
      "Faces, edges, vertices",
      "Nets of cubes, cuboids, cones, cylinders",
      "Drawing solids on flat paper (oblique, isometric sketches)",
      "Cross-sections and views (top, front, side)",
    ],
  },
];

function parseArgs(argv: string[]): { slugs: string[]; force: boolean } {
  const args = argv.slice(2);
  const force = args.includes("--force");
  if (args.includes("--all")) {
    return { slugs: CHAPTERS.map((c) => c.slug), force };
  }
  const idx = args.indexOf("--slug");
  if (idx >= 0 && args[idx + 1]) {
    return { slugs: [args[idx + 1]], force };
  }
  console.error("Usage: tsx scripts/draft-chapter.ts --slug <slug> | --all [--force]");
  console.error("Available slugs:");
  for (const c of CHAPTERS) console.error(`  ${c.slug}  (ch ${c.ncertChapter})`);
  process.exit(1);
}

function buildUserPrompt(spec: ChapterSpec): string {
  return [
    `Please draft the chapter file for: **${spec.title}** (NCERT class 7, chapter ${spec.ncertChapter}).`,
    "",
    "Use this front-matter:",
    "```",
    `slug: ${spec.slug}`,
    `title: "${spec.title}"`,
    `ncertChapter: ${spec.ncertChapter}`,
    `order: ${spec.order}`,
    `estimatedMinutes: <you decide based on length>`,
    `summary: "<one short sentence>"`,
    `prerequisites: []`,
    "```",
    "",
    "Cover these subtopics in order, each as its own `##` section:",
    ...spec.topics.map((t, i) => `${i + 1}. ${t}`),
    "",
    spec.referenceImages?.length
      ? `Reference images already available (you MAY embed these in the markdown where helpful): ${spec.referenceImages.join(", ")}`
      : "No reference images available. Where a diagram would help, leave a placeholder like `![placeholder: ...](/images/...)`.",
    "",
    "Output the complete markdown file now. Do not wrap it in code fences.",
  ].join("\n");
}

async function draftOne(spec: ChapterSpec, force: boolean): Promise<void> {
  const draftsDir = path.join(ROOT, "content", "math", "_drafts");
  await fs.mkdir(draftsDir, { recursive: true });
  const outPath = path.join(draftsDir, `${spec.slug}.md`);

  if (!force) {
    const exists = await fs.stat(outPath).catch(() => null);
    if (exists) {
      console.log(`skip ${spec.slug} — draft already exists (use --force to overwrite)`);
      return;
    }
  }

  const systemPath = path.join(ROOT, "prompts", "chapter-system.md");
  const systemInstruction = await fs.readFile(systemPath, "utf8");
  const userPrompt = buildUserPrompt(spec);

  const ai = getGeminiClient();
  console.log(`drafting ${spec.slug}…`);
  const response = await ai.models.generateContent({
    model: DRAFTING_MODEL,
    contents: [{ role: "user", parts: [{ text: userPrompt }] }],
    config: {
      systemInstruction,
      safetySettings: SAFETY_SETTINGS,
      temperature: 0.8,
    },
  });

  const text = response.text;
  if (!text) {
    console.error(`! ${spec.slug} returned empty text`);
    return;
  }

  await fs.writeFile(outPath, text, "utf8");
  console.log(`wrote ${path.relative(ROOT, outPath)} (${text.length} chars)`);
}

async function main() {
  const { slugs, force } = parseArgs(process.argv);

  try {
    getGeminiClient();
  } catch (err) {
    if (err instanceof MissingApiKeyError) {
      console.error(err.message);
      process.exit(1);
    }
    throw err;
  }

  const specs = slugs.map((slug) => {
    const spec = CHAPTERS.find((c) => c.slug === slug);
    if (!spec) {
      console.error(`Unknown slug: ${slug}`);
      process.exit(1);
    }
    return spec;
  });

  for (const spec of specs) {
    try {
      await draftOne(spec, force);
    } catch (err) {
      console.error(`! ${spec.slug} failed:`, err);
    }
  }

  console.log(`\nReview drafts at content/math/_drafts/ and mv to content/math/ when ready.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
