import feedparser
import requests
from bs4 import BeautifulSoup

RSS_FEEDS = [
    "https://lenta.ru/rss",
    "https://www.vedomosti.ru/rss/news",
    "https://tass.ru/rss/v2.xml",
    "https://ria.ru/export/rss2/archive/index.xml",
    "https://www.interfax.ru/rss.asp",
    "https://iz.ru/xml/rss/all.xml",
]

def fetch_latest_news():
    news_items = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:1]:
            title = entry.title
            summary_raw = getattr(entry, 'summary', '') or getattr(entry, 'description', '') or getattr(entry, 'text', '') or ''
    summary = BeautifulSoup(summary_raw, "html.parser").text
            summary = summary.replace("&nbsp;", " ").replace("&quot;", '"')
            link = entry.link
            image_url = ""

            if hasattr(entry, "media_content"):
                image_url = entry.media_content[0]["url"]
            elif "image" in entry:
                image_url = entry.image

            news_items.append({
                "title": title,
                "summary": summary,
                "url": link,
                "image": image_url
            })

    return news_items