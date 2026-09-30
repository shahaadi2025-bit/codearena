"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import Logo from "@/components/Logo";
import ProblemStatement from "@/components/ProblemStatement";
import { api, ApiError } from "@/lib/api";
import type { MatchData } from "@/lib/types";
import { useRequireAuth } from "@/lib/useRequireAuth";

export default function MatchPage() {
  const { user, loading } = useRequireAuth();
  const { id } = useParams<{ id: string }>();
  const [match, setMatch] = useState<MatchData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    let cancelled = false;
    api
      .get<{ match: MatchData }>(`/matches/${id}`)
      .then((res) => !cancelled && setMatch(res.match))
      .catch((err) => !cancelled && setError(err instanceof ApiError ? err.message : "Could not load the match."));
    return () => {
      cancelled = true;
    };
  }, [user, id]);

  if (loading || !user) return <div className="grid min-h-screen place-items-center text-muted">Loading...</div>;

  return (
    <div className="mx-auto max-w-4xl px-6">
      <header className="flex items-center justify-between py-5">
        <Link href="/dashboard" aria-label="Back to dashboard"><Logo /></Link>
        <Link href="/dashboard" className="text-sm text-muted transition hover:text-text">Back to dashboard</Link>
      </header>

      {error && (
        <p role="alert" className="mt-10 rounded-lg border border-coral/50 bg-coral/10 px-4 py-3 text-coral">{error}</p>
      )}
      {!error && !match && <p className="mt-10 text-muted">Loading match...</p>}

      {match && (
        <main className="pb-16 pt-6">
          <div className="flex items-center justify-center gap-6 rounded-2xl border border-line bg-panel px-6 py-5">
            <div className="text-right">
              <p className="font-display font-medium text-blue">{match.me.username}</p>
              <p className="font-mono text-sm text-muted">{match.me.rating}</p>
            </div>
            <span className="font-display text-lg text-muted">vs</span>
            <div>
              <p className="font-display font-medium text-coral">{match.opponent.username}</p>
              <p className="font-mono text-sm text-muted">{match.opponent.rating}</p>
            </div>
          </div>

          <div className="mt-10 flex flex-wrap items-center gap-3">
            <h1 className="font-display text-2xl font-bold tracking-tight">{match.problem.title}</h1>
            <span className="rounded-md border border-line px-2 py-0.5 font-mono text-xs text-muted">{match.problem.difficulty}</span>
            <span className="font-mono text-xs text-muted">{Math.round(match.problem.timeLimitSec / 60)} min</span>
          </div>

          <div className="mt-6"><ProblemStatement text={match.problem.description} /></div>

          {match.problem.examples.map((ex, i) => (
            <div key={i} className="mt-6 grid gap-3 sm:grid-cols-2">
              <div>
                <p className="mb-1.5 text-sm text-muted">Example input</p>
                <pre className="overflow-x-auto rounded-lg border border-line bg-panel p-3 font-mono text-sm">{ex.input}</pre>
              </div>
              <div>
                <p className="mb-1.5 text-sm text-muted">Example output</p>
                <pre className="overflow-x-auto rounded-lg border border-line bg-panel p-3 font-mono text-sm">{ex.output}</pre>
              </div>
            </div>
          ))}

          <p className="mt-10 rounded-lg border border-line px-4 py-3 text-sm text-muted">
            The code editor and live opponent status arrive in the next update.
          </p>
        </main>
      )}
    </div>
  );
}
