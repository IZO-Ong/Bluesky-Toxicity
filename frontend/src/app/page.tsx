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
          Bluesky Toxicity over Last 30 Days
        </h2>
        <div className="w-full h-[400px]">
          <LineChart stats={stats} />
        </div>
      </section>

      {/* Credits */}
      <section className="text-center text-gray-500 text-sm">
        <p>
          Powered by the <span className="font-medium">Detoxify</span> model
          from <a href="https://unitary.ai" target="_blank" rel="noopener noreferrer" className="underline">Unitary AI</a>
        </p>
        <p>
          Built with <span className="font-medium">Next.js</span> · Created by{" "}
          <span className="font-semibold">Isaac</span>
        </p>
      </section>
    </main>
  );
}
