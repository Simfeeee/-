import os
import asyncio
from aiogram import Bot
from aiogram.types import InputFile
from news_fetcher import fetch_latest_news
from annotator import generate_annotation
from config import CHANNEL_USERNAME

from aiogram import Bot

async def post_news():
    # ВАЖНО: Bot должен быть создан здесь или импортирован глобально!
    TOKEN = os.getenv("BOT_TOKEN")
    bot = Bot(token=TOKEN)
    news_items = fetch_latest_news()
    if not news_items:
        print('Нет новостей для публикации.')
        return
    news = news_items[0]
    annotation = generate_annotation(news['title'], news['summary'])
    summary = news['summary']
    channel_username = CHANNEL_USERNAME
    text = (
        f"<b>{annotation}</b>\n"
        f"{summary}\n\n"
        f"📰 @{channel_username}"
    )
    image_url = news.get('image', '')
    if image_url:
        # Если image — ссылка, передаём её напрямую
        await bot.send_photo(chat_id=f"@{channel_username}", photo=image_url, caption=text)
    else:
        await bot.send_message(chat_id=f"@{channel_username}", text=text)
