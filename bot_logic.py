
from aiogram import Bot
from aiogram.types import InputFile

async def post_news(bot: Bot, annotation: str, summary: str, image_path: str, channel_username: str):
    text = (
        f"<b>{annotation}</b>\n"
        f"{summary}\n\n"
        f"📰 @{channel_username}"
    )
    photo = InputFile(image_path)
    await bot.send_photo(chat_id=f"@{channel_username}", photo=photo, caption=text)
