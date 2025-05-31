posted_links = set()

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv

from utils import fetch_news, format_post, send_post

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@fastnewsrussian")

if not BOT_TOKEN:
    raise RuntimeError("❌ Переменная окружения BOT_TOKEN не установлена!")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("🤖 Бот запущен и готов публиковать новости!")

@dp.message(Command("обновить"))
async def update_news(message: Message):
    await message.answer("🔄 Обновляю новости...")
    await process_news()

async def process_news():
    global posted_links
    logging.info("Получение новостей...")
    news = await fetch_news()
    logging.info(f"Найдено новостей: {len(news)}")
    for item in news:
        link = item.get('link')
        if link not in posted_links:
            text, image_url, keyboard = await format_post(item)
            if text:
                await send_post(bot, CHANNEL_ID, text, image_url=image_url, keyboard=keyboard)
                posted_links.add(link)
                break
    else:
        logging.info("Нет новых новостей для публикации.")

async def news_loop():
    while True:
        await process_news()
        await asyncio.sleep(1800)  # 30 минут
    logging.info("Получение новостей...")
    news = await fetch_news()
    logging.info(f"Найдено новостей: {len(news)}")

    for item in news:
        text, image_url, keyboard = await format_post(item)
        if text:
            await send_post(bot, CHANNEL_ID, text, image_url=image_url, keyboard=keyboard)
            await asyncio.sleep(5)

def run_bot():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(process_news())
    asyncio.create_task(news_loop())
    asyncio.run(dp.start_polling(bot))
