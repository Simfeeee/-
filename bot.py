import os
import logging
import requests
import sqlite3
import openai
from bs4 import BeautifulSoup
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL = os.getenv("CHANNEL_USERNAME")

bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# SQLite: база опубликованных новостей
conn = sqlite3.connect("published.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS published (url TEXT PRIMARY KEY)")
conn.commit()

def is_published(url):
    cursor.execute("SELECT 1 FROM published WHERE url = ?", (url,))
    return cursor.fetchone() is not None

def mark_as_published(url):
    cursor.execute("INSERT OR IGNORE INTO published (url) VALUES (?)", (url,))
    conn.commit()

def fetch_image(query):
    try:
        url = f"https://duckduckgo.com/?q={query}&iax=images&ia=images"
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")
        imgs = soup.find_all("img")
        for img in imgs:
            src = img.get("src")
            if src and "http" in src:
                return src
    except Exception:
        pass
    return "https://via.placeholder.com/800x400.png?text=News"

def summarize(text):
    sentences = text.split(". ")
    return ". ".join(sentences[:2]) + "."

def generate_annotation(title, content):
    prompt = f"Сделай оригинальную ироничную аннотацию к новости:
Заголовок: {title}
Содержание: {content}
Аннотация:"
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY", "sk-fake-key")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.9
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception:
        return "🤔 Мир не перестаёт удивлять..."

def get_news():
    rss = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    response = requests.get(rss)
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")

    for item in items:
        link = item.link.text
        if is_published(link):
            continue

        title = item.title.text
        description = BeautifulSoup(item.description.text, "html.parser").text
        summary = summarize(description)
        image_url = fetch_image(title)
        annotation = generate_annotation(title, summary)

        message = f"📰 <b>{title}</b>

{summary}

{annotation}

🇷🇺@fastnewsrussian"
        bot.send_photo(chat_id=CHANNEL, photo=image_url, caption=message, parse_mode=ParseMode.HTML)

        mark_as_published(link)
        break

def update_command(update, context):
    get_news()
    update.message.reply_text("📬 Новость отправлена!")

dispatcher.add_handler(CommandHandler("обновить", update_command))

scheduler = BackgroundScheduler()
scheduler.add_job(get_news, 'interval', minutes=30)
scheduler.start()

updater.start_polling()
updater.idle()
