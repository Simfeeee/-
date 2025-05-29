import asyncio
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import Message
from scheduler import start_scheduler
from bot_logic import post_news
import os

bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(F.text == "/обновить")
async def manual_post(message: Message):
    user_id = message.from_user.id
    admin_id = os.environ.get("ADMIN_ID")
    if admin_id and str(user_id) == str(admin_id):
        await message.answer("⏳ Публикую следующую новость...")
        await post_news()
    else:
        await message.answer("🚫 У вас нет доступа к этой команде.")

async def main():
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
