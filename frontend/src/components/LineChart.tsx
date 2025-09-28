"use client";

import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Stat } from "../types";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend, Filler);

export default function LineChart({ stats }: { stats: Stat[] }) {
  const chartData = {
    labels: stats.map((s) => s.date).reverse(),
    datasets: [
      {
        label: "Toxic posts",
        data: stats.map((s) => s.toxic_posts).reverse(),
        borderColor: "transparent",
        borderWidth: 0,
        backgroundColor: "rgba(239, 68, 68, 0.4)",
        pointRadius: 0,
        tension: 0.3,
        fill: true,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { intersect: false as const },
    },
    scales: {
      x: { grid: { display: false } },
      y: { grid: { display: false } },
    },
  };

  return <Line data={chartData} options={chartOptions} />;
}
