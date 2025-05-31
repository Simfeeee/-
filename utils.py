import os
import aiohttp
import logging
import random
import feedparser
from bs4 import BeautifulSoup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_NICK = os.getenv("CHANNEL_NICK", "@fastnewsrussian")
CHAT_IDS = os.getenv("CHAT_IDS", os.getenv("CHAT_ID", "")).split(",")

FAKE_ANNOTATIONS = [
    "Вот это поворот!",
    "Классика жанра.",
    "Кажется, снова понедельник.",
    "Интересненько...",
    "Ну такое.",
    "Сами в шоке.",
    "Они там совсем уже?",
    "Это уже не смешно.",
    "Комментировать бессмысленно.",
    "Без комментариев 😐",
    "Новость, которая заслуживает мем.",
    "Как вам такое, Илон Маск?",
]

KEYWORDS = [
    "Путин", "взрыв", "закон", "экономика", "ЧП", "катастрофа", 
    "арест", "авария", "штраф", "облава", "мобилизация", 
    "санкции", "пожар", "смерть", "теракт"
]

async def fetch_news():
    sources = [
        "https://lenta.ru/rss/news",
        "https://tass.ru/rss/v2.xml",
        "https://www.vedomosti.ru/rss/news",
        "https://www.rbc.ru/v10/news.rss",
        "https://ria.ru/export/rss2/archive/index.xml",
        "https://www.interfax.ru/rss.asp",
    ]
    news = []
    for url in sources:
        feed = feedparser.parse(url)
        for item in feed.entries:
            title = item.get("title", "")
            if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                news.append(item)
    return news[:30]

async def get_og_image(link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, timeout=10) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                og_image = soup.find("meta", property="og:image")
                if og_image:
                    return og_image.get("content")
    except:
        return None

async def get_backup_image(query):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://source.unsplash.com/800x600/?{query}") as resp:
                return str(resp.url)
    except:
        return None

async def format_post(item):
    title = item.get("title", "")
    link = item.get("link", "")
    annotation = random.choice(FAKE_ANNOTATIONS)
    text = f"📰 <b>{title}</b>\n\n{annotation}\n\n{CHANNEL_NICK}"
    image_url = await get_og_image(link) or await get_backup_image(title)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁 Подписаться", url=f"https://t.me/{CHANNEL_NICK.strip('@')}"),
                InlineKeyboardButton(text="📢 Поделиться", switch_inline_query=title[:100])
            ]
        ]
    )
    return text, image_url, keyboard

async def send_post(text, image_url, keyboard):
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    for chat_id in CHAT_IDS:
        try:
            if image_url:
                await bot.send_photo(chat_id=chat_id.strip(), photo=image_url, caption=text, reply_markup=keyboard)
            else:
                await bot.send_message(chat_id=chat_id.strip(), text=text, reply_markup=keyboard)
        except Exception as e:
            logging.warning(f"Ошибка при отправке поста: {e}")
    await bot.session.close()