import Link from "next/link";
import Logo from "@/components/Logo";
import DuelDemo from "@/components/DuelDemo";

const primary = "rounded-lg bg-gold px-5 py-2.5 font-semibold text-ink transition hover:brightness-110";
const secondary = "rounded-lg border border-line px-5 py-2.5 font-medium transition hover:bg-panel";

const steps = [
  { title: "Join the queue", body: "Press Find match. You are paired with someone close to your rating." },
  { title: "Get the same problem", body: "You both see the problem, a code editor, and one shared timer." },
  { title: "Race live", body: "See whether your rival is typing, idle, or has submitted. Their code stays hidden." },
  { title: "Pass every test first", body: "Your code runs against hidden tests. The first perfect run ends the match." },
];

export default function Home() {
  return (
    <main>
      <div className="relative overflow-hidden">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              "radial-gradient(620px 420px at 0% 35%, rgba(91,140,255,.18), transparent 70%), radial-gradient(620px 420px at 100% 65%, rgba(255,107,94,.15), transparent 70%)",
          }}
        />
        <header className="relative mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <Logo />
          <nav className="flex items-center gap-2 text-sm">
            <Link href="/auth/login" className="rounded-lg px-4 py-2 text-muted transition hover:text-text">Log in</Link>
            <Link href="/auth/signup" className={primary}>Sign up</Link>
          </nav>
        </header>

        <section className="relative mx-auto grid max-w-6xl items-center gap-12 px-6 pb-24 pt-14 lg:grid-cols-[1fr_1.05fr]">
          <div>
            <h1 className="font-display text-4xl font-bold leading-[1.08] tracking-tight sm:text-5xl lg:text-6xl">
              Same problem. Two coders. One winner.
            </h1>
            <p className="mt-6 max-w-md text-lg leading-relaxed text-muted">
              Get matched with a player at your level, solve the same problem side by side, and watch their progress live.
            </p>
            <div className="mt-9 flex flex-wrap gap-3">
              <Link href="/auth/signup" className={primary}>Find a match</Link>
              <a href="#how" className={secondary}>How it works</a>
            </div>
          </div>
          <DuelDemo />
        </section>
      </div>

      <section id="how" className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="font-display text-2xl font-bold tracking-tight sm:text-3xl">How a match works</h2>
        <ol className="mt-10 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((s, i) => (
            <li key={s.title} className="border-l border-line pl-5">
              <span className="font-mono text-sm text-gold">{i + 1}</span>
              <h3 className="mt-2 font-display text-base font-medium">{s.title}</h3>
              <p className="mt-2 max-w-xs leading-relaxed text-muted">{s.body}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="mx-auto grid max-w-6xl items-center gap-12 px-6 py-20 lg:grid-cols-2">
        <div>
          <h2 className="font-display text-2xl font-bold tracking-tight sm:text-3xl">Every match moves your rating</h2>
          <p className="mt-5 max-w-md leading-relaxed text-muted">
            Everyone starts at 1200. Beat someone rated higher and you gain more. Lose to someone rated lower and you drop further. Your profile keeps the full history.
          </p>
        </div>
        <figure className="rounded-2xl border border-line bg-panel p-5">
          <svg viewBox="0 0 400 170" className="w-full" role="img" aria-label="Example rating climbing from 1200 to about 1340 over ten matches">
            <line x1="0" y1="130" x2="400" y2="130" stroke="var(--line)" strokeDasharray="4 5" />
            <text x="4" y="124" fill="var(--muted)" fontSize="11" fontFamily="var(--font-jetbrains)">1200</text>
            <polyline
              fill="none" stroke="var(--gold)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"
              points="10,130 50,118 90,124 130,98 170,104 210,78 250,86 290,56 330,62 370,30"
            />
            <circle cx="370" cy="30" r="5" fill="var(--gold)" />
          </svg>
        </figure>
      </section>

      <section className="mx-auto max-w-6xl px-6 pb-24">
        <div className="rounded-2xl border border-line bg-panel px-8 py-12 text-center">
          <h2 className="font-display text-2xl font-bold tracking-tight sm:text-3xl">Ready for your first duel?</h2>
          <p className="mx-auto mt-4 max-w-md text-muted">Sign up takes under a minute and playing is free.</p>
          <Link href="/auth/signup" className={`${primary} mt-8 inline-block`}>Create account</Link>
        </div>
      </section>

      <footer className="border-t border-line py-8 text-center text-sm text-muted">CodeArena. Free to play.</footer>
    </main>
  );
}
