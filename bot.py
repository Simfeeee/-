
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
    await message.answer("🔄 Публикую одну новость...")
    await process_news()


async def process_news():
    logging.info("Получение новостей...")
    news = await fetch_news()
    logging.info(f"Найдено новостей: {len(news)}")

    if news:
        item = news[0]  # только первая новость
        try:
            text, image_url, keyboard = await format_post(item)
            await send_post(text, image_url, keyboard)
        except Exception as e:
            logging.warning(f"Ошибка при отправке поста: {e}")


async def scheduler():
    while True:
        await process_news()
        await asyncio.sleep(POST_INTERVAL * 60)


def run_bot():
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    dp.run_polling(bot)


async def auto_posting_loop():
    while True:
        logging.info("⏰ Автопостинг: публикую одну новость...")
        try:
            await process_news()
        except Exception as e:
            logging.error(f"Ошибка при автопостинге: {e}")
        await asyncio.sleep(POST_INTERVAL * 60)



def run_bot():
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(auto_posting_loop())
    loop.run_until_complete(dp.start_polling(bot))
