import os
import psycopg2
from psycopg2.extras import execute_values

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bluesky")

def get_conn():
    return psycopg2.connect(DB_URL)

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                uri TEXT UNIQUE,
                author TEXT,
                created_at TIMESTAMP,
                text TEXT,
                likes INT,
                toxicity FLOAT
            )
            """)
    print("✅ DB initialized")

def insert_post(uri, author, created_at, text, likes, toxicity):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO posts (uri, author, created_at, text, likes, toxicity)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (uri) DO NOTHING
            """, (uri, author, created_at, text, likes, toxicity))
