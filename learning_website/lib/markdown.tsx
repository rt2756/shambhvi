import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

interface Props {
  children: string;
}

export function Markdown({ children }: Props) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm, remarkMath]}
      rehypePlugins={[[rehypeKatex, { strict: false }]]}
      components={{
        img: ({ src, alt }) =>
          src ? (
            <img
              src={src}
              alt={alt ?? ""}
              className="my-4 rounded-lg border border-slate-200"
              loading="lazy"
            />
          ) : null,
        a: ({ href, children }) => (
          <a
            href={href}
            className="text-brand-600 underline-offset-2 hover:underline"
          >
            {children}
          </a>
        ),
        table: ({ children }) => (
          <div className="my-4 overflow-x-auto">
            <table className="min-w-full border-collapse text-sm">
              {children}
            </table>
          </div>
        ),
        th: ({ children }) => (
          <th className="border border-slate-300 bg-slate-100 px-2 py-1 text-left font-semibold">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="border border-slate-300 px-2 py-1">{children}</td>
        ),
      }}
    >
      {children}
    </ReactMarkdown>
  );
}
