import type { Server as HttpServer } from 'http';
import { Server } from 'socket.io';
import { env } from '../config/env';
import { query } from '../config/database';
import { AuthUser, verifyToken } from '../middleware/auth';
import * as matchmaking from '../services/matchmaking';

export function initSockets(httpServer: HttpServer) {
  const io = new Server(httpServer, { cors: { origin: env.clientUrl, credentials: true } });
  matchmaking.init(io);

  // Every socket must present a valid JWT: io(url, { auth: { token } })
  io.use((socket, next) => {
    const token = socket.handshake.auth?.token;
    if (typeof token !== 'string') return next(new Error('Log in to play.'));
    try {
      socket.data.user = verifyToken(token);
      next();
    } catch {
      next(new Error('Your session has expired. Log in again.'));
    }
  });

  io.on('connection', (socket) => {
    const user = socket.data.user as AuthUser;

    socket.on('queue:join', async () => {
      try {
        // Use the current rating from the database, not anything the client sends.
        const { rows } = await query<{ rating: number }>('select rating from users where id = $1', [user.id]);
        if (!rows[0]) return socket.emit('queue:error', 'Account not found. Sign up again.');
        const { replacedSocketId } = matchmaking.join({
          userId: user.id,
          username: user.username,
          rating: rows[0].rating,
          socketId: socket.id,
        });
        if (replacedSocketId) io.to(replacedSocketId).emit('queue:replaced');
        socket.emit('queue:joined', { playersInQueue: matchmaking.size() });
      } catch (err) {
        console.error(err);
        socket.emit('queue:error', 'Could not join the queue. Try again.');
      }
    });

    socket.on('queue:leave', () => {
      if (matchmaking.leave(user.id, socket.id)) socket.emit('queue:left');
    });

    socket.on('disconnect', () => {
      matchmaking.leave(user.id, socket.id);
    });
  });

  return io;
}
