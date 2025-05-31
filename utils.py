import os
import aiohttp
import openai
import logging

openai.api_key = os.getenv("OPENAI_API_KEY")

NEWS_CHANNEL = os.getenv("CHAT_ID", "")
CHANNEL_NICK = os.getenv("CHANNEL_NICK", "@fastnewsrussian")

async def fetch_news():
    import feedparser

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
        news.extend(feed.entries)
    return news[:30]

async def get_image(query):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://source.unsplash.com/800x600/?{query}") as resp:
                return str(resp.url)
    except:
        return None

async def format_post(item):
    title = item.get("title", "")
    link = item.get("link", "")
    summary = item.get("summary", "")
    prompt = f"Сделай краткое и интересное резюме новости: {title}\n{summary}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        annotation = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.warning(f"⚠️ Аннотация не получена, пропускаем.")
        return None, None, None

    text = f"📰 <b>{title}</b>\n\n{annotation}\n\n{CHANNEL_NICK}"
    image_url = await get_image(title)

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁 Подписаться", url=f"https://t.me/{CHANNEL_NICK.strip('@')}"),
                InlineKeyboardButton(text="📢 Поделиться", switch_inline_query=text[:100])
            ]
        ]
    )

    return text, image_url, keyboard

async def send_post(text, image_url, keyboard):
    from aiogram import Bot
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="HTML")

    try:
        if image_url:
            await bot.send_photo(chat_id=NEWS_CHANNEL, photo=image_url, caption=text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=NEWS_CHANNEL, text=text, reply_markup=keyboard)
    except Exception as e:
        logging.warning(f"Ошибка при отправке поста: {e}")
    finally:
        await bot.session.close()