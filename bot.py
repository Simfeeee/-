import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from utils import fetch_news, format_post, send_post

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL")
INTERVAL = int(os.getenv("POST_INTERVAL_MIN", 30))

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")


dp = Dispatcher()

@dp.message(Command("обновить"))
async def handle_update_command(message: types.Message):
    news_items = await fetch_news()
    if news_items:
        post = await format_post(news_items[0])
        if post:
            await bot.send_message(chat_id=CHANNEL_ID, text=post)
            await message.reply("Обновление отправлено в канал.")
        else:
            await message.reply("Не удалось сгенерировать пост.")
    else:
        await message.reply("Нет свежих новостей.")


async def run_bot():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

    while True:
        try:
            news_items = await fetch_news()
            for item in news_items:
                post = await format_post(item)
                if post:
                    await send_post(bot, CHANNEL_ID, post)
        except Exception as e:
            logging.exception("Error in bot loop")
        await asyncio.sleep(INTERVAL * 60)