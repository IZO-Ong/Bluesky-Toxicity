import os
import httpx
from datetime import datetime, timezone, timedelta
import time
from db import insert_post, init_db
from toxicity import score_toxicity
from dotenv import load_dotenv

load_dotenv()

BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")
BLUESKY_IDENTIFIER = os.getenv("BLUESKY_IDENTIFIER")

BASE_URL = "https://bsky.social/xrpc"

def create_session():
    url = f"{BASE_URL}/com.atproto.server.createSession"
    resp = httpx.post(url, json={
        "identifier": BLUESKY_IDENTIFIER,
        "password": BLUESKY_APP_PASSWORD
    })
    resp.raise_for_status()
    return resp.json()["accessJwt"]

def fetch_posts(token, query="python", limit=2500, delay=0.1, max_retries=3, sort="top"):
    url = f"{BASE_URL}/app.bsky.feed.searchPosts"
    headers = {"Authorization": f"Bearer {token}"}

    now = datetime.now(timezone.utc)
    yesterday = (now - timedelta(days=1))

    params = {
        "q": query,
        "sort": sort,
        "limit": 100,
        "since": yesterday.isoformat(),
        "until": now.isoformat()
    }

    posts, cursor = [], None

    while len(posts) < limit:
        # ✅ only include cursor if it’s valid
        if cursor is not None:
            params["cursor"] = cursor
        elif "cursor" in params:
            del params["cursor"]

        retries = 0
        while retries < max_retries:
            try:
                print(f"➡️ Requesting with params: {params}")  # debug
                resp = httpx.get(url, headers=headers, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                break  # ✅ success
            except httpx.HTTPStatusError as e:
                print(f"⚠️ HTTP error {e.response.status_code} at cursor={cursor}, retry {retries+1}/{max_retries}")
            except httpx.RequestError as e:
                print(f"⚠️ Network error: {e}, retry {retries+1}/{max_retries}")

            retries += 1
            time.sleep(2 ** retries)  # exponential backoff

        else:
            print("❌ Max retries exceeded, stopping.")
            break

        new_posts = data.get("posts", [])
        if not new_posts:
            print("⚠️ No more posts available, stopping.")
            break

        posts.extend(new_posts)
        cursor = data.get("cursor")

        print(f"✅ Fetched {len(posts)} posts so far...")
        time.sleep(delay)

    print(f"🎉 Done! Total posts fetched: {len(posts)}")
    return posts[:limit]

def run_scraper():
    init_db()
    token = create_session()
    posts = fetch_posts(token, query="data")
    for p in posts:
        text = p["record"].get("text", "")
        toxicity = score_toxicity(text)
        insert_post(
            uri=p["uri"],
            author=p["author"]["handle"],
            created_at=p["record"]["createdAt"],
            text=text,
            likes=p["likeCount"],
            toxicity=toxicity,
        )

if __name__ == "__main__":
    run_scraper()
