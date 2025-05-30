
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from bot_logic import post_news
from promoter import send_offers
from contact_scraper import run_scraper

def start_scheduler(bot=None):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(post_news()), "interval", minutes=30)
    scheduler.add_job(run_scraper, "cron", hour=2)
    scheduler.add_job(send_offers, "cron", hour=3)
    scheduler.start()
