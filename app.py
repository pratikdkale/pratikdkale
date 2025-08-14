from flask import Flask, render_template, send_from_directory, abort
import markdown, os, re
from datetime import datetime
import feedparser

app = Flask(__name__)

# ---- Blog helpers ----
BLOG_DIR = os.path.join(app.root_path, "blogs")

@app.route("/blog")
def blog():
    # Your local blog posts
    posts = get_local_posts()  # This is your existing logic
    
    # Medium RSS feed URL
    feed_url = "https://medium.com/feed/@yourusername"  # replace with your Medium username
    feed = feedparser.parse(feed_url)
    
    # Extract top 5 articles
    external_posts = []
    for entry in feed.entries[:5]:
        external_posts.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })

    return render_template("blog.html", posts=posts, external_posts=external_posts)

def list_blog_posts():
    posts = []
    if not os.path.isdir(BLOG_DIR):
        return posts
    for fname in os.listdir(BLOG_DIR):
        if fname.endswith(".md"):
            path = os.path.join(BLOG_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                first = f.readline().strip()
            # Expect first line like: # Title | 2025-08-01
            m = re.match(r'^#\s*(.*?)\s*\|\s*([0-9\-]+)\s*$', first)
            title = first.lstrip("# ").strip()
            date = None
            if m:
                title = m.group(1).strip()
                try:
                    date = datetime.strptime(m.group(2), "%Y-%m-%d").date()
                except Exception:
                    date = None
            slug = os.path.splitext(fname)[0]
            posts.append({"title": title, "date": date, "slug": slug})
    posts.sort(key=lambda x: x["date"] or datetime.min.date(), reverse=True)
    return posts

def render_markdown(md_text):
    return markdown.markdown(md_text, extensions=["fenced_code", "tables", "toc"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/blogs")
def blogs():
    return render_template("blogs.html", posts=list_blog_posts())

@app.route("/blog/<slug>")
def blog_post(slug):
    path = os.path.join(BLOG_DIR, f"{slug}.md")
    if not os.path.exists(path):
        abort(404)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    html = render_markdown(content)
    # Get title from first H1 or fallback to slug
    title = slug.replace("-", " ").title()
    m = re.search(r'<h1.*?>(.*?)</h1>', html)
    if m:
        title = m.group(1)
    return render_template("post.html", title=title, content=html)

if __name__ == "__main__":
    app.run(debug=True)