import Link from "next/link";
import type { ReactNode } from "react";
import Logo from "@/components/Logo";

export default function AuthShell({
  title, subtitle, children, footer,
}: { title: string; subtitle: string; children: ReactNode; footer: ReactNode }) {
  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <div className="flex flex-col px-6 py-6 sm:px-12">
        <Link href="/" aria-label="CodeArena home" className="w-fit">
          <Logo />
        </Link>
        <main className="mx-auto flex w-full max-w-sm flex-1 flex-col justify-center py-12">
          <h1 className="font-display text-3xl font-bold tracking-tight">{title}</h1>
          <p className="mt-3 text-muted">{subtitle}</p>
          <div className="mt-8">{children}</div>
          <p className="mt-8 text-sm text-muted">{footer}</p>
        </main>
      </div>

      <aside aria-hidden="true" className="relative hidden overflow-hidden border-l border-line bg-panel lg:block">
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(90deg, rgba(91,140,255,.16) 0%, rgba(91,140,255,.16) 50%, rgba(255,107,94,.14) 50%, rgba(255,107,94,.14) 100%)",
          }}
        />
        <div className="relative flex h-full flex-col items-center justify-center px-12 text-center">
          <svg width="220" height="220" viewBox="0 0 32 32" fill="none" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 7 L5 16 L14 25" stroke="var(--blue)" />
            <path d="M18 7 L27 16 L18 25" stroke="var(--coral)" />
            <circle cx="16" cy="16" r="1.1" fill="var(--gold)" stroke="none" />
          </svg>
          <p className="mt-10 max-w-xs font-display text-xl font-medium leading-snug">
            Everyone starts at 1200. Every match moves it.
          </p>
        </div>
      </aside>
    </div>
  );
}
