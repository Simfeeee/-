import os
import random
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from config import RSS_FEEDS, CHANNEL_ID
from news_fetcher import fetch_latest_news

bot = Bot(token=os.environ.get("BOT_TOKEN"))

def get_theme_emoji(title):
    title = title.lower()
    if "экономик" in title or "курс" in title or "деньги" in title:
        return "💰"
    elif "технолог" in title or "искусственный интеллект" in title or "gpt" in title:
        return "🤖"
    elif "полит" in title or "выборы" in title:
        return "⚖️"
    elif "авар" in title or "взрыв" in title or "чп" in title:
        return "🚨"
    elif "культура" in title or "театр" in title:
        return "🎭"
    else:
        return "📰"

def get_theme_hashtag(title):
    title = title.lower()
    tags = ["#новости", "#Россия"]
    if "экономик" in title or "курс" in title or "деньги" in title:
        tags.append("#экономика")
    elif "технолог" in title or "gpt" in title:
        tags.append("#технологии")
    elif "полит" in title or "выборы" in title:
        tags.append("#политика")
    elif "авар" in title or "взрыв" in title or "чп" in title:
        tags.append("#происшествия")
    elif "культура" in title or "театр" in title:
        tags.append("#культура")
    else:
        tags.append("#главное")
    return " ".join(tags)

def clean_text(text):
    lines = text.split("\n")
    clean_lines = [line for line in lines if not line.lower().startswith(("фото:", "источник:", "photo:", "source:"))]
    return " ".join(clean_lines).strip()

def format_post(news):
    emoji = get_theme_emoji(news['title'])
    date_str = datetime.now().strftime("%d.%m.%Y — %H:%M")
    from annotator import generate_annotation
    summary = generate_annotation(news['title'], news['summary'])
    hashtags = get_theme_hashtag(news['title'])

    header = f"📌 <b>Главная новость</b>\n🕒 {date_str}\n"
    title = f"{emoji} <b>{news['title']}</b>\n"
    body = f"\n<i>{summary}</i>\n"
    footer = f"\n━━━━━━━━━━━━━━━\n📢 @news_russia\n{hashtags}\n━━━━━━━━━━━━━━━"

    return header + "\n" + title + body + footer

def build_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📲 Подписаться", url="https://t.me/news_russia")],
        [InlineKeyboardButton(text="🔁 Поделиться", switch_inline_query="")]
    ])

async def post_news():
    news_list = fetch_latest_news(RSS_FEEDS)
    if not news_list:
        return

    news = random.choice(news_list)
    caption = format_post(news)
    keyboard = build_keyboard()

    if news["image"]:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=news["image"], caption=caption, reply_markup=keyboard, parse_mode="HTML")
    else:
        await bot.send_message(chat_id=CHANNEL_ID, text=caption, reply_markup=keyboard, parse_mode="HTML")
