
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

from utils import fetch_news, format_post, send_post

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
POST_INTERVAL = int(os.getenv("POST_INTERVAL", 30))  # в минутах

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("✅ Skylibot запущен и ждёт новостей.")


@dp.message(Command("обновить"))
async def manual_update(message: Message):
    await message.answer("🔄 Ищу свежую новость...")

    news = await fetch_news()
    for item in news:
        if is_posted(item["link"]):
            continue
        try:
            text, image_url, keyboard = await format_post(item)
            await send_post(text, image_url, keyboard)
            add_posted_link(item["link"])
            break
        except Exception as e:
            logging.warning(f"⚠️ Ошибка при публикации новости: {e}")
    else:
        await message.answer("✅ Новых новостей пока нет.")