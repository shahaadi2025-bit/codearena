# CodeArena

Real-time 1v1 coding battles. Two players get matched, receive the same problem, and race to pass hidden tests while watching each other's progress live. Ratings move after every match.

Built as a full-stack and real-time portfolio project using only free tiers and open-source tools.

## Status

| Area | State |
|---|---|
| Monorepo, PostgreSQL schema, 53 seeded problems | Done |
| Auth: signup, login, JWT sessions, protected routes | Done |
| Matchmaking queue | Planned |
| Real-time match room (Socket.io, Monaco editor) | Planned |
| Code execution via Judge0 | Planned |
| Elo rating, leaderboard, profile | Planned |
| Deployment (Vercel + Render) | Planned |

## Tech stack

- **Frontend:** Next.js (App Router), React, Tailwind CSS, TypeScript
- **Backend:** Node.js, Express 5, TypeScript, Socket.io (from the match-room step)
- **Database:** PostgreSQL on Supabase (free tier), accessed with `pg`
- **Auth:** JWT (HS256) with bcrypt-hashed passwords (`bcryptjs`)
- **Code execution:** Judge0 CE via RapidAPI (free plan), self-hosting supported later
- **Hosting:** Vercel (frontend) and Render (backend)

## Getting started

Prerequisites: Node.js 20 or newer, Git, and a free Supabase project.

### 1. Database

1. Create a Supabase project and save the database password.
2. Open **Connect** and copy the **Session pooler** connection string. The direct connection is usually IPv6-only on the free tier.

### 2. Backend

```bash
cd backend
npm install
cp .env.example .env        # PowerShell: Copy-Item .env.example .env
```

Fill in `.env`:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Supabase Session pooler connection string (URL-encode special characters in the password) |
| `JWT_SECRET` | Long random string: `node -e "console.log(require('crypto').randomBytes(48).toString('hex'))"` |
| `CLIENT_URL` | Frontend origin for CORS, `http://localhost:3000` locally |
| `JUDGE0_API_KEY` | RapidAPI key, needed from the code-execution step |

Create the tables and load the problems, then start the API:

```bash
npm run db:schema
npm run db:seed
npm run dev                 # http://localhost:4000/health
```

`/health` should report `"problems":53`.

### 3. Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev                 # http://localhost:3000
```

On Windows you can start both servers at once with `powershell -ExecutionPolicy Bypass -File .\dev.ps1`.

## Scripts (backend)

| Command | What it does |
|---|---|
| `npm run dev` | Start the API with auto-reload |
| `npm run build` / `npm start` | Compile to `dist/` and run it (used on Render) |
| `npm run typecheck` | Type-check without emitting |
| `npm run db:schema` | Create tables and indexes (safe to re-run) |
| `npm run db:seed` | Insert problems (existing ones are skipped by slug) |

## Project structure

```
codearena/
├── backend/
│   └── src/
│       ├── index.ts              # Express server
│       ├── config/               # env.ts, database.ts
│       ├── middleware/           # auth.ts (JWT), errorHandler.ts
│       ├── routes/               # auth.ts
│       ├── db/                   # schema.sql, seed.sql, migrate.ts
│       └── types/                # Express request typing
├── frontend/
│   └── src/
│       ├── app/                  # pages: landing, auth/login, auth/signup, dashboard
│       ├── components/           # Logo, DuelDemo, AuthShell, Field
│       ├── context/              # AuthContext
│       └── lib/                  # api.ts
├── tools/gen_problems.py         # generates backend/src/db/seed.sql
└── dev.ps1                       # start both servers on Windows
```

## Problem set

53 problems (20 easy, 21 medium, 12 hard). Every problem reads stdin and writes stdout, so any Judge0 language works. Expected outputs are computed by reference solutions in `tools/gen_problems.py`, which also cross-checks the harder ones against brute force. To change the set, edit that file, run `python tools/gen_problems.py`, and re-seed.

## Free-tier limits to know about

- **Judge0 (RapidAPI free plan):** about 50 submission requests per day at the time of writing. Check the plan page for current numbers.
- **Render free web services** sleep after a period of inactivity, so the first request afterwards is slow.
- **Supabase free tier:** 500 MB database; use the Session pooler connection string.

## License

No license chosen yet.
