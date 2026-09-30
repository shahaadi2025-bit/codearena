import http from 'http';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { env } from './config/env';
import { query } from './config/database';
import { notFound, errorHandler } from './middleware/errorHandler';
import authRoutes from './routes/auth';

const app = express();
app.set('trust proxy', 1); // Render sits behind a proxy; needed for correct client IPs in rate limiting
app.use(helmet());
app.use(cors({ origin: env.clientUrl, credentials: true }));
app.use(express.json({ limit: '200kb' })); // code submissions can be long

app.get('/health', async (_req, res, next) => {
  try {
    const time = await query<{ time: Date }>('select now() as time');
    const problems = await query<{ count: number }>('select count(*)::int as count from problems');
    res.json({ status: 'ok', dbTime: time.rows[0].time, problems: problems.rows[0].count });
  } catch (err) {
    next(err);
  }
});

app.use('/api/auth', authRoutes);
// Next steps mount here: /api/users, /api/matches

app.use(notFound);
app.use(errorHandler);

// http server (not app.listen) so Socket.io can attach to it in Step 4
export const server = http.createServer(app);
server.listen(env.port, () => console.log(`CodeArena API running on http://localhost:${env.port}`));
