import { z } from "zod";

export const QuizQuestionSchema = z.object({
  id: z.string(),
  type: z.literal("mcq"),
  difficulty: z.enum(["easy", "medium", "hard"]),
  prompt: z.string(),
  options: z.array(z.string()).length(4),
  correctIndex: z.number().int().min(0).max(3),
  explanation: z.string(),
  topicTags: z.array(z.string()).optional(),
});

export const QuizSchema = z.object({
  slug: z.string(),
  title: z.string(),
  version: z.number().int().default(1),
  questions: z.array(QuizQuestionSchema).min(1),
});

export type QuizQuestion = z.infer<typeof QuizQuestionSchema>;
export type Quiz = z.infer<typeof QuizSchema>;

export interface QuizResult {
  slug: string;
  total: number;
  correct: number;
  perQuestion: Record<string, boolean>;
}
