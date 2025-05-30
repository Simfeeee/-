import os
from aiogram import Bot
from news_fetcher import fetch_latest_news
from annotator import generate_annotation

bot = Bot(token=os.getenv("BOT_TOKEN"))

async def post_news():
    news = fetch_latest_news()
    if not news:
        return

    for item in news:
        title = item["title"]
        summary = item["summary"]
        url = item["url"]
        image_url = item["image"]

        annotation = generate_annotation(title, summary)
        text = f"<b>{annotation}</b>"

{title}

{summary}

"📡 @your_channel_name"

        try:
            if image_url:
                await bot.send_photo(chat_id=os.getenv("CHANNEL_ID"), photo=image_url, caption=text)
            else:
                await bot.send_message(chat_id=os.getenv("CHANNEL_ID"), text=text)
        except Exception as e:
            print("Posting error:", e)
