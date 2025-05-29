import os
import json
from datetime import datetime
from aiogram import Bot
from config import RSS_FEEDS, CHANNEL_ID
from news_fetcher import fetch_latest_news
from annotator import generate_annotation

bot = Bot(token=os.environ.get("BOT_TOKEN"))

QUEUE_FILE = "news_queue.json"

def load_news_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_news_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

def update_news_queue():
    current_titles = {item["title"] for item in load_news_queue()}
    fresh_news = fetch_latest_news(RSS_FEEDS)
    new_items = [n for n in fresh_news if n["title"] not in current_titles]
    if new_items:
        queue = load_news_queue() + new_items
        save_news_queue(queue)

async def post_news():
    update_news_queue()
    queue = load_news_queue()

    if not queue:
        return

    news = queue.pop(0)
    save_news_queue(queue)

    annotation = generate_annotation(news["title"], news["summary"])
    time_now = datetime.now().strftime("%H:%M")
    message = f"📰 <b>{news['title']}</b>\n\n{annotation}\n\n🕓 {time_now} | 🔗 #новости #Россия"

    if news.get("image"):
        await bot.send_photo(CHANNEL_ID, photo=news["image"], caption=message, parse_mode="HTML")
    else:
        await bot.send_message(CHANNEL_ID, message, parse_mode="HTML")
