// Dev only: a second player so you can test matchmaking alone.
// Run in its own PowerShell window (backend folder):  npm run dev:bot
import 'dotenv/config';
import { io } from 'socket.io-client';

const API = process.env.API_URL ?? `http://localhost:${process.env.PORT ?? 4000}`;
const creds = { username: 'practice_bot', email: 'practice_bot@codearena.dev', password: 'practice-bot-pass-123' };

async function post(path: string, body: unknown) {
  const res = await fetch(`${API}/api${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return { status: res.status, data: (await res.json()) as any };
}

async function getToken(): Promise<string> {
  let r = await post('/auth/signup', creds);
  if (r.status === 409) r = await post('/auth/login', { email: creds.email, password: creds.password });
  if (!r.data.token) throw new Error(r.data.error ?? 'Could not sign the bot in.');
  return r.data.token as string;
}

async function main() {
  const socket = io(API, { auth: { token: await getToken() } });
  socket.on('connect', () => {
    console.log('practice_bot connected, waiting in the queue. Click "Find match" in your browser.');
    socket.emit('queue:join');
  });
  socket.on('match:found', ({ matchId }: { matchId: string }) => {
    console.log(`Matched! Match id: ${matchId}`);
    setTimeout(() => process.exit(0), 500);
  });
  socket.on('connect_error', (err) => console.error('Connection failed:', err.message));
  socket.on('queue:error', (msg: string) => console.error('Queue error:', msg));
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
