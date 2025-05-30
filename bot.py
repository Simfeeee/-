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


from aiogram import F, Router
from aiogram.types import Message
from bot_logic import post_news

router = Router()

ADMIN_IDS = [1818993268]

@router.message(F.text == "/update")
async def manual_update(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    await message.answer("Публикую новость...")
    try:
        await post_news()
        await message.answer("Пост опубликован!")
    except Exception as e:
        await message.answer(f"Ошибка при публикации: {e}")

# Подключи роутер к dp (после инициализации диспетчера)
dp.include_router(router)

async def main():
    start_scheduler(bot)  # Запуск планировщика
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
