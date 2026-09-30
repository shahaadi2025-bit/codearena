"use client";

import { useEffect, useState } from "react";

const TOTAL = 5;

type Side = { passed: number; status: "Typing" | "Idle" | "Submitted" };
type Frame = { me: Side; rival: Side; won: boolean };

const frames: Frame[] = [
  { me: { passed: 0, status: "Typing" }, rival: { passed: 0, status: "Typing" }, won: false },
  { me: { passed: 0, status: "Typing" }, rival: { passed: 2, status: "Submitted" }, won: false },
  { me: { passed: 3, status: "Submitted" }, rival: { passed: 2, status: "Typing" }, won: false },
  { me: { passed: 3, status: "Typing" }, rival: { passed: 4, status: "Submitted" }, won: false },
  { me: { passed: 5, status: "Submitted" }, rival: { passed: 4, status: "Idle" }, won: true },
];

const tones = {
  blue: { border: "border-blue/60", bar: "bg-blue", text: "text-blue", dot: "bg-blue" },
  coral: { border: "border-coral/60", bar: "bg-coral", text: "text-coral", dot: "bg-coral" },
};

const myCode = `def solve(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return seen[target - x], i
        seen[x] = i`;

const rivalCode = `for (int i = 0; i < n; i++)
  for (int j = i + 1; j < n; j++)
    if (a[i] + a[j] == t)
      return {i, j};`;

function Panel({
  name, language, tone, side, code, delta, winner,
}: {
  name: string; language: string; tone: "blue" | "coral"; side: Side;
  code: string; delta: string | null; winner: boolean;
}) {
  const t = tones[tone];
  return (
    <div className={`flex flex-col rounded-xl border bg-panel p-4 transition-colors duration-500 ${winner ? "border-gold" : t.border}`}>
      <div className="flex items-center justify-between gap-2">
        <span className={`font-display text-sm font-medium ${t.text}`}>{name}</span>
        <span className="rounded-md border border-line px-2 py-0.5 font-mono text-xs text-muted">{language}</span>
      </div>

      <pre className="my-3 flex-1 overflow-hidden font-mono text-[11px] leading-relaxed text-muted">{code}</pre>

      <div className="flex gap-1" role="presentation">
        {Array.from({ length: TOTAL }).map((_, i) => (
          <span key={i} className={`h-1.5 flex-1 rounded-full transition-colors duration-500 ${i < side.passed ? t.bar : "bg-line"}`} />
        ))}
      </div>

      <div className="mt-2.5 flex items-center justify-between text-xs">
        <span className="flex items-center gap-1.5 text-muted">
          <span className={`h-1.5 w-1.5 rounded-full ${t.dot}`} style={side.status === "Typing" ? { animation: "pulse-dot 1s infinite" } : undefined} />
          {side.status}
        </span>
        <span className="font-mono text-muted">{side.passed}/{TOTAL} tests</span>
      </div>

      <div className={`mt-2 h-5 text-sm font-semibold transition-opacity duration-500 ${delta ? "opacity-100" : "opacity-0"} ${winner ? "text-gold" : "text-muted"}`}>
        {delta ?? "\u00a0"}
      </div>
    </div>
  );
}

export default function DuelDemo() {
  const [i, setI] = useState(0);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setI(frames.length - 1);
      return;
    }
    const last = i === frames.length - 1;
    const id = setTimeout(() => setI((n) => (n + 1) % frames.length), last ? 3800 : 1500);
    return () => clearTimeout(id);
  }, [i]);

  const f = frames[i];

  return (
    <div>
      <p className="sr-only">
        Example match: two players solve Two Sum. The rival passes four of five tests, then you pass all five first and win.
      </p>
      <div aria-hidden="true" className="rounded-2xl border border-line bg-ink/60 p-4 backdrop-blur">
        <div className="mb-3 flex items-center justify-between px-1 text-xs">
          <span className="font-display font-medium">Two Sum</span>
          <span className="rounded-md bg-panel px-2 py-0.5 font-mono text-muted">Medium</span>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <Panel name="You" language="Python" tone="blue" side={f.me} code={myCode} winner={f.won} delta={f.won ? "+18 rating" : null} />
          <Panel name="Rival" language="C++" tone="coral" side={f.rival} code={rivalCode} winner={false} delta={f.won ? "\u221218 rating" : null} />
        </div>
      </div>
    </div>
  );
}
