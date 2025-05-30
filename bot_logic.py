import random
from aiogram import Bot
from aiogram.types import InputMediaPhoto
from news_fetcher import fetch_latest_news
from aiogram.enums import ParseMode

CHANNEL_ID = "@russia_news_bot"

# Примеры аннотаций
ANNOTATIONS = [
    "🗯 А вот и горячее!",
    "⚡️ Свежак с ленты:",
    "🌀 Новости, которые стоит знать:",
    "📢 Только что сообщили:",
    "🔍 Интересное подоспело:",
    "🧩 К новостям дня:"
]

def generate_annotation():
    return random.choice(ANNOTATIONS)

async def post_news(bot: Bot):
    news_items = fetch_latest_news()
    if not news_items:
        return

    news = news_items[0]  # Только одна новость за раз
    annotation = generate_annotation()

    title = news["title"]
    summary = news["summary"]
    image_url = news.get("image_url")

    text = f"<b>{annotation}</b>

📰 <b>{title}</b>

{summary}

🛰 {CHANNEL_ID}"

    if image_url:
        try:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=text, parse_mode=ParseMode.HTML)
        except Exception:
            await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode=ParseMode.HTML)
