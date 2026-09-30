import type { Server } from 'socket.io';
import { query } from '../config/database';

interface Waiting {
  userId: string;
  username: string;
  rating: number;
  socketId: string;
  joinedAt: number;
}

const queue = new Map<string, Waiting>();
let io: Server;

// How far apart two ratings may be. Starts at 100 and widens by 20 per second waited;
// after 30 seconds anyone can be paired with anyone, so nobody waits forever.
function windowFor(w: Waiting, now: number): number {
  const seconds = Math.floor((now - w.joinedAt) / 1000);
  return seconds >= 30 ? Infinity : 100 + seconds * 20;
}

export function init(server: Server) {
  io = server;
  setInterval(() => void sweep(), 2000);
}

export function size(): number {
  return queue.size;
}

// One queue entry per user. A second tab replaces the first and keeps the original wait time.
export function join(entry: Omit<Waiting, 'joinedAt'>): { replacedSocketId?: string } {
  const existing = queue.get(entry.userId);
  queue.set(entry.userId, { ...entry, joinedAt: existing?.joinedAt ?? Date.now() });
  void sweep();
  return { replacedSocketId: existing && existing.socketId !== entry.socketId ? existing.socketId : undefined };
}

export function leave(userId: string, socketId?: string): boolean {
  const waiting = queue.get(userId);
  if (!waiting || (socketId && waiting.socketId !== socketId)) return false;
  queue.delete(userId);
  return true;
}

let sweeping = false;
let again = false;

async function sweep() {
  if (sweeping) {
    again = true;
    return;
  }
  sweeping = true;
  try {
    do {
      again = false;
      await pairUp();
    } while (again);
  } catch (err) {
    console.error('Matchmaking sweep failed:', err);
  } finally {
    sweeping = false;
  }
}

async function pairUp() {
  const now = Date.now();
  const waiting = [...queue.values()].sort((a, b) => a.joinedAt - b.joinedAt);
  const used = new Set<string>();

  for (const a of waiting) {
    if (used.has(a.userId)) continue;
    let best: Waiting | undefined;
    let bestDiff = Infinity;
    for (const b of waiting) {
      if (b.userId === a.userId || used.has(b.userId)) continue;
      const diff = Math.abs(a.rating - b.rating);
      if (diff <= Math.max(windowFor(a, now), windowFor(b, now)) && diff < bestDiff) {
        best = b;
        bestDiff = diff;
      }
    }
    if (best) {
      used.add(a.userId);
      used.add(best.userId);
      queue.delete(a.userId);
      queue.delete(best.userId);
      await createMatch(a, best);
    }
  }
}

async function createMatch(a: Waiting, b: Waiting) {
  try {
    const problemId = await pickProblem(a, b);
    const { rows } = await query<{ id: string }>(
      `insert into matches (player1_id, player2_id, problem_id, player1_rating_before, player2_rating_before)
       values ($1, $2, $3, $4, $5) returning id`,
      [a.userId, b.userId, problemId, a.rating, b.rating],
    );
    const matchId = rows[0].id;
    io.to(a.socketId).emit('match:found', { matchId });
    io.to(b.socketId).emit('match:found', { matchId });
  } catch (err) {
    console.error('Could not create match, returning players to the queue:', err);
    for (const w of [a, b]) if (!queue.has(w.userId)) queue.set(w.userId, w);
  }
}

// Harder problems for higher-rated pairs, and never one either player saw in their last few matches.
function pickDifficulty(avgRating: number): 'easy' | 'medium' | 'hard' {
  const r = Math.random();
  if (avgRating < 1150) return r < 0.7 ? 'easy' : 'medium';
  if (avgRating < 1350) return r < 0.2 ? 'easy' : r < 0.8 ? 'medium' : 'hard';
  return r < 0.3 ? 'medium' : 'hard';
}

async function pickProblem(a: Waiting, b: Waiting): Promise<number> {
  const difficulty = pickDifficulty((a.rating + b.rating) / 2);
  const recent = await query<{ problem_id: number }>(
    `select problem_id from matches
     where player1_id = any($1::uuid[]) or player2_id = any($1::uuid[])
     order by created_at desc limit 10`,
    [[a.userId, b.userId]],
  );
  const exclude = recent.rows.map((r) => r.problem_id);

  const attempts: Array<[string, unknown[]]> = [
    ['select id from problems where difficulty = $1 and id <> all($2::int[]) order by random() limit 1', [difficulty, exclude]],
    ['select id from problems where id <> all($1::int[]) order by random() limit 1', [exclude]],
    ['select id from problems order by random() limit 1', []],
  ];
  for (const [sql, params] of attempts) {
    const { rows } = await query<{ id: number }>(sql, params);
    if (rows[0]) return rows[0].id;
  }
  throw new Error('No problems in the database. Run npm run db:seed.');
}
