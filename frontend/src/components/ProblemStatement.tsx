import { Fragment, type ReactNode } from "react";

// Renders the small Markdown subset used by problem descriptions: paragraphs, "- " bullets,
// **bold** and `code`. No HTML is injected.
function inline(text: string): ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**") && part.length > 4)
      return <strong key={i} className="font-semibold text-text">{part.slice(2, -2)}</strong>;
    if (part.startsWith("`") && part.endsWith("`") && part.length > 2)
      return <code key={i} className="rounded bg-ink px-1.5 py-0.5 font-mono text-[0.85em]">{part.slice(1, -1)}</code>;
    return <Fragment key={i}>{part}</Fragment>;
  });
}

export default function ProblemStatement({ text }: { text: string }) {
  const nodes: ReactNode[] = [];
  let bullets: string[] = [];
  let para: string[] = [];

  const flushBullets = () => {
    if (!bullets.length) return;
    nodes.push(
      <ul key={nodes.length} className="list-disc space-y-1.5 pl-5">
        {bullets.map((b, i) => <li key={i}>{inline(b)}</li>)}
      </ul>,
    );
    bullets = [];
  };
  const flushPara = () => {
    if (!para.length) return;
    nodes.push(<p key={nodes.length}>{inline(para.join(" "))}</p>);
    para = [];
  };

  for (const line of text.split("\n")) {
    if (line.startsWith("- ")) {
      flushPara();
      bullets.push(line.slice(2));
    } else if (line.trim() === "") {
      flushPara();
      flushBullets();
    } else {
      flushBullets();
      para.push(line);
    }
  }
  flushPara();
  flushBullets();

  return <div className="space-y-3 leading-relaxed text-text/90">{nodes}</div>;
}
