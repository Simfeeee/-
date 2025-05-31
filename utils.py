import aiohttp
import feedparser
import openai
import os
import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def fetch_news():
    urls = [
        "https://lenta.ru/rss",
        "https://meduza.io/rss/all",
        "https://www.bbc.com/news/world/rss.xml",
        "https://www.reuters.com/rssFeed/topNews",
    ]
    results = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            results.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "image": entry.get("media_content", [{}])[0].get("url", None)
            })
    return results

async def format_post(item):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        prompt = f"""Сделай краткое и интересное резюме новости на русском языке.
Заголовок: {item['title']}
Описание: {item['summary']}"""
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        summary = gpt_response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.warning(f"GPT ошибка: {e}")
        summary = item["summary"][:300] + "..."

    if not summary.strip():
        return None, None, None

    try:
        joke_prompt = f"Добавь ироничную и смешную подпись к новости: {item['title']}"
        joke_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": joke_prompt}],
            max_tokens=60,
        )
        joke = joke_response["choices"][0]["message"]["content"]
    except Exception:
        joke = "🧠 Пока без шуток. GPT ушёл в отпуск."

    text = f"📰 <b>{item['title']}</b>\n\n{summary}\n\n🤖 {joke}\n\n@fastnewsrussian 📡"

    image_url = item.get("image")

    # 📷 Умная генерация изображения по теме
    KEYWORD_OVERRIDES = {
        "Путин": "Vladimir Putin",
        "Зеленский": "Zelensky",
        "война": "war",
        "Украина": "Ukraine",
        "НАТО": "NATO",
        "Трамп": "Donald Trump",
        "Маск": "Elon Musk",
        "Илон": "Elon Musk",
        "пожар": "fire",
        "протест": "protest",
        "землетрясение": "earthquake",
        "выборы": "election",
        "экономика": "economy"
    }

    stopwords = {"и", "в", "на", "о", "от", "с", "по", "это", "он", "она", "оно", "новости", "как", "из"}
    keyword = None

    for word in item['title'].split():
        clean = word.strip(".,!?\"'():").capitalize()
        if clean in KEYWORD_OVERRIDES:
            keyword = KEYWORD_OVERRIDES[clean]
            break
        if not keyword and clean.lower() not in stopwords:
            keyword = clean

    if not image_url and keyword:
        image_url = f"https://source.unsplash.com/800x600/?{keyword}"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Поделиться", url="https://t.me/share/url?url=https://t.me/fastnewsrussian"),
         InlineKeyboardButton(text="➕ Подписаться", url="https://t.me/fastnewsrussian")]
    ])

    return text, image_url, keyboard

async def send_post(bot, channel_id, text, image_url=None, keyboard=None):
    try:
        if image_url:
            await bot.send_photo(chat_id=channel_id, photo=image_url, caption=text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=channel_id, text=text, reply_markup=keyboard)
    except Exception as e:
        logging.warning(f"Ошибка при отправке поста: {e}")