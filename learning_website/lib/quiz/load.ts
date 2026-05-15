import fs from "node:fs/promises";
import path from "node:path";
import { QuizSchema, type Quiz } from "./schema";

const QUIZ_DIR = path.join(process.cwd(), "content", "math", "quizzes");

export async function getQuiz(slug: string): Promise<Quiz | null> {
  try {
    const raw = await fs.readFile(
      path.join(QUIZ_DIR, `${slug}.json`),
      "utf8",
    );
    const parsed = QuizSchema.safeParse(JSON.parse(raw));
    if (!parsed.success) {
      console.error(
        `Invalid quiz "${slug}":`,
        JSON.stringify(parsed.error.flatten(), null, 2),
      );
      return null;
    }
    return parsed.data;
  } catch {
    return null;
  }
}

export async function quizExists(slug: string): Promise<boolean> {
  try {
    await fs.access(path.join(QUIZ_DIR, `${slug}.json`));
    return true;
  } catch {
    return false;
  }
}
