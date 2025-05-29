import feedparser

def fetch_latest_news(rss_feeds):
    news_items = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            image_url = ""
            if "media_content" in entry:
                media = entry.media_content
                if isinstance(media, list) and media:
                    image_url = media[0].get("url", "")
                elif isinstance(media, dict):
                    image_url = media.get("url", "")
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "image": image_url,
            })
    return news_items
