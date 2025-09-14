import os
import httpx
import datetime
import time
from scraper.db import insert_post
from scraper.toxicity import score_toxicity
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

import time

def fetch_posts(token, query="python", limit=1000):
    url = f"{BASE_URL}/app.bsky.feed.searchPosts"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query}
    posts, cursor = [], None

    while len(posts) < limit:
        if cursor:
            params["cursor"] = cursor

        resp = httpx.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

        new_posts = data.get("posts", [])
        if not new_posts:
            print("⚠️ No more posts available, stopping.")
            break

        posts.extend(new_posts)
        cursor = data.get("cursor")

        print(f"✅ Fetched {len(posts)} posts so far...")

    print(f"🎉 Done! Total posts fetched: {len(posts)}")
    return posts[:limit]

def run_scraper():
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
