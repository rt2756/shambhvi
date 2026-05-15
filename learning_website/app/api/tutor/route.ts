import { NextRequest } from "next/server";
import { getChapter, getFoundation } from "@/lib/content";
import {
  getGeminiClient,
  MissingApiKeyError,
  SAFETY_SETTINGS,
  TUTOR_MODEL,
} from "@/lib/tutor/gemini";
import { buildSystemPrompt, type ChapterContext } from "@/lib/tutor/prompt";
import { checkInput, checkRateLimit, normalizeMath } from "@/lib/tutor/safety";

export const runtime = "nodejs";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface RequestBody {
  messages: ChatMessage[];
  chapterSlug?: string;
}

const MESSAGE_WINDOW = 20;

export async function POST(req: NextRequest) {
  let body: RequestBody;
  try {
    body = (await req.json()) as RequestBody;
  } catch {
    return json({ error: "Invalid JSON body" }, 400);
  }

  if (!Array.isArray(body.messages) || body.messages.length === 0) {
    return json({ error: "messages must be a non-empty array" }, 400);
  }

  const lastUser = body.messages[body.messages.length - 1];
  if (lastUser.role !== "user" || !lastUser.content?.trim()) {
    return json({ error: "Last message must be from user" }, 400);
  }

  const key = req.headers.get("x-forwarded-for") ?? "local";
  const inputCheck = checkInput(lastUser.content);
  if (!inputCheck.ok) {
    return streamCanned(inputCheck.reason);
  }
  const rateCheck = checkRateLimit(key);
  if (!rateCheck.ok) {
    return streamCanned(rateCheck.reason);
  }

  let chapterContext: ChapterContext | undefined;
  if (body.chapterSlug) {
    const chapter =
      (await getChapter(body.chapterSlug)) ??
      (await getFoundation(body.chapterSlug));
    if (chapter) {
      chapterContext = { title: chapter.title, summary: chapter.summary };
    }
  }

  let ai;
  try {
    ai = getGeminiClient();
  } catch (err) {
    if (err instanceof MissingApiKeyError) {
      return streamCanned(
        "The AI tutor isn't set up yet. A grown-up needs to add a Gemini API key to .env.local.",
      );
    }
    throw err;
  }

  const windowed = body.messages.slice(-MESSAGE_WINDOW);
  const contents = windowed.map((m) => ({
    role: m.role === "assistant" ? "model" : "user",
    parts: [{ text: m.content }],
  }));

  try {
    const stream = await ai.models.generateContentStream({
      model: TUTOR_MODEL,
      contents,
      config: {
        systemInstruction: buildSystemPrompt(chapterContext),
        safetySettings: SAFETY_SETTINGS,
        temperature: 0.7,
      },
    });

    const encoder = new TextEncoder();
    const readable = new ReadableStream({
      async start(controller) {
        try {
          for await (const chunk of stream) {
            const finish = chunk.candidates?.[0]?.finishReason;
            if (finish === "SAFETY" || finish === "PROHIBITED_CONTENT") {
              controller.enqueue(
                encoder.encode(
                  "I can't help with that. Let's try a math question instead.",
                ),
              );
              break;
            }
            const text = chunk.text;
            if (text) {
              controller.enqueue(encoder.encode(normalizeMath(text)));
            }
          }
          controller.close();
        } catch (err) {
          console.error("Tutor stream error:", err);
          controller.enqueue(
            encoder.encode(
              "\n\n(Sorry, something went wrong. Try asking again?)",
            ),
          );
          controller.close();
        }
      },
    });

    return new Response(readable, {
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Accel-Buffering": "no",
      },
    });
  } catch (err) {
    console.error("Tutor request error:", err);
    return json({ error: "Failed to call Gemini" }, 500);
  }
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function streamCanned(message: string) {
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(encoder.encode(message));
      controller.close();
    },
  });
  return new Response(stream, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}
