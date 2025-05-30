import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from scheduler import start_scheduler

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(token=TOKEN, default=Bot.DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    start_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
