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
    asyncio.run(dp.start_polling(bot))

