"use client";

import Image from "next/image";

interface ToxicCardProps {
  type: "most" | "least";
  author?: string;
  text?: string;
  likes?: number;
  toxicity?: number;
  uri?: string;
}

// Convert at:// URIs to usable Bluesky web URLs
function formatBlueskyUrl(uri: string) {
  const match = uri.match(/^at:\/\/(did:[^/]+)\/app\.bsky\.feed\.post\/(.+)$/);
  if (!match) return uri; // fallback if invalid
  const [, did, postId] = match;
  return `https://bsky.app/profile/${did}/post/${postId}`;
}

export default function ToxicCard({
  type,
  author,
  text,
  likes,
  toxicity,
  uri,
}: ToxicCardProps) {
  const isMost = type === "most";

  return (
    <div className="text-center max-w-md">
      <h2
        className={`text-2xl font-semibold flex items-center justify-center gap-2 ${
          isMost ? "text-red-600" : "text-green-600"
        }`}
      >
        {isMost ? "Today’s Most Toxic" : "Today’s Least Toxic"}
      </h2>

      {author && text && likes !== undefined && toxicity !== undefined ? (
        <div className="mt-3 text-gray-700">
          <p className="font-medium">👤 {author}</p>
          <p className="mt-2 italic">&quot;{text}&quot;</p>
          <p className="mt-2 text-sm text-gray-500 flex items-center justify-center gap-2">
            ❤️ {likes} · Toxicity {toxicity.toFixed(2)}
            {uri && (
              <a
                href={formatBlueskyUrl(uri)}
                target="_blank"
                rel="noopener noreferrer"
                title="View on Bluesky"
              >
                <Image
                  src="/bluesky.svg"
                  alt="Bluesky"
                  width={20}
                  height={20}
                  className="inline-block hover:opacity-80"
                />
              </a>
            )}
          </p>
        </div>
      ) : (
        <p className="italic text-gray-400 mt-2">No data today</p>
      )}
    </div>
  );
}
