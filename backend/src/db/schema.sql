create extension if not exists "pgcrypto";

create table if not exists users (
  id             uuid primary key default gen_random_uuid(),
  username       varchar(30) unique not null,
  email          varchar(255) unique not null,
  password_hash  text not null,
  rating         int not null default 1200,
  matches_played int not null default 0,
  wins           int not null default 0,
  created_at     timestamptz not null default now()
);

create table if not exists problems (
  id             serial primary key,
  title          text not null,
  slug           text unique not null,
  description    text not null,
  difficulty     text not null check (difficulty in ('easy','medium','hard')),
  time_limit_sec int not null default 900,
  examples       jsonb not null default '[]',
  test_cases     jsonb not null,
  starter_code   jsonb not null default '{}',
  created_at     timestamptz not null default now()
);

create table if not exists matches (
  id                    uuid primary key default gen_random_uuid(),
  player1_id            uuid not null references users(id),
  player2_id            uuid not null references users(id),
  problem_id            int  not null references problems(id),
  status                text not null default 'active'
                        check (status in ('active','completed','timeout','abandoned')),
  winner_id             uuid references users(id),
  player1_rating_before int,
  player2_rating_before int,
  player1_rating_change int,
  player2_rating_change int,
  created_at            timestamptz not null default now(),
  ended_at              timestamptz,
  check (player1_id <> player2_id)
);

create table if not exists submissions (
  id                uuid primary key default gen_random_uuid(),
  match_id          uuid not null references matches(id) on delete cascade,
  user_id           uuid not null references users(id),
  code              text not null,
  language          text not null,
  status            text not null default 'pending'
                    check (status in ('pending','accepted','wrong_answer','runtime_error',
                                      'compile_error','time_limit','error')),
  passed_tests      int not null default 0,
  total_tests       int not null default 0,
  error_message     text,
  execution_time_ms int,
  submitted_at      timestamptz not null default now()
);

create table if not exists rating_history (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references users(id),
  match_id      uuid not null references matches(id) on delete cascade,
  rating_before int not null,
  rating_after  int not null,
  created_at    timestamptz not null default now()
);

create unique index if not exists idx_users_username_lower on users (lower(username));
create index if not exists idx_users_rating        on users(rating desc);
create index if not exists idx_matches_p1          on matches(player1_id);
create index if not exists idx_matches_p2          on matches(player2_id);
create index if not exists idx_submissions_match   on submissions(match_id, user_id);
create index if not exists idx_rating_history_user on rating_history(user_id, created_at);

alter table users          enable row level security;
alter table problems       enable row level security;
alter table matches        enable row level security;
alter table submissions    enable row level security;
alter table rating_history enable row level security;
