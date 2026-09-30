import { Router } from 'express';
import bcrypt from 'bcryptjs';
import rateLimit from 'express-rate-limit';
import { z } from 'zod';
import { query } from '../config/database';
import { HttpError } from '../middleware/errorHandler';
import { requireAuth, signToken } from '../middleware/auth';

const router = Router();

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  limit: 30,
  standardHeaders: 'draft-7',
  legacyHeaders: false,
  message: { error: 'Too many attempts. Try again in a few minutes.' },
});

const signupSchema = z.object({
  username: z
    .string()
    .trim()
    .regex(/^[A-Za-z0-9_]{3,20}$/, 'Username must be 3 to 20 letters, numbers or underscores.'),
  email: z.string().trim().toLowerCase().email('Enter a valid email address.').max(255, 'Email is too long.'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters.')
    .refine((p) => Buffer.byteLength(p, 'utf8') <= 72, 'Password is too long (72 bytes maximum).'),
});

const loginSchema = z.object({
  email: z.string().trim().toLowerCase().min(1, 'Enter your email.'),
  password: z.string().min(1, 'Enter your password.'),
});

function parse<S extends z.ZodType>(schema: S, body: unknown): z.infer<S> {
  const result = schema.safeParse(body);
  if (!result.success) {
    const issue = result.error.issues[0];
    const field = issue.path.length ? String(issue.path[0]) : undefined;
    throw new HttpError(400, field ? issue.message : 'Send the details as a JSON body.', field);
  }
  return result.data;
}

interface DbUser {
  id: string;
  username: string;
  email: string;
  rating: number;
}

const publicUser = (u: DbUser) => ({ id: u.id, username: u.username, email: u.email, rating: u.rating });

// Compared against when the email is unknown, so response time does not reveal which emails exist.
const DUMMY_HASH = bcrypt.hashSync('not-a-real-password', 10);

router.post('/signup', limiter, async (req, res, next) => {
  try {
    const { username, email, password } = parse(signupSchema, req.body);
    const passwordHash = await bcrypt.hash(password, 10);
    try {
      const { rows } = await query<DbUser>(
        'insert into users (username, email, password_hash) values ($1, $2, $3) returning id, username, email, rating',
        [username, email, passwordHash],
      );
      const user = rows[0];
      res.status(201).json({ token: signToken(user), user: publicUser(user) });
    } catch (err: any) {
      if (err?.code === '23505') {
        const emailTaken = String(err.constraint).includes('email');
        throw new HttpError(
          409,
          emailTaken ? 'That email is already registered. Log in instead.' : 'That username is taken.',
          emailTaken ? 'email' : 'username',
        );
      }
      throw err;
    }
  } catch (err) {
    next(err);
  }
});

router.post('/login', limiter, async (req, res, next) => {
  try {
    const { email, password } = parse(loginSchema, req.body);
    const { rows } = await query<DbUser & { password_hash: string }>(
      'select id, username, email, rating, password_hash from users where email = $1',
      [email],
    );
    const user = rows[0];
    const ok = await bcrypt.compare(password, user ? user.password_hash : DUMMY_HASH);
    if (!user || !ok) throw new HttpError(401, 'Incorrect email or password.');
    res.json({ token: signToken(user), user: publicUser(user) });
  } catch (err) {
    next(err);
  }
});

router.get('/me', requireAuth, async (req, res, next) => {
  try {
    const { rows } = await query<DbUser & { wins: number; matches_played: number }>(
      'select id, username, email, rating, wins, matches_played from users where id = $1',
      [req.user!.id],
    );
    const user = rows[0];
    if (!user) throw new HttpError(401, 'Your account no longer exists. Sign up again.');
    res.json({ user: { ...publicUser(user), wins: user.wins, matchesPlayed: user.matches_played } });
  } catch (err) {
    next(err);
  }
});

export default router;
