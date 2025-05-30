from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
import os

from scheduler import start_scheduler

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

async def main():
    start_scheduler()  # Запуск планировщика
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
