import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from promoter import send_offers
from contact_scraper import run_scraper
from bot_logic import post_news

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(post_news, "interval", minutes=15)  # Постинг новостей
    scheduler.add_job(run_scraper, "interval", hours=24)  # Поиск каналов
    scheduler.add_job(send_offers, "interval", hours=24)  # Отправка предложений
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
    asyncio.get_event_loop().run_forever()
