"use client";

import { useEffect, useState } from "react";
import LineChart from "../components/LineChart";
import ToxicCard from "../components/ToxicCard";
import { Stat, LeaderboardResponse } from "../types";

export default function Page() {
  const [stats, setStats] = useState<Stat[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardResponse>({
    most_toxic: null,
    least_toxic: null,
  });

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/stats/last30days`)
      .then((res) => res.json())
      .then(setStats);

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/leaderboard/today`)
      .then((res) => res.json())
      .then(setLeaderboard);
  }, []);

  return (
    <main className="p-8 space-y-16">
      {/* Title */}
      <header className="text-center">
        <h1 className="text-4xl font-bold flex items-center justify-center gap-2">
          Bluesky Toxicity Dashboard
        </h1>
        <p className="text-gray-500 mt-2">
          A real-time look at toxicity trends in Bluesky posts
        </p>
      </header>

      {/* Toxic Cards */}
      <section className="flex justify-center gap-72">
        <ToxicCard
          type="most"
          author={leaderboard.most_toxic?.author}
          text={leaderboard.most_toxic?.text}
          likes={leaderboard.most_toxic?.likes}
          toxicity={leaderboard.most_toxic?.toxicity}
          uri={leaderboard.most_toxic?.uri}
        />
        <ToxicCard
          type="least"
          author={leaderboard.least_toxic?.author}
          text={leaderboard.least_toxic?.text}
          likes={leaderboard.least_toxic?.likes}
          toxicity={leaderboard.least_toxic?.toxicity}
          uri={leaderboard.least_toxic?.uri}
        />
      </section>

      {/* Full-width Graph */}
      <section>
        <h2 className="text-2xl font-semibold flex items-center justify-center gap-2 mb-4">
          📈 Last 30 Days
        </h2>
        <div className="w-full h-[400px]">
          <LineChart stats={stats} />
        </div>
      </section>
    </main>
  );
}
