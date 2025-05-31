
import os
import aiohttp
import logging
import random
import feedparser
from bs4 import BeautifulSoup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import openai

async def generate_annotation(text):
    try:
        prompt = (
            "Прочитай новость и сформулируй краткий вывод (1-2 предложения), как в СМИ:
\n"
            f"{text}\n\n"
            "Вывод:"
        )
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.warning(f"⚠️ GPT ошибка: {e}")
        return random.choice(FAKE_ANNOTATIONS)

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
    "Без комментариев.",
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
    summary = item.get("summary", "") or title
    annotation = await generate_annotation(summary)

    formatted_text = (
        "▔▔▔▔▔▔▔▔▔▔▔▔▔▔\n"
        f"📢 <b>{title}</b>\n\n"
        f"🧱 {annotation}\n\n"
        f"💥 Этот факт уже вызвал резонанс в соцсетях.\n"
        f"🗣 Мнения разделились, но ситуация развивается.\n\n"
        f"🔥 312   ❤️ 142   💬 76   😂 24\n\n"
        f"🔗 t.me/{CHANNEL_NICK.strip('@')}\n"
        "▁▁▁▁▁▁▁▁▁▁▁▁▁▁"
    )

    image_url = await get_og_image(link) or await get_backup_image(title)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁 Подписаться", url=f"https://t.me/{CHANNEL_NICK.strip('@')}")
            ]
        ]
    )
    return formatted_text, image_url, keyboard


    formatted_text = (
        f"<b>{title}</b>\n\n"
        f"📍 {annotation}\n"
        f"💥 Этот факт уже вызвал резонанс в соцсетях.\n"
        f"🗣 Мнения разделились, но ситуация развивается.\n\n"
        f"🔹 t.me/{CHANNEL_NICK.strip('@')}"
    )

    image_url = await get_og_image(link) or await get_backup_image(title)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁 Подписаться", url=f"https://t.me/{CHANNEL_NICK.strip('@')}")
            ]
        ]
    )
    return formatted_text, image_url, keyboard


    # Подготовим блок в виде абзацев с эмодзи
    formatted_text = (
        f"<b>{title}</b>\n\n"
        f"📍 {annotation}\n"
        f"💥 Этот факт уже вызвал резонанс в соцсетях.\n"
        f"🗣 Мнения разделились, но ситуация развивается.\n\n"
        f"🔹 t.me/{CHANNEL_NICK.strip('@')}"
    )

    image_url = await get_og_image(link) or await get_backup_image(title)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁 Подписаться", url=f"https://t.me/{CHANNEL_NICK.strip('@')}")
            ]
        ]
    )
    return formatted_text, image_url, keyboard


    text = (
        f"📰 <b>{title}</b>\n\n"
        f"🧠 {annotation}\n\n"
        f"👉 Подробнее читай в канале: https://t.me/{CHANNEL_NICK.strip('@')}"
    )

    image_url = await get_og_image(link) or await get_backup_image(title)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁 Подписаться", url=f"https://t.me/{CHANNEL_NICK.strip('@')}")
            ]
        ]
    )
    return text, image_url, keyboard


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁 Подписаться", url=f"https://t.me/{CHANNEL_NICK.strip('@')}")
            ]
        ]
    )
    return text, image_url, keyboard


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁 Подписаться", url=f"https://t.me/{CHANNEL_NICK.strip('@')}")
            ]
        ]
    )
    return text, image_url, keyboard

async def send_post(text, image_url, keyboard):
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    for chat_id in CHAT_IDS:
        try:
            if chat_id.strip():
                if image_url:
                    await bot.send_photo(chat_id=chat_id.strip(), photo=image_url, caption=text, reply_markup=keyboard)
                else:
                    await bot.send_message(chat_id=chat_id.strip(), text=text, reply_markup=keyboard)
        except Exception as e:
            logging.warning(f"Ошибка при отправке поста: {e}")
    await bot.session.close()
