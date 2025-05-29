from config import RSS_FEEDS, CHANNEL_ID
from news_fetcher import fetch_latest_news
from annotator import generate_annotation
from aiogram import Bot
import os

bot = Bot(token=os.environ.get("BOT_TOKEN"))

async def post_news():
    news_list = fetch_latest_news(RSS_FEEDS)
    for news in news_list:
        annotation = generate_annotation(news["title"], news["summary"])
        message = f"<b>{news['title']}</b>\n\n{annotation}\n\n<a href='{news['link']}'>Читать полностью</a>"
        await bot.send_message(CHANNEL_ID, message, parse_mode="HTML")
