from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot_logic import post_news
from promoter import send_offers
from contact_scraper import run_scraper

def start_scheduler():
    scheduler = AsyncIOScheduler()

    # Публикуем новости каждые 15 минут
    scheduler.add_job(post_news, "interval", minutes=15)

    # Запускаем парсер каждый день в 01:00
    scheduler.add_job(run_scraper, "cron", hour=1, minute=0)

    # Рассылаем предложения в 02:00
    scheduler.add_job(send_offers, "cron", hour=2, minute=0)

    scheduler.start()
