export type Player = { id: string; username: string; rating: number };

export type MatchData = {
  id: string;
  status: string;
  winnerId: string | null;
  createdAt: string;
  endsAt: string;
  me: Player;
  opponent: Player;
  problem: {
    id: number;
    title: string;
    slug: string;
    description: string;
    difficulty: "easy" | "medium" | "hard";
    timeLimitSec: number;
    examples: { input: string; output: string }[];
    starterCode: Record<string, string>;
  };
};
