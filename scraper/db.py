import os
import psycopg2
import time

DB_URL = os.environ["DATABASE_URL"]

def get_conn():
    # Attempt to connect up to 5 times
    for i in range(5):
        try:
            return psycopg2.connect(DB_URL)
        except psycopg2.OperationalError as e:
            print(f"⚠️ Connection failed (attempt {i+1}/5). Retrying in 2s...")
            time.sleep(2)
    raise Exception("❌ Could not connect to the database after 5 attempts.")

def init_db():
    print("🔄 Initializing database...")
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
