"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Logo from "@/components/Logo";
import { useAuth } from "@/context/AuthContext";

// Placeholder: replaced by the real dashboard (matchmaking + leaderboard) in later steps.
export default function DashboardPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) router.replace("/auth/login");
  }, [loading, user, router]);

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
      <main className="py-16">
        <h1 className="font-display text-3xl font-bold tracking-tight">Welcome, {user.username}</h1>
        <p className="mt-4 max-w-md text-muted">You are signed in with a rating of {user.rating}. Matchmaking arrives next.</p>
      </main>
    </div>
  );
}
