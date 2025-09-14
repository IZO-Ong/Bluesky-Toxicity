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
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend);

export default function LineChart({ stats }: { stats: any[] }) {
  const chartData = {
    labels: stats.map((s) => s.date).reverse(),
    datasets: [
      {
        label: "Toxic posts",
        data: stats.map((s) => s.toxic_posts).reverse(),
        borderColor: "rgb(239, 68, 68)", // Tailwind red-500
        backgroundColor: "rgba(239, 68, 68, 0.3)",
        tension: 0.3,
        fill: true,
      },
    ],
  };

  return <Line data={chartData} />;
}
