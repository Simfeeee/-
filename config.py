import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

RSS_FEEDS = [
    "https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru",
    "https://lenta.ru/rss",
    "https://www.rbc.ru/static/rss/news.rss",
    "https://tass.ru/rss/v2.xml",
    "https://www.interfax.ru/rss.asp",
    "https://www.kommersant.ru/RSS/news.xml"
]
