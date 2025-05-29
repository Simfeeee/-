import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_latest_news(feed_urls):
    latest_news = []
    cutoff = datetime.utcnow() - timedelta(hours=2)

    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = entry.get("published_parsed")
            if not published:
                continue

            pub_date = datetime(*published[:6])
            if pub_date < cutoff:
                continue

            summary = entry.get("summary", "")[:500]
            link = entry.get("link")
            title = entry.get("title", "").strip()

            image = ""
            media_content = entry.get("media_content", [])
            if media_content:
                image = media_content[0].get("url", "")

            if not image and link:
                try:
                    r = requests.get(link, timeout=5)
                    soup = BeautifulSoup(r.text, "html.parser")
                    og_image = soup.find("meta", property="og:image")
                    if og_image and og_image.get("content"):
                        image = og_image["content"]
                except Exception:
                    pass

            summary = summary.replace("&nbsp;", " ").replace("&quot;", "\"")

            latest_news.append({
                "title": title,
                "summary": summary,
                "link": link,
                "image": image
            })

    return latest_news
