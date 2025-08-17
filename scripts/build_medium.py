# scripts/build_medium.py
import json, math, datetime as dt
import feedparser
from bs4 import BeautifulSoup
from pathlib import Path

FEED_URL = "https://medium.com/feed/@quantquill"
OUT = Path("static/data")
OUT.mkdir(parents=True, exist_ok=True)

def extract_image(html: str):
    soup = BeautifulSoup(html or "", "html.parser")
    img = soup.find("img")
    return img["src"] if img and img.get("src") else None

def extract_text(html: str):
    soup = BeautifulSoup(html or "", "html.parser")
    return soup.get_text(" ", strip=True)

def main():
    feed = feedparser.parse(FEED_URL)
    posts = []
    for e in feed.entries:
        raw = e.get("content", [{"value": e.get("summary", "")}])[0]["value"]
        text = extract_text(raw)
        img = extract_image(raw)
        words = len(text.split())
        read_min = max(1, math.ceil(words/220))
        posts.append({
            "title": e.title,
            "url": e.link,
            "published": e.get("published", ""),
            "summary": (text[:240] + "…") if len(text) > 240 else text,
            "image": img,
            "read_min": read_min,
        })
    payload = {
        "updated": dt.datetime.utcnow().isoformat() + "Z",
        "posts": posts[:12]
    }
    (OUT / "medium_posts.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"Wrote {(OUT/ 'medium_posts.json').as_posix()} with {len(payload['posts'])} posts.")

if __name__ == "__main__":
    main()
