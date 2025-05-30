import os
import asyncio
from aiogram import Bot
from aiogram.types import InputFile
from news_fetcher import fetch_latest_news
from annotator import generate_annotation
from config import CHANNEL_USERNAME

from aiogram import Bot

async def post_news():
    try:
        TOKEN = os.getenv("BOT_TOKEN")
        bot = Bot(token=TOKEN)

        news_items = fetch_latest_news()
        if not news_items:
            print('Нет новостей для публикации.')
            return

        news = news_items[0]
        print("news:", news)
        print("Ключи в news:", list(news.keys()))

        summary = news.get('summary') or news.get('description') or news.get('text') or ''
        annotation = generate_annotation(news.get('title', ''), summary)
        channel_username = CHANNEL_USERNAME

        text = (
            f"<b>{annotation}</b>\n"
            f"{summary}\n\n"
            f"📰 @{channel_username}"
        )

        image_url = news.get('image', '')

        if image_url:
            try:
                await bot.send_photo(chat_id=f"@{channel_username}", photo=image_url, caption=text)
                print(f"Пост опубликован с фото в @{channel_username}")
            except Exception as e:
                print(f"Не удалось отправить фото, ошибка: {e}. Пробую отправить только текст.")
                await bot.send_message(chat_id=f"@{channel_username}", text=text)
                print(f"Пост опубликован без фото в @{channel_username}")
        else:
            await bot.send_message(chat_id=f"@{channel_username}", text=text)
            print(f"Пост опубликован без фото в @{channel_username}")

    except Exception as e:
        print(f"Ошибка при автопостинге: {e}")
