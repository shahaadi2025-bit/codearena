"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import Logo from "@/components/Logo";
import MatchmakingQueue from "@/components/MatchmakingQueue";
import { useRequireAuth } from "@/lib/useRequireAuth";

export default function DashboardPage() {
  const { user, loading, logout } = useRequireAuth();
  const router = useRouter();

  if (loading || !user) {
    return <div className="grid min-h-screen place-items-center text-muted">Loading...</div>;
  }

  return (
    <div className="mx-auto max-w-6xl px-6">
      <header className="flex items-center justify-between py-5">
        <Link href="/" aria-label="CodeArena home"><Logo /></Link>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-muted">{user.username}</span>
          <span className="rounded-md bg-panel px-2.5 py-1 font-mono text-gold">{user.rating}</span>
          <button
            onClick={() => { logout(); router.push("/"); }}
            className="rounded-lg border border-line px-4 py-2 font-medium transition hover:bg-panel"
          >
            Log out
          </button>
        </div>
      </header>

      <main className="grid gap-6 py-10 lg:grid-cols-[1.4fr_1fr]">
        <MatchmakingQueue rating={user.rating} />
        <section className="rounded-2xl border border-line bg-panel p-8">
          <h2 className="font-display text-xl font-bold tracking-tight">Your record</h2>
          <dl className="mt-6 grid grid-cols-3 gap-4">
            <div>
              <dt className="text-sm text-muted">Rating</dt>
              <dd className="mt-1 font-mono text-2xl text-gold">{user.rating}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted">Matches</dt>
              <dd className="mt-1 font-mono text-2xl">{user.matchesPlayed ?? 0}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted">Wins</dt>
              <dd className="mt-1 font-mono text-2xl">{user.wins ?? 0}</dd>
            </div>
          </dl>
        </section>
      </main>
    </div>
  );
}
