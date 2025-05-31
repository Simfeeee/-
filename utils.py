
import feedparser
import aiohttp
import logging
import random
import os
import openai

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

NEWS_FEEDS = [
    "https://lenta.ru/rss",
    "https://tass.ru/rss/v2.xml",
    "https://www.rbc.ru/static/rss/news.rus.rbc.ru/news.rus/index.rss",
    "https://www.kommersant.ru/RSS/news.xml",
    "https://ria.ru/export/rss2/archive/index.xml",
    "https://meduza.io/rss/all"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

async def fetch_news():
    all_news = []
    for url in NEWS_FEEDS:
        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            all_news.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", ""),
                "published": entry.get("published", ""),
            })
    random.shuffle(all_news)
    return all_news

async def generate_summary(title, summary):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return None

async def find_image_url(query):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as resp:
                data = await resp.json()
                items = data.get("data", {}).get("result", {}).get("items", [])
                if items:
                    return items[0].get("media")
    except Exception as e:
        return None

def generate_annotation(title):
    annotations = [
        "🔥 Срочно!", "📢 Интересно!", "🧐 Важная новость!", "🚨 Что происходит?", "📌 Обратите внимание!"
    ]

async def format_post(item):
    title = item.get("title")
    summary = item.get("summary")
    link = item.get("link")

    gpt_summary = await generate_summary(title, summary)
    annotation = generate_annotation(title)
    annotation = generate_annotation(title)

    text = "<b>" + title + "</b>\n\n"
    if gpt_summary:
        text += gpt_summary + "\n\n"
    else:
        text += summary + "\n\n"
    if annotation:
        text += annotation + "\n\n"
    else:
        logging.warning("⚠️ Аннотация не получена, пропускаем.")
        return None, None, None
    text += "👉 <b>@fastnewsrussian</b>"
    if annotation:
        text += annotation + "\n\n"
    else:
        logging.warning("⚠️ Аннотация не получена, пропускаем.")
        return None, None, None
    text += "👉 <b>@fastnewsrussian</b>"

    text += "👉 <b>@fastnewsrussian</b>"

    image_url = await find_image_url(title)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📣 Поделиться", switch_inline_query=title)],
            [InlineKeyboardButton(text="🔔 Подписаться", url="https://t.me/fastnewsrussian")]
        ]
    )

    return text.strip(), image_url, keyboard

async def send_post(bot, channel_id, text, image_url=None, keyboard=None):
    try:
        if image_url:
            await bot.send_photo(chat_id=channel_id, photo=image_url, caption=text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=channel_id, text=text, reply_markup=keyboard)
    except Exception as e:
        return None
        logging.warning(f"GPT ошибка: {e}")
