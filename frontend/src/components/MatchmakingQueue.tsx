"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { getSocket } from "@/lib/socket";

type Phase = "idle" | "connecting" | "searching" | "found";

const fmt = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

export default function MatchmakingQueue({ rating }: { rating: number }) {
  const router = useRouter();
  const [phase, setPhase] = useState<Phase>("idle");
  const [seconds, setSeconds] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const phaseRef = useRef<Phase>("idle");

  useEffect(() => {
    phaseRef.current = phase;
  }, [phase]);

  useEffect(() => {
    const socket = getSocket();

    // Also re-joins after a reconnect, e.g. if the server restarted and lost the queue.
    const onConnect = () => {
      if (phaseRef.current === "connecting" || phaseRef.current === "searching") socket.emit("queue:join");
    };
    const onDisconnect = () => {
      if (phaseRef.current === "searching") setPhase("connecting");
    };
    const onJoined = () => setPhase((p) => (p === "found" ? p : "searching"));
    const onLeft = () => setPhase((p) => (p === "found" ? p : "idle"));
    const onFound = ({ matchId }: { matchId: string }) => {
      setPhase("found");
      setTimeout(() => router.push(`/match/${matchId}`), 900);
    };
    const onReplaced = () => {
      setPhase("idle");
      setError("You started searching in another tab.");
    };
    const onQueueError = (msg: string) => {
      setPhase("idle");
      setError(msg);
    };
    const onConnectError = (err: Error) => {
      setPhase("idle");
      setError(/log in|session/i.test(err.message) ? err.message : "Cannot reach the server. Check that the backend is running.");
    };

    socket.on("connect", onConnect);
    socket.on("disconnect", onDisconnect);
    socket.on("queue:joined", onJoined);
    socket.on("queue:left", onLeft);
    socket.on("match:found", onFound);
    socket.on("queue:replaced", onReplaced);
    socket.on("queue:error", onQueueError);
    socket.on("connect_error", onConnectError);

    return () => {
      // Leaving the page while searching must not leave a ghost player in the queue.
      if (phaseRef.current === "searching" || phaseRef.current === "connecting") socket.emit("queue:leave");
      socket.off("connect", onConnect);
      socket.off("disconnect", onDisconnect);
      socket.off("queue:joined", onJoined);
      socket.off("queue:left", onLeft);
      socket.off("match:found", onFound);
      socket.off("queue:replaced", onReplaced);
      socket.off("queue:error", onQueueError);
      socket.off("connect_error", onConnectError);
    };
  }, [router]);

  useEffect(() => {
    if (phase !== "searching") return;
    const id = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(id);
  }, [phase]);

  function start() {
    setError(null);
    setSeconds(0);
    setPhase("connecting");
    const socket = getSocket();
    if (socket.connected) socket.emit("queue:join");
    else socket.connect();
  }

  function cancel() {
    const socket = getSocket();
    if (socket.connected) socket.emit("queue:leave");
    setPhase("idle");
  }

  const busy = phase === "connecting" || phase === "searching";

  return (
    <section className="rounded-2xl border border-line bg-panel p-8">
      <h2 className="font-display text-xl font-bold tracking-tight">
        {phase === "found" ? "Opponent found" : busy ? "Searching for an opponent" : "Find a match"}
      </h2>

      <div aria-live="polite" className="mt-3 min-h-12 text-muted">
        {phase === "idle" && <p>You will be paired with a player near your rating of {rating}.</p>}
        {busy && (
          <p>
            <span className="font-mono text-text">{fmt(seconds)}</span> elapsed. The search widens the longer you wait.
          </p>
        )}
        {phase === "found" && <p>Loading your match...</p>}
      </div>

      <div aria-hidden="true" className="my-6 flex h-24 items-center justify-center">
        {busy && (
          <div className="relative h-20 w-20" style={{ animation: "orbit 1.6s linear infinite" }}>
            <span className="absolute left-1/2 top-0 h-4 w-4 -translate-x-1/2 rounded-full bg-blue" />
            <span className="absolute bottom-0 left-1/2 h-4 w-4 -translate-x-1/2 rounded-full bg-coral" />
          </div>
        )}
        {phase === "found" && (
          <div className="flex items-center">
            <span className="h-6 w-6 rounded-full bg-blue" />
            <span className="-ml-1 h-6 w-6 rounded-full bg-coral" />
          </div>
        )}
        {phase === "idle" && (
          <div className="flex items-center gap-10 opacity-60">
            <span className="h-4 w-4 rounded-full bg-blue" />
            <span className="h-4 w-4 rounded-full bg-coral" />
          </div>
        )}
      </div>

      {error && (
        <p role="alert" className="mb-4 rounded-lg border border-coral/50 bg-coral/10 px-3.5 py-2.5 text-sm text-coral">
          {error}
        </p>
      )}

      {phase === "idle" && (
        <button onClick={start} className="rounded-lg bg-gold px-6 py-2.5 font-semibold text-ink transition hover:brightness-110">
          Find match
        </button>
      )}
      {busy && (
        <button onClick={cancel} className="rounded-lg border border-line px-6 py-2.5 font-medium transition hover:bg-ink">
          Cancel
        </button>
      )}
    </section>
  );
}
