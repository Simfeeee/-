import os
import random
from aiogram import Bot
from aiogram.types import InputMediaPhoto
from config import RSS_FEEDS, CHANNEL_ID
from news_fetcher import fetch_latest_news
from annotator import generate_annotation

bot = Bot(token=os.environ.get("BOT_TOKEN"))

def format_post(news, annotation):
    text = f"📰 <b>{news['title']}</b>\n\n"
    text += f"📍 <i>{annotation}</i>\n\n"
    text += f"💬 <i>{news['summary']}</i>"
    return text

async def post_news():
    news_list = fetch_latest_news(RSS_FEEDS)
    if not news_list:
        return

    news = random.choice(news_list)
    annotation = generate_annotation(news["title"], news["summary"])
    caption = format_post(news, annotation)

    if news["image"]:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=news["image"], caption=caption, parse_mode="HTML")
    else:
        await bot.send_message(chat_id=CHANNEL_ID, text=caption, parse_mode="HTML")
