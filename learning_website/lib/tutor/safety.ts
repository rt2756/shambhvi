// First-line content filter — runs before any Gemini call.
const DENYLIST: RegExp[] = [
  /\b(porn|nude|naked|sexual|sex\s*chat)\b/i,
  /\b(gambling|cocaine|heroin|marijuana|weed|meth|alcohol|whisky|whiskey|beer|vodka)\b/i,
  /\b(kill\s*(myself|my\s*self|her|him)|suicide|self\s*harm)\b/i,
  /\b(hate\s*(you|her|him|jews|muslims|hindus|christians|blacks|whites))\b/i,
];

export const REDIRECT_MESSAGE =
  "Let's keep our chat about your studies. Ask your parents or teacher about that. Want to try a math question instead?";

export function checkInput(
  text: string,
): { ok: true } | { ok: false; reason: string } {
  for (const pattern of DENYLIST) {
    if (pattern.test(text)) return { ok: false, reason: REDIRECT_MESSAGE };
  }
  return { ok: true };
}

const buckets = new Map<string, number[]>();
const SHORT_WINDOW_MS = 5 * 60 * 1000;
const SHORT_LIMIT = 30;
const LONG_WINDOW_MS = 24 * 60 * 60 * 1000;
const LONG_LIMIT = 200;

export function checkRateLimit(
  key: string,
): { ok: true } | { ok: false; reason: string } {
  const now = Date.now();
  const arr = (buckets.get(key) ?? []).filter(
    (t) => now - t < LONG_WINDOW_MS,
  );

  const shortCount = arr.filter((t) => now - t < SHORT_WINDOW_MS).length;
  if (shortCount >= SHORT_LIMIT) {
    return {
      ok: false,
      reason:
        "Whoa, that's a lot of questions in a short time! Take a 5-minute break and try again.",
    };
  }
  if (arr.length >= LONG_LIMIT) {
    return {
      ok: false,
      reason:
        "You've asked a lot today! Let's pause and come back tomorrow with fresh energy.",
    };
  }

  arr.push(now);
  buckets.set(key, arr);
  return { ok: true };
}

const SUPERSCRIPT_MAP: Record<string, string> = {
  "⁰": "0",
  "¹": "1",
  "²": "2",
  "³": "3",
  "⁴": "4",
  "⁵": "5",
  "⁶": "6",
  "⁷": "7",
  "⁸": "8",
  "⁹": "9",
};

// Normalize Gemini output: convert Unicode math glyphs back to KaTeX so
// react-markdown + rehype-katex can render them properly.
export function normalizeMath(text: string): string {
  return text
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
    .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]+/g, (match) => {
      const digits = [...match]
        .map((c) => SUPERSCRIPT_MAP[c] ?? c)
        .join("");
      return `$^{${digits}}$`;
    });
}
