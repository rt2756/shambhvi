"use client";

import { useEffect, useRef, useState } from "react";
import { Markdown } from "@/lib/markdown";
import { recordTutorMessage } from "@/lib/progress/events";

interface Props {
  chapterSlug?: string;
  chapterTitle?: string;
  variant?: "page" | "panel";
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const STORAGE_PREFIX = "shambhvi-tutor-chat-v1";

function storageKey(slug?: string) {
  return slug ? `${STORAGE_PREFIX}:${slug}` : `${STORAGE_PREFIX}:global`;
}

export function TutorChat({
  chapterSlug,
  chapterTitle,
  variant = "page",
}: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    try {
      const raw = sessionStorage.getItem(storageKey(chapterSlug));
      if (raw) setMessages(JSON.parse(raw));
    } catch {
      // ignore
    }
  }, [chapterSlug]);

  useEffect(() => {
    try {
      sessionStorage.setItem(
        storageKey(chapterSlug),
        JSON.stringify(messages),
      );
    } catch {
      // quota — ignore
    }
  }, [messages, chapterSlug]);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, streaming]);

  async function send() {
    const trimmed = input.trim();
    if (!trimmed || streaming) return;
    setError(null);

    const next: ChatMessage[] = [
      ...messages,
      { role: "user", content: trimmed },
      { role: "assistant", content: "" },
    ];
    setMessages(next);
    setInput("");
    setStreaming(true);
    recordTutorMessage();

    try {
      const res = await fetch("/api/tutor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: next.slice(0, -1),
          chapterSlug,
        }),
      });

      if (!res.ok || !res.body) {
        const errBody = await res.json().catch(() => ({}));
        throw new Error(errBody.error ?? `HTTP ${res.status}`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        setMessages((prev) => {
          const copy = [...prev];
          const last = copy[copy.length - 1];
          if (last?.role === "assistant") {
            copy[copy.length - 1] = { ...last, content: buffer };
          }
          return copy;
        });
      }
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Something went wrong";
      setError(msg);
      setMessages((prev) => {
        const copy = [...prev];
        if (copy[copy.length - 1]?.content === "") copy.pop();
        return copy;
      });
    } finally {
      setStreaming(false);
      inputRef.current?.focus();
    }
  }

  function clear() {
    setMessages([]);
    setError(null);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      void send();
    }
  }

  const containerClass =
    variant === "page"
      ? "flex h-[70vh] flex-col rounded-2xl border border-slate-200 bg-white shadow-sm"
      : "flex h-full flex-col";

  return (
    <div className={containerClass}>
      <div
        ref={scrollRef}
        className="flex-1 space-y-4 overflow-y-auto p-4"
        aria-live="polite"
      >
        {messages.length === 0 ? (
          <EmptyState chapterTitle={chapterTitle} />
        ) : (
          messages.map((m, i) => <MessageBubble key={i} message={m} />)
        )}
        {streaming && (
          <div className="text-xs italic text-slate-400">Thinking…</div>
        )}
      </div>

      {error && (
        <div className="border-t border-rose-200 bg-rose-50 px-4 py-2 text-sm text-rose-700">
          {error}
        </div>
      )}

      <form
        className="flex items-end gap-2 border-t border-slate-200 p-3"
        onSubmit={(e) => {
          e.preventDefault();
          void send();
        }}
      >
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder={
            chapterTitle
              ? `Ask about ${chapterTitle}…`
              : "Ask any math question…"
          }
          rows={2}
          className="flex-1 resize-none rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-600 focus:outline-none focus:ring-1 focus:ring-brand-600"
          disabled={streaming}
        />
        <div className="flex flex-col gap-2">
          <button
            type="submit"
            disabled={streaming || !input.trim()}
            className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            Ask
          </button>
          {messages.length > 0 && (
            <button
              type="button"
              onClick={clear}
              disabled={streaming}
              className="text-xs text-slate-500 hover:text-slate-700"
            >
              Clear
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

function MessageBubble({ message }: { message: ChatMessage }) {
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-2xl rounded-br-md bg-brand-600 px-4 py-2 text-sm text-white">
          {message.content}
        </div>
      </div>
    );
  }
  return (
    <div className="flex justify-start">
      <div className="prose prose-sm max-w-[85%] rounded-2xl rounded-bl-md bg-slate-100 px-4 py-2 text-slate-900">
        {message.content ? (
          <Markdown>{message.content}</Markdown>
        ) : (
          <span className="text-slate-400">…</span>
        )}
      </div>
    </div>
  );
}

function EmptyState({ chapterTitle }: { chapterTitle?: string }) {
  return (
    <div className="flex h-full items-center justify-center text-center text-sm text-slate-500">
      <div>
        <p className="mb-2 text-base font-medium text-slate-700">
          Hi Shambhvi! 👋
        </p>
        <p>
          {chapterTitle
            ? `Ask me anything about ${chapterTitle}.`
            : "Ask me any math question. I'm here to help you think it through."}
        </p>
        <p className="mt-3 text-xs text-slate-400">
          Tip: press <kbd className="rounded border px-1">Enter</kbd> to send,{" "}
          <kbd className="rounded border px-1">Shift+Enter</kbd> for a new line.
        </p>
      </div>
    </div>
  );
}
