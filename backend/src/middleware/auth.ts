import { NextFunction, Request, Response } from 'express';
import jwt, { SignOptions } from 'jsonwebtoken';
import { env } from '../config/env';
import { HttpError } from './errorHandler';

export interface AuthUser {
  id: string;
  username: string;
}

export function signToken(user: AuthUser): string {
  return jwt.sign({ username: user.username }, env.jwtSecret, {
    subject: user.id,
    algorithm: 'HS256',
    expiresIn: env.jwtExpiresIn as SignOptions['expiresIn'],
  });
}

export function verifyToken(token: string): AuthUser {
  const payload = jwt.verify(token, env.jwtSecret, { algorithms: ['HS256'] });
  if (typeof payload === 'string' || !payload.sub || typeof payload.username !== 'string') {
    throw new Error('Malformed token');
  }
  return { id: payload.sub, username: payload.username };
}

// Protects an Express route: 401 unless a valid "Authorization: Bearer <token>" header is sent.
export function requireAuth(req: Request, _res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  const token = header?.startsWith('Bearer ') ? header.slice(7) : undefined;
  if (!token) return next(new HttpError(401, 'Log in to continue.'));
  try {
    req.user = verifyToken(token);
    next();
  } catch {
    next(new HttpError(401, 'Your session has expired. Log in again.'));
  }
}
