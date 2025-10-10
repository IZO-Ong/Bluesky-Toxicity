import os
import psycopg2
import traceback
from flask import Flask, jsonify
from flask_cors import CORS

# --- Database setup ---
DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/bluesky")


def query_db(sql, params=(), one=False):
    """Run a query and return results as dict(s)."""
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                colnames = [desc[0] for desc in cur.description]

                if one:
                    row = cur.fetchone()
                    return dict(zip(colnames, row)) if row else None

                rows = cur.fetchall()
                return [dict(zip(colnames, row)) for row in rows]
    except Exception as e:
        print("Database query failed!")
        traceback.print_exc()
        raise


# --- Flask app setup ---
app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {
    "origins": ["https://blueskytoxicity.org", "https://api.blueskytoxicity.org"],
    "allow_headers": "*",
    "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    "supports_credentials": True
}})


# Root route
@app.route("/")
def root():
    return jsonify({"message": "Bluesky Toxicity API (Flask) is running 🚀"})


# Leaderboard
@app.route("/leaderboard/today")
def leaderboard_today():
    """Get most and least toxic posts today (likes > 10)."""
    most = query_db(
        """
        SELECT uri, author, text, likes, toxicity
        FROM posts
        WHERE created_at::date = CURRENT_DATE
          AND likes >= 5
          AND text IS NOT NULL
          AND text <> ''
        ORDER BY toxicity DESC
        LIMIT 1
        """,
        one=True,
    )

    least = query_db(
        """
        SELECT uri, author, text, likes, toxicity
        FROM posts
        WHERE created_at::date = CURRENT_DATE
          AND likes >= 5
          AND text IS NOT NULL
          AND text <> ''
        ORDER BY toxicity ASC
        LIMIT 1
        """,
        one=True,
    )

    return jsonify({"most_toxic": most, "least_toxic": least})


# Stats
@app.route("/stats/last30days")
def stats_last30days():
    """Count toxic posts (>0.5) per day for the last 30 days."""
    rows = query_db(
        """
        SELECT created_at::date AS date, COUNT(*) AS toxic_posts
        FROM posts
        WHERE toxicity > 0.5
        GROUP BY created_at::date
        ORDER BY created_at::date DESC
        LIMIT 30
        """
    )
    return jsonify([{"date": str(r["date"]), "toxic_posts": r["toxic_posts"]} for r in rows])


# Health check
@app.route("/health")
def health():
    """Simple health check for API and DB connection."""
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return jsonify({"status": "ok", "db": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "db": str(e)})


if __name__ == "__main__":
    # Flask’s built-in server (dev only)
    app.run(host="0.0.0.0", port=8000, debug=True)
