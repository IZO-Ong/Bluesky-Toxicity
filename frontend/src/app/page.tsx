"use client";

import { useEffect, useState } from "react";
import LineChart from "../components/LineChart";

export default function Page() {
  const [stats, setStats] = useState<any[]>([]);
  const [leaderboard, setLeaderboard] = useState<any>({});

  useEffect(() => {
    fetch("${process.env.NEXT_PUBLIC_API_URL}/stats/last30days")
      .then((res) => res.json())
      .then(setStats);

    fetch("${process.env.NEXT_PUBLIC_API_URL}/leaderboard/today")
      .then((res) => res.json())
      .then(setLeaderboard);
  }, []);

  return (
    <main className="p-8 space-y-8">
      <h1 className="text-3xl font-bold">📊 Bluesky Toxicity Dashboard</h1>

      <section>
        <h2 className="text-xl font-semibold mb-2">Last 30 Days</h2>
        <div className="bg-white rounded-xl shadow p-4">
          <LineChart stats={stats} />
        </div>
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Today’s Leaderboard</h2>
        <div className="bg-white rounded-xl shadow p-4">
          <h3 className="font-medium text-red-600">🔥 Most Toxic</h3>
          <pre className="whitespace-pre-wrap text-sm">
            {JSON.stringify(leaderboard.most_toxic, null, 2)}
          </pre>

          <h3 className="font-medium text-green-600 mt-4">🌱 Least Toxic</h3>
          <pre className="whitespace-pre-wrap text-sm">
            {JSON.stringify(leaderboard.least_toxic, null, 2)}
          </pre>
        </div>
      </section>
    </main>
  );
}
