from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bluesky")

def query_db(sql, params=()):
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

@app.get("/leaderboard/today")
def leaderboard():
    sql = """
    SELECT uri, author, text, likes, toxicity
    FROM posts
    WHERE created_at::date = CURRENT_DATE
      AND likes > 10000
    ORDER BY toxicity DESC
    LIMIT 1
    """
    most = query_db(sql)
    sql = """
    SELECT uri, author, text, likes, toxicity
    FROM posts
    WHERE created_at::date = CURRENT_DATE
      AND likes > 10000
    ORDER BY toxicity ASC
    LIMIT 1
    """
    least = query_db(sql)
    return {"most_toxic": most, "least_toxic": least}

@app.get("/stats/last30days")
def stats():
    sql = """
    SELECT created_at::date, COUNT(*)
    FROM posts
    WHERE toxicity > 0.5
    GROUP BY created_at::date
    ORDER BY created_at::date DESC
    LIMIT 30
    """
    return [{"date": str(d), "toxic_posts": c} for d, c in query_db(sql)]