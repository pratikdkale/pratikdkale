# utils/medium.py
import datetime as dt
import feedparser
from bs4 import BeautifulSoup

FEED_URL = "https://medium.com/feed/@quantquill"

_cache = {"ts": None, "posts": []}

def _extract_image(html: str) -> str | None:
    soup = BeautifulSoup(html or "", "html.parser")
    img = soup.find("img")
    return img["src"] if img and img.get("src") else None

def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    return soup.get_text(" ", strip=True)

def get_medium_posts(limit: int = 8, max_age_minutes: int = 60):
    # lightweight server-side cache to avoid hitting Medium on every request
    if _cache["ts"] and (dt.datetime.utcnow() - _cache["ts"]).total_seconds() < max_age_minutes * 60:
        return _cache["posts"][:limit]

    feed = feedparser.parse(FEED_URL)
    posts = []
    for e in feed.entries:
        raw = e.get("content", [{"value": e.get("summary", "")}])[0]["value"]
        text = _extract_text(raw)
        img = _extract_image(raw)
        words = len(text.split())
        read_min = max(1, round(words / 220))

        posts.append({
            "title": e.title,
            "url": e.link,
            "published": e.get("published", ""),
            "summary": (text[:240] + "…") if len(text) > 240 else text,
            "image": img,                        # may be None → we’ll handle in template
            "read_min": read_min,
        })

    _cache["posts"] = posts
    _cache["ts"] = dt.datetime.utcnow()
    return posts[:limit]
