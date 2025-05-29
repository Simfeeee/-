import feedparser
from datetime import datetime, timedelta
import time
from langdetect import detect
from googletrans import Translator

translator = Translator()

def fetch_latest_news(rss_feeds):
    news_items = []
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=2)
    seen_titles = set()

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            published = None
            if hasattr(entry, "published_parsed"):
                published = datetime.utcfromtimestamp(time.mktime(entry.published_parsed))
            elif hasattr(entry, "updated_parsed"):
                published = datetime.utcfromtimestamp(time.mktime(entry.updated_parsed))

            if published and published < cutoff:
                continue

            title = entry.title.strip()
            summary = entry.get("summary", "").strip()

            # Фильтрация дубликатов по заголовкам
            if title in seen_titles:
                continue
            seen_titles.add(title)

            # Перевод если не на русском
            try:
                if detect(title) != "ru":
                    title = translator.translate(title, dest="ru").text
                if summary and detect(summary) != "ru":
                    summary = translator.translate(summary, dest="ru").text
            except Exception:
                pass

            image_url = ""
            if "media_content" in entry:
                media = entry.media_content
                if isinstance(media, list) and media:
                    image_url = media[0].get("url", "")
                elif isinstance(media, dict):
                    image_url = media.get("url", "")

            news_items.append({
                "title": title,
                "link": entry.link,
                "summary": summary,
                "image": image_url,
                "published": published.isoformat() if published else ""
            })

    return sorted(news_items, key=lambda x: x["published"], reverse=True)
