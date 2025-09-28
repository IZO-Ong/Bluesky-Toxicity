// Type for each daily stat row
export type Stat = {
  date: string;
  toxic_posts: number;
};

// Type for leaderboard entry (can be null if no data today)
export type LeaderboardEntry = {
  uri: string;
  author: string;
  text: string;
  likes: number;
  toxicity: number;
} | null;

// Shape of the leaderboard response
export type LeaderboardResponse = {
  most_toxic: LeaderboardEntry;
  least_toxic: LeaderboardEntry;
};
