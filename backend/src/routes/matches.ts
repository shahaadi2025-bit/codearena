import { Router } from 'express';
import { query } from '../config/database';
import { HttpError } from '../middleware/errorHandler';
import { requireAuth } from '../middleware/auth';

const router = Router();
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

interface MatchRow {
  id: string;
  status: string;
  winner_id: string | null;
  created_at: Date;
  player1_id: string;
  player2_id: string;
  player1_rating_before: number | null;
  player2_rating_before: number | null;
  p1_username: string;
  p2_username: string;
  problem_id: number;
  title: string;
  slug: string;
  description: string;
  difficulty: string;
  time_limit_sec: number;
  examples: unknown;
  starter_code: unknown;
}

// A match and its problem, for the two players only. Hidden test cases are never selected.
router.get('/:id', requireAuth, async (req, res, next) => {
  try {
    const id = String(req.params.id);
    if (!UUID.test(id)) throw new HttpError(404, 'Match not found.');

    const { rows } = await query<MatchRow>(
      `select m.id, m.status, m.winner_id, m.created_at, m.player1_id, m.player2_id,
              m.player1_rating_before, m.player2_rating_before,
              u1.username as p1_username, u2.username as p2_username,
              p.id as problem_id, p.title, p.slug, p.description, p.difficulty,
              p.time_limit_sec, p.examples, p.starter_code
       from matches m
       join users u1 on u1.id = m.player1_id
       join users u2 on u2.id = m.player2_id
       join problems p on p.id = m.problem_id
       where m.id = $1`,
      [id],
    );
    const m = rows[0];
    if (!m) throw new HttpError(404, 'Match not found.');

    const userId = req.user!.id;
    if (userId !== m.player1_id && userId !== m.player2_id) throw new HttpError(403, 'This is not your match.');

    const p1 = { id: m.player1_id, username: m.p1_username, rating: m.player1_rating_before };
    const p2 = { id: m.player2_id, username: m.p2_username, rating: m.player2_rating_before };
    const isPlayer1 = userId === m.player1_id;

    res.json({
      match: {
        id: m.id,
        status: m.status,
        winnerId: m.winner_id,
        createdAt: m.created_at,
        endsAt: new Date(m.created_at.getTime() + m.time_limit_sec * 1000),
        me: isPlayer1 ? p1 : p2,
        opponent: isPlayer1 ? p2 : p1,
        problem: {
          id: m.problem_id,
          title: m.title,
          slug: m.slug,
          description: m.description,
          difficulty: m.difficulty,
          timeLimitSec: m.time_limit_sec,
          examples: m.examples,
          starterCode: m.starter_code,
        },
      },
    });
  } catch (err) {
    next(err);
  }
});

export default router;
