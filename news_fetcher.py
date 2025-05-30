import feedparser

def fetch_latest_news():
    sources = [
        "https://lenta.ru/rss",
        "https://www.rbc.ru/rss/",
        "https://tass.ru/rss/v2.xml",
        "https://www.vedomosti.ru/rss/news",
        "https://ria.ru/export/rss2/archive/index.xml",
    ]
    news_list = []

    for url in sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                summary = entry.get("summary", "")
                summary = summary.replace("&nbsp;", " ").replace("&quot;", '"')
                image = ""
                if "media_content" in entry:
                    image = entry.media_content[0].get("url", "")
                elif "links" in entry:
                    for link in entry.links:
                        if link.type.startswith("image"):
                            image = link.href
                            break
                news_list.append({
                    "title": entry.title,
                    "summary": summary,
                    "image_url": image
                })
        except Exception:
            continue

    return news_list
