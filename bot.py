import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from dotenv import load_dotenv

from utils import fetch_news, format_post, send_post

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def process_news():
    logging.info("Получение новостей...")
    news = await fetch_news()
    logging.info(f"Найдено новостей: {len(news)}")
    for item in news:
        text, image_url, keyboard = await format_post(item)
        if text is None:
            continue
        await send_post(text, image_url, keyboard)
        await asyncio.sleep(1)

async def news_loop():
    while True:
        await process_news()
        await asyncio.sleep(1800)  # каждые 30 минут

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Бот работает и будет публиковать новости каждые 30 минут.")

@dp.message(F.text == "/обновить")
async def cmd_update(message: types.Message):
    await message.answer("Обновляю новости...")
    await process_news()
    await message.answer("Готово!")

async def main():
    await process_news()
    asyncio.create_task(news_loop())
    await dp.start_polling(bot)

def run_bot():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())