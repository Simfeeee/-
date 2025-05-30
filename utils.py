import aiohttp
import feedparser
import openai
import os

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
            max_tokens=150,
        )
        summary = gpt_response["choices"][0]["message"]["content"]
    except Exception:
        summary = item["summary"][:200] + "..."

    text = f"""📰 <b>{item['title']}</b>

{summary}

@fastnewsrussian 📡"""
    return text

async def send_post(bot, channel_id, text):
    await bot.send_message(chat_id=channel_id, text=text)